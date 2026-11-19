"""Additive historical status taxonomy, never architectural qualification.
Preserves exact producer outcomes/codes/attempt states. Unknown evidence stays
UNKNOWN; zero candidates never proves global geometric infeasibility.
"""
from copy import deepcopy
TOP={'INVALID_INPUT':'INVALID_INPUT','UNSUPPORTED':'UNSUPPORTED','EXECUTION_TIMEOUT':'TIMEOUT',
     'CANCELLED':'CANCELLED','EXECUTION_ERROR':'EXECUTION_ERROR','DEPENDENCY_UNAVAILABLE':'DEPENDENCY_UNAVAILABLE',
     'INVALID_REPAIR_SOURCE':'INVALID_INPUT','INVALID_EXPLICIT_REDIRECTION_SOURCE':'INVALID_INPUT'}
CANDIDATE={'REJECTED_PHYSICAL':'REJECTED','UNKNOWN_REVIEW':'UNKNOWN','PHYSICAL_PASS_SEMANTIC_UNKNOWN':'UNKNOWN'}
NO_PROPOSAL={'NO_PROPOSAL_IN_THIS_RESTRICTED_MASTER','NO_PROPOSAL_IN_THIS_TOPOLOGY','NO_PROPOSAL_IN_THIS_PROGRAM',
             'FIXED_WITNESS_CONSTRAINT_REJECTED','ROUNDED_PROPOSAL_REJECTED'}
TIMEOUT={'TIMEOUT_NO_WITNESS','SEARCH_TIMEOUT_NO_WITNESS'}
UNSUPPORTED={'UNSUPPORTED_BUNDLE_FIT','UNSUPPORTED_CURRENT_CORE_FIT','UNSUPPORTED_CURRENT_SOURCE_RECORD_SCHEMA'}
CONSTRUCTED={'CONSTRUCTED_AND_FRESHLY_REVIEWED','CONSTRUCTED_AND_FRESHLY_REVIEWED_EXPLICIT_PROGRAM'}
SKIPPED={'NOT_ATTEMPTED_REQUESTED_COUNT_REACHED','NOT_ATTEMPTED_BUDGET'}

def summarize(result,candidate_rows):
    if type(result)is not dict or type(candidate_rows)is not list:raise ValueError('HISTORY_STATUS_SCHEMA')
    if result.get('accepted')is not False or result.get('delivery_allowed')is not False:raise ValueError('HISTORY_STATUS_AUTHORITY')
    if 'qualified_count'in result and (type(result['qualified_count'])is not int or result['qualified_count']!=0):raise ValueError('HISTORY_STATUS_UNREGISTERED_QUALIFIED')
    outcome=result.get('outcome')
    if type(outcome)is not str or outcome not in set(TOP)|{'EXPERIMENT_COMPLETED'}:raise ValueError('HISTORY_STATUS_UNKNOWN_OUTCOME')
    attempts=result.get('attempts',[])
    if type(attempts)is not list:raise ValueError('HISTORY_STATUS_ATTEMPTS')
    causes=[];categories=set();candidate_states=[]
    for index,a in enumerate(attempts):
        if type(a)is not dict or type(a.get('state'))is not str:raise ValueError('HISTORY_STATUS_ATTEMPT_SCHEMA')
        state=a['state']
        for key in ('code','reason','family','organization'):
            if key in a and type(a[key])is not str:raise ValueError('HISTORY_STATUS_ATTEMPT_FIELD')
        category=('NO_PROPOSAL'if state in NO_PROPOSAL else'TIMEOUT'if state in TIMEOUT else'UNSUPPORTED'if state in UNSUPPORTED
                  else'EXECUTION_ERROR'if state=='EXECUTION_ERROR'else'CONSTRUCTED'if state in CONSTRUCTED else'NOT_ATTEMPTED'if state in SKIPPED else'UNKNOWN')
        causes.append({'attempt_index':index,'category':category,**{k:deepcopy(a[k])for k in ('state','code','reason','family','organization')if k in a}})
        if category not in ('CONSTRUCTED','NOT_ATTEMPTED'):categories.add(category)
    for row in candidate_rows:
        if type(row)is not dict or row.get('state')not in CANDIDATE:raise ValueError('HISTORY_STATUS_CANDIDATE_STATE')
        category=CANDIDATE[row['state']];categories.add(category)
        candidate_states.append({'candidate_id':row.get('candidate_id'),'state':row['state'],'category':category})
    if outcome!='EXPERIMENT_COMPLETED':
        if candidate_rows:raise ValueError('HISTORY_STATUS_NONCOMPLETED_CANDIDATES')
        categories.add(TOP[outcome])
    if not categories:categories.add('UNKNOWN')
    for key in ('code','field'):
        if key in result and result[key]is not None and type(result[key])is not str:raise ValueError('HISTORY_STATUS_TOP_FIELD')
    return {'schema':'V25_HISTORICAL_STATUS_TAXONOMY_V1','primary':next(iter(categories))if len(categories)==1 else'MULTIPLE',
        'categories':sorted(categories),'original_outcome':outcome,'original_code':result.get('code'),'original_field':result.get('field'),
        'attempt_causes':causes,'candidate_states':candidate_states,'qualified':False,'global_infeasibility_proven':False,
        'scope':'Historical status explanation only; constructed is not qualified, zero witnesses are not global infeasibility, and skipped attempts are not search results.'}
