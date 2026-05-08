"""Queue abstraction for Sherlock worker system.

Phase 15 provides a local in-memory queue backend for development and testing.
A future phase can swap this for a Redis/RQ or Celery-backed implementation
by subclassing QueueBackend.
"""
from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Dict, List, Optional

from .jobs import JobPayload, JobResult, JobStatus


class QueueBackend(ABC):
    """Abstract queue backend interface."""

    @abstractmethod
    def enqueue(self, payload: JobPayload) -> str:
        """Add a job to the queue and return the job_id."""
        raise NotImplementedError

    @abstractmethod
    def dequeue(self) -> Optional[JobPayload]:
        """Remove and return the next job from the queue, or None if empty."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self, job_id: str) -> Optional[str]:
        """Return the current status of a job, or None if not found."""
        raise NotImplementedError

    @abstractmethod
    def update_status(self, job_id: str, status: str) -> None:
        """Update the status of a job."""
        raise NotImplementedError

    @abstractmethod
    def store_result(self, result: JobResult) -> None:
        """Store a completed job result."""
        raise NotImplementedError

    @abstractmethod
    def get_result(self, job_id: str) -> Optional[JobResult]:
        """Return the stored result for a job, or None."""
        raise NotImplementedError

    @abstractmethod
    def pending_count(self) -> int:
        """Return the number of jobs waiting in the queue."""
        raise NotImplementedError

    @abstractmethod
    def list_jobs(self) -> List[Dict[str, Any]]:
        """Return a summary list of all known jobs."""
        raise NotImplementedError


class LocalMemoryQueue(QueueBackend):
    """Thread-safe in-memory queue for local development only.

    This queue does not persist across process restarts. It is intended for
    local dry-runs, tests, and Phase 15 foundation work only. Production
    deployments should use a durable queue backend such as Redis/RQ or Celery.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._queue: deque[JobPayload] = deque()
        self._statuses: Dict[str, str] = {}
        self._payloads: Dict[str, JobPayload] = {}
        self._results: Dict[str, JobResult] = {}

    def enqueue(self, payload: JobPayload) -> str:
        with self._lock:
            self._queue.append(payload)
            self._statuses[payload.job_id] = JobStatus.QUEUED
            self._payloads[payload.job_id] = payload
        return payload.job_id

    def dequeue(self) -> Optional[JobPayload]:
        with self._lock:
            if not self._queue:
                return None
            payload = self._queue.popleft()
            self._statuses[payload.job_id] = JobStatus.RUNNING
            return payload

    def get_status(self, job_id: str) -> Optional[str]:
        with self._lock:
            return self._statuses.get(job_id)

    def update_status(self, job_id: str, status: str) -> None:
        with self._lock:
            self._statuses[job_id] = status

    def store_result(self, result: JobResult) -> None:
        with self._lock:
            self._results[result.job_id] = result
            self._statuses[result.job_id] = result.status

    def get_result(self, job_id: str) -> Optional[JobResult]:
        with self._lock:
            return self._results.get(job_id)

    def pending_count(self) -> int:
        with self._lock:
            return len(self._queue)

    def list_jobs(self) -> List[Dict[str, Any]]:
        with self._lock:
            jobs = []
            for job_id, status in self._statuses.items():
                entry: Dict[str, Any] = {"job_id": job_id, "status": status}
                payload = self._payloads.get(job_id)
                if payload:
                    entry["job_type"] = payload.job_type
                    entry["created_at"] = payload.created_at
                jobs.append(entry)
            return jobs
