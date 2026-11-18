"""Canonical index cached by exact manifest bytes; every read rechecks manifest and target."""
import json,hashlib,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
MANIFEST=W/'review388_preaudit/source_freeze.json'
_EXPECTED=None
_CACHE={}

def configure(expected):
 global _EXPECTED
 if _EXPECTED is not None and _EXPECTED!=expected:raise ValueError('FREEZE_CONTEXT_ALREADY_CONFIGURED')
 _EXPECTED=expected
 _index()

def _index():
 if _EXPECTED is None:raise ValueError('FREEZE_CONTEXT_REQUIRED')
 raw=MANIFEST.read_bytes();sha=hashlib.sha256(raw).hexdigest()
 if sha!=_EXPECTED:raise ValueError('FREEZE_CHANGED')
 if sha not in _CACHE:
  canonical={}
  for name,h in json.loads(raw)['files'].items():
   p=(W/name).resolve()
   if not p.is_relative_to(W.resolve()):raise ValueError('FROZEN_PATH_OUTSIDE_WORKSPACE')
   if p in canonical and canonical[p]!=h:raise ValueError('CONFLICTING_CANONICAL_PINS')
   canonical[p]=h
  _CACHE[sha]=(raw,canonical)
 cached,index=_CACHE[sha]
 if cached!=raw:raise ValueError('MANIFEST_BYTES_CHANGED')
 return index

def bytes_for(path):
 path=Path(path).resolve()
 if not path.is_relative_to(W.resolve()):raise ValueError('FROZEN_PATH_OUTSIDE_WORKSPACE')
 index=_index()
 if path not in index:raise ValueError('UNREGISTERED_FROZEN_DEPENDENCY:'+str(path.relative_to(W)))
 data=path.read_bytes()
 if hashlib.sha256(data).hexdigest()!=index[path]:raise ValueError('FROZEN_DEPENDENCY_CHANGED:'+str(path.relative_to(W)))
 return data

def read(path):return json.loads(bytes_for(path))
def module(path,name):
 path=Path(path);data=bytes_for(path);spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
 exec(compile(data,str(path),'exec'),m.__dict__);return m
