"""Bounded hybrid-study orchestrator. Proposals are not user-admitted plans."""
import json,time,hashlib
from pathlib import Path
from contract114 import parse,core_first,program,S,digest
from search114 import propose
from assemble114 import assemble
from checker114 import evaluate as _independent_evaluate
from gate_cache118 import GateCache
_GATE_CACHE=GateCache(limit=8)
from capacity_program118 import proposed_program
from schedule123 import requested_count,schedule,bind_runtime
from diversity124 import audit_batch

def revision():
 root=Path(__file__).parent
 files=[*root.glob('*.py'),*root.glob('*.json'),*(p for p in (root/'references').rglob('*')if p.is_file())]
 return digest({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)})

def generation_context(inputs,trace=None):
 root=Path(__file__).parent
 context={'operation':'generate_from_dimensions','inputs':inputs,'baseline_model_hash':None,'existing_plan_id':None,'source_files':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()for name in ('engine114.py','assemble114.py')}}
 if trace is not None:context['construction_trace']=trace
 return context

def _run_independent(model,context):
 return _independent_evaluate(model,workflow_context=context)

def evaluate(model,workflow_context=None,*,force=False):
 # Model generation/search is never cached here. Only the already computed,
 # same-source/context independent report may be reused for reopen/download.
 return _GATE_CACHE.evaluate(model,workflow_context,revision(),_run_independent,force=force)

def check_candidate(candidate,raw):
 W,L,n=parse(raw);m=candidate['model']
 if m['inputs']!=[S(W),S(L),n]:raise ValueError('INPUT_BINDING_MISMATCH')
 context=candidate.get('generation_context')
 if not isinstance(context,dict)or {k:v for k,v in context.items()if k!='construction_trace'}!=generation_context(m['inputs'])or not context.get('construction_trace'):raise ValueError('GENERATION_PROVENANCE_BINDING_MISMATCH')
 gate=evaluate(m,workflow_context=context)
 if (gate['status']!='PASS_CONCEPT_SCOPED_REVIEW' or gate.get('gate_scope')!='CONCEPT117_SOURCE_COMPAT_V1') or gate['errors'] or gate['pending'] or not gate.get('eligible_for_draft_export'):raise ValueError('INDEPENDENT_GATE_NOT_ADMITTED')
 result=dict(candidate,gate=gate)
 if candidate.get('gate')!=gate:raise ValueError('GATE_RECEIPT_CHANGED')
 return result

def _eligible(gate):
 return gate.get('status')=='PASS_CONCEPT_SCOPED_REVIEW' and gate.get('gate_scope')=='CONCEPT117_SOURCE_COMPAT_V1' and not gate.get('errors') and not gate.get('pending') and gate.get('eligible_for_draft_export',False)

def _geometry_identity(m):
 return digest({'inputs':m.get('inputs'),'units':[{k:u.get(k)for k in ('id','rooms','fixtures')}for u in m.get('units',[])],'walls':m.get('walls'),'openings':[{k:o.get(k)for k in ('id','rect','connects')}for o in m.get('openings',[])],'common_spaces':m.get('common_spaces'),'concept_windows':m.get('concept_windows')})

def _review_candidates(candidates):
 # A review preference, not a physical gate, regulation or optimality claim.
 from whole_circulation_compare119 import metrics,signature
 result={'scope':'Same-program fresh independently admitted drafts only; no global optimum or six-layout claim.','ranking_policy':'Prefer the shorter worst-unit actual serving route, then smaller worst-unit actual route-body union; engineering review preference only. All other route tradeoffs remain explicit.','comparisons':[]}
 if len(candidates)<2:
  result.update(status='SINGLE_VALID_DRAFT_NO_COMPARATIVE_QUALITY_PROOF',alternative_shortfall=1)
  return candidates,result
 a,b=candidates[:2]
 if signature(a['model'])!=signature(b['model']):
  result.update(status='PROGRAM_DIFFERENT_NOT_COMPARATIVELY_RANKED');return candidates,result
 ma,mb=metrics(a['model']),metrics(b['model'])
 if set(ma)!=set(mb):
  result.update(status='ROUTE_TARGETS_DIFFER_NO_COMPARATIVE_RANKING');return candidates,result
 def score(mm):
  return (max((v for k,v in mm.items()if 'kitchen_to_dining_floor' in k and k.endswith(':length')),default=0),max((v for k,v in mm.items()if k.endswith(':circulation_union')),default=0))
 if score(mb)<score(ma):a,b=b,a;ma,mb=mb,ma
 delta={k:ma[k]-mb[k]for k in ma}
 result.update(status='TWO_VALID_DRAFTS_WITH_DISCLOSED_TRADEOFFS',alternative_shortfall=0)
 result['comparisons'].append({'preferred_model_hash':digest(a['model']),'alternative_model_hash':digest(b['model']),'preferred_metrics':{k:str(v)for k,v in ma.items()},'alternative_metrics':{k:str(v)for k,v in mb.items()},'preferred_minus_alternative':{k:str(v)for k,v in delta.items()},'preferred_better':[k for k,v in delta.items()if v<0],'preferred_worse':[k for k,v in delta.items()if v>0],'globally_optimal':False,'all_preferences_satisfied':False})
 return [a,b]+candidates[2:],result

def run(raw,budget_seconds=15):
 started=time.monotonic();rev=revision()
 response={'schema':'GENERAL124_RESPONSE_V1','diversity_scope':'geometry-only; architectural organization uniqueness not independently verified','verified_architectural_diversity':False,'unverified_requested_organization_count':6,'requested_count':6,'admitted_count':0,'distinct_count':0,'shortfall':6,'candidates':[],'rejections':[],'program_assumptions':[],'search_evidence':{'budget_seconds':budget_seconds,'max_solver_calls':12,'per_call_budget_seconds':3,'budget_scope':'cumulative proposal preparation plus solver cap; at most twelve unique program/variant calls; per-call solver3s. Validation and total caps are derived from measured cost and requested count, and are admission-work start checkpoints, not interruptible hard timeouts.','search_seconds':0,'assembly_seconds':0,'validation_seconds':0,'attempts':[],'program_attempts':[]},'engine_revision':rev}
 try:W,L,n=parse(raw)
 except(ValueError,TypeError)as e:return dict(response,status='INVALID_INPUT',reason=str(e),total_seconds=time.monotonic()-started)
 requested=requested_count(raw);validation_cap=17.0*min(12,requested+2);total_cap=budget_seconds+21.0*min(12,requested+2);response.update(requested_count=requested,unverified_requested_organization_count=requested,shortfall=requested)
 response['input_exact']={'W':S(W),'L':S(L),'n':n};core=core_first(W,L)
 if core is None:return dict(response,status='NO_ADMITTED_LAYOUT',reason='CURRENT_CORE_TOPOLOGY_NOT_APPLICABLE_NOT_GLOBAL_INFEASIBILITY',total_seconds=time.monotonic()-started)
 try:pr=proposed_program(core,raw)
 except(ValueError,TypeError)as e:return dict(response,status='PROGRAM_UNRESOLVED',reason=str(e),total_seconds=time.monotonic()-started)
 attempts=schedule(pr);pr=bind_runtime(pr,attempts)
 response.update(program_assumptions=pr,core_assumptions=core['assumptions'],internal_proposals=[])
 response['search_evidence'].update(scheduled_attempts=attempts,validation_checkpoint_cap_seconds=validation_cap,total_checkpoint_cap_seconds=total_cap,validation_estimate_seconds_per_model=17.0,validation_estimate_source='case1 shared-side fresh gate 16.831s; empirical estimate not guarantee',max_solver_calls=len(attempts),max_full_gate_calls=min(12,requested+2),full_gate_calls=0)
 response['search_evidence']['programs_skipped_without_solver']=[{'bedrooms_per_unit':b,'reason':'CURRENT_THREE_BEDROOM_TOPOLOGY_NOT_OPERATIONALLY_INTEGRATED','not_global_infeasibility':True} for b in pr['bedroom_choices'] if b==3]
 choices=pr['runtime_supported_bedroom_counts']
 if not choices:return dict(response,status='PROGRAM_UNRESOLVED',reason='NO_RUNTIME_SUPPORTED_PROGRAM_IN_REQUESTED_CHOICES_THREE_BEDROOM_TOPOLOGY_PENDING_NOT_GLOBAL_CAP',total_seconds=time.monotonic()-started)
 seen=set();checked_geometry=set();last_reason='NO_ATTEMPT_WITHIN_BUDGET'
 for scheduled in attempts:
  if audit_batch(response['candidates'],requested)['distinct_count']>=requested:
   last_reason='REQUESTED_GEOMETRIC_CANDIDATE_TARGET_REACHED_NOT_ARCHITECTURAL_PROOF';break
  if time.monotonic()-started>=total_cap or response['search_evidence']['validation_seconds']>=validation_cap or response['search_evidence']['full_gate_calls']>=response['search_evidence']['max_full_gate_calls']:
   last_reason='VALIDATION_OR_TOTAL_CHECKPOINT_BUDGET_EXHAUSTED';break
  bedrooms=scheduled['bedrooms'];variant=scheduled['variant']
  remaining=budget_seconds-response['search_evidence']['search_seconds']
  if remaining<=0:
   last_reason='CUMULATIVE_SEARCH_BUDGET_EXHAUSTED';break
  if revision()!=rev:raise ValueError('SOURCE_CHANGED_DURING_GENERATION')
  t=time.monotonic();p=propose(core,bedrooms,time_limit=min(3,max(.05,remaining)),variant=variant,sleep_roles=pr['sleep_roles_by_count'][str(bedrooms)],ordered_macro=False,topology=scheduled['topology']);response['search_evidence']['search_seconds']+=time.monotonic()-t
  response['search_evidence']['attempts'].append(p)
  pa={'bedrooms_per_unit':bedrooms,'sleep_roles':pr['sleep_roles_by_count'][str(bedrooms)],'unit_count_unchanged':n,'variant':variant,'organization_topology':scheduled['topology'],'proposal_status':p['status'],'fresh_search':True};response['search_evidence']['program_attempts'].append(pa)
  eligible=False;shared_pending=False
  if 'rectangles'not in p:
   last_reason='SEARCH_TIMEOUT_NO_WITNESS'if 'TIMEOUT'in str(p)else'NO_PROPOSAL_IN_CURRENT_TOPOLOGY'
   response['rejections'].append({'stage':'SEARCH','program':pa,'details':p})
  else:
   t=time.monotonic()
   try:m=assemble(W,L,core,p)
   except ValueError as e:
    response['search_evidence']['assembly_seconds']+=time.monotonic()-t;response['rejections'].append({'stage':'PRIVATE_MODULE_OR_ASSEMBLY','program':pa,'reason':str(e)});last_reason='ASSEMBLY_REJECTED'
   else:
    response['search_evidence']['assembly_seconds']+=time.monotonic()-t
    if revision()!=rev:raise ValueError('SOURCE_CHANGED_DURING_GENERATION')
    geometry_key=_geometry_identity(m)
    if geometry_key in checked_geometry:
     response['rejections'].append({'stage':'DUPLICATE_GEOMETRY_BEFORE_GATE','program':pa});continue
    checked_geometry.add(geometry_key)
    if time.monotonic()-started>=total_cap:
     last_reason='TOTAL_CHECKPOINT_BUDGET_BEFORE_GATE';break
    response['search_evidence']['full_gate_calls']+=1
    trace={'schema':'CONSTRUCTION_TRACE118_V1','raw':dict(raw),'core':core,'proposal':p,'model_hash':digest(m),'source_revision':rev};context=generation_context(m['inputs'],trace)
    t=time.monotonic();gate=evaluate(m,workflow_context=context);response['search_evidence']['validation_seconds']+=time.monotonic()-t
    if revision()!=rev:raise ValueError('SOURCE_CHANGED_DURING_GENERATION')
    eligible=_eligible(gate);shared_pending=not gate['errors']and bool(gate['pending'])
    pa.update(gate_status=gate['status'],mandatory_error_count=len(gate['errors']),mandatory_pending_count=len(gate['pending']))
    response['internal_proposals'].append({'model':m,'gate':gate,'generation_context':context,'not_for_admitted_export':not eligible})
    if eligible:
     key=_geometry_identity(m)
     if key not in seen:
      seen.add(key);response['candidates'].append({'model':m,'gate':gate,'generation_context':context,'eligible_for_draft_export':True,'accepted':False,'release':False})
     else:response['rejections'].append({'stage':'DUPLICATE_ACTUAL_MODEL','program':pa})
     last_reason='LIMITED_CONCEPT_DRAFT_NOT_FINAL_ACCEPTANCE'
    else:
     last_reason='MANDATORY_EVIDENCE_PENDING'if shared_pending else'INDEPENDENT_PHYSICAL_OR_NAMED_REJECTION'
     response['rejections'].append({'stage':'WHOLE_MODEL_GATE','program':pa,'status':gate['status'],'errors':gate['errors'],'pending':gate['pending'],'route_failures':m.get('route_failures',[])})
 pool=response['candidates'];pool_audit=audit_batch(pool,requested)
 response['geometric_candidate_count']=len(pool)
 response['organization_pool_evidence']=pool_audit
 # One supported program at a time. Never add different capacity programs to six.
 groups=pool_audit['program_groups']
 chosen=max(groups,key=lambda g:g['distinct_count'])['representative_indices'][:requested] if groups else []
 response['candidates']=[pool[i] for i in chosen]
 response['nonselected_physical_candidate_count']=len(pool)-len(chosen)
 response['candidates'],response['circulation_review']=_review_candidates(response['candidates'])
 for c in response['candidates']:c['circulation_review']=response['circulation_review']
 count=len(response['candidates']);response.update(admitted_count=len(pool),distinct_count=count,shortfall=requested-count,status='LIMITED_DRAFT_SET'if count else'SEARCH_TIMEOUT_NO_WITNESS'if last_reason=='SEARCH_TIMEOUT_NO_WITNESS'else'NO_ADMITTED_LAYOUT')
 da=audit_batch(response['candidates'],requested)
 response.update(organization_diversity=da,organization_count=da['distinct_count'],organization_shortfall=da['shortfall'],geometric_shortfall=max(0,requested-len(pool)))
 response['search_evidence']['stop_reason']=last_reason
 response['search_evidence']['attempted_profile_count']=len(response['search_evidence']['attempts'])
 response['search_evidence']['unattempted_profile_count']=len(attempts)-len(response['search_evidence']['attempts'])
 response['search_evidence']['not_proven_infeasible_by_unattempted_or_timeout']=True
 response['total_seconds']=time.monotonic()-started
 return response
