import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parents[2]
HISTORICAL_FREEZE_SHA256 = "3c77b90d4bbf425148c1c8482c7127cb07ae9503c54f94271debad7728a7f0f1"
HISTORICAL_FREEZE = W / "review390_preaudit/source_freeze.json"
CURRENT_FREEZE = W / "review391_e1_1_preaudit/source_freeze.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guard(expected):
    if sha256(HISTORICAL_FREEZE) != HISTORICAL_FREEZE_SHA256:
        raise ValueError("HISTORICAL_390_FREEZE_CHANGED")
    historical = json.loads(HISTORICAL_FREEZE.read_text())["files"]
    if sha256(CURRENT_FREEZE) != expected:
        raise ValueError("FREEZE_CHANGED")
    files = json.loads(CURRENT_FREEZE.read_text())["files"]
    if any(files.get(name) != digest for name, digest in historical.items()):
        raise ValueError("HISTORICAL_390_KEYSET_OR_PIN_CHANGED")
    for name, digest in files.items():
        path = W / name
        if not path.is_file() or sha256(path) != digest:
            raise ValueError("SOURCE_OR_EVIDENCE_CHANGED:" + name)
    return len(files)
