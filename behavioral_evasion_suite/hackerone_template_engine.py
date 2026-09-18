"""
HackerOne Triaged Report Template Engine (v1.0 Enterprise)
Module: hackerone_template_engine.py

Translates raw diagnostic telemetry, SSPP scan results, and dynamic probe outputs
into polished, triage-ready HackerOne markdown submission reports.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

try:
    from .clinical_orchestrator import HackerOneSubmissionReport
except ImportError:
    from clinical_orchestrator import HackerOneSubmissionReport

try:
    from .dynamic_probe_protocol import DynamicProbeSpec, DynamicProbeResult
except ImportError:
    from dynamic_probe_protocol import DynamicProbeSpec, DynamicProbeResult


class HackerOneReportDTO(BaseModel):
    """Normalized DTO for HackerOne submission rendering."""
    title: str
    target_url: str
    cwe_id: str
    severity: str = "Medium"
    cvss_score: float = 6.5
    summary: str
    business_impact: str
    steps_to_reproduce: List[str]
    curl_command: str
    raw_evidence: str
    remediation_guidance: str
    remediation_code_snippet: Optional[str] = None
    research_reference: str = "Bug Hunter Automated Clinical Engine"
    timestamp: float = Field(default_factory=time.time)


class HackerOneTemplateEngine:
    """Master exporter converting diagnostic outputs to structured HackerOne markdown."""

    CWE_REMEDIATION_MAP: Dict[str, Dict[str, str]] = {
        "CWE-1321": {
            "name": "Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution')",
            "impact": "An attacker can inject malicious properties into the server's global Object.prototype, altering application flow, enabling authorization bypasses, or corrupting state across all concurrent sessions.",
            "remediation": "Use Object.create(null) for unprototyped hash maps, freeze sensitive prototypes via Object.freeze(Object.prototype), validate recursive merge keys to reject __proto__, constructor, and prototype, or upgrade vulnerable parser dependencies.",
            "snippet": "const safeObject = Object.create(null);\n// Or sanitize input:\nfunction sanitizeKey(key) {\n  if (['__proto__', 'constructor', 'prototype'].includes(key)) {\n    throw new Error('Disallowed prototype key');\n  }\n  return key;\n}"
        },
        "CWE-200": {
            "name": "Exposure of Sensitive Information to an Unauthorized Actor",
            "impact": "Schema introspection exposure allows attackers to map internal types, hidden queries, administrative mutations, and backend business logic schemas.",
            "remediation": "Disable GraphQL schema introspection in production environments. Configure Apollo Server / GraphQL Yoga with introspection: false when NODE_ENV === 'production'.",
            "snippet": "const server = new ApolloServer({\n  typeDefs,\n  resolvers,\n  introspection: process.env.NODE_ENV !== 'production'\n});"
        },
        "CWE-444": {
            "name": "Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling')",
            "impact": "Discrepancies in reverse proxy and backend header handling enable cache poisoning, header reflection, and routing bypasses.",
            "remediation": "Enforce strict HTTP/2 protocol enforcement on reverse proxies, sanitize incoming X-Forwarded-* headers, and disable unkeyed header routing in caching layers.",
            "snippet": "proxy_set_header X-Forwarded-Host $host;\nproxy_hide_header X-Forwarded-Host;"
        }
    }

    @classmethod
    def from_dynamic_probe(
        cls,
        spec: DynamicProbeSpec,
        result: DynamicProbeResult,
        target_url: str = ""
    ) -> HackerOneReportDTO:
        """Constructs a HackerOneReportDTO from a dynamic probe execution."""
        cwe_info = cls.CWE_REMEDIATION_MAP.get(spec.cwe, {
            "name": spec.cwe,
            "impact": "Unsanitized client-controllable input mutates server state or reflections.",
            "remediation": "Implement strict input validation, type contracts, and defensive boundary sanitation.",
            "snippet": "# Sanitize input at boundary\nassert is_valid(input_data)"
        })

        # Build clean cURL command
        headers_str = " ".join([f"-H \"{k}: {v}\"" for k, v in spec.headers.items()])
        data_str = f" -d '{json.dumps(spec.payload)}'" if spec.payload else ""
        url = target_url or result.target_endpoint
        curl_cmd = f"curl -s -i -X {spec.method.upper()} \"{url}\" {headers_str}{data_str}"

        steps = [
            f"Navigate or send HTTP request to the target endpoint: `{url}`.",
            f"Inject the diagnostic headers: `{spec.headers}`." if spec.headers else "Send requested payload structure.",
            f"Observe differential mutation or reflection conforming to indicator: `{spec.expected_indicator}`.",
            f"Observed evidence captured: `{result.evidence}`."
        ]

        return HackerOneReportDTO(
            title=f"Security Finding: {spec.probe_name.replace('_', ' ').title()} on {url}",
            target_url=url,
            cwe_id=spec.cwe,
            severity="High" if spec.cwe == "CWE-1321" else "Medium",
            cvss_score=7.5 if spec.cwe == "CWE-1321" else 5.3,
            summary=f"Automated surgical audit detected confirmed anomaly `{spec.probe_name}` conforming to {cwe_info['name']}.",
            business_impact=cwe_info["impact"],
            steps_to_reproduce=steps,
            curl_command=curl_cmd,
            raw_evidence=result.evidence,
            remediation_guidance=cwe_info["remediation"],
            remediation_code_snippet=cwe_info.get("snippet"),
            research_reference=spec.research_source
        )

    @classmethod
    def render_markdown(cls, report: Union[HackerOneReportDTO, HackerOneSubmissionReport]) -> str:
        """Renders complete, polished HackerOne submission markdown."""
        if isinstance(report, HackerOneSubmissionReport):
            # Convert legacy orchestrator report
            return report.to_markdown()

        steps_rendered = "\n".join([f"{idx+1}. {step}" for idx, step in enumerate(report.steps_to_reproduce)])
        snippet_rendered = (
            f"\n\n### Code Remediation Example:\n```javascript\n{report.remediation_code_snippet}\n```"
            if report.remediation_code_snippet
            else ""
        )

        md = f"""# {report.title}

## 1. Executive Summary
{report.summary}

## 2. Vulnerability Classification
- **CWE Identifier:** `{report.cwe_id}`
- **Assessed Severity:** **{report.severity}** (Estimated CVSS: {report.cvss_score})
- **Target URL / Asset:** `{report.target_url}`
- **Knowledge / Research Reference:** {report.research_reference}

## 3. Business & Security Impact
{report.business_impact}

## 4. Step-by-Step Reproduction Guide
{steps_rendered}

### Proof of Concept (cURL Command):
```bash
{report.curl_command}
```

## 5. Raw Evidence & Verification
```text
{report.raw_evidence}
```

## 6. Remediation & Fix Guidance
{report.remediation_guidance}{snippet_rendered}

---
*Report auto-generated via **Bug Hunter Enterprise Triage Engine** on {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report.timestamp))}*
"""
        return md.strip()

    @classmethod
    def export_to_file(
        cls,
        report: Union[HackerOneReportDTO, HackerOneSubmissionReport],
        output_path: Union[str, Path] = "HackerOne_Report.md"
    ) -> Path:
        """Renders markdown and writes to disk."""
        path = Path(output_path)
        content = cls.render_markdown(report)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
