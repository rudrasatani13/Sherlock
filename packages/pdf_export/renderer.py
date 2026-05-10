"""Print-ready HTML renderer for Phase 19 PDF exports."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from .models import PdfReportExport
from .safety import resolve_export_path, validate_pdf_export_safety


def render_print_html(export: PdfReportExport) -> str:
    """Render a dependency-light print/PDF-ready HTML document."""
    validate_pdf_export_safety(export)
    rows = "\n".join(_finding_row(row) for row in export.findings_table)
    detailed = "\n".join(_detailed_finding(finding) for finding in export.detailed_findings)
    tested = "\n".join(f"<li>{_e(item.get('display_name') or item.get('category'))}</li>" for item in export.tested_categories)
    not_tested = _list_items(export.not_tested)
    limitations = _list_items(export.limitations)
    top_fixes = "\n".join(
        f"<li><strong>{_e(fix.get('title'))}</strong><p>{_e(fix.get('recommendation'))}</p></li>"
        for fix in export.top_fixes
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{_e(export.title)}</title>
    <style>
      :root {{
        color: #172026;
        background: #f6f4ef;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      body {{ margin: 0; background: #f6f4ef; }}
      main {{ max-width: 920px; margin: 0 auto; background: #ffffff; min-height: 100vh; }}
      section, header, footer {{ padding: 34px 46px; border-bottom: 1px solid #d8d4ca; }}
      h1, h2, h3 {{ margin: 0 0 12px; line-height: 1.12; letter-spacing: 0; }}
      h1 {{ font-size: 38px; }}
      h2 {{ font-size: 23px; }}
      h3 {{ font-size: 18px; }}
      p, li, td, th, dd, dt {{ font-size: 13px; line-height: 1.55; }}
      table {{ border-collapse: collapse; width: 100%; margin-top: 14px; }}
      th, td {{ border: 1px solid #d8d4ca; padding: 9px; vertical-align: top; text-align: left; }}
      th {{ background: #f0eee7; }}
      dl {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px 22px; }}
      dt {{ color: #59636a; font-weight: 700; }}
      dd {{ margin: 0; }}
      .label {{ color: #6f4a1f; font-weight: 800; text-transform: uppercase; font-size: 11px; }}
      .cover {{ background: #172026; color: #fff; }}
      .cover dt {{ color: #b8c0c5; }}
      .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }}
      .metric {{ border: 1px solid #d8d4ca; padding: 14px; background: #faf9f5; }}
      .metric strong {{ display: block; font-size: 28px; }}
      .finding {{ break-inside: avoid; }}
      .evidence {{ background: #f7f7f4; border-left: 4px solid #6f4a1f; padding: 10px 12px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; white-space: pre-wrap; }}
      footer {{ color: #59636a; }}
      @page {{ margin: 18mm; }}
      @media print {{
        body, main {{ background: #fff; }}
        section, header, footer {{ break-inside: avoid; }}
      }}
    </style>
  </head>
  <body>
    <main>
      <header class="cover">
        <p class="label">{_e(export.cover_page.demo_static_label)}</p>
        <h1>{_e(export.cover_page.report_title)}</h1>
        <p>{_e(export.cover_page.brand)} {_e(export.cover_page.product_name)} PDF-ready report export.</p>
        <dl>
          <div><dt>Project</dt><dd>{_e(export.cover_page.project_name)}</dd></div>
          <div><dt>Target</dt><dd>{_e(export.cover_page.target_name)}</dd></div>
          <div><dt>Scan type</dt><dd>{_e(export.cover_page.scan_type)}</dd></div>
          <div><dt>Report date</dt><dd>{_e(export.cover_page.report_date)}</dd></div>
          <div><dt>Report ID</dt><dd>{_e(export.cover_page.report_id)}</dd></div>
          <div><dt>Export ID</dt><dd>{_e(export.export_id)}</dd></div>
        </dl>
        <p>{_e(export.cover_page.disclaimer)}</p>
      </header>
      <section>
        <p class="label">Executive summary</p>
        <h2>Launch readiness summary</h2>
        <p>{_e(export.executive_summary)}</p>
      </section>
      <section>
        <p class="label">Verdict and score</p>
        <div class="grid">
          <div class="metric"><span>Verdict</span><strong>{_e(export.verdict.get("label"))}</strong><p>{_e(export.verdict.get("summary"))}</p></div>
          <div class="metric"><span>Score</span><strong>{_e(export.score.get("score"))}/{_e(export.score.get("max_score"))}</strong><p>{_e(export.score.get("rating"))}</p></div>
          <div class="metric"><span>Total findings</span><strong>{_e(export.severity_breakdown.get("total"))}</strong><p>Severity breakdown for the documented scope.</p></div>
        </div>
      </section>
      <section>
        <p class="label">Top fixes</p>
        <h2>Recommended remediation order</h2>
        <ol>{top_fixes}</ol>
      </section>
      <section>
        <p class="label">Findings table</p>
        <h2>Actionable findings summary</h2>
        <table>
          <thead><tr><th>Finding</th><th>Category</th><th>Severity</th><th>Confidence</th><th>Status</th><th>Fix</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </section>
      <section>
        <p class="label">Detailed findings</p>
        <h2>Evidence, reproduction, and fixes</h2>
        {detailed}
      </section>
      <section>
        <p class="label">Scope</p>
        <h2>Tested categories and not-tested scope</h2>
        <h3>Tested categories</h3>
        <ul>{tested}</ul>
        <h3>Not tested</h3>
        <ul>{not_tested}</ul>
      </section>
      <section>
        <p class="label">Limitations and evidence handling</p>
        <h2>Report boundaries</h2>
        <ul>{limitations}</ul>
        <p>{_e(export.evidence_handling_note)}</p>
        <p><strong>Retest status placeholder:</strong> Phase 19 keeps retest status display only. Phase 20 retest flow is not implemented.</p>
      </section>
      <footer>
        <p>{_e(export.footer_disclaimer)}</p>
        <p>Generated artifact path is local-only when written by the CLI. Public sharing, billing gates, production storage, and customer PDF delivery are not live.</p>
      </footer>
    </main>
  </body>
</html>
"""


def write_print_html(export: PdfReportExport, output_dir: str | Path = "pdf-exports", *, base_dir: str | Path = ".") -> Path:
    """Write print-ready HTML to an allowed ignored local output directory."""
    validate_pdf_export_safety(export)
    target = resolve_export_path(output_dir, export.filename, base_dir=base_dir)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_print_html(export), encoding="utf-8")
    return target


def _finding_row(row: object) -> str:
    return (
        "<tr>"
        f"<td>{_e(getattr(row, 'title', ''))}</td>"
        f"<td>{_e(getattr(row, 'category', ''))}</td>"
        f"<td>{_e(getattr(row, 'severity', ''))}</td>"
        f"<td>{_e(getattr(row, 'confidence', ''))}</td>"
        f"<td>{_e(getattr(row, 'status', ''))}</td>"
        f"<td>{_e(getattr(row, 'fix_recommendation_summary', ''))}</td>"
        "</tr>"
    )


def _detailed_finding(finding: object) -> str:
    evidence = "\n".join(f'<div class="evidence">{_e(item)}</div>' for item in getattr(finding, "evidence_snippets", []))
    steps = _list_items(getattr(finding, "reproduction_steps", []))
    limitations = _list_items(getattr(finding, "limitations", []))
    return f"""
        <article class="finding">
          <h3>{_e(getattr(finding, "finding_id", ""))}: {_e(getattr(finding, "title", ""))}</h3>
          <p><strong>Category:</strong> {_e(getattr(finding, "category", ""))} | <strong>Severity:</strong> {_e(getattr(finding, "severity", ""))} | <strong>Confidence:</strong> {_e(getattr(finding, "confidence", ""))} | <strong>Status:</strong> {_e(getattr(finding, "status", ""))}</p>
          <p>{_e(getattr(finding, "description", ""))}</p>
          <p><strong>Business impact:</strong> {_e(getattr(finding, "business_impact", ""))}</p>
          <h4>Evidence snippets</h4>{evidence}
          <h4>Reproduction steps</h4><ol>{steps}</ol>
          <h4>Fix recommendation</h4><p>{_e(getattr(finding, "fix_recommendation", ""))}</p>
          <h4>Limitations</h4><ul>{limitations}</ul>
          <p><strong>Retest status:</strong> {_e(getattr(finding, "retest_status", ""))}</p>
        </article>
    """


def _list_items(items: Iterable[object]) -> str:
    return "\n".join(f"<li>{_e(item)}</li>" for item in items)


def _e(value: object) -> str:
    return escape(str(value or ""), quote=True)
