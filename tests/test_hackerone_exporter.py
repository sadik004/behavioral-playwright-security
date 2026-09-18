"""
Unit tests for HackerOne Triaged Report Template Engine
Module: test_hackerone_exporter.py
"""

import os
import tempfile
import pytest
from pathlib import Path

from behavioral_evasion_suite.hackerone_template_engine import (
    HackerOneTemplateEngine,
    HackerOneReportDTO
)
from behavioral_evasion_suite.dynamic_probe_protocol import (
    DynamicProbeSpec,
    DynamicProbeResult
)
from behavioral_evasion_suite.clinical_orchestrator import HackerOneSubmissionReport


def test_01_report_dto_rendering():
    """Verifies markdown formatting and all 6 required triage sections."""
    dto = HackerOneReportDTO(
        title="Prototype Pollution in Target API",
        target_url="https://api.target.com/v1/update",
        cwe_id="CWE-1321",
        severity="High",
        cvss_score=7.5,
        summary="Server-side prototype pollution detected via json spaces mutation.",
        business_impact="Global prototype alteration leading to logic bypass.",
        steps_to_reproduce=[
            "Send POST request to target endpoint.",
            "Inspect json spaces indentation in HTTP response.",
            "Verify rollback restored baseline formatting."
        ],
        curl_command='curl -X POST "https://api.target.com/v1/update" -d \'{"__proto__":{"json spaces":10}}\'',
        raw_evidence="HTTP/1.1 200 OK\n10-space indentation detected",
        remediation_guidance="Use Object.create(null) or sanitize input keys.",
        remediation_code_snippet="Object.freeze(Object.prototype);"
    )

    md = HackerOneTemplateEngine.render_markdown(dto)

    assert "# Prototype Pollution in Target API" in md
    assert "## 1. Executive Summary" in md
    assert "## 2. Vulnerability Classification" in md
    assert "`CWE-1321`" in md
    assert "**High**" in md
    assert "## 3. Business & Security Impact" in md
    assert "## 4. Step-by-Step Reproduction Guide" in md
    assert "1. Send POST request to target endpoint." in md
    assert "```bash\ncurl -X POST" in md
    assert "## 5. Raw Evidence & Verification" in md
    assert "## 6. Remediation & Fix Guidance" in md
    assert "Object.freeze(Object.prototype);" in md


def test_02_from_dynamic_probe_conversion():
    """Verifies that dynamic probe execution can be directly converted to a triaged report."""
    spec = DynamicProbeSpec(
        probe_name="graphql_introspection_leak",
        target_endpoint="/graphql",
        method="POST",
        headers={"Content-Type": "application/json"},
        payload={"query": "{__schema{types{name}}}"},
        mutation_check_type="body_substring",
        expected_indicator="__schema",
        cwe="CWE-200"
    )

    result = DynamicProbeResult(
        probe_name="graphql_introspection_leak",
        target_endpoint="/graphql",
        vulnerable=True,
        evidence="Observed __schema root type definitions in response body",
        mutation_detected=True,
        rollback_success=True,
        duration_ms=12.4
    )

    report_dto = HackerOneTemplateEngine.from_dynamic_probe(
        spec=spec,
        result=result,
        target_url="https://api.target.com/graphql"
    )

    assert report_dto.cwe_id == "CWE-200"
    assert "Graphql Introspection Leak" in report_dto.title
    assert "curl -s -i -X POST" in report_dto.curl_command
    assert "ApolloServer" in report_dto.remediation_code_snippet

    md = HackerOneTemplateEngine.render_markdown(report_dto)
    assert "CWE-200" in md
    assert "Observed __schema root type definitions" in md


def test_03_export_to_file():
    """Verifies writing markdown report to disk."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = Path(tmp_dir) / "HackerOne_Report.md"

        dto = HackerOneReportDTO(
            title="Header Smuggling Diagnostic",
            target_url="https://api.target.com",
            cwe_id="CWE-444",
            summary="Diagnostic summary",
            business_impact="Impact summary",
            steps_to_reproduce=["Step 1"],
            curl_command="curl https://api.target.com",
            raw_evidence="Reflected header",
            remediation_guidance="Sanitize reverse proxy headers"
        )

        saved_path = HackerOneTemplateEngine.export_to_file(dto, output_path=out_file)
        assert saved_path.exists()
        assert out_file.read_text(encoding="utf-8").startswith("# Header Smuggling Diagnostic")


def test_04_legacy_hackerone_submission_report_rendering():
    """Verifies compatibility with existing clinical orchestrator reports."""
    legacy = HackerOneSubmissionReport(
        title="Legacy Finding",
        target_url="https://example.com",
        cwe_id="CWE-1321",
        severity="Critical",
        vulnerability_summary="Prototype pollution",
        steps_to_reproduce="Step 1",
        curl_proof_of_concept="curl https://example.com",
        business_impact="DoS",
        remediation_guidance="Upgrade express"
    )

    rendered = HackerOneTemplateEngine.render_markdown(legacy)
    assert "# Legacy Finding" in rendered
    assert "CWE-1321" in rendered
