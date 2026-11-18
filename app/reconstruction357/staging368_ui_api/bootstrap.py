"""Stdlib-only preimport verification. Does not import project modules."""
import hashlib,json
from pathlib import Path
def verify(root,manifest_path,expected_sha):
 p=Path(manifest_path);data=p.read_bytes()
 if hashlib.sha256(data).hexdigest()!=expected_sha:raise ValueError('BOOTSTRAP_MANIFEST_CHANGED')
 m=json.loads(data)
 for n,h in m['files'].items():
  p=Path(root)/n
  if hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('BOOTSTRAP_SOURCE_CHANGED:'+n)
 return m
