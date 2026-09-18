# Behavioral Playwright Security: Clinical Bug Hunter Suite 🩺⚡

[![Automated Tests](https://img.shields.io/badge/tests-23%20passed-brightgreen.svg)](tests/)
[![Architecture](https://img.shields.io/badge/clean--architecture-3--tier-blue.svg)](behavioral_evasion_suite/)
[![WAF Evasion](https://img.shields.io/badge/WAF--Bypass-Cloudflare%20%7C%20DataDome%20%7C%20Akamai-purple.svg)](behavioral_evasion_suite/)
[![AI Doctor](https://img.shields.io/badge/AI--Doctor-Gemini%202.0%20Flash%20%7C%20NotebookLM-orange.svg)](behavioral_evasion_suite/doctor_bridge.py)
[![Bounty Target](https://img.shields.io/badge/Output-HackerOne%20Triaged%20Reports-red.svg)](behavioral_evasion_suite/clinical_orchestrator.py)

**Behavioral Playwright Security** is a production-grade, stateful autonomous web vulnerability auditing engine. It merges **biomechanical human evasion physics** (bypassing modern anti-bot systems like Cloudflare, DataDome, and Akamai) with a **Clinical Doctor-Patient diagnostic loop** powered by **Google Gemini 2.0 Flash**, **Google NotebookLM**, and curated security research from **PortSwigger Web Security** and **HackerOne**.

---

## 🏛️ The Clinical Bug Hunter Architecture

The engine treats the target web application like a **medical patient**, separating concerns across 4 strictly isolated layers:

```mermaid
graph TD
    subgraph Layer1["Layer 1: Pathology Diagnostic Lab (Stealth Browser)"]
        A[Target Web Application] -->|Non-Invasive Passive Telemetry| B[WebsiteDNAExtractor]
        B -->|Pydantic DTO Serialization| C[WebsiteDNAReport]
    end

    subgraph Layer2["Layer 2: Specialist Doctor Bridge (Diagnostic Intelligence)"]
        C --> D[GeminiDoctorBridge]
        D -->|Tier 1: 0ms Local Memory| E[LocalNotebookKnowledgeStore<br/>PortSwigger & HackerOne Papers]
        D -->|Tier 2: Source-Grounded Search| F[NotebookLMBridge<br/>Your Active Research Notebook]
        D -->|Tier 3: Live GenAI Reasoning| G[google.genai Client<br/>gemini-2.0-flash]
        E & F & G --> H[DoctorPrescription<br/>Targeted Surgical Probes]
    end

    subgraph Layer3["Layer 3: Surgical Strike & Safe Rollback (Pure HTTP Context)"]
        H --> I[ClinicalBugHunterOrchestrator]
        I -->|SSPP Surgical Probe| J[SSPPBlackBoxAuditor<br/>Differential Baselines]
        I -->|GraphQL Surgical Probe| K[GraphQLSecurityAuditor<br/>Introspection & Depth]
        J -->|Mandatory Reversion Payload| L[Zero-Footprint Rollback<br/>Restores Server Prototype]
    end

    subgraph Layer4["Layer 4: Triage & Submission (HackerOne Ready)"]
        J & K --> M[HackerOneSubmissionReport]
        M --> N[Markdown Report<br/>Reproducible cURL PoC + CVSS + Remediation]
    end
```

---

## 🚀 Key Superpowers

### 1. Full Behavioral Stealth Suite (WAF & Anti-Bot Armor)
Unlike traditional scanners that get blocked within seconds, this framework operates with full behavioral human cloaking:
- **Biomechanical Movement Physics**: 5th-order Bézier curves, jerk minimization, and subpixel mouse trajectory jitter.
- **CDP Evasion & Fingerprint Hardening**: 10-patch cloaking including Canvas shader noise, WebRTC masking, subpixel font variance, and WebAuthn virtual TPM.
- **TLS JA4 Network Stack Spoofing**: Simulates genuine modern Chromium networking fingerprints.

### 2. Clinical Doctor Diagnostic Reasoning
- **Website DNA Extraction**: Non-blocking passive analysis of framework signatures (`Next.js`, `Express`, `Apollo GraphQL`), REST routes, client-side DOM sinks, and WAF immune profiles.
- **Source-Grounded NotebookLM Integration**: Automatically connects to your private Google NotebookLM research notebooks for source-grounded vulnerability analysis.
- **Instant Fallback Local Store**: Offline in-memory database of PortSwigger, OWASP, and HackerOne writeups with zero latency.

### 3. Surgical Non-Destructive Testing & Rollback
- **Differential Baselines**: Validates mutations against standard baselines (eliminating false positives from generic error handlers or HTML redirects).
- **Mandatory Rollback Execution**: Server-side prototype pollution probes are immediately followed by clean reversion payloads (e.g. restoring `json spaces` to `0`, clearing polluted properties) ensuring zero server harm.

### 4. HackerOne Triaged Submission Reports
Automatically exports submission-ready markdown reports complete with:
- Executive Vulnerability Summary
- CVSS Severity Classification
- Copy-paste reproducible cURL Proof of Concept
- Concrete Remediation Instructions
- Verified Non-Destructive Ethical Disclaimers

---

## 🛠️ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/sadik004/behavioral-playwright-security.git
cd behavioral-playwright-security

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### Running an Automated Clinical Audit

```python
import asyncio
from behavioral_evasion_suite.clinical_orchestrator import ClinicalBugHunterOrchestrator
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate stealthily
        await page.goto("https://api.target.com")

        # Execute Clinical Orchestration
        orchestrator = ClinicalBugHunterOrchestrator()
        results = await orchestrator.execute_clinical_audit(
            request_context=page.request,
            target_url="https://api.target.com",
            page=page
        )
        
        for report in results["hackerone_reports"]:
            print(report["title"])
            print(report["curl_proof_of_concept"])

asyncio.run(run())
```

---

## 🧪 Automated Terminal Quality Gates

Run the complete 23-test test suite:

```bash
pytest tests/test_sspp_auditor.py tests/test_graphql_auditor.py tests/test_clinical_doctor.py -v
```

```text
============================= test session starts =============================
tests/test_sspp_auditor.py (7 passed)
tests/test_graphql_auditor.py (11 passed)
tests/test_clinical_doctor.py (5 passed)

============================= 23 passed in 0.40s ==============================
```

---

## 🛡️ Ethical & Legal Disclosure

This framework is built strictly for authorized security auditing, bug bounty programs adhering to HackerOne/Bugcrowd Safe Harbor policies, and defensive resilience engineering. Never audit targets without explicit written authorization.
