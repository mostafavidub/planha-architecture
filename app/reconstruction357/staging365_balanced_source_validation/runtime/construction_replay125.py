"""Origin-only replay of dimensions/proposal. Never trusts a geometry receipt."""
import copy,hashlib
from pathlib import Path
from contract114 import digest,parse
from construction_replay118 import source_revision
_CACHE={}
def verify(model,context):
 errors=[];pending=[]
 try:
  t=context['construction_trace'];rev=source_revision()
  if t['schema']!='CONSTRUCTION_TRACE125_WORLD_V1':raise ValueError('TRACE_SCHEMA')
  if context.get('operation')!='generate_from_dimensions'or context.get('existing_plan_id')is not None or context.get('baseline_model_hash')is not None:raise ValueError('NOT_NEW_DIMENSION_REQUEST')
  raw=t['raw']
  if any(k in raw for k in ('model','existing_plan_id','baseline_model_hash','previous_model','candidate')):raise ValueError('PREVIOUS_PLAN_INPUT')
  if rev!=t['source_revision']or digest(model)!=t['model_hash']:raise ValueError('REVISION_OR_MODEL_HASH')
  for n in ('engine114.py','assemble114.py','constructor125.py','frame_contract125.py','common_core125.py','world_transform125.py'):
   if context['source_files'][n]!=hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest():raise ValueError('SOURCE_FILE:'+n)
  key=(rev,digest(t))
  if key not in _CACHE:
   from constructor125 import build
   p=build(copy.deepcopy(raw),copy.deepcopy(t['proposal']))
   if digest(p['world_model'])!=digest(model)or digest(p['local_model'])!=t['local_model_hash']or digest(p['core'])!=t['core_hash']:raise ValueError('EXACT_REPLAY_MISMATCH')
   _CACHE[key]=True
 except (KeyError,ValueError,TypeError)as ex:errors.append({'code':'WORLD_CONSTRUCTION_REPLAY','detail':str(ex)})
 return dict(verified=not errors,errors=errors,pending=pending,model_hash=digest(model),scope='Origin only; deterministic replay without solver; no physical approval')
