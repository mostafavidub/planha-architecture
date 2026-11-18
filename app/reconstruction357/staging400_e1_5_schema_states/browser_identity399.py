"""Real-390-schema replay tests for frontend identity gates; no generation."""
from __future__ import annotations

import copy
import json
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
HTML398 = ROOT / "reconstruction357/staging398_e1_5_stale_response/index.html"
HTML399 = Path(__file__).resolve().parent / "index.html"
REAL_RESULT_PATH = ROOT / "review390_actual_v1/runs/c72145e6-a608-4122-ad15-29ee430ce4bf/result.json"
REAL = json.loads(REAL_RESULT_PATH.read_text())
RUN_ID = REAL["transport_run_id"]
OUT = Path(sys.argv[1])


def fixture(kind):
    value = copy.deepcopy(REAL)
    if kind == "member_wrong_run":
        value["members"][0]["binding"]["run_id"] = "11111111-1111-4111-8111-111111111111"
    elif kind == "model_digest_mismatch":
        value["members"][0]["model"]["_synthetic_tamper"] = True
    elif kind == "outer_wrong_run":
        value["transport_run_id"] = "22222222-2222-4222-8222-222222222222"
    elif kind == "request_body_mismatch":
        wrong = "0" * 64
        value["binding"]["transport_body_sha256"] = wrong
        for member in value["members"]:
            member["binding"]["transport_body_sha256"] = wrong
    elif kind != "compatible":
        raise ValueError(kind)
    return value


class Local:
    def __init__(self, html, result=None, invalid=False):
        self.html = html.read_bytes()
        self.result = result
        self.invalid = invalid
        self.posts = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_): pass
            def send_value(self, code, value, kind="application/json"):
                data = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode()
                self.send_response(code); self.send_header("Content-Type", kind); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
            def do_GET(self):
                if self.path == "/": return self.send_value(200, outer.html, "text/html; charset=utf-8")
                if self.path == "/api/runs/" + RUN_ID: return self.send_value(200, outer.result)
                return self.send_value(404, {})
            def do_POST(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", "0"))).decode(); outer.posts.append(body)
                if outer.invalid: return self.send_value(422, {"state":"INPUT_INVALID","reason":"UNSUPPORTED_EXACT_FIXED_DIMENSION:W","generation_started":False})
                return self.send_value(202, {"transport_run_id":RUN_ID,"status_url":"/api/runs/"+RUN_ID,"test_only":True,"synthetic_replay":True})

        self.http = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.http.serve_forever); self.thread.start()
        self.url = f"http://127.0.0.1:{self.http.server_port}"

    def close(self):
        port = self.http.server_port; self.http.shutdown(); self.http.server_close(); self.thread.join()
        probe = socket.socket(); probe.settimeout(1); result = probe.connect_ex(("127.0.0.1", port)); probe.close()
        return {"port": port, "thread_alive": self.thread.is_alive(), "listener_connect_ex_after": result}


def browser_state(page):
    return page.evaluate("""() => ({models:document.querySelector('#models').children.length,modelText:document.querySelector('#models').textContent,summary:document.querySelector('#summary').textContent,values:Object.fromEntries(new FormData(document.querySelector('#form'))),finalResult:window.finalResult||null,displayBinding:window.displayBinding||null,ledger:window.requestLedger||null})""")


def run_case(playwright, html, kind):
    local = Local(html, fixture(kind))
    browser = playwright.chromium.launch(headless=True, executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    row = {"source_html": str(html.relative_to(ROOT)), "fixture": kind, "real_schema_source": str(REAL_RESULT_PATH.relative_to(ROOT)), "synthetic_replay": True}
    try:
        page = browser.new_page(); page.goto(local.url + "/", wait_until="domcontentloaded"); page.locator("#submit").click()
        page.wait_for_function("window.finalResult !== null && window.finalResult !== undefined", timeout=5000)
        row.update(state=browser_state(page), posts=list(local.posts))
    finally:
        browser.close(); row["cleanup"] = local.close()
    return row


def invalid_with_prior_model(playwright):
    local = Local(HTML399, invalid=True)
    browser = playwright.chromium.launch(headless=True, executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    row = {"source_html": str(HTML399.relative_to(ROOT)), "fixture": "prior_replayed_model_then_invalid", "synthetic_replay": True}
    try:
        page = browser.new_page(); page.goto(local.url + "/", wait_until="domcontentloaded")
        page.evaluate("members => { render(members); window.displayBinding={synthetic_prior:true}; }", REAL["members"])
        row["prior_models"] = page.locator("#models").locator(":scope > *").count()
        page.locator('input[name="W"]').fill("۲۵")
        row["after_edit_before_submit"] = browser_state(page)
        page.locator("#submit").click(); page.wait_for_function("window.finalResult && window.finalResult.state === 'INPUT_INVALID'")
        row.update(state=browser_state(page), posts=list(local.posts))
    finally:
        browser.close(); row["cleanup"] = local.close()
    return row


with sync_playwright() as playwright:
    cases = {
        "398_member_wrong_run_baseline": run_case(playwright, HTML398, "member_wrong_run"),
        "399_compatible": run_case(playwright, HTML399, "compatible"),
        "399_member_wrong_run": run_case(playwright, HTML399, "member_wrong_run"),
        "399_model_digest_mismatch": run_case(playwright, HTML399, "model_digest_mismatch"),
        "399_outer_wrong_run": run_case(playwright, HTML399, "outer_wrong_run"),
        "399_request_body_mismatch": run_case(playwright, HTML399, "request_body_mismatch"),
        "399_prior_model_then_invalid": invalid_with_prior_model(playwright),
    }

baseline = cases["398_member_wrong_run_baseline"]["state"]
assert baseline["models"] == 2 and baseline["finalResult"]["state"] == REAL["state"]
positive = cases["399_compatible"]["state"]
assert positive["models"] == 2 and positive["finalResult"]["state"] == REAL["state"]
assert positive["displayBinding"]["transport_run_id"] == RUN_ID
assert positive["displayBinding"]["raw_snapshot"] == {"W":"۲۶","L":"۲۸","n":"۲","requested_count":"۲"}
assert positive["displayBinding"]["model_ids"] == [member["binding"]["model_digest"] for member in REAL["members"]]
for name, reason in (("399_member_wrong_run","MEMBER_RUN_OR_KIND_MISMATCH"),("399_model_digest_mismatch","MEMBER_MODEL_DIGEST_MISMATCH"),("399_outer_wrong_run","POLL_RUN_ID_MISMATCH"),("399_request_body_mismatch","OUTER_REQUEST_BODY_MISMATCH")):
    state = cases[name]["state"]
    assert state["models"] == 0 and state["displayBinding"] is None
    assert state["finalResult"]["state"] == "IDENTITY_MISMATCH" and state["finalResult"]["reason"] == reason
    assert any(event["type"] == "IDENTITY_REJECTED" and event["reason"] == reason for event in state["ledger"])
invalid = cases["399_prior_model_then_invalid"]
assert invalid["prior_models"] == 2 and invalid["after_edit_before_submit"]["models"] == 0
assert invalid["state"]["models"] == 0 and invalid["state"]["displayBinding"] is None and invalid["state"]["finalResult"]["state"] == "INPUT_INVALID"
for case in cases.values():
    assert len(case["posts"]) == 1 and not case["cleanup"]["thread_alive"] and case["cleanup"]["listener_connect_ex_after"] == 111

OUT.joinpath("MEMBER_IDENTITY_BROWSER_RESULT.json").write_text(json.dumps({"schema":"E1_5_MEMBER_IDENTITY399_BROWSER_V1","verified":True,"real_schema_fixture_sha256":__import__('hashlib').sha256(REAL_RESULT_PATH.read_bytes()).hexdigest(),"real_generation":False,"cases":cases}, ensure_ascii=False, indent=2)+"\n")
