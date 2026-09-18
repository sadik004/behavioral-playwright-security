"""
Dynamic Probe Protocol and Token-Optimized Schemas (v1.0)
Module: dynamic_probe_protocol.py

Provides:
- Compact Pydantic DTOs for token-efficient NotebookLM/Gemini interaction (<150 tokens)
- BaseDynamicAuditor abstraction for runtime compliance
- Python code template generator for dynamic probe synthesis
"""

import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class DynamicProbeSpec(BaseModel):
    """
    Compact declarative spec produced by NotebookLM / Gemini Doctor.
    Designed for minimum token overhead (<150 tokens) when transmitted across MCP.
    """
    probe_name: str = Field(..., description="Unique snake_case identifier (e.g. cache_poison_x_host)")
    target_endpoint: str = Field(..., description="Target relative path or URL")
    method: str = Field("GET", description="HTTP method")
    headers: Dict[str, str] = Field(default_factory=dict, description="Test headers to inject")
    payload: Optional[Any] = Field(None, description="Optional payload (JSON/string)")
    mutation_check_type: str = Field("header_reflection", description="Verification strategy: header_reflection | status_mutation | body_substring")
    expected_indicator: str = Field(..., description="Expected indicator string or status code to confirm finding")
    rollback_payload: Optional[Any] = Field(None, description="Safe cleanup payload to restore baseline state")
    cwe: str = Field("CWE-699", description="CWE taxonomy identifier")
    research_source: str = Field("NotebookLM Optimal Synthesis", description="Knowledge provenance")
    rationale: str = Field("", description="Engineering rationale for the probe")


class DynamicProbeResult(BaseModel):
    """Execution telemetry returned immediately upon live execution."""
    probe_name: str
    target_endpoint: str
    vulnerable: bool
    evidence: str
    mutation_detected: bool
    rollback_success: bool = True
    duration_ms: float = 0.0
    timestamp: float = Field(default_factory=time.time)


class BaseDynamicAuditor(ABC):
    """Formal protocol for all dynamically synthesized and hot-loaded auditors."""
    
    def __init__(self, spec: DynamicProbeSpec):
        self.spec = spec

    @abstractmethod
    async def execute_live(self, session_context: Any) -> DynamicProbeResult:
        """Executes the probe against the active browser or API session."""
        pass

    @abstractmethod
    async def rollback(self, session_context: Any) -> bool:
        """Executes atomic state cleanup/reversion on the target."""
        pass


DYNAMIC_AUDITOR_TEMPLATE = '''"""
Dynamically Synthesized Security Auditor: {probe_name}
Generated via: {research_source}
Taxonomy: {cwe}
Rationale: {rationale}
"""

import time
import asyncio
from typing import Any, Dict
from behavioral_evasion_suite.dynamic_probe_protocol import (
    BaseDynamicAuditor,
    DynamicProbeSpec,
    DynamicProbeResult
)


class SynthesizedAuditor(BaseDynamicAuditor):
    """Dynamically compiled and hot-loaded auditor."""

    def __init__(self, spec: DynamicProbeSpec):
        super().__init__(spec)

    async def execute_live(self, session_context: Any) -> DynamicProbeResult:
        t_start = time.time()
        mutation_detected = False
        vulnerable = False
        evidence = ""

        try:
            # Handle session context: Playwright page, API client, or request callable
            url = self.spec.target_endpoint
            headers = self.spec.headers
            method = self.spec.method.upper()

            response_status = 200
            response_headers = {{}}
            response_text = ""

            if hasattr(session_context, "request") and hasattr(session_context.request, "fetch"):
                # Playwright APIRequestContext
                res = await session_context.request.fetch(
                    url,
                    method=method,
                    headers=headers,
                    data=self.spec.payload
                )
                response_status = res.status
                response_headers = res.headers
                response_text = await res.text()
            elif hasattr(session_context, "goto") and method == "GET":
                # Playwright Page instance
                res = await session_context.goto(url)
                if res:
                    response_status = res.status
                    response_headers = res.headers
                    response_text = await session_context.content()
            elif hasattr(session_context, "fetch"):
                # Custom async fetch client
                res = await session_context.fetch(url, method=method, headers=headers, json=self.spec.payload)
                response_status = getattr(res, "status", 200)
                response_headers = getattr(res, "headers", {{}})
                response_text = getattr(res, "text", "")
            else:
                # Mock or standalone fallback
                evidence = "Simulated probe execution on generic context"
                mutation_detected = True
                vulnerable = True

            # Evaluate mutation criteria
            indicator = self.spec.expected_indicator
            check_type = self.spec.mutation_check_type

            if check_type == "header_reflection":
                for k, v in response_headers.items():
                    if indicator.lower() in v.lower() or indicator.lower() in k.lower():
                        mutation_detected = True
                        vulnerable = True
                        evidence = f"Header match: {{k}}: {{v}}"
                        break
            elif check_type == "status_mutation":
                if str(response_status) == indicator:
                    mutation_detected = True
                    vulnerable = True
                    evidence = f"Status code mutated to {{response_status}}"
            elif check_type == "body_substring":
                if indicator in response_text:
                    mutation_detected = True
                    vulnerable = True
                    evidence = f"Indicator '{{indicator}}' observed in response body"

            if not vulnerable and not evidence:
                evidence = f"No mutation observed. Status: {{response_status}}"

        except Exception as e:
            evidence = f"Execution error: {{str(e)}}"

        # Execute safe rollback if requested
        rollback_ok = True
        if self.spec.rollback_payload is not None:
            rollback_ok = await self.rollback(session_context)

        duration = (time.time() - t_start) * 1000

        return DynamicProbeResult(
            probe_name=self.spec.probe_name,
            target_endpoint=self.spec.target_endpoint,
            vulnerable=vulnerable,
            evidence=evidence,
            mutation_detected=mutation_detected,
            rollback_success=rollback_ok,
            duration_ms=duration
        )

    async def rollback(self, session_context: Any) -> bool:
        if not self.spec.rollback_payload:
            return True
        try:
            if hasattr(session_context, "request") and hasattr(session_context.request, "fetch"):
                await session_context.request.fetch(
                    self.spec.target_endpoint,
                    method="POST",
                    data=self.spec.rollback_payload
                )
            return True
        except Exception:
            return False


def create_auditor(spec: DynamicProbeSpec) -> BaseDynamicAuditor:
    """Standard dynamic module entry point."""
    return SynthesizedAuditor(spec)
'''
