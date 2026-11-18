"""One hierarchical six-person profile, then explicit bounded lower-program fallback."""
import time
from copy import deepcopy
from contract114 import digest,core_first
from engine114 import revision,_eligible
from engine125 import validate_raw
from coarse_master129 import propose
from constructor129 import build,context,frame
from program_selection130 import select
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
  return evaluate(p,envelope['workflow_context'])
 return _CACHE.evaluate(model,envelope,revision(),compute,force=force)
def select_scoped(cs,n):
 proof=select(cs,n);return [cs[i]for i in proof['selected_indices']],proof

def runtime(raw,budget_seconds=26):
 W,L,n,requested=validate_raw(raw);start=time.monotonic();rev=revision();search=assembly=validation=0;fullcalls=0
 r={'schema':'GENERAL130_RESPONSE_V1','raw':deepcopy(raw),'requested_count':requested,'engine_revision':rev,'candidates':[],'internal_proposals':[],'attempts':[],'admitted_pool':[],'verified_architectural_diversity':False,'limits':['Two ownership families with one restricted three-bedroom profile each, not six organizations.','All program priorities require actual-source inventory and complete current gate.','Three bedrooms/six occupants do not establish overall capacity suitability or quality.','Fallback2/1 retains its own pair trace; no transferred gate receipts.','Light and ventilation excluded.'],'budget':{'search_checkpoint_seconds':min(26,float(budget_seconds)),'max_full_gates':8,'validation_checkpoint_seconds':100,'total_checkpoint_seconds':135,'solver_seconds_per_call':3,'scope':'Start checkpoints, not in-flight cancellation or guaranteed hard wall time.'}}
 errors=[]
 for family in ('FRONT_REAR','LEFT_RIGHT'):
  attempt={'family':family,'program':['double','twin','twin'],'not_global_infeasibility':True}
  r['attempts'].append(attempt)
  if search>=r['budget']['search_checkpoint_seconds'] or validation>=100 or time.monotonic()-start>=135:
   attempt.update(status='NOT_ATTEMPTED_BUDGET_CHECKPOINT');errors.append(family+':BUDGET');continue
  try:
   core,_=frame(raw,family)
   if core is None:raise ValueError('CORE_METHOD_UNSUPPORTED')
   t=time.monotonic();p=propose(core,min(3,r['budget']['search_checkpoint_seconds']-search));dt=time.monotonic()-t;search+=dt
   attempt.update(status=p['status'],proposal=p,seconds=dt)
   if p['status']!='PROPOSAL_ONLY':errors.append(family+':'+p['status']);continue
   t=time.monotonic();packet=build(raw,family,p);ctx=context(raw,p,packet);dt=time.monotonic()-t;assembly+=dt;attempt['assembly_seconds']=dt
   t=time.monotonic();g=evaluate_current(packet,ctx);dt=time.monotonic()-t;validation+=dt;fullcalls+=1;attempt['validation_seconds']=dt
   e={'family':family,'packet':packet,'generation_context':ctx,'gate':g,'status':g['status'],'program':['double','twin','twin']};r['internal_proposals'].append(e)
   if _eligible(g):r['admitted_pool'].append({'model':packet['world_model'],'packet':packet,'generation_context':ctx,'gate':g})
   else:errors.append(family+':HIGHER_PROGRAM_WHOLE_GATE_NOT_ADMITTED')
  except Exception as ex:
   reason=type(ex).__name__+':'+str(ex);attempt.update(status='PIPELINE_ERROR',reason=reason);errors.append(family+':'+reason)
 error=errors
 if not r['admitted_pool']:
  r['fallback_reason']=error
  remaining={'search_checkpoint_seconds':max(0,min(26,float(budget_seconds))-search),'validation_checkpoint_seconds':max(0,100-validation),'total_checkpoint_seconds':max(0,135-(time.monotonic()-start)),'max_full_gates':8-fullcalls,'max_solver_calls':6}
  if all(remaining[k]>0 for k in ('search_checkpoint_seconds','validation_checkpoint_seconds','total_checkpoint_seconds','max_full_gates')):
   from engine127 import run as lower
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
