from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path

if not sys.platform.startswith("linux"):
    raise SystemExit("LINUX_REQUIRED_FOR_PSUTIL_AND_MANAGED_PROCESS_IDENTITY")

import psutil
from guard390 import guard

HERE = Path(__file__).resolve().parent
if len(sys.argv) != 3:
    raise SystemExit("usage: python -B launch_negative_matrix397.py NEW_EVIDENCE_DIRECTORY EXPECTED_FREEZE_SHA256")
evidence = Path(sys.argv[1]).resolve()
expected = sys.argv[2]
if evidence.exists():
    raise SystemExit("EVIDENCE_PATH_MUST_NOT_EXIST")
if len(expected) != 64 or any(character not in "0123456789abcdef" for character in expected):
    raise SystemExit("EXPECTED_FREEZE_SHA256_REQUIRED")
if evidence.name in {"review390_actual_v1", "review391_e1_1_actual_v1"}:
    raise SystemExit("HISTORICAL_EVIDENCE_PATH_FORBIDDEN")

evidence.mkdir(parents=True)
receipt = {
    "schema": "E1_4_NEGATIVE_MATRIX397_ENTRYPOINT_V1",
    "experimental": True,
    "test_only": False,
    "valid_input_authorized": False,
    "generation_authorized": False,
    "evidence_path": str(evidence),
    "expected_freeze_sha256": expected,
    "source_guard_before": guard(expected),
}
(evidence / "ENTRYPOINT_PREREGISTRATION.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

server_stdout = (evidence / "server.stdout.log").open("wb")
server_stderr = (evidence / "server.stderr.log").open("wb")
server = subprocess.Popen(
    [sys.executable, "-B", str(HERE / "server390.py"), str(evidence), expected],
    stdout=server_stdout,
    stderr=server_stderr,
    start_new_session=True,
)
server_identity = {"pid": server.pid, "create_time": psutil.Process(server.pid).create_time()}
(evidence / "SERVER_PROCESS_IDENTITY.json").write_text(json.dumps(server_identity, indent=2) + "\n", encoding="utf-8")


def get_json(url):
    with urllib.request.urlopen(url, timeout=3) as response:
        return response.status, json.loads(response.read())


def post_json(url, value):
    data = json.dumps(value).encode()
    request = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=3) as response:
        return response.status, json.loads(response.read())


base = None
failure = None
try:
    deadline = time.monotonic() + 30
    address_path = evidence / "server_address.json"
    while time.monotonic() < deadline:
        if server.poll() is not None:
            raise RuntimeError("SERVER_EXITED_BEFORE_ADDRESS")
        if address_path.is_file():
            try:
                address = json.loads(address_path.read_text())
                if address.get("pid") == server_identity["pid"] and abs(address.get("create_time") - server_identity["create_time"]) < 0.01:
                    base = address["url"]
                    break
            except (json.JSONDecodeError, KeyError, TypeError):
                pass
        time.sleep(0.05)
    if base is None:
        raise TimeoutError("SERVER_ADDRESS_TIMEOUT")
    status, health = get_json(base + "/health")
    receipt["health_before_browser"] = {"status": status, "body": health}
    if status != 200 or health.get("active") or health.get("unsafe_cleanup") or health.get("one_shot_used"):
        raise RuntimeError("SERVER_NOT_FRESH_IDLE")
    browser = subprocess.run(
        [sys.executable, "-B", str(HERE / "browser_negative397.py"), base, str(evidence)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    (evidence / "browser.stdout.log").write_bytes(browser.stdout)
    (evidence / "browser.stderr.log").write_bytes(browser.stderr)
    receipt["browser_returncode"] = browser.returncode
    if browser.returncode != 0:
        raise RuntimeError("INVALID_BROWSER_RUNNER_FAILED")
    status, health = get_json(base + "/health")
    receipt["health_after_browser"] = {"status": status, "body": health}
    if status != 200 or health.get("active") or health.get("unsafe_cleanup") or health.get("one_shot_used"):
        raise RuntimeError("GENERATION_OR_ONE_SHOT_STATE_CHANGED")
    if (evidence / "runs").exists():
        raise RuntimeError("RUN_DIRECTORY_UNEXPECTED")
    receipt["source_guard_after"] = guard(expected)
except Exception as error:
    failure = type(error).__name__ + ":" + str(error)
    (evidence / "ENTRYPOINT_ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
finally:
    safe_shutdown = False
    if base is not None:
        try:
            _, health = get_json(base + "/health")
            receipt["health_before_shutdown"] = health
            if not health.get("active") and not health.get("unsafe_cleanup"):
                receipt["shutdown_response"] = post_json(base + "/shutdown", {})
                safe_shutdown = True
        except Exception as error:
            receipt["shutdown_observation_error"] = type(error).__name__ + ":" + str(error)
    try:
        receipt["server_returncode"] = server.wait(timeout=30 if safe_shutdown else 1)
    except subprocess.TimeoutExpired:
        receipt["server_returncode"] = None
        receipt["server_preserved_due_to_unproven_safe_shutdown"] = True
    server_stdout.close()
    server_stderr.close()
    alive = False
    try:
        process = psutil.Process(server_identity["pid"])
        alive = abs(process.create_time() - server_identity["create_time"]) < 0.01
    except psutil.NoSuchProcess:
        pass
    receipt["server_identity_alive_after"] = alive
    if base is not None:
        port = int(base.rsplit(":", 1)[1])
        probe = socket.socket()
        probe.settimeout(1)
        receipt["listener_connect_ex_after"] = probe.connect_ex(("127.0.0.1", port))
        probe.close()
    receipt["failure"] = failure
    receipt["completed"] = failure is None and receipt.get("server_returncode") == 0 and not alive and receipt.get("listener_connect_ex_after") == 111
    (evidence / "ENTRYPOINT_RESULT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

if not receipt["completed"]:
    raise SystemExit(1)
