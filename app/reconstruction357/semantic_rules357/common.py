"""Reconstructed evidence identity checks; never a fresh-execution attestation."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REGISTRY_NAME='method_registry.json'
CONTRACT='b286c31d09fd58b962e0af1a81ee0e5c79c43c17271c40580ff6ee5b7ce3a1ac'
def digest(v):
 return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def result(verdict='UNKNOWN',codes=None,evidence=None,missing=None):
 return dict(verdict=verdict,codes=codes or [],evidence=evidence or {},missing=missing or [])
def rows(model,raw):
 registry=json.loads((HERE/REGISTRY_NAME).read_text())
 # This manifest is pinned by the importing frozen engine, not caller supplied.
 for name,sha in registry['sources'].items():
  p=ROOT/name
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_CHANGED:'+name)
 h=digest(model)
 if type(raw)is not dict or raw.get('model_hash')!=h:raise ValueError('RAW_MODEL_BINDING')
 c=raw.get('rule_contract_evidence')
 if type(c)is not dict or c.get('model_hash')!=h or c.get('contract_hash')!=CONTRACT:raise ValueError('CONTRACT_MODEL_BINDING')
 rs=c.get('requirements')
 if type(rs)is not list:raise ValueError('REQUIREMENTS_LIST')
 out={}
 for r in rs:
  if type(r)is not dict or type(r.get('requirement_id'))is not str:raise ValueError('ROW_ID')
  k=r['requirement_id']
  if k in out:raise ValueError('DUPLICATE_REQUIREMENT')
  out[k]=r
  if r.get('method') is not None:
   if r.get('model_hash')!=h or r.get('contract_hash')!=CONTRACT:raise ValueError('ROW_MODEL_BINDING:'+k)
   if r['method']!=registry['methods'].get(k):raise ValueError('METHOD_BINDING:'+k)
  elif r.get('evidence') not in (None,{}) or r.get('status') in ('PASS_LIMITED','FAIL'):raise ValueError('UNBOUND_ROW_EVIDENCE:'+k)
 if set(out)!=set(registry['requirement_ids']):raise ValueError('REQUIREMENT_INVENTORY')
 return out

def registry_methods():
 """Fixed profile selected by internal dispatcher; not caller supplied methods."""
 registry=json.loads((HERE/REGISTRY_NAME).read_text())
 for name,sha in registry['sources'].items():
  p=ROOT/name
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_CHANGED:'+name)
 return registry['methods']
