"""Bounded two-family proposal/pair orchestration. Pair enumeration is not diversity."""
import time
from copy import deepcopy
from contract114 import digest
from engine125 import validate_raw
from engine114 import revision,_eligible
from constructor127 import frame,build,context
from schedule127 import schedule,pairs,BUDGET
from search114 import propose
_GATE_CACHE127={}
def evaluate_current(packet,ctx):
 from evaluate_pair127 import evaluate
 key=(revision(),digest(packet),digest(ctx))
 if key not in _GATE_CACHE127:
  if len(_GATE_CACHE127)>=16:_GATE_CACHE127.pop(next(iter(_GATE_CACHE127)))
  _GATE_CACHE127[key]=deepcopy(evaluate(packet,ctx))
 return deepcopy(_GATE_CACHE127[key])

def run(raw,*,physical_evaluator=None,budget=None):
 validate_raw(raw);limits=dict(BUDGET,**(budget or {}));start=time.monotonic();rev=revision()
 result={'schema':'GENERAL127_PAIR_STUDY','raw':deepcopy(raw),'requested_count':raw['requested_count'],'candidates':[],'attempts':[],'pair_attempts':[],'internal_proposals':[],'budget':limits,'engine_revision':rev,'verified_architectural_diversity':False,'organization_count':0,'organization_shortfall':raw['requested_count'],'supported_programs':[2,1],'unsupported_programs':[3],'limits':['Objective variants are not distinct organizations.','Horizontal two-bedroom pair only; vertical private grouping unsupported.','LEFT_RIGHT world semantic inventory is currently proven for one bedroom only; unknown two-bedroom fields mean unsupported witness schema, not physical impossibility.','One-bedroom fallback does not establish capacity suitability.','Both ownership grammars considered, neither universally preferred.','Light and ventilation excluded.']}
 pool={};search_time=0;validation_time=0
 for item in schedule()[:limits['max_solver_calls']]:
  if search_time>=limits['search_checkpoint_seconds'] or time.monotonic()-start>=limits['total_checkpoint_seconds']:break
  attempt=dict(item);t=time.monotonic()
  if item['family']=='LEFT_RIGHT'and item['bedrooms']==2:
   attempt.update(status='UNSUPPORTED_WORLD_WITNESS_SCHEMA',solver_executed=False,seconds=0,not_global_infeasibility=True)
   result['attempts'].append(attempt);continue
  try:
   core,_=frame(raw,item['family']);roles=['double','twin']if item['bedrooms']==2 else['double']
   p=propose(core,item['bedrooms'],time_limit=limits['solver_seconds_per_call'],variant=item['variant'],sleep_roles=roles,topology=item['topology'],organization_profile=item['organization_profile'])
   attempt.update(status=p.get('status'),proposal=p)
   if p.get('status')=='PROPOSAL_ONLY':
    key=(item['family'],tuple(roles));group=pool.setdefault(key,[])
    if digest(p.get('rectangles'))not in [digest(q.get('rectangles'))for q in group]:group.append(p)
  except ValueError as ex:attempt.update(status='UNSUPPORTED_FAMILY_OR_PROGRAM',reason=str(ex),not_global_infeasibility=True)
  attempt['seconds']=time.monotonic()-t;search_time+=attempt['seconds'];result['attempts'].append(attempt)
 gates=0;assembly_time=0
 queues=[[(family,roles,group,i,j)for i,j in pairs(range(len(group)))]for (family,roles),group in pool.items()]
 while any(queues):
  if gates>=limits['max_full_gates']or validation_time>=limits['validation_checkpoint_seconds']or time.monotonic()-start>=limits['total_checkpoint_seconds']:break
  for queue in queues:
   if not queue:continue
   if gates>=limits['max_full_gates']or validation_time>=limits['validation_checkpoint_seconds']or time.monotonic()-start>=limits['total_checkpoint_seconds']:break
   family,roles,group,i,j=queue.pop(0);entry={'family':family,'sleep_roles':roles,'pair':[i,j]}
   try:
    t=time.monotonic()
    try:packet=build(raw,family,group[i],group[j])
    finally:assembly_time+=time.monotonic()-t
    ctx=context(raw,packet,{'A':group[i],'B':group[j]});entry.update(packet=packet,generation_context=ctx)
    if physical_evaluator is None:entry['status']='NO_ADMISSION_EVALUATOR_CONNECTED'
    else:
     t=time.monotonic();gates+=1
     try:g=physical_evaluator(packet,ctx)
     finally:validation_time+=time.monotonic()-t
     entry['gate']=g;entry['status']=g['status']
     if _eligible(g):result['candidates'].append({'model':packet['world_model'],'packet':packet,'generation_context':ctx,'gate':g})
   except Exception as ex:entry.update(status='PAIR_PIPELINE_ERROR',error_type=type(ex).__name__,reason=str(ex),not_global_infeasibility=True)
   result['internal_proposals'].append(entry);result['pair_attempts'].append({k:entry[k]for k in ('family','sleep_roles','pair','status')})
 result['assembly_seconds']=assembly_time
 result['unprocessed_pair_count']=sum(map(len,queues))
 result.update(admitted_count=len(result['candidates']),search_seconds=search_time,validation_seconds=validation_time,total_seconds=time.monotonic()-start,full_gate_calls=gates,status='PAIR_STUDY_NOT_SIX_ORGANIZATION_PROOF',source_unchanged=revision()==rev)
 return result

def select_scoped(candidates,requested):
 from program_selection127 import select
 proof=select(candidates,requested)
 return [candidates[i]for i in proof['selected_indices']],proof

def runtime(raw,budget_seconds=26):
 result=run(raw,physical_evaluator=evaluate_current,budget={'search_checkpoint_seconds':min(float(budget_seconds),26)})
 admitted=result['candidates'];selected,pool_proof=select_scoped(admitted,raw['requested_count']);n=len(selected)
 _,proof=select_scoped(selected,raw['requested_count'])
 result['pool_diversity_diagnostics']=pool_proof
 result['admitted_pool']=admitted
 result.update(candidates=selected,admitted_count=len(admitted),distinct_count=n,shortfall=raw['requested_count']-n,organization_count=n,organization_shortfall=raw['requested_count']-n,scoped_diversity=proof,status='LIMITED_DRAFT_SET'if n else'NO_ADMITTED_LAYOUT')
 return result

def check_candidate(c,raw):
 validate_raw(raw)
 if c['generation_context']['construction_trace']['raw']!=raw:raise ValueError('REQUEST_SOURCE_BINDING')
 if c['model']!=c['packet']['world_model']:raise ValueError('MODEL_PACKET_BINDING')
 g=evaluate_current(c['packet'],c['generation_context'])
 if not _eligible(g)or digest(g)!=digest(c['gate']):raise ValueError('FRESH_PAIR_GATE_BINDING')
 return c
