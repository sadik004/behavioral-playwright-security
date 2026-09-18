"""
Unit and Integration Tests for Dynamic Probe Synthesizer & Hot-Loader
Module: test_dynamic_synthesizer.py
"""

import asyncio
import os
import shutil
import tempfile
import pytest
from pathlib import Path

from behavioral_evasion_suite.dynamic_probe_protocol import (
    DynamicProbeSpec,
    DynamicProbeResult,
    BaseDynamicAuditor
)
from behavioral_evasion_suite.dynamic_synthesizer import DynamicSynthesizer
from behavioral_evasion_suite.doctor_bridge import (
    GeminiDoctorBridge,
    NotebookLMBridge,
    WebsiteDNAReport,
    EndpointDNA
)
from behavioral_evasion_suite.mcp_server import AVAILABLE_TOOLS


class MockFetchResponse:
    def __init__(self, status=200, headers=None, text=""):
        self.status = status
        self.headers = headers or {}
        self.text_content = text

    async def text(self):
        return self.text_content


class MockSessionContext:
    def __init__(self):
        self.url = "https://api.internal-target.com"
        self.requested = []

    class RequestMock:
        def __init__(self, outer):
            self.outer = outer

        async def fetch(self, url, method="GET", headers=None, data=None):
            self.outer.requested.append({"url": url, "method": method, "headers": headers, "data": data})
            # Return response that reflects canary header if present
            headers_resp = {}
            if headers and "X-Forwarded-Host" in headers:
                headers_resp["X-Forwarded-Host"] = headers["X-Forwarded-Host"]
            return MockFetchResponse(
                status=200,
                headers=headers_resp,
                text='{"status": "ok", "indicator": "found"}'
            )

    @property
    def request(self):
        return self.RequestMock(self)


@pytest.fixture
def temp_plugins_dir():
    temp_dir = Path(tempfile.mkdtemp(prefix="test_plugins_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_01_dynamic_probe_spec_validation():
    """Verifies DTO schema requirements and default fields."""
    spec = DynamicProbeSpec(
        probe_name="test_header_leak",
        target_endpoint="/api/v1/auth",
        method="POST",
        headers={"X-Test": "1"},
        mutation_check_type="header_reflection",
        expected_indicator="reflected_val",
        cwe="CWE-200"
    )
    assert spec.probe_name == "test_header_leak"
    assert spec.method == "POST"
    assert spec.cwe == "CWE-200"
    assert spec.research_source == "NotebookLM Optimal Synthesis"


def test_02_synthesizer_code_generation(temp_plugins_dir):
    """Verifies local template synthesis writes syntactically valid Python code."""
    synth = DynamicSynthesizer(plugins_dir=temp_plugins_dir)
    spec = DynamicProbeSpec(
        probe_name="sample_header_probe",
        target_endpoint="/test",
        method="GET",
        headers={"X-Forwarded-Host": "security-canary.internal"},
        mutation_check_type="header_reflection",
        expected_indicator="security-canary.internal",
        cwe="CWE-444"
    )
    file_path = synth.synthesize_probe(spec)
    assert file_path.exists()
    assert file_path.name == "sample_header_probe.py"

    # Verify python syntax
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    compile(code, str(file_path), "exec")
    assert "class SynthesizedAuditor(BaseDynamicAuditor):" in code


@pytest.mark.asyncio
async def test_03_hot_load_and_live_execution(temp_plugins_dir):
    """Verifies that generated code is immediately loaded into memory via importlib and executed."""
    synth = DynamicSynthesizer(plugins_dir=temp_plugins_dir)
    spec = DynamicProbeSpec(
        probe_name="canary_reflection_probe",
        target_endpoint="/",
        method="GET",
        headers={"X-Forwarded-Host": "security-canary.internal"},
        mutation_check_type="header_reflection",
        expected_indicator="security-canary.internal",
        rollback_payload={"reset": True},
        cwe="CWE-444"
    )

    mock_session = MockSessionContext()

    # Synthesize and execute in one call without git persist
    result = await synth.synthesize_and_execute(spec, mock_session, auto_persist=False)

    assert isinstance(result, DynamicProbeResult)
    assert result.probe_name == "canary_reflection_probe"
    assert result.vulnerable is True
    assert result.mutation_detected is True
    assert "Header match" in result.evidence
    assert result.duration_ms >= 0.0
    assert result.rollback_success is True


@pytest.mark.asyncio
async def test_04_doctor_bridge_synthesis_graphql():
    """Verifies that GeminiDoctorBridge synthesizes GraphQL optimal probe deterministically."""
    doctor = GeminiDoctorBridge()
    dna = WebsiteDNAReport(
        target_url="https://api.example.com",
        framework_hints=["Apollo GraphQL", "Node.js"],
        endpoints=[EndpointDNA(url="https://api.example.com/graphql", method="POST", is_rest_api=False)]
    )
    spec = await doctor.synthesize_optimal_probe(dna)
    assert spec.probe_name == "graphql_introspection_check"
    assert spec.target_endpoint == "/graphql"
    assert spec.method == "POST"
    assert spec.cwe == "CWE-200"


@pytest.mark.asyncio
async def test_05_doctor_bridge_synthesis_express():
    """Verifies that GeminiDoctorBridge synthesizes Express SSPP optimal probe deterministically."""
    doctor = GeminiDoctorBridge()
    dna = WebsiteDNAReport(
        target_url="https://api.example.com",
        framework_hints=["Express.js", "Node.js"],
        endpoints=[EndpointDNA(url="https://api.example.com/api/v1/status", method="POST", is_rest_api=True)]
    )
    spec = await doctor.synthesize_optimal_probe(dna)
    assert spec.probe_name == "express_json_spaces_sspp"
    assert spec.cwe == "CWE-1321"
    assert spec.rollback_payload is not None


def test_06_mcp_tool_registration():
    """Verifies dynamic_diagnose_and_synthesize is properly exposed in MCP AVAILABLE_TOOLS."""
    tool_names = [t["name"] for t in AVAILABLE_TOOLS]
    assert "dynamic_diagnose_and_synthesize" in tool_names

    tool_def = next(t for t in AVAILABLE_TOOLS if t["name"] == "dynamic_diagnose_and_synthesize")
    assert "session_id" in tool_def["inputSchema"]["required"]
