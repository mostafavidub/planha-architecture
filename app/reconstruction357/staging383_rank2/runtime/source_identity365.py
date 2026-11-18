"""Explicit versioned source equivalence; old pins and behavioral tests retained."""
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;CANONICAL=HERE.parents[1]/'planha_general150_runtime_work'
def replace_once(s,a,b):
 if s.count(a)!=1:raise ValueError('SOURCE_SHAPE_CHANGED')
 return s.replace(a,b)
def expected(name,original):
 s=original.decode()
 if name=='q11_boundary118.py':
  a=' from fractions import Fraction as F\n errors=[];verified=False'
  s=replace_once(s,a,' from source_registry365 import CurrentContext,verify_context\n if isinstance(context,CurrentContext):return verify_context(model,context)\n'+a)
 elif name=='circulation_frame148.py':
  a='  if not isinstance(context,dict):'
  s=replace_once(s,a,"  from source_registry365 import CurrentContext,verify_context\n  if isinstance(context,CurrentContext) and not verify_context(m,context)['verified']:raise ValueError('REGISTERED_CONTEXT_INVALID')\n"+a)
 elif name=='named_checks118.py':
  a="in('CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1','CONSTRUCTION_TRACE125_WORLD_V1','CONSTRUCTION_TRACE126_PAIR_V1','CONSTRUCTION_TRACE127_PAIR_V1'):"
  s=replace_once(s,a,"in('FINITE_PORTALS383_SOURCE_TRACE_V1','CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1','CONSTRUCTION_TRACE125_WORLD_V1','CONSTRUCTION_TRACE126_PAIR_V1','CONSTRUCTION_TRACE127_PAIR_V1'):")
  s=replace_once(s,"callbacks['circulation_functional_integrity']=lambda m:circulation_functional_integrity120(m,frame_core=workflow_context.get('frame_core125'),frame_local=workflow_context.get('frame_local129'))","callbacks['circulation_functional_integrity']=lambda m:__import__('notch_grammar365').checked_integrity(m,workflow_context,circulation_functional_integrity120)")
  a=' return callbacks\nfrom project_input_audit118'
  s=replace_once(s,a," callbacks['no_hidden_project_inputs']=lambda m:no_hidden_project_inputs(m,workflow_context=workflow_context)\n"+a)
 elif name=='core_circulation_scope118.py':
  s=replace_once(s," if m.get('frame_binding125'):\n  from frame_circulation125 import grammar as frame_grammar"," from notch_grammar365 import allowed_walls\n expected.update(allowed_walls(m,frame_core))\n if m.get('frame_binding125'):\n  from frame_circulation125 import grammar as frame_grammar")
 return s.encode()
def check_one(name,original,current,pin):
 if hashlib.sha256(original).hexdigest()!=pin:raise ValueError('CANONICAL_PIN_MISMATCH:'+name)
 if current!=expected(name,original):raise ValueError('UNREVIEWED_SOURCE_TRANSFORMATION:'+name)
 return {'file':name,'canonical_sha256':pin,'current_sha256':hashlib.sha256(current).hexdigest(),'relation':'EXACT_BYTES'if current==original else'EXPLICIT_PROVENANCE_SEAM_ONLY'}
def verify_identity(model,context,pins):
 from source_registry365 import verify_context
 proof=verify_context(model,context)
 if not proof['verified']:raise ValueError('LIVE_REGISTERED_SOURCE_REQUIRED')
 rows=[check_one(n,(CANONICAL/n).read_bytes(),(HERE/n).read_bytes(),p)for n,p in pins.items()]
 return {'scope':'REVIEWED_IDENTITY_FOR_RUNNING_UNCHANGED_INPUT_BEHAVIOR_CHECKS_NOT_LAYOUT_ADMISSION','rows':rows,'origin_model_hash':proof['proof']['model_hash']}
