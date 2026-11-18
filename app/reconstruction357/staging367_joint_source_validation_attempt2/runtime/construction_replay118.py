"""Provenance-only deterministic replay, NEVER a geometry acceptance oracle.
No search or solver call. Independent physical and named-rule gates remain.
Cache holds only exact source+trace+model matches in this process, not receipts.
"""
from pathlib import Path
from fractions import Fraction
import hashlib,json,copy
_CACHE={}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def source_revision():
 root=Path(__file__).parent
 files=[*root.glob('*.py'),*root.glob('*.json'),*(p for p in(root/'references').rglob('*')if p.is_file())]
 return digest({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)})
def verify(model,context):
 errors=[];pending=[];trace=context.get('construction_trace')if isinstance(context,dict)else None
 if not isinstance(trace,dict):return {'verified':False,'errors':[],'pending':['Q11_CONSTRUCTION_TRACE_MISSING']}
 rev=source_revision();mh=digest(model);key=(rev,mh,digest(trace))
 if key in _CACHE:return copy.deepcopy(_CACHE[key])
 if trace.get('schema')!='CONSTRUCTION_TRACE118_V1':errors.append({'code':'CONSTRUCTION_TRACE_SCHEMA'})
 if trace.get('source_revision')!=rev:errors.append({'code':'CONSTRUCTION_SOURCE_REVISION_CHANGED'})
 if trace.get('model_hash')!=mh:errors.append({'code':'CONSTRUCTION_MODEL_HASH_CHANGED'})
 raw=trace.get('raw')
 if not isinstance(raw,dict)or any(k in raw for k in('model','existing_plan_id','baseline_model_hash','previous_model','candidate')):errors.append({'code':'REVISION_INPUT_NOT_DIMENSIONS_ONLY'})
 if errors:return {'verified':False,'errors':errors,'pending':pending}
 try:
  from contract114 import parse,core_first
  from assemble114 import assemble
  W,L,n=parse(raw)
  if [Fraction(str(x))for x in model['inputs']]!=[W,L,n]:raise ValueError('EXACT_INPUT_MISMATCH')
  core=core_first(W,L)
  if digest(core)!=digest(trace['core']):raise ValueError('CORE_WORKFLOW_MISMATCH')
  actual=assemble(W,L,copy.deepcopy(trace['core']),copy.deepcopy(trace['proposal']))
  if digest(actual)!=mh:raise ValueError('DETERMINISTIC_ASSEMBLY_MODEL_MISMATCH')
 except (KeyError,ValueError,TypeError,IndexError)as e:errors.append({'code':'CONSTRUCTION_REPLAY_MISMATCH','detail':str(e)})
 result={'verified':not errors,'errors':errors,'pending':pending,'model_hash':mh,'trace_hash':key[2],'source_revision':rev,'scope':'Same dimensions/core/proposal deterministic constructor replay only; no solver and no transfer of geometry or architectural PASS'}
 if result['verified']:_CACHE[key]=copy.deepcopy(result)
 return result
