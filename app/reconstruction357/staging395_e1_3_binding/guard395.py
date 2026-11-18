import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parents[2]
HISTORICAL_FREEZE_SHA256 = "3c77b90d4bbf425148c1c8482c7127cb07ae9503c54f94271debad7728a7f0f1"
HISTORICAL_FREEZE = W / "review390_preaudit/source_freeze.json"
PARENT_FREEZE_SHA256 = "79163ac103be263017db9fd776b70cff76c582ce47dad3b11ef1a6c79f67be55"
PARENT_FREEZE = W / "review394_e1_2_preaudit/source_freeze.json"
CURRENT_FREEZE = W / "review395_e1_3_preaudit/source_freeze.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guard(expected):
    if sha256(HISTORICAL_FREEZE) != HISTORICAL_FREEZE_SHA256:
        raise ValueError("HISTORICAL_390_FREEZE_CHANGED")
    if sha256(PARENT_FREEZE) != PARENT_FREEZE_SHA256:
        raise ValueError("PARENT_E1_2_394_FREEZE_CHANGED")
    historical = json.loads(HISTORICAL_FREEZE.read_text())["files"]
    parent = json.loads(PARENT_FREEZE.read_text())["files"]
    if sha256(CURRENT_FREEZE) != expected:
        raise ValueError("FREEZE_CHANGED")
    files = json.loads(CURRENT_FREEZE.read_text())["files"]
    if any(files.get(name) != digest for name, digest in historical.items()):
        raise ValueError("HISTORICAL_390_KEYSET_OR_PIN_CHANGED")
    if any(files.get(name) != digest for name, digest in parent.items()):
        raise ValueError("PARENT_E1_2_394_KEYSET_OR_PIN_CHANGED")
    for name, digest in files.items():
        path = W / name
        if not path.is_file() or sha256(path) != digest:
            raise ValueError("SOURCE_OR_EVIDENCE_CHANGED:" + name)
    return len(files)
