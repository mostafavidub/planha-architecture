"""JOINT367 geometry seam. Full replay binds core; no private check waiver."""
from fractions import Fraction as F
from contract114 import digest

def allowed_walls(model,core):
 if not isinstance(core,dict) or core.get('kind')!='COMPACT_CORE_SOUTH_LIFT_NOTCH367':return set()
 def exact(a,b):return tuple(map(F,a))==tuple(map(F,b))
 key='core.notch367.A_separator';n=core['notch367'];separator=n['new_separator']
 right=F(core['core_extent_x'][1]);y,Y=F(core['band'][1]),F(core['band'][3]);t=F('.15');lift=list(map(F,core['lift']));floor=list(map(F,n['new_A_floor_ownership']))
 if right-t!=lift[2] or floor[2]!=lift[2] or floor[1]!=y-t:raise ValueError('JOINT_EXTERIOR_SOURCE_GEOMETRY')
 for source in ('walls','wall_hosts','source_wall_hosts'):
  if not exact(model[source][key],separator):raise ValueError('JOINT_SEPARATOR_HOST_MISMATCH')
  if not exact(model[source]['core.lobby.outer_right'],[right-t,y-t,right,Y]):raise ValueError('JOINT_EXTERIOR_HOST_MISMATCH')
 if digest(model['common_spaces']['lobby'])!=digest(core['lobby']):raise ValueError('JOINT_COMMON_FRAME')
 if {u['id']for u in model['units']}!=set(core['unit_ownership']):raise ValueError('JOINT_UNIT_INVENTORY')
 for u in model['units']:
  if digest(u['ownership'])!=digest(core['unit_ownership'][u['id']]):raise ValueError('JOINT_OWNERSHIP_FRAME')
 return {key}

def checked_integrity(model,context,fn):
 from source_registry_joint367 import verify_context
 proof=verify_context(model,context)
 if not proof['verified']:raise ValueError('JOINT_LIVE_SOURCE_CONTEXT_REQUIRED')
 core=context.get('frame_core125');local=context.get('frame_local129')
 if digest(core)!=proof['proof']['core_digest'] or digest(local)!=proof['proof']['local_model_digest']:raise ValueError('JOINT_REPLAY_FRAME_BINDING')
 allowed_walls(model,core)
 return fn(model,frame_core=core,frame_local=local)
