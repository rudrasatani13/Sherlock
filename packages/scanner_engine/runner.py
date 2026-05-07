from __future__ import annotations

import time
import uuid
from typing import List

from .adapters import TargetAdapter, build_target_adapter
from .config import ScanConfig
from .models import ScanRun, ScanSession, ScannerTest, TestResult, utc_now_iso
from .output import write_scan_outputs
from .prompts import get_safe_smoke_tests


class ScannerEngine:
    def __init__(self, scan_config: ScanConfig, adapter: TargetAdapter | None = None) -> None:
        self.scan_config = scan_config
        self.adapter = adapter or build_target_adapter(scan_config)

    def create_session(self) -> ScanSession:
        scan_id = f"shk_{utc_now_iso().replace(':', '').replace('-', '').replace('Z', '')}_{uuid.uuid4().hex[:8]}"
        return ScanSession(
            scan_id=scan_id,
            target_name=self.scan_config.target.name,
            target_type=self.scan_config.target.type,
            mode=self.scan_config.scan_mode,
        )

    def run(self) -> ScanRun:
        session = self.create_session()
        tests = self._select_tests()
        scan_run = ScanRun(
            session=session,
            target=self.scan_config.target.to_dict(),
            tests=tests,
        )
        session.state = "running"
        session.started_at = utc_now_iso()
        try:
            for test in tests:
                scan_run.results.append(self._run_test(test))
            session.state = "completed"
        except Exception as error:
            session.state = "failed"
            session.error = str(error)
        finally:
            session.completed_at = utc_now_iso()
            write_scan_outputs(scan_run, self.scan_config.output_dir)
        return scan_run

    def _select_tests(self) -> List[ScannerTest]:
        if self.scan_config.scan_mode == "safe_smoke":
            return get_safe_smoke_tests(self.scan_config.max_tests)
        raise ValueError(f"Unsupported scan mode: {self.scan_config.scan_mode}")

    def _run_test(self, test: ScannerTest) -> TestResult:
        started_at = utc_now_iso()
        started = time.perf_counter()
        try:
            response = self.adapter.send(test)
            status = "completed"
            error = None
        except Exception as exception:
            response = None
            status = "failed"
            error = str(exception)
        completed_at = utc_now_iso()
        duration_ms = int((time.perf_counter() - started) * 1000)
        return TestResult(
            test_id=test.test_id,
            category=test.category,
            input=test.input,
            response=response,
            status=status,
            error=error,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            metadata={
                "scan_mode": self.scan_config.scan_mode,
                "phase": "phase_5_internal_scanner_engine_v0",
                "evaluation_status": "not_evaluated_by_scanner_engine",
                "severity": "not_assigned_by_scanner_engine",
            },
        )
