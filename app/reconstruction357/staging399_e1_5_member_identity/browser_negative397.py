from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "staging368_final_pipeline"))
from request_contract368 import parse_json
from negative_cases397 import FORM_CASES, API_CASES, RAW_API_CASES, VALID_PREFLIGHT_ONLY

base = sys.argv[1].rstrip("/")
out = Path(sys.argv[2])
evidence = {"schema": "E1_4_REAL_NEGATIVE_MATRIX397_V1", "scope": "NEGATIVE_INPUT_ONLY_NO_GENERATION", "form_fields": ["W", "L", "n", "requested_count"], "form_cases": [], "api_cases": [], "valid_preflight_only": [], "post_events": [], "console": [], "page_errors": []}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


for name, value in VALID_PREFLIGHT_ONLY:
    envelope = parse_json(encoded(value))
    evidence["valid_preflight_only"].append({"name": name, "raw": value, "normalized": envelope["normalized_raw"], "network_sent": False, "reason": "valid decimal dimension text; valid POST forbidden in e1-4"})

for name, value, reason in FORM_CASES + API_CASES:
    body = encoded(value)
    try:
        parse_json(body)
        raise AssertionError("NEGATIVE_PRECHECK_ACCEPTED:" + name)
    except ValueError as error:
        assert str(error) == reason, (name, str(error), reason)
for name, body, reason in RAW_API_CASES:
    try:
        parse_json(body)
        raise AssertionError("NEGATIVE_PRECHECK_ACCEPTED:" + name)
    except ValueError as error:
        assert str(error) == reason, (name, str(error), reason)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    context = browser.new_context()
    page = context.new_page()
    page.on("console", lambda message: evidence["console"].append({"type": message.type, "text": message.text}))
    page.on("pageerror", lambda error: evidence["page_errors"].append(str(error)))
    page.on("request", lambda request: evidence["post_events"].append({"url": request.url, "method": request.method, "body": request.post_data}) if request.method == "POST" and request.url == base + "/api/runs" else None)
    before = context.request.get(base + "/health")
    evidence["health_before"] = {"status": before.status, "body": before.json()}
    page.goto(base + "/", wait_until="domcontentloaded")
    evidence["ui_before"] = {"models_children": page.locator("#models").locator(":scope > *").count(), "models_text": page.locator("#models").inner_text(), "status": page.locator("#status").inner_text()}
    for name, values, reason in FORM_CASES:
        for field, value in values.items():
            page.locator(f'input[name="{field}"]').fill(value)
        with page.expect_response(lambda response: response.url == base + "/api/runs" and response.request.method == "POST") as observed:
            page.locator("#submit").click()
        response = observed.value
        body = response.json()
        page.wait_for_function(
            "reason => window.finalResult && window.finalResult.state === 'INPUT_INVALID' && window.finalResult.reason === reason",
            arg=reason,
        )
        row = {"name": name, "route": "real_form_click", "raw_body": response.request.post_data, "status": response.status, "response": body, "summary": page.locator("#summary").inner_text(), "values": {field: page.locator(f'input[name="{field}"]').input_value() for field in values}, "button_enabled": page.locator("#submit").is_enabled(), "models_children": page.locator("#models").locator(":scope > *").count(), "models_text": page.locator("#models").inner_text()}
        assert row["status"] == 422 and body == {"state": "INPUT_INVALID", "reason": reason, "generation_started": False}
        assert row["values"] == values and row["button_enabled"] is True and row["models_children"] == 0 and row["models_text"] == ""
        assert not ({"model", "members", "transport_run_id", "status_url"} & set(body))
        evidence["form_cases"].append(row)
    for name, value, reason in API_CASES:
        raw = encoded(value)
        observed = page.evaluate("""async ({url, body}) => { const response = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body}); return {status:response.status, text:await response.text()}; }""", {"url": base + "/api/runs", "body": raw})
        body = json.loads(observed["text"])
        row = {"name": name, "route": "browser_fetch_api", "raw_body": raw, "status": observed["status"], "response": body, "models_children": page.locator("#models").locator(":scope > *").count(), "models_text": page.locator("#models").inner_text()}
        assert row["status"] == 422 and body == {"state": "INPUT_INVALID", "reason": reason, "generation_started": False}
        assert row["models_children"] == 0 and row["models_text"] == "" and not ({"model", "members", "transport_run_id", "status_url"} & set(body))
        evidence["api_cases"].append(row)
    for name, raw, reason in RAW_API_CASES:
        observed = page.evaluate("""async ({url, body}) => { const response = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body}); return {status:response.status, text:await response.text()}; }""", {"url": base + "/api/runs", "body": raw})
        body = json.loads(observed["text"])
        row = {"name": name, "route": "browser_fetch_raw_api", "raw_body": raw, "status": observed["status"], "response": body, "models_children": page.locator("#models").locator(":scope > *").count(), "models_text": page.locator("#models").inner_text()}
        assert row["status"] == 422 and body == {"state": "INPUT_INVALID", "reason": reason, "generation_started": False}
        assert row["models_children"] == 0 and row["models_text"] == "" and not ({"model", "members", "transport_run_id", "status_url"} & set(body))
        evidence["api_cases"].append(row)
    after = context.request.get(base + "/health")
    evidence["health_after"] = {"status": after.status, "body": after.json()}
    evidence["ui_after"] = {"models_children": page.locator("#models").locator(":scope > *").count(), "models_text": page.locator("#models").inner_text(), "status": page.locator("#status").inner_text(), "final_result": page.evaluate("window.finalResult")}
    browser.close()

assert len(evidence["form_cases"]) == len(FORM_CASES) == 8
assert len(evidence["api_cases"]) == len(API_CASES) + len(RAW_API_CASES) == 7
assert len(evidence["post_events"]) == 15
for health in (evidence["health_before"]["body"], evidence["health_after"]["body"]):
    assert health["one_shot_used"] is False and health["active"] is False and health["unsafe_cleanup"] is False
assert evidence["ui_before"]["models_children"] == evidence["ui_after"]["models_children"] == 0
assert evidence["ui_before"]["models_text"] == evidence["ui_after"]["models_text"] == ""
evidence["verified"] = True
(out / "REAL_NEGATIVE_MATRIX_RESULT.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
