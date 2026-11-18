import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parents[2]
HISTORICAL_FREEZE_SHA256 = "3c77b90d4bbf425148c1c8482c7127cb07ae9503c54f94271debad7728a7f0f1"
HISTORICAL_FREEZE = W / "review390_preaudit/source_freeze.json"
PARENT_FREEZE_SHA256 = "f2d9a37fc42c913bd7aa96c12dbcf9031e4856487de6e451536414a85f05dc9a"
PARENT_FREEZE = W / "review398_e1_5_preaudit/source_freeze.json"
CURRENT_FREEZE = W / "review399_e1_5_identity_preaudit/source_freeze.json"


def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def guard(expected):
    if sha256(HISTORICAL_FREEZE) != HISTORICAL_FREEZE_SHA256: raise ValueError("HISTORICAL_390_FREEZE_CHANGED")
    if sha256(PARENT_FREEZE) != PARENT_FREEZE_SHA256: raise ValueError("PARENT_E1_5_398_FREEZE_CHANGED")
    historical = json.loads(HISTORICAL_FREEZE.read_text())["files"]
    parent = json.loads(PARENT_FREEZE.read_text())["files"]
    if sha256(CURRENT_FREEZE) != expected: raise ValueError("FREEZE_CHANGED")
    files = json.loads(CURRENT_FREEZE.read_text())["files"]
    if any(files.get(name) != digest for name, digest in historical.items()): raise ValueError("HISTORICAL_390_KEYSET_OR_PIN_CHANGED")
    if any(files.get(name) != digest for name, digest in parent.items()): raise ValueError("PARENT_E1_5_398_KEYSET_OR_PIN_CHANGED")
    for name, digest in files.items():
        path = W / name
        if not path.is_file() or sha256(path) != digest: raise ValueError("SOURCE_OR_EVIDENCE_CHANGED:" + name)
    return len(files)
