"""AP07 bounded ordering policy, not exhaustive search or quality selection.
Pure policy records. No geometry execution and no implicit programme repair.
"""
import copy
from program_profile_registry import lookup
from same_version_front_rear_contract import digest
STAGES=('CORE','SPLIT','PLACEMENT','OPTIONAL_NONBED_MERGE')
STATES=('ATTEMPTED_NO_WITNESS','ATTEMPTED_WITH_WITNESS','TIMED_OUT','NOT_IMPLEMENTED','NOT_ENUMERATED','NOT_APPLICABLE')
def policy():
 return {'schema':'BOUNDED_AP07_ORDER_POLICY_V1','stage_order':list(STAGES),
  'source':{'document_id':'17X8Q5nsiFBmJqAodCQpIfewsDIUeP5eosc3D72ALi3s','tab_id':'t.jgj9urck6sd','start_index':39358,'end_index':39692},
  'budget_source':{'tab_id':'t.jgj9urck6sd','start_index':38709,'end_index':39126},
  'exhaustive_required':False,'budget_reset_on_transition':False,
  'order_is_quality_ranking':False,'no_witness_is_infeasible':False,
  'stage_slots_are_engineering_coverage':True,'fixed_unit_count':2,
  'minimum_bedrooms':1,'accepted':False,'qualified':False,'delivery_allowed':False}
def stage_record(stage,state,reason,attempt_ids=()):
 if type(stage) is not str or stage not in STAGES:raise ValueError('STAGE')
 if type(state) is not str or state not in STATES:raise ValueError('STAGE_STATE')
 if type(reason) is not str or not reason.strip():raise ValueError('REASON_REQUIRED')
 if type(attempt_ids) not in (list,tuple) or any(type(x) is not str or not x for x in attempt_ids) or len(set(attempt_ids))!=len(attempt_ids):raise ValueError('ATTEMPT_IDS')
 if state.startswith('ATTEMPTED') or state=='TIMED_OUT':
  if not attempt_ids:raise ValueError('ATTEMPT_EVIDENCE_REQUIRED')
 elif attempt_ids:raise ValueError('NONATTEMPT_WITH_ATTEMPT_IDS')
 return {'stage':stage,'state':state,'reason':reason,'attempt_ids':list(attempt_ids)}
def lower_program_transition(from_id,to_id,records,*,unit_count,budget_ledger):
 if type(unit_count) is not int or unit_count!=2:raise ValueError('UNIT_COUNT_LOCK')
 before=lookup(from_id);after=lookup(to_id)
 if any(p['approval']['status']!='APPROVED_DESIGN_PROGRAM' for p in (before,after)):raise ValueError('UNAPPROVED_PROGRAM')
 if after['bedrooms_per_unit']!=before['bedrooms_per_unit']-1 or after['bedrooms_per_unit']<1:raise ValueError('LOWER_PROGRAM_ADJACENCY')
 if type(records) is not list or len(records)!=len(STAGES):raise ValueError('STAGE_DISPOSITIONS_REQUIRED')
 normalized=[]
 for expected,row in zip(STAGES,records):
  if type(row) is not dict or set(row)!={'stage','state','reason','attempt_ids'} or row['stage']!=expected:raise ValueError('STAGE_ORDER')
  normalized.append(stage_record(row['stage'],row['state'],row['reason'],row['attempt_ids']))
 ids=[i for row in normalized for i in row['attempt_ids']]
 if len(ids)!=len(set(ids)):raise ValueError('ATTEMPT_DOUBLE_COUNT')
 # Budget account is caller-owned evidence, not new allocation or reset.
 if type(budget_ledger) is not dict or set(budget_ledger)!={'account_id','limit_attempts','used_attempts','limit_seconds','used_seconds'}:raise ValueError('BUDGET_LEDGER')
 if type(budget_ledger['account_id']) is not str or not budget_ledger['account_id']:raise ValueError('BUDGET_ACCOUNT')
 import math
 for k in ('limit_attempts','used_attempts'):
  if type(budget_ledger[k]) is not int or budget_ledger[k]<0:raise ValueError('BUDGET_INTEGER')
 for k in ('limit_seconds','used_seconds'):
  if type(budget_ledger[k]) not in (int,float) or not math.isfinite(budget_ledger[k]) or budget_ledger[k]<0:raise ValueError('BUDGET_FINITE')
 if budget_ledger['used_attempts']>budget_ledger['limit_attempts'] or budget_ledger['used_seconds']>budget_ledger['limit_seconds']:raise ValueError('BUDGET_OVERRUN')
 if len(ids)>budget_ledger['used_attempts']:raise ValueError('ATTEMPT_BUDGET_MISMATCH')
 available=budget_ledger['used_attempts']<budget_ledger['limit_attempts'] and budget_ledger['used_seconds']<budget_ledger['limit_seconds']
 return {'schema':'AP07_NEW_PROGRAM_TRANSITION_V1','from_program':from_id,'to_program':to_id,
  'from_registry_digest':digest(before),'to_registry_digest':digest(after),
  'unit_count':unit_count,'stage_dispositions':normalized,
  'state':'NEW_ALTERNATIVE_RECORDED_ADAPTER_NOT_READY',
  'reason':'Bounded preceding-stage dispositions are explicit; unenumerated or unimplemented branches are not an exhaustive-search demand.',
  'programme_repair':False,'new_programme_alternative':True,
  'prior_programme_infeasible':False,'quality_winner':False,
  'budget_ledger':copy.deepcopy(budget_ledger),'budget_ledger_digest':digest(budget_ledger),
  'budget_remaining_for_study':available,'budget_reset':False,
  'execution_ready':False,'execute_lower_program':False,
  'adapter_status':after['execution_readiness']['status'],
  'authorization_scope':'Study-policy record only; adapter readiness and same-version execution contract still required.',
  'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
