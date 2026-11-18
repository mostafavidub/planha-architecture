"""Exact source geometry predicate for one additional source-bound wall."""
import importlib.util
from pathlib import Path
from fractions import Fraction as F
from contract114 import digest,WALL
ROOT=Path(__file__).resolve().parents[2]/'staging362_core_notch'
def module(name):
 spec=importlib.util.spec_from_file_location('_notch_geometry_'+name,ROOT/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def allowed_walls(model,core):
 if not isinstance(core,dict)or core.get('kind')!='COMPACT_CORE_SOUTH_LIFT_NOTCH362':return set()
 expected=module('core_variant362').core(*map(F,model['inputs'][:2]))
 if digest(core)!=digest(expected):raise ValueError('NOTCH_CORE_SOURCE_GEOMETRY_MISMATCH')
 key='core.notch362.A_separator';rect=core['notch362']['new_separator']
 for source in ('walls','wall_hosts','source_wall_hosts'):
  if model[source].get(key)!=rect:raise ValueError('NOTCH_SEPARATOR_SOURCE_HOST_MISMATCH')
 right=list(map(str,module('notch_frame362').outer_right(core,WALL)))
 def exact(a,b):return list(map(F,a))==list(map(F,b))
 for source in ('walls','wall_hosts','source_wall_hosts'):
  if not exact(model[source]['core.lobby.outer_right'],right):raise ValueError('NOTCH_EXTERIOR_JUNCTION_SOURCE_MISMATCH')
 if digest(model['common_spaces']['lobby'])!=digest(core['lobby']):raise ValueError('NOTCH_COMMON_FRAME_MISMATCH')
 for u in model['units']:
  if digest(u['ownership'])!=digest(core['unit_ownership'][u['id']]):raise ValueError('NOTCH_OWNERSHIP_FRAME_MISMATCH')
 return {key}

def checked_integrity(model,context,fn):
 from source_registry362 import verify_context
 if not verify_context(model,context)['verified']:raise ValueError('NOTCH_LIVE_SOURCE_CONTEXT_REQUIRED')
 return fn(model,frame_core=context.get('frame_core125'),frame_local=context.get('frame_local129'))
