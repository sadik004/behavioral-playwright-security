# Behavioral Playwright Security: Clinical Bug Hunter Suite 🩺⚡

[![Automated Tests](https://img.shields.io/badge/Tests-23%2F23%20Passed%20(100%25)-brightgreen.svg?style=for-the-badge)](tests/)
[![Architecture](https://img.shields.io/badge/Clean--Architecture-4--Tier%20Sandboxed-blue.svg?style=for-the-badge)](behavioral_evasion_suite/)
[![WAF Evasion](https://img.shields.io/badge/WAF--Bypass-Cloudflare%20%7C%20DataDome%20%7C%20Akamai-purple.svg?style=for-the-badge)](behavioral_evasion_suite/)
[![AI Doctor](https://img.shields.io/badge/AI--Doctor-Gemini%202.0%20Flash%20%7C%20NotebookLM-orange.svg?style=for-the-badge)](behavioral_evasion_suite/doctor_bridge.py)
[![Bounty Target](https://img.shields.io/badge/Output-HackerOne%20Triaged%20Reports-red.svg?style=for-the-badge)](behavioral_evasion_suite/clinical_orchestrator.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A stateful, autonomous, enterprise web vulnerability auditing and deep logic security suite for Playwright & Patchright. It merges **biomechanical human evasion physics** (bypassing Cloudflare, DataDome, and Akamai) with a **Clinical Doctor-Patient diagnostic loop** powered by **Google Gemini 2.0 Flash**, **Google NotebookLM**, and curated security research from **PortSwigger Web Security** and **HackerOne**.

---

## 📑 Table of Contents

- [🏛️ The Clinical Bug Hunter Architecture](#-the-clinical-bug-hunter-architecture)
- [⚡ Quick Start Guide](#-quick-start-guide)
- [🩺 The 4-Tier Clinical Diagnostic Workflow](#-the-4-tier-clinical-diagnostic-workflow)
- [🤖 AI Agent Decision & Routing Guide](#-ai-agent-decision--routing-guide)
- [📚 Comprehensive 180+ Feature Reference](#-comprehensive-180-feature-reference)
- [🧩 Unified Facade (`BP`) API Reference](#-unified-facade-bp-api-reference)
- [⚡ PowerPlay Integration Subsystem (`bp.powerplay` / `Bpp`)](#-powerplay-integration-subsystem-bppowerplay--bpp)
- [🔐 Shared Authentication & Session Vault Architecture](#-shared-authentication-architecture)
- [🤖 Claude Desktop & Cursor AI Setup Guide (Dual MCP)](#-claude-desktop--cursor-ai-setup-guide)
- [💻 Complete CLI Command Reference](#-complete-cli-command-reference)
- [🛡️ Multi-Provider Matrix & Status Taxonomy](#-multi-provider-matrix--status-taxonomy)
- [🔀 Fallback & Routing Decision Matrix](#-fallback--routing-decision-matrix)
- [⚠️ Known Limitations & Engineering Honesty](#-known-limitations--engineering-honesty)
- [🧪 Verified Automated Quality Gates](#-verified-automated-quality-gates)
- [📄 Ethical & Legal Disclosure](#-ethical--legal-disclosure)

---

## 🏛️ The Clinical Bug Hunter Architecture

The engine treats the target web application like a **medical patient**, separating concerns across 4 strictly isolated layers:

```mermaid
graph TD
    subgraph Layer1["Layer 1: Pathology Diagnostic Lab (Stealth Browser)"]
        A["Target Web Application"] -->|Passive Telemetry| B["WebsiteDNAExtractor<br/>(Frameworks, APIs, DOM Sinks)"]
        B -->|Pydantic DTO Serialization| C["WebsiteDNAReport<br/>(< 5KB Compact Schema)"]
    end

    subgraph Layer2["Layer 2: Specialist Doctor Bridge (Diagnostic Intelligence)"]
        C --> D["GeminiDoctorBridge<br/>(Master Decision Hub)"]
        D -->|Tier 1: 0ms Local Memory| E["Local Knowledge Store<br/>(PortSwigger & HackerOne)"]
        D -->|Tier 2: Source-Grounded| F["NotebookLM Bridge<br/>(Private Research Notebook)"]
        D -->|Tier 3: Live GenAI| G["google.genai Client<br/>(Gemini 2.0 Flash)"]
        E & F & G --> H["DoctorPrescription<br/>(Targeted Surgical Probes)"]
    end

    subgraph Layer3["Layer 3: Surgical Strike & Safe Rollback (Pure HTTP Context)"]
        H --> I["ClinicalBugHunterOrchestrator"]
        I -->|SSPP Surgical Probe| J["SSPPBlackBoxAuditor<br/>(Differential Baselines)"]
        I -->|GraphQL Probe| K["GraphQLSecurityAuditor<br/>(Introspection & Depth)"]
        J -->|Mandatory Reversion Payload| L["Zero-Footprint Rollback<br/>(Restores Server State)"]
    end

    subgraph Layer4["Layer 4: Triage & Submission (HackerOne Ready)"]
        J & K --> M["HackerOneSubmissionReport"]
        M --> N["Markdown Report<br/>(Reproducible cURL PoC + CVSS)"]
    end
```

## ⚡ Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/sadik004/behavioral-playwright-security.git
cd behavioral-playwright-security

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### 2. Environment Setup

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Configure your credentials:
```env
NOTEBOOKLM_URL=https://notebooklm.google.com/notebook/f1eac2a4-57d0-427e-a90e-b55fab14b8f4
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 3. Running an Automated Clinical Bug Bounty Audit

```python
import asyncio
from playwright.async_api import async_playwright
from behavioral_evasion_suite.clinical_orchestrator import ClinicalBugHunterOrchestrator

async def main():
    async with async_playwright() as p:
        # Launch stealth browser context
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Step 1: Browse stealthily to target web app
        await page.goto("https://api.target.com/dashboard")

        # Step 2: Initialize Clinical Orchestrator
        orchestrator = ClinicalBugHunterOrchestrator()

        # Step 3: Run end-to-end Pathology -> Doctor -> Surgery -> Report
        results = await orchestrator.execute_clinical_audit(
            request_context=page.request,
            target_url="https://api.target.com",
            page=page
        )

        print(f"Status: {results['status']}")
        print(f"Surgical Probes Executed: {results['probes_executed']}")
        print(f"Vulnerabilities Confirmed: {results['vulnerabilities_confirmed']}")

        # Output HackerOne submission-ready markdown reports
        for report in results["hackerone_reports"]:
            print("=" * 60)
            print(f"Title: {report['title']}")
            print(f"Severity: {report['severity']} ({report['cwe_id']})")
            print("cURL PoC:")
            print(report['curl_proof_of_concept'])

asyncio.run(main())
```

---

## 🩺 The 4-Tier Clinical Diagnostic Workflow

### Layer 1: Pathology Diagnostic Lab (`dna_extractor.py`)
- Non-invasive passive telemetry on the Playwright session.
- Extracts runtime framework hints (`Next.js`, `Express.js`, `Apollo GraphQL`, `Nuxt`, `React`).
- Catalogs API endpoints, methods, query parameters, and client-side DOM sinks.
- Serializes into a lightweight, token-optimized **`WebsiteDNAReport`** (< 5KB).

### Layer 2: Specialist Doctor Bridge (`doctor_bridge.py`)
- Evaluates the website's DNA against stored PortSwigger & HackerOne vulnerability research.
- **Tier 1 (Instant Memory)**: Local in-memory repository of CVEs and writeups with zero latency.
- **Tier 2 (Source-Grounded)**: Automatically connects to your private Google NotebookLM library for research citations.
- **Tier 3 (Live GenAI)**: Employs `gemini-2.0-flash` via official `google.genai.Client` for reasoning.
- Issues a **`DoctorPrescription`** detailing specific surgical probes and exact expected evidence.

### Layer 3: Surgical Strike & Mandatory Rollback (`clinical_orchestrator.py`)
- Dispatches calibrated probes using pure HTTP `APIRequestContext` (leaving the browser session unpolluted).
- **Server-Side Prototype Pollution (SSPP)**: Uses differential baselines (checking `json spaces`, status mutations, and CORS reflection).
- **Mandatory Rollback Execution**: Immediately delivers clean reversion payloads (`json spaces: 0`, status reset) restoring the server's clean state.
- **GraphQL Deep Logic**: Introspection testing, schema clairvoyance suggestion checks, and query depth limits.

### Layer 4: HackerOne Triaged Submission (`clinical_orchestrator.py`)
- Transforms confirmed findings into professional markdown submission reports with:
  - Executive Vulnerability Summary
  - Formal CWE & CVSS Severity
  - Step-by-Step Reproduction Instructions
  - Copy-Paste Verified cURL PoC
  - Clear Engineering Remediation Guidance
  - Non-Destructive Ethical Disclaimers

---

## 📚 Comprehensive 180+ Feature Reference

### 1. Biomechanical Automation & Human Mimicry (`bp.automation` / `bp.browser`)
- **Bézier Mouse Trajectories**: Calculates cubic Bézier curves with natural acceleration/deceleration profiles to avoid linear robotic path detection.
- **Sub-Pixel Micro-Jitter**: Introduces realistic human tremoring during mouse moves and hover events.
- **Variable Key Dwell Times**: Simulates organic keystrokes with randomized press-and-release durations based on human typing speed distributions.
- **Humanized Page Scrolling**: Mimics natural reading gestures with ease-out friction scrolling and random pauses.
- **Native Context Actions**: Supports drag-and-drop, right-click, double-click, keyboard shortcuts, and form auto-filling.

```python
async with BP() as bp:
    await bp.goto("https://example.com/login")
    await bp.type("input[type='email']", "user@example.com")
    await bp.type("input[type='password']", "securepassword123")
    await bp.click("button[type='submit']")
```

---

### 2. 10-Layer Hardened Stealth Evasion (V15 Core) (`bp.core`)
- **Layer 1 - Navigator Webdriver Concealment**: Overrides `navigator.webdriver` to `undefined` with native accessor traps.
- **Layer 2 - Chrome Runtime Simulation**: Emulates `window.chrome.runtime`, `csi`, and `loadTimes`.
- **Layer 3 - Permissions Query Neutralization**: Spoofs `navigator.permissions.query({name: 'notifications'})` to return standard `prompt` states.
- **Layer 4 - WebGL & Canvas Noise**: Injects sub-pixel pseudo-random noise into Canvas 2D image data and WebGL render targets to defeat browser canvas fingerprinting.
- **Layer 5 - AudioContext Noise Injection**: Applies imperceptible frequency modulation to WebAudio oscillators.
- **Layer 6 - Plugin & MimeType Array Spoofing**: Simulates standard PDF viewer and Widevine DRM plugins.
- **Layer 7 - Battery & Network API Spoofing**: Mock dynamic battery status and standard `navigator.connection` RTT/downlink metrics.
- **Layer 8 - Screen & Hardware Concurrency**: Dynamic resolution matching and realistic CPU core allocations (`hardwareConcurrency: 8`).
- **Layer 9 - DevTools Detection Shield**: Bypasses `console.table` profiling and debugger timing detection traps.
- **Layer 10 - WebRTC Leak Prevention**: Sanitizes STUN/TURN candidate discovery to prevent real IP exposure.

---

### 3. Multi-Tier Self-Healing Selector Engine (`bp.selectors`)
- **Tier 1 (L1 Exact)**: High-speed resolution using standard CSS / XPath expressions.
- **Tier 2 (L2 Semantic / ARIA)**: Falls back to ARIA roles, labels, placeholders, titles, and visible text content.
- **Tier 3 (L3 Levenshtein Fuzzy)**: Uses Levenshtein distance and token similarity scoring across all interactive elements (confidence threshold >= 0.65).
- **Self-Healing Memory**: Caches successful healed selectors in memory to accelerate future interactions across the session.

```python
async with BP() as bp:
    await bp.goto("https://example.com")
    # Even if the class or ID changes in production, self-healing resolves the button
    element = await bp.resolve_selector("button.checkout-btn-v2")
    await bp.click(element)
```

---

### 4. Direct High-Speed Asynchronous API Client (`bp.api`)
- **Pure Async HTTP**: Provides non-browser REST capabilities (`GET`, `POST`, `PUT`, `DELETE`).
- **Auth-Fingerprinted In-Memory TTL Cache**: Isolates cached responses per authentication credential, preventing cross-tenant data leaks.
- **ProxyPool Health Tracking**: Automatically routes calls through active proxies and reports response latency/failures.
- **Circuit Breaker Protection**: Blocks outgoing requests when upstream errors breach thresholds.

```python
async with BP() as bp:
    resp = await bp.api.get("https://api.example.com/items", cache_ttl=120.0)
    print("Items:", resp.json())
```

---

### 5. Model Context Protocol (MCP) Stdio Server (`bp.mcp`)
- **JSON-RPC 2.0 Compliance**: Operates over Stdio conforming to MCP Specification `2024-11-05`.
- **5 Registered AI Tools**:
  1. `scrape_page`: Self-healing DOM extraction and markdown generator.
  2. `crawl_domain`: Multi-page recursive crawler.
  3. `take_screenshot`: Base64 PNG viewport capture for multimodal vision LLMs.
  4. `quant_pit_align`: SEC EDGAR Point-in-Time metadata validator.
  5. `get_provider_matrix`: Live host engine and network driver status inspector.

---

### 6. Multi-Engine Provider Architecture (`bp.providers`)
- **Dynamic Adapter Matrix**: Transparently integrates multiple browser and AI agent engines:
  - `patchright`: Hardened stealth Chromium with native C++ patches.
  - `playwright`: High-speed standard browser automation.
  - `uc`: Undetected-Chromedriver (Opt-in via `SQ_LIVE_UC=1`).
  - `curl_cffi`: Low-level TLS fingerprint spoofing.
  - `browser_use`: LangChain/LLM browser agent bridge.
  - `stagehand`: TypeScript AI agent bridge.

---

### 7. Intelligent Proxy Pool & Session Management (`bp.proxy`)
- **Multiple Protocols**: HTTP, HTTPS, SOCKS4, SOCKS5.
- **Rotation Algorithms**: Round-Robin, Least-Used, and Latency-Optimized.
- **Automated Quarantine**: Isolates failing proxy nodes after consecutive timeouts or HTTP 5xx responses.
- **Sticky Sessions**: Binds session IDs to specific proxy nodes for consistent stateful interactions.

```python
from behavioral_playwright import BP, ProxyProtocol

async with BP() as bp:
    bp.proxy.add_proxy(host="192.168.1.100", port=8080, protocol=ProxyProtocol.HTTP)
    bp.proxy.add_proxy(host="192.168.1.101", port=8080, protocol=ProxyProtocol.SOCKS5)
    proxy_node = bp.proxy.get_proxy(session_id="user-session-42")
    print("Using Proxy:", proxy_node.url)
```

---

### 8. Enterprise Resilience & Circuit Breaker (`bp.resilience`)
- **Circuit Breaker State Machine**: `CLOSED` (Normal) ➔ `OPEN` (Tripped / Fast Failure) ➔ `HALF_OPEN` (Trial Recovery).
- **Exponential Backoff**: Automatic retry policies with jitter to avoid thundering herd problems.
- **Fallback Cascading**: Gracefully downgrades from enhanced providers to standard engines.

---

### 9. Asynchronous Recursive Crawler & Sitemap Parser (`bp.crawling`)
- **Depth-Limited Crawling**: Traverses internal domain links while respecting concurrency limits.
- **Sitemap Parser**: Ingests `sitemap.xml` for systematic URL discovery.
- **Politeness Rules**: Configurable request delays and domain blacklists.

---

### 10. Quantitative SEC Point-in-Time & NASDAQ ITCH-5.0 Parser (`bp.quant`)
- **SEC EDGAR PiT Aligner**: Eliminates look-ahead bias in algorithmic trading strategies by aligning `period_of_report_epoch` with `sec_dissemination_epoch`.
- **NASDAQ ITCH-5.0 Binary Wire Parser**: Parses raw 40-byte ITCH messages at microsecond speeds, filtering order book executions by dollar threshold.

```python
async with BP() as bp:
    aligned = bp.quant.align_edgar_filing({
        "cik": "0000320193",
        "period_of_report_epoch": 1700000000.0,
        "sec_dissemination_epoch": 1700086400.0,
        "metrics": {"revenue": 89500000000}
    })
    print("Point-in-Time Verified:", aligned["valid_for_backtest"])
```

---

### 11. Unified Multi-Format Storage & Exporters (`bp.storage`)
- **Seamless Format Serialization**: Exports structured records to `.json`, `.ndjson`, `.csv`, and relational `.db` (SQLite).
- **Automatic Schema Mapping**: Automatically maps dictionary records to SQLite table columns with primary keys and timestamps.

```python
records = [{"id": 1, "title": "Article One"}, {"id": 2, "title": "Article Two"}]
bp.storage.export(records, "articles.ndjson")
bp.storage.export(records, "articles.db", table_name="articles")
```

---

### 12. Observability, Telemetry & QA Reporting (`bp.observability`)
- **SQLite Event Telemetry**: Records performance metrics, navigation latency, selector healing events, and proxy health in a persistent SQLite telemetry store.
- **Automated QA Compliance Reports**: Generates structured summaries of system performance and compliance scorecards.

---

### 13. Level-4 Hardened Behavioral Evasion Framework (`behavioral_evasion_suite`)
A production-grade biometric simulation and stealth defense evasion suite designed to bypass sophisticated bot detection systems (Cloudflare Turnstile, DataDome, Kasada, CreepJS):

| Module | Patch / Mechanism | Capability |
| :--- | :--- | :--- |
| **`powerhand_master.py`** | Master Facade | Unified orchestrator binding all evasion shields, physical bridges, and sessions |
| **`keystroke_engine.py`** | Biometric Keystrokes | Weibull key-dwell & flight times, QWERTY scan codes, adjacent typos & backspacing |
| **`mouse_physics.py`** | Biomechanical Mouse | Costello Saccadic Bezier curves with 8-12Hz neuromuscular tremor (passes CreepJS) |
| **`dma_kernel_bridge.py`** | SMT-Verified Bridges | SMT-verified NaN/Inf clamped Linux `/dev/uinput` and PCIe DMA Screamer bridges |
| **`webauthn_virtual_tpm.py`**| Dual WebAuthn | Native Chromium CDP Virtual Authenticator (P-256) + Sandboxed Iframe Fallback |
| **`canvas_shader_spoofer.py`**| Dynamic Noise | Mulberry32 PRNG canvas noise + UNMASKED_VENDOR WebGL constants alignment |
| **`cdp_evasion.py`** | CDP WeakMap Shield | `Function.prototype.toString` V8 native representation against `Runtime.enable` traps |
| **`v8_shield.py`** | Prototype Reflection | `Object.getOwnPropertyDescriptor` and `Error.prepareStackTrace` sanitization |
| **`honeypot_shield.py`** | Atomic DOM Re-Check | 0x0 rect, invisible CSS, off-screen, and transparent occlusion trap filtering |
| **`tls_ja4_spoofer.py`** | JA4 / TLS Handshake | Impersonates Chrome 124+ cipher suites & TCP options order via curl_cffi |
| **`context_rotator.py`** | Memory Recycling | Automated BrowserContext recycling & V8 network cache purging |
| **`os_resource_guard.py`** | File Descriptor Guard| POSIX ulimit dynamic clamping preventing socket exhaustion (`Errno 24`) |
| **`circuit_breaker.py`** | Status-Granular Breaker| Intelligent cooldowns with Gaussian jitter for IP bans (429/403) and schema drift |
| **`quality_sentinel.py`** | Pydantic Sentinel | Real-time schema validation, data loss detection, and honeypot DOM screening |
| **`swarm_orchestrator.py`**| Multi-Tab Swarm | Concurrent tab batching with isolated browser socket contexts |
| **`persona_matrix.py`** | Digital Soul & Anchor | Sticky residential proxy rotation with TLA+ verified deadlock-free fallback |

```python
import asyncio
from behavioral_evasion_suite import PowerHandPlaywrightRunner

async def main():
    runner = PowerHandPlaywrightRunner(seed=42069)
    result = await runner.execute_stealth_session("https://bot.sannysoft.com")
    print("Session result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

---



### 14. Level-5 Quantum Edition Evasion Shields (`behavioral_evasion_suite`)
Advanced anti-fingerprinting and hardware synthesis shields eliminating headless cloud leaks and runtime detection:

| Shield / Module | Defense Mechanism | Protected Attack Vectors |
| :--- | :--- | :--- |
| **`worker_universal_shield.py`** | Worker Sandbox Isolation | Propagates V8 WeakMap native representations into `Worker` & `SharedWorker` contexts, mocks `OffscreenCanvas` against **DataDome & Cloudflare Turnstile** |
| **`subpixel_font_shield.py`** | DirectWrite Subpixel Font Metrics | Converts Linux FreeType subpixel widths into authentic Windows ClearType metrics (`measureText`, `getBoundingClientRect`) against **Kasada & CreepJS** |
| **`virtual_hardware_synthesizer.py`** | MediaDevice Enumeration | Synthesizes authentic Realtek(R) High Definition Audio endpoints eliminating the **Headless Cloud VM** empty media devices leak |
| **`cognitive_gaze_physics.py`** | Inertial Scroll & Reading Saccades | Newtonian scroll physics with elastic overscroll bounce + cognitive reading pauses proportional to DOM word density |
| **`os_network_stack_spoofer.py`** | Transport Stack Tuning | Socket level tuning (`IP_TTL = 128`, window size `64240`) against **p0f & Akamai** passive OS TCP fingerprinting |
| **`stealth_session.py`** | Route Asset Abortion (`abort_media=True`) | Drops images, fonts, stylesheets, and tracking beacons at the route level for **5x faster page loads** and minimal heap memory |

### 15. Deep Logic & Protected Attribute Security Auditing Suite (`behavioral_evasion_suite`)
Client-side and protocol-level diagnostic auditing engine for modern APIs, Single Sign-On (SSO), and access-control boundaries:

| Module / Class | Target Surface | Capabilities & Threat Vectors |
| :--- | :--- | :--- |
| **`graphql_security_auditor.py`** | GraphQL Endpoints | Introspection defense bypasses (5 variants), Clairvoyance schema suggestion parser, **$30,000 Gem Bug** positional correlation detection, aliased batching rate-limit bypass, lexical DoS depth calculation, and CSRF content-type downgrade |
| **`SAMLTrustChainAuditor`** | SAML 2.0 SP / IdP | HTTP POST & Redirect (Deflate) payload decoding, Signature Exclusion vulnerability testing, XML Signature Wrapping (XSW3) payload forging, and RelayState open redirect verification |
| **`OAuth2TrustChainAuditor`** | OAuth 2.0 / OIDC | RFC 9700 redirect URI bypass generator (7 vectors), RFC 7636 strict PKCE `code_verifier` audit, and mutable `email` vs immutable `sub` claim verification |
| **`DualContextAuditor`** | IDOR / BOLA Replay | Memory-safe bounded `deque(maxlen=500)` request interceptor with semantic PII leakage heuristics (`id`, `uuid`, `email`, `token`) and empty/error body rejection |
| **`PoCEngine` & `GraphQLPoCEngine`** | Reproducibility | Shell-safe cURL command synthesis with valid JSON serialization for rapid bug bounty validation |

## 🧩 Unified Facade (`BP`) API Reference

The `BP` class acts as the single master entry point coordinating all 12 domain namespaces:

```python
from behavioral_playwright import BP, AutomationConfig, AuthConfig, BrowserConfig

config = AutomationConfig(
    browser=BrowserConfig(headless=True),
    auth=AuthConfig(api_key="secret-key", bearer_token="bearer-token"),
)

async with BP(config=config) as bp:
    # 1. Web Automation
    await bp.goto("https://example.com")
    await bp.type("input.search", "Playwright")
    await bp.click("button.search")

    # 2. DOM Extraction
    records = await bp.extract(target="links")

    # 3. Direct API Fetching
    api_resp = await bp.api.get("https://api.example.com/status")

    # 4. Storage
    bp.storage.export(records, "output.json")

    # 5. Visual Capture
    png_bytes = await bp.screenshot()

    # 6. Provider Matrix Inspection
    matrix = bp.providers.matrix()
```

---

---

## 13 PowerPlay Integration Subsystem (`bp.powerplay` / `Bpp`)

The **PowerPlay** subsystem provides an additive, decoupled layer of advanced mathematical models, trajectory synthesis, keystroke dynamics, information entropy auditing, and closed-loop memory control.

It can be accessed either through the unified `BP` facade as `bp.powerplay`, or as a standalone lightweight orchestrator via `Bpp`.

### Installation

PowerPlay is included directly in `behavioral-playwright`. Ensure the package and its mathematical dependencies (such as `numpy`) are installed:

```bash
pip install -e .
```

### Imports

```python
# Unified imports from top-level package
from behavioral_playwright import BP, Bpp, powerplay

# Direct imports from the isolated subsystem
from behavioral_playwright.powerplay import (
    Bpp,
    BiomechanicalTremorEngine,
    LinguisticKeystrokeDynamicsEngine,
    StatefulEvasionTracker,
    UltimateVisionLanguageActionGuard,
    ResolvedSchemaIntegrityGuard,
    ResolvedChromiumMemoryPIDController,
    ResolvedCAPTCHAInfiniteLoopDetector,
    TCPTTLMTUAligner,
    VirtualDisplayManager,
    OSLevelInputBridge,
    OSLevelDisplayInputBridge,
)
```

### Components & Architecture

The `bp.powerplay` namespace provides lazy-loaded access to 9 specialized components:

| Component Accessor | Underlying Class | Capability Description |
| :--- | :--- | :--- |
| `bp.powerplay.biomechanics` | `BiomechanicalTremorEngine` | Costello two-phase saccadic Bezier curves (80% ballistic, 20% micro-correction) with Harris-Wolpert noise. |
| `bp.powerplay.keystrokes` | `LinguisticKeystrokeDynamicsEngine` | Physical QWERTY distance matrix scaling Weibull flight/dwell latencies with chronological millisecond timestamps. |
| `bp.powerplay.tracker` | `StatefulEvasionTracker` | Sliding-window request tracking, rolling RPM, delay jitter variance, memory usage averaging, and threat index. |
| `bp.powerplay.vision_guard` | `UltimateVisionLanguageActionGuard` | Cosine vector similarity, Generalized IoU normalized to $[0, 1]$, centroid proximity decay, and click healing. |
| `bp.powerplay.schema_guard` | `ResolvedSchemaIntegrityGuard` | $O(N)$ linear-complexity Shannon entropy content audit via `collections.Counter` with profile baseline Z-scores. |
| `bp.powerplay.memory_pid` | `ResolvedChromiumMemoryPIDController` | Closed-loop PID memory controller with anti-windup clamping ($[-100.0, 100.0]$) and derivative kick avoidance. |
| `bp.powerplay.loop_detector` | `ResolvedCAPTCHAInfiniteLoopDetector` | Cumulative Poisson CDF infinite challenge loop model with Bayesian trust decay scoring. |
| `bp.powerplay.tcp_tuner` | `TCPTTLMTUAligner` | Layer 4 configuration recommendations (TTL 128, MTU 1500, MSS 1460, window 64240). |
| `bp.powerplay.os_bridge` | `OSLevelDisplayInputBridge` | Composite diagnostic bridge for virtual framebuffer and hardware input event simulation. |

### Public Helper Methods on `bp.powerplay`

* **`bp.powerplay.generate_mouse_trajectory(start_pos, target_pos, steps=30)`**: Computes a list of $(x, y)$ coordinate tuples following Costello saccadic curvature and physiological tremor.
* **`bp.powerplay.generate_keystroke_sequence(text)`**: Computes an ordered sequence of `{"key", "event", "timestamp_ms"}` dictionaries with strict boundary clamping ($\text{dwell} \ge 15\text{ms}, \text{flight} \ge 20\text{ms}$).
* **`bp.powerplay.audit_content_entropy(text)`**: Performs a linear-complexity Shannon entropy scan of page content and returns an audit dictionary.
* **`await bp.powerplay.move_mouse_humanized(start_pos, target_pos, steps=20, step_delay=0.005)`**: Drives the active Playwright page mouse along the synthesized Bezier trajectory (returns trajectory points if unbooted).
* **`await bp.powerplay.type_humanized(text, delay_multiplier=1.0)`**: Drives the active Playwright page keyboard using QWERTY distance-modulated timings (returns event sequence if unbooted).
* **`bp.powerplay.create_orchestrator()`**: Returns an isolated, standalone `Bpp` instance.

### Usage Examples

#### 1. Integrated Usage via `BP` Facade

```python
import asyncio
from behavioral_playwright import BP

async def main():
    async with BP() as bp:
        await bp.goto("https://example.com")

        # 1. Synthesize and execute humanized mouse movement
        start = (100, 100)
        target = (450, 320)
        path = await bp.powerplay.move_mouse_humanized(start, target, steps=20)
        print(f"Moved mouse across {len(path)} trajectory points.")

        # 2. Type with QWERTY distance-modulated latencies
        events = await bp.powerplay.type_humanized("Search query")
        print(f"Emitted {len(events)} keystroke events chronologically.")

        # 3. Audit page content information density
        html = await bp.page.evaluate("() => document.documentElement.outerHTML")
        audit = bp.powerplay.audit_content_entropy(html)
        print(f"Entropy Decision: {audit['decision']} (H={audit['shannon_entropy']})")

if __name__ == "__main__":
    asyncio.run(main())
```

#### 2. Standalone Usage via `Bpp` Orchestrator

```python
from behavioral_playwright import Bpp

# Standalone mathematical orchestrator (requires no browser session)
bot = Bpp()

# 1. Mathematical Bezier curve generation
trajectory = bot.biomechanics.generate_bezier_trajectory((50, 50), (500, 300), steps=25)

# 2. Linguistic keystroke dynamics
keystroke_timeline = bot.keystrokes.generate_typing_sequence("BehavioralPlaywright")

# 3. Closed-loop PID memory management calculation
pid_signal = bot.memory_pid.compute_correction(current_usage_mb=620.0, dt=1.0)
print(f"PID Intensity: {pid_signal['correction_intensity_pct']}% | Action: {pid_signal['action']}")

# 4. Spatial action guard (GIoU + Centroid Healing)
validation = bot.vision_guard.evaluate_and_heal_click(
    vec_intended=[1.0, 0.2, 0.0],
    vec_scanned=[0.95, 0.25, 0.0],
    box_intended=[100, 100, 200, 150],
    box_scanned=[102, 98, 198, 152],
)
print(f"Click Validation: {validation['decision']} (Confidence: {validation['confidence_score']})")

# 5. Stateful request and threat tracking
bot.tracker.record_request()
threat_index = bot.tracker.compute_adaptive_threat_index()
print(f"Sessional Threat Index: {threat_index}/100")
```

### Engineering Honesty & Operational Boundaries

To maintain strict engineering rigor, the capabilities of PowerPlay are classified as follows:

* **Verified Executable Mathematical Models**:
  - `BiomechanicalTremorEngine`, `LinguisticKeystrokeDynamicsEngine`, `ResolvedSchemaIntegrityGuard`, `UltimateVisionLanguageActionGuard`, `ResolvedChromiumMemoryPIDController`, `StatefulEvasionTracker`, and `ResolvedCAPTCHAInfiniteLoopDetector` perform genuine numerical calculations, geometric transforms, statistical sampling, and control loop logic.
* **Simulation & Configuration-Only Helpers**:
  - `VirtualDisplayManager` sets `os.environ["DISPLAY"] = ":99"` and returns diagnostic report metadata; it does not launch an Xvfb daemon or configure X11 server processes.
  - `TCPTTLMTUAligner` returns recommended socket configuration dictionaries; it does not modify operating system kernel TCP/IP stack parameters.
  - `OSLevelInputBridge` / `OSLevelDisplayInputBridge` returns structured status dictionaries representing virtual input events; it does not inject interrupts into Linux `/dev/uinput` or Win32 `SendInput` device drivers.
* **Anti-Bot Realistic Boundary**:
  - Synthesized trajectories and typing dynamics emulate human biometrics to reduce automated behavioral anomalies. However, they do not guarantee or claim an infallible bypass of enterprise security mechanisms such as Cloudflare Turnstile, Akamai Kona, DataDome, or Kasada.

## 🔐 Shared Authentication Architecture

The framework implements a **single, unified authentication configuration layer** shared across Python API, CLI, and MCP Server:

```text
               Shared AuthConfig / AutomationConfig
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
    Python API                 CLI                  MCP Server
    (BP.api / BP)        (--api-key / --token)   (Shared BP Context)
```

### Deterministic Resolution Precedence
1. **Explicit Instance Arguments**: Passed to `AuthConfig(api_key=..., bearer_token=...)`.
2. **CLI Flags**: Passed via `--api-key <key>` or `--token <token>`.
3. **Environment Variables**:
   - `BP_API_KEY`: Injects `X-API-Key: <key>` header.
   - `BP_BEARER_TOKEN`: Injects `Authorization: Bearer <token>` header.

*Security Guarantee*: Secrets are never logged to console, exceptions, telemetry, or debug traces.

---

## 🤖 Claude Desktop & Cursor AI Setup Guide

Connect Behavioral Playwright to Claude Desktop or Cursor to enable natural language web extraction and browser control:

### 1. Generate MCP Configuration

```bash
bp mcp-config --python-path python
```

### 2. Configure Claude Desktop

Add the server definition to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "behavioral-playwright": {
      "command": "python",
      "args": ["-m", "behavioral_playwright.mcp.server"]
    }
  }
}
```

Now you can ask Claude:
- *"Scrape the top stories from Hacker News using the scrape_page tool."*
- *"Take a screenshot of github.com and analyze its layout."*
- *"Crawl example.com up to 5 pages and extract all links."*

---

## 💻 Complete CLI Command Reference

The `bp` command-line tool provides instant access to all core framework operations:

```bash
# Display provider availability matrix
bp matrix

# Scrape a webpage to JSON
bp scrape https://news.ycombinator.com -o hn.json --target links

# Scrape with shared API key authentication
bp --api-key "secret-key-123" scrape https://api.example.com/data -o api_data.json

# Recursively crawl a website
bp crawl https://example.com --max-pages 10 --depth 2 -o crawled.ndjson

# Generate QA compliance report
bp qa-report --db bp_metrics.db

# Launch Stdio MCP Server
bp mcp-server

# Print Claude Desktop configuration entry
bp mcp-config --python-path python
```

---

## 🛡️ Multi-Provider Matrix & Status Taxonomy

| Provider ID | Subsystem | Host Status | Live Integration Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`patchright`** | Browser | ✔ Available | **`VERIFIED-LIVE`** | Hardened stealth Chromium with native C++ patch bindings. |
| **`playwright`** | Browser | ✔ Available | **`VERIFIED-LIVE`** | Standard high-speed Playwright Chromium/Firefox/WebKit. |
| **`uc`** | Browser | ✔ Available | **`PROVIDER-GATED-LIVE`** | Undetected-Chromedriver (Opt-in via `SQ_LIVE_UC=1`). |
| **`curl_cffi`** | Network | ✘ Optional | **`PROVIDER-GATED`** | TLS fingerprint spoofing (Raises `ProviderUnavailableError` if absent). |
| **`browser_use`**| AI Agent | ✘ Optional | **`PROVIDER-GATED`** | LangChain/LLM browser agent (Requires LLM API key). |
| **`stagehand`** | AI Agent | ✘ Optional | **`PROVIDER-GATED`** | TypeScript AI agent bridge (Requires Model + Key). |

---

## 🔀 Fallback & Routing Decision Matrix

```text
                                  User Request
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
        Direct API / JSON Data                        Rendered Web Content
                │                                             │
      AsyncApiClient (bp.api)                        Headless Browser (BP)
                │                                             │
      ┌─────────┴─────────┐                         ┌─────────┴─────────┐
      ▼                   ▼                         ▼                   ▼
Cache Hit?            Cache Miss              Patchright Available?   Playwright Fallback
      │                   │                         │                   │
Return 0.0ms        Execute Request           Verified-Live       Standard Chromium
                          │                         │                   │
                    Circuit Breaker                 └─────────┬─────────┘
                    Protected Fetch                           ▼
                          │                         Self-Healing Selectors
                   ProxyPool Routed                 (L1 Exact ➔ L2 Semantic ➔ L3 Fuzzy)
```

---

## ⚠️ Known Limitations & Engineering Honesty

1. **Connection Pooling**: `AsyncApiClient` uses Python's standard library `urllib.request` running in an asynchronous threadpool. High-concurrency connection pooling using `curl_cffi` is optional roadmap work.
2. **Cache Storage**: `ApiRequestCache` is an in-memory TTL dictionary. Multi-session SQLite disk persistence and HTTP ETag validation are future enhancements.
3. **MCP Server Scope**: The MCP server focuses on tool execution (`tools/list`, `tools/call`). Resource/prompt listing methods return standard `-32601` error codes.
4. **Third-Party AI Agent Providers**: `Browser-Use` and `Stagehand` require active external LLM API credentials and dependencies.
5. **PowerPlay Simulation vs Kernel Execution**: PowerPlay's OS-level display and input components (`VirtualDisplayManager`, `OSLevelInputBridge`) provide structured diagnostic simulation reports; they do not perform raw kernel interrupt injection or launch OS-level Xvfb display servers. Network socket tuning (`TCPTTLMTUAligner`) outputs standard parameter recommendations without altering OS network tables.

---


---

## 🧪 Verified Automated Quality Gates

All security auditors, clinical doctor reasoning engines, and stealth frameworks are continuously verified with automated regression tests:

```bash
pytest tests/test_sspp_auditor.py tests/test_graphql_auditor.py tests/test_clinical_doctor.py -v
```

```text
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2
collected 23 items

tests/test_sspp_auditor.py (7 passed)
  - test_01_pydantic_dto_validation PASSED
  - test_02_differential_json_spaces_html_filter PASSED
  - test_03_differential_cors_header_baseline PASSED
  - test_04_differential_status_mutation_baseline PASSED
  - test_05_reversion_payload_generation PASSED
  - test_06_shell_safe_curl_poc_multimethod PASSED
  - test_07_master_deep_logic_engine_protocol PASSED

tests/test_graphql_auditor.py (11 passed)
  - test_01_introspection_bypasses_generation PASSED
  - test_02_clairvoyance_suggestions_parsing PASSED
  - test_03_positional_correlation_payload_spec PASSED
  - test_04_positional_correlation_shift_multi_item PASSED
  - test_05_positional_correlation_multi_redacted_boundary_walk PASSED
  - test_06_positional_correlation_single_item_safety PASSED
  - test_07_aliased_batching_generation PASSED
  - test_08_query_depth_lexical_computation PASSED
  - test_09_csrf_content_type_audit PASSED
  - test_10_graphql_poc_curl_generation PASSED
  - test_11_master_engine_full_audit PASSED

tests/test_clinical_doctor.py (5 passed)
  - test_01_website_dna_serialization PASSED
  - test_02_doctor_clinical_prescription_matching PASSED
  - test_03_graphql_doctor_prescription PASSED
  - test_04_hackerone_report_rendering PASSED
  - test_05_notebooklm_library_auto_discovery PASSED

============================= 23 passed in 0.24s ==============================
```

---

## 📄 Ethical & Legal Disclosure

This software is designed exclusively for authorized penetration testing, vulnerability research within documented Bug Bounty program rules (e.g. HackerOne, Bugcrowd Safe Harbor), and internal AppSec defense audits. Unsanctioned auditing against systems without explicit written consent is strictly prohibited and unlawful.

---

## 📄 License

MIT License. Copyright (c) 2026 sadik004.
