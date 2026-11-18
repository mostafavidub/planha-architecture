"""Synthetic timing/replayed-response browser test of the actual HTML; never generation evidence."""
from __future__ import annotations

import json
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "reconstruction357/staging397_e1_4_negative_matrix/index.html"
FIXED = Path(__file__).resolve().parent / "index.html"
OUT = Path(sys.argv[1])


class ScenarioServer:
    def __init__(self, html, post_delay=0, poll_delay=0, reject=False):
        self.html = html.read_bytes()
        self.post_delay = post_delay
        self.poll_delay = poll_delay
        self.reject = reject
        self.posts = []
        self.events = []
        self.post_seen = threading.Event()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def send(self, code, value, kind="application/json"):
                data = value if isinstance(value, bytes) else json.dumps(value).encode()
                self.send_response(code)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                outer.events.append({"type": "GET", "path": self.path, "time": time.monotonic()})
                if self.path == "/":
                    return self.send(200, outer.html, "text/html; charset=utf-8")
                if self.path == "/api/runs/run-old":
                    time.sleep(outer.poll_delay)
                    return self.send(200, {
                        "state": "COMPLETED_SYNTHETIC_REPLAY",
                        "transport_run_id": "run-old",
                        "request_fulfilled": False,
                        "members": [{"kind": "balanced", "binding": {"model_digest": "model-old"}, "model": {"units": [], "walls": {}}, "physical_review_status": "SYNTHETIC", "qualification": {"qualified": False, "missing": ["NOT_REAL_GENERATION"]}}],
                    })
                return self.send(404, {})

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length", "0"))).decode()
                outer.posts.append(raw)
                outer.events.append({"type": "POST", "path": self.path, "raw": raw, "time": time.monotonic()})
                outer.post_seen.set()
                time.sleep(outer.post_delay)
                if outer.reject:
                    return self.send(422, {"state": "INPUT_INVALID", "reason": "UNSUPPORTED_EXACT_FIXED_DIMENSION:W", "generation_started": False})
                return self.send(202, {"transport_run_id": "run-old", "status_url": "/api/runs/run-old", "test_only": True, "synthetic": True})

        self.http = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.http.serve_forever)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.http.server_port}"

    def close(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()


def state(page):
    return page.evaluate("""() => ({values:Object.fromEntries(new FormData(document.querySelector('#form'))),summary:document.querySelector('#summary').textContent,status:document.querySelector('#status').textContent,models:document.querySelector('#models').children.length,modelText:document.querySelector('#models').textContent,buttonDisabled:document.querySelector('#submit').disabled,transportRunId:window.transportRunId||null,displayBinding:window.displayBinding||null,staleResult:window.staleResult||null,finalResult:window.finalResult||null,ledger:window.requestLedger||null})""")


def run_case(playwright, html, name, post_delay=0, poll_delay=0, reject=False, edit_field="W", edit_value="۲۵", wait_for_accept=False):
    server = ScenarioServer(html, post_delay, poll_delay, reject)
    browser = playwright.chromium.launch(headless=True, executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    page = browser.new_page()
    timeline = []
    result = None
    try:
        page.goto(server.url + "/", wait_until="domcontentloaded")
        timeline.append({"event": "loaded", "state": state(page)})
        page.locator("#submit").click()
        assert server.post_seen.wait(2)
        timeline.append({"event": "post_received", "post_count": len(server.posts), "raw": server.posts[0]})
        if wait_for_accept:
            page.wait_for_function("window.transportRunId === 'run-old'")
            timeline.append({"event": "accepted", "state": state(page)})
        page.locator(f'input[name="{edit_field}"]').fill(edit_value)
        timeline.append({"event": "input_changed", "state": state(page)})
        page.evaluate("document.querySelector('#form').requestSubmit()")
        timeline.append({"event": "duplicate_submit_attempt", "state": state(page)})
        page.wait_for_timeout(1400)
        timeline.append({"event": "late_response_settled", "state": state(page), "post_count": len(server.posts)})
        result = {"name": name, "synthetic_timing_and_response": True, "source_html": str(html.relative_to(ROOT)), "server_events": server.events, "posts": server.posts, "timeline": timeline}
        return result
    finally:
        browser.close()
        port = server.http.server_port
        server.close()
        probe = socket.socket()
        probe.settimeout(1)
        connect_ex = probe.connect_ex(("127.0.0.1", port))
        probe.close()
        if result is not None:
            result["cleanup"] = {"browser_closed": True, "server_thread_alive": server.thread.is_alive(), "loopback_port": port, "listener_connect_ex_after": connect_ex}


with sync_playwright() as playwright:
    cases = []
    for label, html in (("original397", ORIGINAL), ("fixed398", FIXED)):
        cases.append(run_case(playwright, html, label + "_edit_before_accept", post_delay=.45))
        cases.append(run_case(playwright, html, label + "_edit_during_poll", poll_delay=.45, edit_field="L", edit_value="۲۷", wait_for_accept=True))
        cases.append(run_case(playwright, html, label + "_delayed_invalid_after_edit", post_delay=.45, reject=True))
        cases.append(run_case(playwright, html, label + "_display_then_edit", edit_field="requested_count", edit_value="۳", wait_for_accept=True))

by_name = {case["name"]: case for case in cases}
for suffix in ("edit_before_accept", "edit_during_poll"):
    old = by_name["original397_" + suffix]["timeline"][-1]
    new = by_name["fixed398_" + suffix]["timeline"][-1]
    assert old["state"]["models"] == 1, (suffix, old)
    assert new["state"]["models"] == 0 and new["state"]["displayBinding"] is None, (suffix, new)
    assert new["post_count"] == 1
    assert any(row["type"] == "TERMINAL_SUPPRESSED_STALE" for row in new["state"]["ledger"])
old_invalid = by_name["original397_delayed_invalid_after_edit"]["timeline"][-1]["state"]
new_invalid = by_name["fixed398_delayed_invalid_after_edit"]["timeline"][-1]["state"]
assert old_invalid["finalResult"]["state"] == "INPUT_INVALID"
assert new_invalid["finalResult"] is None and new_invalid["values"]["W"] == "۲۵" and new_invalid["buttonDisabled"] is False
old_edit = by_name["original397_display_then_edit"]["timeline"][-1]["state"]
new_edit = by_name["fixed398_display_then_edit"]["timeline"][-1]["state"]
assert old_edit["models"] == 1
assert new_edit["models"] == 0 and new_edit["displayBinding"] is None
for case in cases:
    assert len(case["posts"]) == 1
    assert case["cleanup"]["browser_closed"] is True and case["cleanup"]["server_thread_alive"] is False and case["cleanup"]["listener_connect_ex_after"] == 111

result = {"schema": "E1_5_STALE_RESPONSE398_BROWSER_EVIDENCE_V1", "scope": "SYNTHETIC_TIMING_AND_REPLAYED_RESPONSE_ON_ACTUAL_HTML_NO_GENERATION", "verified": True, "cases": cases, "limitations": ["Synthetic responses are not fresh construction or reviewer evidence.", "The real one-shot server has no public redesign submission flow; this test does not claim redesign support."]}
(OUT / "BROWSER_RACE_RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
