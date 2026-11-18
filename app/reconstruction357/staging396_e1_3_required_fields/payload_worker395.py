"""Build actual registered reviewer input from the current record; do not call the checker."""
import json
import sys
import time
from pathlib import Path

kind, record_path, output_path = sys.argv[1:]
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
record = json.loads(Path(record_path).read_text())
if kind == "balanced":
    sys.path.insert(0, str(ROOT / "staging378_finite_portals" / "runtime"))
    sys.path.insert(0, str(ROOT / "staging378_finite_portals"))
    from source_registry365 import resolve
elif kind == "joint":
    sys.path.insert(0, str(ROOT / "staging367_joint_source_validation_attempt2" / "runtime"))
    sys.path.insert(0, str(ROOT / "staging367_joint_source_validation_attempt2"))
    from source_registry_joint367 import resolve
else:
    raise ValueError("KIND")
context = resolve(record, time.monotonic() + 60)
Path(output_path).write_text(json.dumps({"payload": dict(context), "proof": context._proof, "reviewer_interface": "registered CurrentContext consumed by checker114.evaluate", "checker_executed": False}, ensure_ascii=False, indent=2))
