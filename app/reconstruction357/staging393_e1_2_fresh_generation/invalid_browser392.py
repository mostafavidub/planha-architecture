from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

base = sys.argv[1].rstrip("/")
out = Path(sys.argv[2])

cases = [
    ("empty_width", {"W": "", "L": "۲۸", "n": "۲", "requested_count": "۲"}, "EXACT_DECIMAL_REQUIRED:W", "عرض را با عدد معتبر"),
    ("unsupported_width", {"W": "۲۵", "L": "۲۸", "n": "۲", "requested_count": "۲"}, "UNSUPPORTED_EXACT_FIXED_DIMENSION:W", "عرض در این فرم باید دقیقاً ۲۶ متر باشد"),
    ("leading_zero_units", {"W": "۲۶", "L": "۲۸", "n": "۰۲", "requested_count": "۲"}, "COUNT_CANONICAL_DIGITS_REQUIRED:n", "تعداد واحد باید عدد صحیح ۲ باشد"),
    ("decimal_requested_count", {"W": "۲۶", "L": "۲۸", "n": "۲", "requested_count": "۲٫۵"}, "COUNT_CANONICAL_DIGITS_REQUIRED:requested_count", "تعداد گزینه باید عدد صحیح ۲ باشد"),
]
evidence = {"schema": "E1_1_REAL_INVALID_BROWSER392_V1", "scope": "INVALID_INPUT_ONLY_NO_GENERATION", "cases": [], "post_events": [], "console": [], "page_errors": []}

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    context = browser.new_context()
    page = context.new_page()
    page.on("console", lambda message: evidence["console"].append({"type": message.type, "text": message.text}))
    page.on("pageerror", lambda error: evidence["page_errors"].append(str(error)))
    page.on("request", lambda request: evidence["post_events"].append({"url": request.url, "method": request.method, "body": request.post_data}) if request.method == "POST" else None)
    before = context.request.get(base + "/health")
    evidence["health_before"] = {"status": before.status, "body": before.json()}
    page.goto(base + "/", wait_until="domcontentloaded")
    for name, values, reason, message in cases:
        for field, value in values.items():
            page.locator(f'input[name="{field}"]').fill(value)
        with page.expect_response(lambda response: response.url == base + "/api/runs" and response.request.method == "POST") as observed:
            page.locator("#submit").click()
        response = observed.value
        body = response.json()
        page.wait_for_function("window.finalResult && window.finalResult.state === 'INPUT_INVALID'")
        row = {
            "name": name,
            "status": response.status,
            "response": body,
            "summary": page.locator("#summary").inner_text(),
            "values": {field: page.locator(f'input[name="{field}"]').input_value() for field in values},
            "button_enabled": page.locator("#submit").is_enabled(),
            "window_result": page.evaluate("window.finalResult"),
        }
        assert row["status"] == 422
        assert body == {"state": "INPUT_INVALID", "reason": reason, "generation_started": False}
        assert message in row["summary"]
        assert row["values"] == values
        assert row["button_enabled"] is True
        evidence["cases"].append(row)
    after = context.request.get(base + "/health")
    evidence["health_after"] = {"status": after.status, "body": after.json()}
    evidence["final_dom"] = {
        "summary": page.locator("#summary").inner_text(),
        "button_enabled": page.locator("#submit").is_enabled(),
        "values": {field: page.locator(f'input[name="{field}"]').input_value() for field in ("W", "L", "n", "requested_count")},
    }
    browser.close()

assert len(evidence["cases"]) == 4
assert len(evidence["post_events"]) == 4
assert evidence["health_before"]["body"]["one_shot_used"] is False
assert evidence["health_after"]["body"]["one_shot_used"] is False
assert evidence["health_after"]["body"]["active"] is False
assert evidence["health_after"]["body"]["unsafe_cleanup"] is False
evidence["verified"] = True
(out / "REAL_BROWSER_INVALID_RESULT.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
