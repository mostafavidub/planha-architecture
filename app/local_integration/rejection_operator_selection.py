"""Task4.1 select a bounded existing operator from retained verified rejection evidence.
No proposal, constructor, repair, child generation or solver is invoked here.
"""
import copy,hashlib,inspect
from pathlib import Path
from front_rear_runtime_adapter import ROOT,source_audit,transport,ensure
from same_version_front_rear_contract import digest,ENGINE_REVISION
from live_program_scheduler import preflight,bind_completed
from current_four_decision import assemble
from explicit_pair_redirection import require_rejection,inventory
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def select(request,runtime,child,scheduler,decision,expected):
 values=[request,runtime,child,scheduler,decision];values=[transport(x)[0] for x in values]
 request,runtime,child,scheduler,decision=values;pin=digest(values)
 ensure(type(expected) is dict and set(expected)=={'request','runtime','child','scheduler','decision'},'SELECTION_RECEIPT_KEYS')
 for key,value in zip(('request','runtime','child','scheduler','decision'),values):ensure(expected[key]==digest(value),'SELECTION_RECEIPT:'+key)
 from producer_provenance import snapshot,require_unchanged
 paths=['app/local_integration/'+p for p in ('rejection_operator_selection.py','explicit_pair_redirection.py','live_program_scheduler.py','current_four_decision.py','candidate/four_seat_group_candidate.py')]
 snap=snapshot(ROOT,paths);audit=source_audit()
 for fn,name in ((require_rejection,'explicit_pair_redirection.py'),(inventory,'explicit_pair_redirection.py'),(assemble,'current_four_decision.py'),(bind_completed,'live_program_scheduler.py')):
  ensure(Path(inspect.getsourcefile(fn)).resolve()==(ROOT/'app/local_integration'/name).resolve(),'SELECTION_IMPORT_PATH')
 bind_completed(child,request,runtime,decision)
 pf=preflight(bytes.fromhex(request['body_hex']));ensure(pf['execution_ready'] is True,'SELECTED_CASE')
 ensure(digest(scheduler['preflight'])==digest(pf),'SCHEDULER_PUBLIC_BINDING')
 ensure(scheduler['source_integrity_verified'] is True and len(scheduler['attempts'])==1,'VERIFIED_SINGLE_ATTEMPT')
 attempt=scheduler['attempts'][0]
 ensure(attempt['receipt_verified'] is True and attempt['nonce']==request['nonce'],'ATTEMPT_RECEIPT')
 ensure(attempt['runtime_digest']==digest(runtime) and attempt['decision_digest']==digest(decision),'ATTEMPT_OUTPUT_BINDING')
 ensure(digest(scheduler['current_decision'])==digest(decision['decision']),'SCHEDULER_DECISION')
 ensure(all(scheduler[k] is False for k in AUTH),'SCHEDULER_AUTHORITY')
 rebuilt=assemble(runtime,decision['assessments'],{k:digest(v) for k,v in decision['assessments'].items()})
 ensure(digest(rebuilt)==digest(decision),'CURRENT_DECISION_REBUILD')
 report=runtime['reports']['physical'];model=runtime['packet']['world_model'];mh=digest(model)
 ensure(report['model_hash']==mh==runtime['model_digest']==decision['model_digest'],'SAME_PARENT_MODEL')
 ensure(digest(report)==runtime['report_digests']['physical']==decision['physical_digest'],'FULL_PHYSICAL_REPORT')
 require_rejection(report)
 ensure(runtime['reports']['replay']['verified'] is True and runtime['reports']['replay']['source_revision']==ENGINE_REVISION,'ORIGIN')
 profile=pf['binding']['program_registry'];ensure(profile['id']=='PROGRAM_2BED_V1','REGISTRY')
 protected={'inputs':copy.deepcopy(model['inputs']),'program':copy.deepcopy(model['program']),'profile':copy.deepcopy(model['profile']),
  'fixture_inventory':inventory(model),'core_digest':digest(runtime['packet']['core']),'unit_count':2}
 out={'schema':'SOURCE_BOUND_REJECTION_OPERATOR_SELECTION_V1','state':'EXISTING_OPERATOR_SELECTED_EXECUTION_NOT_STARTED',
  'parent_model_digest':mh,'parent_context_digest':digest(runtime['context']),'parent_attempt_id':attempt['attempt_id'],
  'public_request_digest':pf['public_envelope']['canonical_request_digest'],'programme_registry_digest':pf['binding']['program_registry_digest'],
  'full_physical_report':copy.deepcopy(report),'full_physical_digest':digest(report),'current_decision':copy.deepcopy(decision),
  'current_decision_digest':digest(decision),'protected':protected,'protected_digest':digest(protected),
  'selected_operator':{'id':'SOURCE_BOUND_GROUPED_GUEST_MOTION_V1','callable':'explicit_pair_redirection.redirect','source_file':'app/local_integration/explicit_pair_redirection.py',
   'candidate_source':'app/local_integration/candidate/four_seat_group_candidate.py','family':'FRONT_REAR','programme':'PROGRAM_2BED_V1',
   'diagnostic_internal_programme':{'bedrooms_per_unit':2},'internal_programme_origin':'Derived from approved registry and verified original public three-field request, never a hidden user input',
   'scope':'Existing exploratory grouped seating and actual guest-motion reservations; not production repair or new family',
   'reason':'Exact retained A/B guest_dining NO_CONNECTED_BODY_ROUTE under legacy whole-kitchen-exclusion physical profile',
   'variant_order_from_existing_source':[0,1,2],'solver_seconds_per_variant_from_existing_source':12,'existing_loop_check_seconds':100,
   'existing_loop_limit_is_outer_kill':False,'outer_kill_budget':'MUST_BE_BOUND_BY_EXECUTION_ADAPTER_TASK4_3',
   'execution_started':False,'child_generated':False,'production_repair_registered':False},
  'next_execution_requirements':['Revalidate exact parent provenance/rejection immediately before execution','Preserve programme/core/input/profile/exact fixture source inventory','Fresh child original replay/full physical/current four reports before decision','No child if source/identity/budget fails; retain actual rejection and partial evidence','No lower-bedroom fallback; lower programme is separate alternative','No filtered errors/pending or substitution of work-only route profile for original physical gate'],
  'not_claimed':['No guarantee selected operator will fix rejection','No current UNKNOWN resolved by selection','No exhaustive search, global infeasibility, quality winner or product admission'],
  'source_snapshot':snap,'historical_pending_preserved':copy.deepcopy(report['pending']),
  'operator_selection_uses_retained_fresh_runtime_evidence_not_new_evaluation':True,
  **{k:False for k in AUTH}}
 ensure(digest(values)==pin,'SELECTION_INPUT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SELECTION_SOURCE_CHANGED')
 out['integrity_verified']=True
 return out
