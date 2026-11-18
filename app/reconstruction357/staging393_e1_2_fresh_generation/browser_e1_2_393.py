"""One valid corrected-form submission to real registered builders; drain owner before shutdown."""
import errno
import hashlib
import json
import socket
import subprocess
import sys
import time
import traceback
import urllib.request
from pathlib import Path

import psutil
from playwright.sync_api import sync_playwright

from guard390 import guard

P = Path(sys.argv[1])
expected = sys.argv[2]
HERE = Path(__file__).resolve().parent
guard(expected)
historical_run = "c72145e6-a608-4122-ad15-29ee430ce4bf"
historical_candidates = {
    "f6acda6459444bb86080dea68d5939d2b0b04c85514491cde367b8f603b4cf8d",
    "035740e68e9bad94312d4c1c31396ca467b670174c55f6cf0e888f8cee1d246b",
}
historical_records = {
    "0ba59aad03b730e463567c40d5549304de29fcebe0bb2d3f4421defd75bf53a1",
    "b08c38854e21b6225e2c8fe47eebb0759ecd6f01c414ab533a1f7b02219791df",
}
server = subprocess.Popen([sys.executable, "-B", str(HERE / "server393.py"), str(P), expected])
start = time.monotonic()
started_wall_ns = time.time_ns()
url = None
error = None
posts = []


def api(path, data=None):
    request = urllib.request.Request(url + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.load(response)


try:
    while not (P / "server_address.json").exists():
        if server.poll() is not None or time.monotonic() - start > 20:
            raise ValueError("SERVER_NOT_READY")
        time.sleep(0.1)
    address = json.loads((P / "server_address.json").read_text())
    url = address["url"]
    if api("/health") != {"test_only": False, "experimental": True, "active": False, "unsafe_cleanup": False, "one_shot_used": False}:
        raise ValueError("SERVER_NOT_FRESH_IDLE")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path="/usr/bin/chromium", headless=True, args=["--no-sandbox"])
        try:
            page = browser.new_page(viewport={"width": 1200, "height": 1000})
            page.on("request", lambda request: posts.append({"url": request.url, "method": request.method, "body": request.post_data}) if request.method == "POST" and request.url == url + "/api/runs" else None)
            page.goto(url, wait_until="networkidle")
            values = {"W": "۲۶", "L": "۲۸", "n": "۲", "requested_count": "۲"}
            for key, value in values.items():
                page.locator('input[name="' + key + '"]').fill(value)
            click_wall_ns = time.time_ns()
            page.locator("#submit").click()
            page.wait_for_function("window.finalResult !== undefined", timeout=600000)
            result = page.evaluate("window.finalResult")
            dom = {
                "summary": page.locator("#summary").inner_text(),
                "button_enabled": page.locator("#submit").is_enabled(),
                "values": {key: page.locator('input[name="' + key + '"]').input_value() for key in values},
            }
            (P / "browser_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
            (P / "browser_dom.json").write_text(json.dumps(dom, ensure_ascii=False, indent=2))
            if len(posts) != 1:
                raise ValueError("EXACTLY_ONE_BROWSER_POST_REQUIRED")
            if json.loads(posts[0]["body"]) != values:
                raise ValueError("RAW_PERSIAN_REQUEST_CHANGED")
            if result.get("transport_run_id") == historical_run:
                raise ValueError("HISTORICAL_RUN_REUSED")
            if result.get("test_only") is not False or result.get("experimental") is not True or result.get("accepted") is not False:
                raise ValueError("PARTIAL_EXPERIMENTAL_SCOPE")
            if result.get("transport_run_id") != page.evaluate("window.transportRunId"):
                raise ValueError("BROWSER_TRANSPORT_RUN_BINDING")
            binding = result.get("binding", {})
            if binding.get("run_id") != result["transport_run_id"] or binding.get("transport_body_sha256") != hashlib.sha256(posts[0]["body"].encode()).hexdigest():
                raise ValueError("BROWSER_BODY_RESULT_BINDING")
            from contract390 import digest, verify

            runfolder = P / "runs" / result["transport_run_id"]
            request = json.loads((runfolder / "request.json").read_text())
            verify(request)
            audits = {}
            for kind in ("balanced", "joint"):
                folder = runfolder / kind
                record = json.loads((folder / "record.json").read_text())
                member = next(item for item in result["members"] if item["kind"] == kind)
                model = record["candidate"]["model"]
                if member["binding"]["run_id"] != result["transport_run_id"] or member["binding"]["candidate_id"] != record["candidate_id"] or member["binding"]["record_digest"] != digest(record) or member["binding"]["model_digest"] != digest(model):
                    raise ValueError("BROWSER_MEMBER_BINDING_CHANGED:" + kind)
                receipt = json.loads((folder / "construct_worker_receipt.json").read_text())
                record_digest = digest(record)
                if receipt.get("run_id") != result["transport_run_id"] or receipt.get("kind") != kind or receipt.get("phase") != "construct" or receipt.get("record_digest") != record_digest:
                    raise ValueError("FRESH_CONSTRUCT_RECEIPT_BINDING:" + kind)
                if (folder / "record.json").stat().st_mtime_ns < click_wall_ns:
                    raise ValueError("RECORD_NOT_CREATED_AFTER_FORM_CLICK:" + kind)
                audits[kind] = {
                    "registered_builder": "staging378_finite_portals/source378.construct" if kind == "balanced" else "staging367_service_joint_attempt2/joint367.construct",
                    "candidate_id": member["binding"]["candidate_id"],
                    "record_digest": record_digest,
                    "model_digest": member["binding"]["model_digest"],
                    "deterministic_candidate_matches_historical390": member["binding"]["candidate_id"] in historical_candidates,
                    "deterministic_record_matches_historical390": record_digest in historical_records,
                    "construct_receipt": receipt,
                    "record_sha256": hashlib.sha256((folder / "record.json").read_bytes()).hexdigest(),
                    "record_mtime_ns": (folder / "record.json").stat().st_mtime_ns,
                }
            (P / "FRESH_GENERATION_AUDIT.json").write_text(json.dumps({
                "schema": "E1_2_FRESH_REGISTERED_BUILDERS393_V1",
                "fresh_generation_verified": True,
                "browser_click_wall_ns": click_wall_ns,
                "runner_started_wall_ns": started_wall_ns,
                "run_id": result["transport_run_id"],
                "historical390_run_id": historical_run,
                "historical_result_reused": False,
                "raw_received_input": request["received_input"],
                "normalized_raw": request["normalized_raw"],
                "canonical_request": request["canonical_request"],
                "canonical_request_digest": request["canonical_request_digest"],
                "transport_body_sha256": request["transport_body_sha256"],
                "builders": audits,
                "dependent_pipeline_phases_observed": [],
                "reviews_started": False,
                "e1_3_or_later_claimed": False,
                "technical_acceptance_claimed": False,
            }, ensure_ascii=False, indent=2))
            (P / "browser_binding_audit.json").write_text(json.dumps({"verified": True, "members": {kind: value["construct_receipt"] for kind, value in audits.items()}, "post_count": len(posts)}, indent=2))
        finally:
            browser.close()
except BaseException as exception:
    error = type(exception).__name__ + ":" + str(exception)
    (P / "browser_error.txt").write_text(traceback.format_exc())
finally:
    (P / "browser_posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=2))
    if url:
        drain = []
        while True:
            try:
                state = api("/health")
                drain.append({"seconds": time.monotonic() - start, **state})
                if not state["active"] and not state["unsafe_cleanup"]:
                    (P / "shutdown_response.json").write_text(json.dumps(api("/shutdown", b"{}")))
                    break
            except Exception as exception:
                drain.append({"seconds": time.monotonic() - start, "error": str(exception)})
            if time.monotonic() - start > 640:
                (P / "drain_unresolved.json").write_text(json.dumps(drain, indent=2))
                raise RuntimeError("OWNER_DRAIN_UNRESOLVED_OUTER_CONTAINMENT_REQUIRED")
            time.sleep(0.25)
        (P / "drain_evidence.json").write_text(json.dumps(drain, indent=2))
        server.wait(timeout=10)
        (P / "server_reaped.json").write_text(json.dumps({"returncode": server.returncode, "safe_shutdown_requested": True}))
        try:
            connection = socket.create_connection(("127.0.0.1", int(url.rsplit(":", 1)[1])), timeout=2)
            connection.close()
            raise ValueError("LISTENER_STILL_OPEN")
        except OSError as exception:
            if exception.errno != errno.ECONNREFUSED:
                raise
            (P / "listener_closed.json").write_text(json.dumps({"verified": True, "errno": exception.errno, "url": url}))
        alive = False
        try:
            alive = abs(psutil.Process(address["pid"]).create_time() - address["create_time"]) < 0.01
        except psutil.NoSuchProcess:
            pass
        (P / "server_identity_audit.json").write_text(json.dumps({"pid": address["pid"], "create_time": address["create_time"], "original_process_gone": not alive}))
        if alive:
            raise ValueError("SERVER_IDENTITY_STILL_ALIVE")
    guard(expected)
if error:
    raise RuntimeError(error)
