"""One hierarchical six-person profile, then explicit bounded lower-program fallback."""
import time
from copy import deepcopy
from contract114 import digest,core_first
from engine114 import revision,_eligible
from engine125 import validate_raw
from coarse_master129 import propose
from coarse_l3_master131 import propose as propose_l3
from coarse_access_master132 import propose as propose_access
from coarse_t_master133 import propose as propose_t
from coarse_t_connected134 import propose as propose_t_connected
from coarse_sidecar_seating136 import propose as propose_sidecar_protected
from coarse_sidecar_group138 import propose as propose_group
from shared_gate140 import require_runtime_group_proposal, ROOT_MARKER, GROUP_MARKER
from shared_gate145 import apply_shared_gate
from seating_binding142 import MARKER as COMPACT_MARKER
from nonseating144 import require as validate_compact
from coarse_sidecar_circulation144 import propose as propose_compact
from coarse_sidecar_rooted139 import propose as propose_rooted
from constructor129 import build,context,frame
from program_selection145 import select
from gate_cache118 import GateCache
_CACHE=GateCache(limit=16)
def evaluate_current(packet,ctx,*,force=False):
 schema=ctx.get('construction_trace',{}).get('schema')
 if schema=='CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1':
  from evaluate_hierarchical129 import evaluate
 elif schema=='CONSTRUCTION_TRACE127_PAIR_V1':
  from evaluate_pair127 import evaluate
 else:raise ValueError('UNSUPPORTED_GENERATION_TRACE')
 model=packet.get('model',packet.get('world_model'))
 envelope={'gate_kind':schema,'packet':packet,'workflow_context':ctx}
 def compute(actual,envelope):
  p=envelope['packet']
  if p.get('model',p.get('world_model'))!=actual:raise ValueError('CACHE_PACKET_MODEL_BINDING')
  return apply_shared_gate(p,envelope['workflow_context'],evaluate(p,envelope['workflow_context']))
 return _CACHE.evaluate(model,envelope,revision(),compute,force=force)
def select_scoped(cs,n):
 proof=select(cs,n);return [cs[i]for i in proof['selected_indices']],proof

def compact_policy(attempts):
 # Only explicit restricted-master NO_PROPOSAL is eligible, never timeout,
 # exception, rejected geometry, unsupported fit or whole-gate rejection.
 prior={a['organization']:a for a in attempts}
 return all(prior.get(k,{}).get('status')=='NO_PROPOSAL_IN_THIS_RESTRICTED_MASTER'for k in ('SIDECAR_ROOTED139','SIDECAR_GROUP138'))

def runtime(raw,budget_seconds=26):
 W,L,n,requested=validate_raw(raw);start=time.monotonic();rev=revision();search=assembly=validation=0;fullcalls=0
 r={'schema':'GENERAL145_EXPERIMENTAL_RESPONSE_V1','raw':deepcopy(raw),'requested_count':requested,'engine_revision':rev,'candidates':[],'internal_proposals':[],'attempts':[],'admitted_pool':[],'verified_architectural_diversity':False,'limits':['Right-rooted source group, then source-fixed opposing group (both 2-body shared band), then protected seating sidecar in LEFT_RIGHT, plus row organization in two ownership families and connected-service T134 and T133, L3 and ACCESS in LEFT_RIGHT only; optional compact D4 fallback only after both explicit restricted-master NO_PROPOSAL outcomes; at most ten hierarchy attempt records under the unchanged eight-gate cap; skipped attempts explicitly recorded, not six guaranteed organizations.','Compact144 is experimental and requires source-bound local/world nonseating receipts; no guarantee of new organization, superior overall quality or six layouts. Runtime order is not a quality endorsement; actual runtime comparison remains required.','All program priorities require actual-source inventory and complete current gate.','Three bedrooms/six occupants do not establish overall capacity suitability or quality.','Fallback2/1 retains its own pair trace; no transferred gate receipts.','Light and ventilation excluded.'],'budget':{'search_checkpoint_seconds':min(26,float(budget_seconds)),'max_full_gates':8,'validation_checkpoint_seconds':500,'total_checkpoint_seconds':600,'solver_seconds_per_call':3,'scope':'Start checkpoints, not in-flight cancellation or guaranteed hard wall time.'}}
 errors=[]
 for organization,family in (('SIDECAR_ROOTED139','LEFT_RIGHT'),('SIDECAR_GROUP138','LEFT_RIGHT'),('SIDECAR_COMPACT144','LEFT_RIGHT'),('SIDECAR_PROTECTED','LEFT_RIGHT'),('TURN_T_CONNECTED','LEFT_RIGHT'),('TURN_T','LEFT_RIGHT'),('ACCESS','LEFT_RIGHT'),('L3','LEFT_RIGHT'),('ROW','FRONT_REAR'),('ROW','LEFT_RIGHT')):
  roles=['twin','twin','double']if organization=='L3'else['double','twin','twin']
  attempt={'organization':organization,'family':family,'program':roles,'not_global_infeasibility':True}
  r['attempts'].append(attempt)
  if organization=='SIDECAR_COMPACT144' and not compact_policy(r['attempts']):
   attempt.update(status='NOT_SCHEDULED_POLICY',reason='COMPACT_REQUIRES_BOTH_EXPLICIT_RESTRICTED_MASTER_NO_PROPOSAL');continue
  if fullcalls>=r['budget']['max_full_gates'] or search>=r['budget']['search_checkpoint_seconds'] or validation>=500 or time.monotonic()-start>=600:
   attempt.update(status='NOT_ATTEMPTED_BUDGET_CHECKPOINT');errors.append(family+':BUDGET');continue
  try:
   core,_=frame(raw,family)
   if core is None:raise ValueError('CORE_METHOD_UNSUPPORTED')
   t=time.monotonic()
   try:
    allowance=min(3,r['budget']['search_checkpoint_seconds']-search)
    if organization=='SIDECAR_ROOTED139':p=propose_rooted(core,allowance,gap_bodies=2)
    elif organization=='SIDECAR_GROUP138':p=propose_group(core,allowance,gap_bodies=2)
    elif organization=='SIDECAR_COMPACT144':p=propose_compact(core,allowance)
    else:p=(propose_sidecar_protected if organization=='SIDECAR_PROTECTED'else propose_t_connected if organization=='TURN_T_CONNECTED'else propose_t if organization=='TURN_T'else propose_access if organization=='ACCESS'else propose_l3 if organization=='L3'else propose)(core,allowance)
   finally:dt=time.monotonic()-t;search+=dt;attempt['seconds']=dt
   attempt.update(status=p['status'],proposal=p,seconds=dt)
   if p['status']!='PROPOSAL_ONLY':errors.append(family+':'+p['status']);continue
   if organization in ('SIDECAR_ROOTED139','SIDECAR_GROUP138'):require_runtime_group_proposal(p,expected_marker=ROOT_MARKER if organization=='SIDECAR_ROOTED139'else GROUP_MARKER,core=core)
   if organization=='SIDECAR_COMPACT144':
    if p.get('generation_method')!=COMPACT_MARKER:raise ValueError('COMPACT145_DISPATCH_MARKER_REQUIRED')
    validate_compact(p)
   t=time.monotonic()
   try:packet=build(raw,family,p);ctx=context(raw,p,packet)
   finally:dt=time.monotonic()-t;assembly+=dt;attempt['assembly_seconds']=dt
   if fullcalls>=r['budget']['max_full_gates']or validation>=500 or time.monotonic()-start>=600:
    attempt.update(status='NOT_ADMITTED_GATE_BUDGET_CHECKPOINT');errors.append(family+':GATE_BUDGET');continue
   t=time.monotonic();fullcalls+=1
   try:g=evaluate_current(packet,ctx)
   finally:dt=time.monotonic()-t;validation+=dt;attempt['validation_seconds']=dt
   e={'organization':organization,'family':family,'packet':packet,'generation_context':ctx,'gate':g,'status':g['status'],'program':roles};r['internal_proposals'].append(e)
   if _eligible(g):r['admitted_pool'].append({'model':packet['world_model'],'packet':packet,'generation_context':ctx,'gate':g})
   else:errors.append(family+':HIGHER_PROGRAM_WHOLE_GATE_NOT_ADMITTED')
  except Exception as ex:
   reason=type(ex).__name__+':'+str(ex);attempt.update(status='PIPELINE_ERROR',reason=reason);errors.append(family+':'+reason)
 error=errors
 if not r['admitted_pool']:
  r['fallback_reason']=error
  remaining={'search_checkpoint_seconds':max(0,min(26,float(budget_seconds))-search),'validation_checkpoint_seconds':max(0,500-validation),'total_checkpoint_seconds':max(0,600-(time.monotonic()-start)),'max_full_gates':8-fullcalls,'max_solver_calls':6}
  if all(remaining[k]>0 for k in ('search_checkpoint_seconds','validation_checkpoint_seconds','total_checkpoint_seconds','max_full_gates')):
   from engine_pair135 import run as lower
   f=lower(raw,physical_evaluator=evaluate_current,budget=remaining);r['fallback_evidence']=f;r['attempts']+=f['attempts'];r['internal_proposals']+=f['internal_proposals'];r['admitted_pool']+=f['candidates'];search+=f['search_seconds'];assembly+=f['assembly_seconds'];validation+=f['validation_seconds'];fullcalls+=f['full_gate_calls']
  else:r['fallback_not_attempted']='SHARED_BUDGET_EXHAUSTED'
 else:r['lower_programs_not_attempted']='HIGHER_SUPPORTED_SOURCE_PROGRAM_ADMITTED; not evidence of optimal capacity or six organizations'
 selected,proof=select_scoped(r['admitted_pool'],requested);_,sp=select_scoped(selected,requested);count=len(selected)
 r.update(candidates=selected,admitted_count=len(r['admitted_pool']),distinct_count=count,shortfall=requested-count,organization_count=count,organization_shortfall=requested-count,pool_diversity_diagnostics=proof,scoped_diversity=sp,status='LIMITED_DRAFT_SET'if count else'NO_ADMITTED_LAYOUT',search_seconds=search,assembly_seconds=assembly,validation_seconds=validation,full_gate_calls=fullcalls,total_seconds=time.monotonic()-start,source_unchanged=revision()==rev)
 if not r['source_unchanged']:raise ValueError('SOURCE_CHANGED_DURING_GENERATION')
 return r

def check_candidate(c,raw):
 validate_raw(raw);ctx=c['generation_context'];packet=c['packet'];m=packet.get('model',packet.get('world_model'))
 if c['model']!=m or ctx['construction_trace']['raw']!=raw:raise ValueError('MODEL_REQUEST_PACKET_BINDING')
 g=evaluate_current(packet,ctx)
 if not _eligible(g)or digest(g)!=digest(c['gate']):raise ValueError('FRESH_GATE_RECEIPT_BINDING')
 return c
