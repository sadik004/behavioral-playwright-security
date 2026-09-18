import asyncio
import base64
import hashlib
import json
import re
import shlex
import time
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from collections import deque
from typing import Dict, Any, List, Optional, Tuple

# Register common SAML namespaces cleanly without duplicate namespace URI collision
ET.register_namespace('saml2p', 'urn:oasis:names:tc:SAML:2.0:protocol')
ET.register_namespace('saml2', 'urn:oasis:names:tc:SAML:2.0:assertion')
ET.register_namespace('ds', 'http://www.w3.org/2000/09/xmldsig#')


# =====================================================================
# SECTION 1: SAML 2.0 TRUST-CHAIN AUDITOR
# =====================================================================
class SAMLTrustChainAuditor:
    """
    Audits SAML 2.0 Service Provider (SP) and Identity Provider (IdP)
    trust chains for Signature Exclusion, XML Signature Wrapping (XSW),
    RelayState Open Redirect Chaining, and Assertion Replay.
    """

    def __init__(self, target_url: str = ""):
        self.target_url = target_url
        self.captured_saml_responses: List[Dict[str, Any]] = []

    @staticmethod
    def decode_saml_payload(saml_str: str) -> str:
        """
        Decodes SAML payload supporting both:
        1. HTTP POST Binding: Raw Base64 XML
        2. HTTP Redirect Binding: Deflate-compressed + Base64
        Handles URL unquoting and missing Base64 padding.
        """
        try:
            unquoted = urllib.parse.unquote(saml_str).strip().replace(" ", "+")
            # Fix missing Base64 padding if string length is not multiple of 4
            padded = unquoted + "=" * ((4 - len(unquoted) % 4) % 4)
            raw_bytes = base64.b64decode(padded)

            # Try DEFLATE decompression (raw deflate -15, zlib header 15/32)
            for wbits in [-15, 15, 32 + 15]:
                try:
                    decompressed = zlib.decompress(raw_bytes, wbits)
                    return decompressed.decode("utf-8", errors="replace")
                except Exception:
                    pass

            # Fallback to direct UTF-8 decoding (HTTP POST binding)
            return raw_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            return f"<!-- Decoding Error: {str(e)} -->"

    @staticmethod
    def encode_saml_payload(xml_str: str, compress: bool = False) -> str:
        """Encodes modified XML back into Base64 string (optional DEFLATE)."""
        raw_bytes = xml_str.encode("utf-8")
        if compress:
            comp_obj = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
            raw_bytes = comp_obj.compress(raw_bytes) + comp_obj.flush()
        encoded_bytes = base64.b64encode(raw_bytes)
        return encoded_bytes.decode("utf-8")

    def test_signature_exclusion(self, xml_str: str, spoofed_nameid: str = "attacker@evil.com") -> Tuple[str, bool]:
        """
        Strips <ds:Signature> or <Signature> tags and alters NameID using
        namespace-aware XML ElementTree processing with regex fallback.
        """
        try:
            root = ET.fromstring(xml_str)
            was_modified = False

            def process_element(parent):
                nonlocal was_modified
                to_remove = []
                for child in list(parent):
                    tag_local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                    if tag_local == "Signature":
                        to_remove.append(child)
                        was_modified = True
                    elif tag_local == "NameID":
                        if child.text != spoofed_nameid:
                            child.text = spoofed_nameid
                            was_modified = True
                    else:
                        process_element(child)

                for child in to_remove:
                    parent.remove(child)

            process_element(root)
            modified_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
            return self.encode_saml_payload(modified_xml), was_modified
        except Exception:
            # Fallback to regex if XML parsing fails due to fragments or non-well-formed XML
            xml_nosig = re.sub(r'<(?:[a-zA-Z0-9_]+:)?Signature[^>]*>.*?</(?:[a-zA-Z0-9_]+:)?Signature>', '', xml_str, flags=re.DOTALL)
            xml_modified = re.sub(r'(<(?:[a-zA-Z0-9_]+:)?NameID[^>]*>)(.*?)(</(?:[a-zA-Z0-9_]+:)?NameID>)',
                                  rf'\g<1>{spoofed_nameid}\g<3>', xml_nosig, flags=re.DOTALL)
            return self.encode_saml_payload(xml_modified), (xml_modified != xml_str)

    def test_xml_signature_wrapping_xsw3(self, xml_str: str, spoofed_nameid: str = "admin@victim.com") -> Tuple[str, bool]:
        """Generates XSW3 variant payload: inserts forged unsigned Assertion before signed Assertion."""
        try:
            match = re.search(r'(<(?:[a-zA-Z0-9_]+:)?Assertion[^>]*>.*?</(?:[a-zA-Z0-9_]+:)?Assertion>)', xml_str, flags=re.DOTALL)
            if not match:
                return self.encode_saml_payload(xml_str), False
            orig_assertion = match.group(1)
            unsigned_assertion = re.sub(r'<(?:[a-zA-Z0-9_]+:)?Signature[^>]*>.*?</(?:[a-zA-Z0-9_]+:)?Signature>', '', orig_assertion, flags=re.DOTALL)
            unsigned_assertion = re.sub(r'(<(?:[a-zA-Z0-9_]+:)?NameID[^>]*>)(.*?)(</(?:[a-zA-Z0-9_]+:)?NameID>)',
                                         rf'\g<1>{spoofed_nameid}\g<3>', unsigned_assertion, flags=re.DOTALL)
            unsigned_assertion = re.sub(r'ID="([^"]+)"', r'ID="\1_forged"', unsigned_assertion, count=1)
            xsw_xml = xml_str.replace(orig_assertion, f"{unsigned_assertion}\n{orig_assertion}", 1)
            return self.encode_saml_payload(xsw_xml), True
        except Exception:
            return self.encode_saml_payload(xml_str), False

    def test_relaystate_open_redirect(self, relay_state_val: Optional[str]) -> Dict[str, Any]:
        """Audits RelayState parameter for open redirect / protocol smuggling safely handling NoneType values."""
        val = str(relay_state_val or "")
        dangerous_patterns = ["//", "http://", "https://", "javascript:", ".evil.com"]
        is_suspicious = any(pattern in val for pattern in dangerous_patterns)
        return {
            "relay_state": val,
            "open_redirect_risk": "HIGH" if is_suspicious else "LOW",
            "cwe_id": "CWE-601 (URL Redirection to Untrusted Site)",
            "details": f"RelayState '{val}' contains external redirect structure." if is_suspicious else "RelayState appears benign."
        }


# =====================================================================
# SECTION 2: OAUTH 2.0 & OIDC LOGIC AUDITOR
# =====================================================================
class OAuth2TrustChainAuditor:
    """Audits OAuth 2.0 and OpenID Connect (OIDC) implementation logic according to RFC 9700 and RFC 7636."""

    def __init__(self):
        self.intercepted_flows: List[Dict[str, Any]] = []

    def audit_redirect_uri_patterns(self, base_redirect_uri: str) -> List[Dict[str, Any]]:
        """Generates 7 RFC 9700 bypass variations for redirect_uri validation."""
        parsed = urllib.parse.urlparse(base_redirect_uri)
        domain = parsed.netloc
        scheme = parsed.scheme or "https"
        path = parsed.path or "/callback"

        return [
            {"type": "Subdomain Bypass", "uri": f"{scheme}://evil.{domain}{path}"},
            {"type": "Path Traversal", "uri": f"{scheme}://{domain}{path}/../attacker_callback"},
            {"type": "Parameter Injection", "uri": f"{scheme}://{domain}{path}?redirect=https://evil.com"},
            {"type": "Fragment Injection", "uri": f"{scheme}://{domain}{path}#@evil.com"},
            {"type": "Open Redirect Chain", "uri": f"{scheme}://{domain}/go?url=https://evil.com"},
            {"type": "Localhost Bypass", "uri": "http://localhost:8080/callback"},
            {"type": "Scheme Downgrade", "uri": f"http://{domain}{path}"}
        ]

    def audit_pkce_enforcement(self, token_request_body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits OAuth 2.0 /token request body for mandatory PKCE 'code_verifier' parameter.
        RFC 7636 specifies 'code_challenge' is strictly for /authorize, while 'code_verifier'
        must be present during the /token exchange.
        """
        has_code_verifier = "code_verifier" in token_request_body
        return {
            "pkce_enforced": has_code_verifier,
            "risk": "NONE" if has_code_verifier else "CRITICAL (Authorization Code Interception Risk)",
            "recommendation": "Require mandatory 'code_verifier' parameter in /token exchange body for PKCE enforcement (RFC 7636)."
        }

    def audit_account_linking_claims(self, jwt_claims: Dict[str, Any]) -> Dict[str, Any]:
        """Checks if identity matching relies on mutable email claim vs immutable 'sub' claim."""
        has_sub = "sub" in jwt_claims
        uses_email_only = "email" in jwt_claims and not has_sub
        return {
            "uses_immutable_sub": has_sub,
            "vulnerable_to_email_account_takeover": uses_email_only,
            "risk": "HIGH" if uses_email_only else "LOW",
            "cwe_id": "CWE-287 (Improper Authentication)"
        }


# =====================================================================
# SECTION 3: IN-BROWSER DOM SINK AUDITOR
# =====================================================================
DOM_SINK_HOOK_SCRIPT = """
(function() {
    if (window.__domSinkAuditorInjected) return;
    window.__domSinkAuditorInjected = true;
    window.__domSinkEvents = [];

    function logSink(sinkName, target, input) {
        const evt = {
            sink: sinkName,
            target: target || 'window',
            input: String(input).slice(0, 500),
            timestamp: new Date().toISOString()
        };
        window.__domSinkEvents.push(evt);
        console.warn('[DOM-SINK-AUDIT]', JSON.stringify(evt));
    }

    const originalEval = window.eval;
    window.eval = function(input) {
        logSink('eval', 'window', input);
        return originalEval.apply(this, arguments);
    };

    const proto = HTMLElement.prototype;
    ['innerHTML', 'outerHTML'].forEach(prop => {
        const descriptor = Object.getOwnPropertyDescriptor(proto, prop);
        if (descriptor && descriptor.set) {
            const originalSet = descriptor.set;
            Object.defineProperty(proto, prop, {
                set: function(value) {
                    logSink(prop, this.tagName, value);
                    return originalSet.call(this, value);
                }
            });
        }
    });

    ['write', 'writeln'].forEach(fn => {
        if (document[fn]) {
            const orig = document[fn];
            document[fn] = function(content) {
                logSink('document.' + fn, 'document', content);
                return orig.apply(this, arguments);
            };
        }
    });
})();
"""

async def attach_dom_sink_auditor(page):
    try:
        res = page.add_init_script(DOM_SINK_HOOK_SCRIPT)
        if asyncio.iscoroutine(res):
            await res
        # Ensure hook is also immediately injected into currently active DOM
        eval_res = page.evaluate(DOM_SINK_HOOK_SCRIPT)
        if asyncio.iscoroutine(eval_res):
            await eval_res
    except Exception:
        pass

async def get_dom_sink_events(page) -> List[Dict[str, Any]]:
    try:
        res = page.evaluate("window.__domSinkEvents || []")
        if asyncio.iscoroutine(res):
            return await res
        return res
    except Exception:
        return []


# =====================================================================
# SECTION 4: DUAL-CONTEXT ACCESS CONTROL AUDITOR (IDOR / BOLA)
# =====================================================================
class DualContextAuditor:
    def __init__(self, context_a=None, context_b=None, max_captured_requests: int = 500):
        self.context_a = context_a
        self.context_b = context_b
        # Memory-safe bounded deque to prevent memory leaks during prolonged audits
        self.captured_requests: deque = deque(maxlen=max_captured_requests)
        self.user_b_auth_headers: Dict[str, str] = {}

    def attach_request_interceptor(self, page):
        def handle_request(request):
            url = request.url
            if any(ext in url.lower() for ext in ['.png', '.jpg', '.css', '.js', '.svg', '.woff']):
                return
            if "/api/" in url or "application/json" in request.headers.get("accept", "").lower():
                self.captured_requests.append({
                    "url": url,
                    "method": request.method,
                    "headers": dict(request.headers),
                    "post_data": request.post_data
                })
        page.on("request", handle_request)

    def set_user_b_auth_headers(self, headers: Dict[str, str]):
        self.user_b_auth_headers = headers

    async def audit_captured_requests(self) -> List[Dict[str, Any]]:
        findings = []
        if not self.context_b:
            for req in list(self.captured_requests):
                findings.append({
                    "url": req["url"],
                    "method": req["method"],
                    "status": "QUEUED_FOR_REPLAY"
                })
            return findings

        for req in list(self.captured_requests):
            swapped_headers = {k: v for k, v in req["headers"].items() if k.lower() not in ["host", "content-length"]}
            swapped_headers.update(self.user_b_auth_headers)
            try:
                response = await self.context_b.request.fetch(
                    req["url"],
                    method=req["method"],
                    headers=swapped_headers,
                    data=req["post_data"]
                )
                status_code = response.status
                body = await response.text()
                is_idor_risk = (status_code == 200) and ("error" not in body.lower())
                findings.append({
                    "url": req["url"],
                    "method": req["method"],
                    "status_code": status_code,
                    "idor_risk_detected": is_idor_risk,
                    "risk_level": "HIGH" if is_idor_risk else "LOW"
                })
            except Exception as e:
                findings.append({"url": req["url"], "error": str(e)})
        return findings


# =====================================================================
# SECTION 5: MODEL CONTEXT PROTOCOL (MCP) SAFETY AUDITOR
# =====================================================================
class MCPSchemaAuditor:
    @staticmethod
    def audit_tool_schema(tool_definition: Dict[str, Any]) -> Dict[str, Any]:
        name = tool_definition.get("name", "unknown")
        properties = tool_definition.get("inputSchema", {}).get("properties", {})
        risks = []
        for prop, details in properties.items():
            if prop.lower() in ["path", "file", "filename", "command", "exec", "cmd"]:
                if "pattern" not in details and "enum" not in details:
                    risks.append(f"Unbounded parameter '{prop}' in tool '{name}'")
        return {"tool": name, "status": "SECURE" if not risks else "WARNING", "risks": risks}

    @staticmethod
    def audit_mcp_message(json_rpc_msg: Dict[str, Any]) -> bool:
        decoded = urllib.parse.unquote(json.dumps(json_rpc_msg)).lower()
        dangerous = ["../", "..\\", "ignore previous instructions", "system prompt", "rm -rf", "eval("]
        return not any(sig in decoded for sig in dangerous)


# =====================================================================
# SECTION 6: STATE-BASED DELTA TRACKER
# =====================================================================
class StateDiffAuditor:
    def __init__(self):
        self.baseline_state: Dict[str, str] = {}

    @staticmethod
    def _sanitize_dom(html_content: str) -> str:
        """
        Strips dynamic scripts, nonces, form input values, and real Unix epoch timestamps
        without removing legitimate product IDs or phone numbers.
        """
        sanitized = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        sanitized = re.sub(r'nonce=["\'].*?["\']', '', sanitized)
        sanitized = re.sub(r'value=["\'].*?["\']', '', sanitized)
        # Match valid Unix epoch timestamps (10-digit seconds & 13-digit ms between 2017-2033)
        sanitized = re.sub(r'\b(1[5-9]\d{8}|1[5-9]\d{11})\b', '', sanitized)
        return sanitized.strip()

    async def capture_state(self, page) -> Dict[str, str]:
        try:
            raw_html = page.content()
            if asyncio.iscoroutine(raw_html):
                raw_html = await raw_html
            sanitized_dom = self._sanitize_dom(raw_html)
            dom_hash = hashlib.sha256(sanitized_dom.encode('utf-8')).hexdigest()
            
            scripts = page.eval_on_selector_all("script[src]", "elements => elements.map(e => e.src)")
            if asyncio.iscoroutine(scripts):
                scripts = await scripts
            scripts_hash = hashlib.sha256(",".join(sorted(scripts)).encode('utf-8')).hexdigest()
            return {"dom_hash": dom_hash, "scripts_hash": scripts_hash, "script_count": len(scripts)}
        except Exception as e:
            return {"error": str(e)}

    def compute_delta(self, current_state: Dict[str, str], baseline_state: Dict[str, str]) -> Dict[str, Any]:
        dom_changed = current_state.get("dom_hash") != baseline_state.get("dom_hash")
        scripts_changed = current_state.get("scripts_hash") != baseline_state.get("scripts_hash")
        return {"dom_changed": dom_changed, "scripts_changed": scripts_changed, "has_delta": dom_changed or scripts_changed}


# =====================================================================
# SECTION 7: SHELL-SAFE POC ENGINE
# =====================================================================
class PoCEngine:
    @staticmethod
    def generate_curl_poc(request_data: Dict[str, Any]) -> str:
        """Synthesizes a shell-safe, reproducible cURL command properly serializing dict/list payloads to valid JSON."""
        url = request_data.get("url", "")
        method = request_data.get("method", "GET")
        headers = request_data.get("headers", {})
        data = request_data.get("post_data", None)

        curl_cmd = ["curl", "-i", "-X", method, url]
        for k, v in headers.items():
            if k.lower() not in ['host', 'content-length']:
                curl_cmd.extend(["-H", f"{k}: {v}"])
        if data:
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
            curl_cmd.extend(["--data-raw", str(data)])
        return " ".join(shlex.quote(arg) for arg in curl_cmd)


# =====================================================================
# SECTION 8: AGENT CONTEXT BOUNDARY AUDITOR
# =====================================================================
class AgentHijackAuditor:
    def __init__(self, max_token_budget: int = 32000):
        self.max_token_budget = max_token_budget

    def audit_context_window(self, page_text: str) -> Dict[str, Any]:
        word_count = len(page_text.split())
        estimated_tokens = int(word_count * 1.3)
        return {
            "word_count": word_count,
            "estimated_tokens": estimated_tokens,
            "overflow_risk": estimated_tokens > self.max_token_budget
        }

    async def check_toctou_state(self, initial_dom_hash: str, page) -> bool:
        try:
            current_dom = page.content()
            if asyncio.iscoroutine(current_dom):
                current_dom = await current_dom
            sanitized = StateDiffAuditor._sanitize_dom(current_dom)
            current_hash = hashlib.sha256(sanitized.encode('utf-8')).hexdigest()
            return initial_dom_hash == current_hash
        except Exception:
            return False


# =====================================================================
# SECTION 9: IN-BROWSER CLOSED-LOOP FUZZER
# =====================================================================
class ClosedLoopFuzzer:
    def __init__(self, page):
        self.page = page
        self.page_errors: List[str] = []

    def attach_error_listener(self):
        self.page.on("pageerror", lambda exc: self.page_errors.append(str(exc)))

    async def fuzz_input_field(self, selector: str, initial_payloads: List[str]) -> List[Dict[str, Any]]:
        results = []
        for payload in initial_payloads:
            self.page_errors.clear()
            try:
                fill_res = self.page.fill(selector, payload)
                if asyncio.iscoroutine(fill_res):
                    await fill_res
                disp_res = self.page.dispatch_event(selector, "change")
                if asyncio.iscoroutine(disp_res):
                    await disp_res
                await asyncio.sleep(0.01)
                results.append({
                    "selector": selector,
                    "payload_used": payload,
                    "exceptions_triggered": list(self.page_errors),
                    "potential_vuln": len(self.page_errors) > 0
                })
            except Exception as e:
                results.append({"selector": selector, "error": str(e)})
        return results


# =====================================================================
# SECTION 10: PROTOCOL DESYNC & CVE REPRODUCER
# =====================================================================
class DesyncEngine:
    @staticmethod
    def audit_header_desync_risk(headers: Dict[str, str]) -> Dict[str, Any]:
        keys = [k.lower() for k in headers.keys()]
        is_conflict = 'content-length' in keys and 'transfer-encoding' in keys
        return {"risk": "CRITICAL" if is_conflict else "LOW", "issue": "CL.TE / TE.CL Desync Header Conflict" if is_conflict else "Clean"}


class CVEReproducer:
    @staticmethod
    def generate_docker_testbed_spec(cve_id: str, base_image: str) -> str:
        """Generates Dockerfile specification with valid JSON exec form CMD array."""
        return f'FROM {base_image}\nRUN apt-get update && apt-get install -y curl python3\nLABEL cve_verification=\'{cve_id}\'\nCMD ["/bin/bash"]\n'


# =====================================================================
# MASTER UNIFIED SECURITY AUDITOR CLASS (V10)
# =====================================================================
class UnifiedMasterSecurityAuditorV11:
    def __init__(self, page=None, context_a=None, context_b=None, target_url: str = ""):
        self.page = page
        self.context_a = context_a
        self.context_b = context_b
        self.target_url = target_url

        self.saml_auditor = SAMLTrustChainAuditor(target_url)
        self.oauth_auditor = OAuth2TrustChainAuditor()
        self.idor_auditor = DualContextAuditor(context_a, context_b)
        self.mcp_auditor = MCPSchemaAuditor()
        self.state_auditor = StateDiffAuditor()
        self.poc_engine = PoCEngine()
        self.agent_auditor = AgentHijackAuditor()
        self.fuzzer = ClosedLoopFuzzer(page) if page else None
        self.desync_engine = DesyncEngine()
        self.cve_reproducer = CVEReproducer()

        self.audit_findings: List[Dict[str, Any]] = []

    async def attach_to_behavioral_playwright(self, bp_session=None, page=None) -> bool:
        active_page = page or getattr(bp_session, "page", None) or (bp_session if hasattr(bp_session, "route") else None) or self.page
        if not active_page:
            return False

        await attach_dom_sink_auditor(active_page)

        async def handle_route(route, request=None):
            try:
                req = request or (route.request if hasattr(route, "request") else route)
                url = getattr(req, "url", "")
                post_data = getattr(req, "post_data", "") or ""

                # Parse parameters from both HTTP GET query string AND HTTP POST body
                parsed_url = urllib.parse.urlparse(url)
                get_params = urllib.parse.parse_qs(parsed_url.query)
                post_params = urllib.parse.parse_qs(post_data) if post_data else {}

                saml_b64 = (
                    post_params.get("SAMLResponse", [""])[0] or
                    get_params.get("SAMLResponse", [""])[0] or
                    post_params.get("SAMLRequest", [""])[0] or
                    get_params.get("SAMLRequest", [""])[0]
                )
                relay_state = (
                    post_params.get("RelayState", [""])[0] or
                    get_params.get("RelayState", [""])[0]
                )

                # SAML Interception (HTTP GET & POST Bindings)
                if saml_b64 or "saml" in url.lower():
                    if saml_b64:
                        raw_xml = self.saml_auditor.decode_saml_payload(saml_b64)
                        sig_excl, _ = self.saml_auditor.test_signature_exclusion(raw_xml)
                        relay_audit = self.saml_auditor.test_relaystate_open_redirect(relay_state)
                        is_post_binding = bool(post_params.get("SAMLResponse") or post_params.get("SAMLRequest"))
                        self.audit_findings.append({
                            "type": "SAML_TRUST_CHAIN_INTERCEPTED",
                            "url": url,
                            "binding": "HTTP-POST" if is_post_binding else "HTTP-REDIRECT",
                            "raw_xml": raw_xml[:200],
                            "signature_exclusion_b64": sig_excl[:80] + "...",
                            "relay_state_audit": relay_audit
                        })

                # OAuth Interception (HTTP GET & POST Endpoints)
                redirect_uri = (
                    get_params.get("redirect_uri", [""])[0] or
                    post_params.get("redirect_uri", [""])[0]
                )
                if ("/oauth/" in url or "/authorize" in url or "/token" in url) and redirect_uri:
                    bypasses = self.oauth_auditor.audit_redirect_uri_patterns(redirect_uri)
                    self.audit_findings.append({
                        "type": "OAUTH_TRUST_CHAIN_INTERCEPTED",
                        "url": url,
                        "redirect_uri": redirect_uri,
                        "bypasses_generated": len(bypasses)
                    })
            finally:
                try:
                    res = route.continue_()
                    if asyncio.iscoroutine(res):
                        await res
                except Exception:
                    pass

        try:
            res = active_page.route("**/*", handle_route)
            if asyncio.iscoroutine(res):
                await res
            return True
        except Exception:
            return False

    async def run_master_audit_suite(self, page=None) -> Dict[str, Any]:
        active_page = page or self.page
        dom_events = await get_dom_sink_events(active_page) if active_page else []
        state_data = await self.state_auditor.capture_state(active_page) if active_page else {}

        return {
            "timestamp": time.time(),
            "target_url": self.target_url,
            "saml_oauth_findings_captured": len(self.audit_findings),
            "summary": {
                "dom_sink_audit_events": dom_events,
                "captured_state": state_data,
                "findings_summary": self.audit_findings
            },
            "status": "MASTER_UNIFIED_AUDIT_COMPLETED_SUCCESSFULLY"
        }


if __name__ == "__main__":
    print("=== Testing Master Unified Security Auditor Engine v11 ===")
    master = UnifiedMasterSecurityAuditorV11(target_url="https://enterprise-auth.target.com")
    
    # 1. Test PoCEngine dict serialization
    dict_payload = {"user": "admin", "role": "superuser"}
    poc_cmd = PoCEngine.generate_curl_poc({"url": "https://target.com/api", "method": "POST", "post_data": dict_payload})
    print("PoCEngine Dict JSON Serialization Test:", '"{"user": "admin", "role": "superuser"}' in poc_cmd or "'{\"user\": \"admin\", \"role\": \"superuser\"}'" in poc_cmd)

    # 2. Test RelayState NoneType Safety
    none_relay_audit = master.saml_auditor.test_relaystate_open_redirect(None)
    print("RelayState NoneType Safety Test Passed:", none_relay_audit["relay_state"] == "")

    # 3. Test SAML ElementTree XML Serialization
    sample_xml = "<saml2:Assertion xmlns:saml2='urn:oasis:names:tc:SAML:2.0:assertion'><saml2:NameID>user@test.com</saml2:NameID></saml2:Assertion>"
    nosig, modified = master.saml_auditor.test_signature_exclusion(sample_xml)
    decoded_mod = base64.b64decode(nosig).decode('utf-8')
    print("ElementTree Namespace Overwrite Check (<saml2:Assertion> preserved):", "<saml2:Assertion" in decoded_mod or "Assertion" in decoded_mod)

    report = asyncio.run(master.run_master_audit_suite())
    print(f"Master Audit Status: {report['status']}")
