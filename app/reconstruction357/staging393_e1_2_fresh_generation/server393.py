"""Real loopback e1-2 server: one valid request, two registered constructors, no review."""
import json, sys, threading, uuid
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from guard390 import guard

HERE = Path(__file__).resolve().parent
P = Path(sys.argv[1])
expected = sys.argv[2]
guard(expected)
from contract390 import parse_json, partial
sys.path.insert(0, str(HERE.parent / "staging368_final_pipeline"))
from supervisor import supervise

lock = threading.Lock()
jobs = {}
active = False
used = False
unsafe = False


def work(rid, folder):
    global active, unsafe
    try:
        unsafe = True
        evidence = folder / "owner_supervision_evidence"
        evidence.mkdir()
        state = supervise([sys.executable, "-B", str(HERE / "cycle393.py"), str(folder), rid, expected], 540, evidence_directory=evidence)
        (folder / "owner_supervision.json").write_text(json.dumps(state, indent=2))
        guard(expected)
        unsafe = not (state["cleanup_verified"] and state["worker_reaped"] and not state["unresolved"])
        if state["reason"] != "COMPLETED" or state["worker_returncode"] != 0 or unsafe:
            raise ValueError("OWNER_NOT_CLEAN")
        result = json.loads((folder / "result.json").read_text())
        if result["transport_run_id"] != rid:
            raise ValueError("RESULT_RUN")
        jobs[rid] = result
    except Exception as error:
        jobs[rid] = {**partial("UNKNOWN", rid), "semantic_state": "NOT_RUN_E1_2_OWNER_FAILURE", "reason": type(error).__name__ + ":" + str(error)}
    finally:
        with lock:
            active = False


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def send_value(self, status, value, kind="application/json"):
        data = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type", kind + "; charset=utf-8"); self.send_header("Content-Length", str(len(data))); self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(data)
    def goodhost(self):
        return self.headers.get("Host") == "127.0.0.1:" + str(self.server.server_port)
    def do_GET(self):
        if not self.goodhost(): return self.send_value(403, {"error": "LOOPBACK_HOST"})
        if self.path == "/": return self.send_value(200, (HERE / "index.html").read_bytes(), "text/html")
        if self.path == "/health": return self.send_value(200, {"test_only": False, "experimental": True, "active": active, "unsafe_cleanup": unsafe, "one_shot_used": used})
        if self.path.startswith("/api/runs/"):
            rid = self.path.rsplit("/", 1)[-1]
            if rid not in jobs: return self.send_value(404, {"error": "NOT_FOUND"})
            out = dict(jobs[rid]); events = P / "runs" / rid / "events.jsonl"; out["events"] = []
            if events.exists():
                for line in events.read_text().splitlines(keepends=True):
                    if line.endswith("\n"):
                        try: out["events"].append(json.loads(line))
                        except json.JSONDecodeError: out["event_warning"] = "INCOMPLETE_EVENT_IGNORED"
            return self.send_value(200, out)
        self.send_value(404, {"error": "NOT_FOUND"})
    def do_POST(self):
        global active, used
        if not self.goodhost() or self.headers.get("Origin") not in (None, "http://127.0.0.1:" + str(self.server.server_port)): return self.send_value(403, {"error": "LOCAL_ORIGIN"})
        if self.path == "/shutdown":
            if active or unsafe: return self.send_value(409, {"error": "OWNER_MUST_DRAIN_FIRST"})
            self.send_value(200, {"shutdown": "SAFE_IDLE"}); threading.Thread(target=self.server.shutdown).start(); return
        if self.path != "/api/runs": return self.send_value(404, {"error": "NOT_FOUND"})
        try:
            guard(expected); size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 16384 or self.headers.get("Content-Type", "").split(";")[0] != "application/json": raise ValueError("JSON_BODY_REQUIRED")
            envelope = parse_json(self.rfile.read(size).decode())
        except Exception as error:
            return self.send_value(422, {"state": "INPUT_INVALID", "reason": str(error), "generation_started": False})
        with lock:
            if active or used: return self.send_value(409, {"state": "ONE_SHOT_ALREADY_USED"})
            active = True; used = True
        rid = str(uuid.uuid4()); folder = P / "runs" / rid; folder.mkdir(parents=True, exist_ok=False)
        (folder / "request.json").write_text(json.dumps(envelope, ensure_ascii=False, indent=2)); jobs[rid] = {**partial("RUNNING", rid), "semantic_state": "NOT_RUN_E1_2"}
        threading.Thread(target=work, args=(rid, folder), daemon=False).start()
        self.send_value(202, {"transport_run_id": rid, "status_url": "/api/runs/" + rid, "test_only": False, "experimental": True})


http = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
import os, psutil
(P / "server_address.tmp").write_text(json.dumps({"url": "http://127.0.0.1:" + str(http.server_port), "pid": os.getpid(), "create_time": psutil.Process().create_time(), "test_only": False, "experimental": True}))
(P / "server_address.tmp").replace(P / "server_address.json")
http.serve_forever(); http.server_close()
(P / "server_shutdown.json").write_text(json.dumps({"active": active, "unsafe_cleanup": unsafe, "safe_idle": not active and not unsafe}))
