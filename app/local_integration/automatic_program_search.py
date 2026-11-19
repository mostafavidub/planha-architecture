"""Task 1.3 scheduler framework. No live geometry adapter until task 2.5.
Synthetic test adapters cannot produce model or admission evidence.
"""
import copy,json,math,time
from public_wln_contract import parse_public,verify_public
from program_profile_registry import lookup
from same_version_front_rear_contract import bind_request,contract,digest
DEFAULT_BUDGET={'max_attempts':1,'wall_seconds':90,'seconds_per_attempt':3}
AUTHORITY=('accepted','qualified','display_allowed','delivery_allowed')
def _budget(value):
    b=copy.deepcopy(DEFAULT_BUDGET if value is None else value)
    if type(b) is not dict or set(b)!=set(DEFAULT_BUDGET):raise ValueError('BUDGET_FIELDS')
    if type(b['max_attempts']) is not int or not 0<=b['max_attempts']<=1:raise ValueError('BUDGET_ATTEMPTS')
    for k in ('wall_seconds','seconds_per_attempt'):
        if type(b[k]) not in (int,float) or not math.isfinite(b[k]) or not 0<=b[k]<=DEFAULT_BUDGET[k]:
            raise ValueError('BUDGET_FINITE_NUMBER')
    return b
def alternatives():
    # Order is enumeration only; detailed policy and transitions belong to1.4.
    return [{'alternative_id':p['id'],'registry':p,'registry_digest':digest(p),
      'implementation_status':'SELECTED_CONTRACT_ONLY_LIVE_ADAPTER_NOT_CONNECTED' if n==2 else 'ONE_BED_ADAPTER_NOT_AUDITED',
      'selected_contract':contract()['schema'] if n==2 else None,
      'quality_status':'PROFILE_NOT_READY',**{k:False for k in AUTHORITY}}
      for n in (2,1) for p in [lookup('PROGRAM_'+str(n)+'BED_V1')]]
def _clock_value(clock,previous=None):
    value=clock()
    if type(value) not in (int,float) or not math.isfinite(value):raise ValueError('CLOCK_FINITE')
    if previous is not None and value<previous:raise ValueError('CLOCK_REVERSED')
    return value
def _synthetic_result(result,request):
    expected={'schema','kind','attempt_id','request_digest','programme_digest','contract_digest','state',*AUTHORITY}
    if type(result) is not dict or set(result)!=expected:raise ValueError('SYNTHETIC_RECEIPT_SCHEMA')
    if result['schema']!='SCHEDULER_SYNTHETIC_RESULT_V1' or result['kind']!='SYNTHETIC_TEST_ONLY':raise ValueError('SYNTHETIC_ONLY')
    for key in ('attempt_id','request_digest','programme_digest','contract_digest'):
        if digest(result[key])!=digest(request[key]):raise ValueError('RECEIPT_BINDING:'+key)
    if result['state'] not in ('SIMULATED_WITNESS','SIMULATED_NO_WITNESS','SIMULATED_TIMEOUT'):raise ValueError('SYNTHETIC_STATE')
    if any(result[k] is not False for k in AUTHORITY):raise ValueError('ADAPTER_AUTHORITY')
    return copy.deepcopy(result)
def run(body,*,test_adapter=None,clock=None,budget=None):
    """Public bytes -> registry -> selected contract -> scheduling.
    No default solver, no HTTP injection, no externally supplied PASS receipts.
    test_adapter is internal unit-test-only; outputs are never real witnesses.
    Wall limit is accounting, not a synchronous Python callback preemption guarantee.
    """
    limits=_budget(budget)
    envelope=parse_public(body);verify_public(body,envelope)
    binding=bind_request(body,envelope,'PROGRAM_2BED_V1')
    alts=alternatives();initial=digest([binding,alts,limits])
    clock=time.monotonic if clock is None else clock
    started=_clock_value(clock);last=started
    out={'schema':'AUTOMATIC_PROGRAM_SCHEDULER_FRAMEWORK_V1',
      'status':'SINGLE_CASE_SCHEDULER_FRAMEWORK_ONLY','binding':binding,'alternatives':alts,
      'attempts':[],'budget':limits,'used_attempts':0,'allocated_seconds':0,
      'selected_alternative':None,'pareto_selected':[],'quality_status':'PROFILE_NOT_READY',
      'production_supported':False,'request_fulfilled':False,'fresh_model_executed':False,
      'scope':'Only18x20/n2 selected contract; other cases rejected before scheduling. Digest binds data, not proof of runtime producer origin. One attempt, not multi-option search.',
      'test_mode':test_adapter is not None,'ap07_complete':False,
      'global_infeasibility_proven':False,'transitions':[],
      'remaining_stages':[{'stage':s,'status':'NOT_IMPLEMENTED_IN_SELECTED_SCHEDULER'} for s in
        ('OTHER_CORE','OTHER_SPLIT','OTHER_PLACEMENT','OPTIONAL_NONBED_MERGE','LOWER_PROGRAM_TRANSITION_POLICY')],
      'order_reason':'Two before one is a bounded framework enumeration, not quality ranking or proof of exhaustive search.',
      'budget_scope':'Engineering accounting; count1 is not product output count. No budget reset per alternative. Future live execution budget must be explicitly selected at task2.5.',
      **{k:False for k in AUTHORITY}}
    for alt in alts:
        row={'attempt_id':alt['alternative_id']+':0','alternative_id':alt['alternative_id'],
          'attempted':False,'programme_digest':alt['registry_digest'],
          'state':'NOT_SCHEDULED',**{k:False for k in AUTHORITY}}
        out['attempts'].append(row)
        now=_clock_value(clock,last);last=now
        if alt['alternative_id']!='PROGRAM_2BED_V1':
            row.update(state='UNSUPPORTED_ADAPTER',reason='Approved programme does not establish one-bedroom whole-bundle adapter readiness; no hidden fallback.')
            continue
        if test_adapter is None:
            row.update(state='LIVE_ADAPTER_NOT_CONNECTED',reason='Task1.3 only; fresh generation/evaluation deferred to2.5.')
            continue
        remaining=max(0,limits['wall_seconds']-(now-started))
        seconds=min(limits['seconds_per_attempt'],remaining)
        if out['used_attempts']>=limits['max_attempts'] or seconds<=0:
            row.update(state='BUDGET_EXHAUSTED',reason='Not evidence of infeasibility.')
            continue
        request={'schema':'SCHEDULER_TEST_REQUEST_V1','kind':'SYNTHETIC_TEST_ONLY',
          'attempt_id':row['attempt_id'],'request_digest':envelope['canonical_request_digest'],
          'programme_digest':alt['registry_digest'],'contract_digest':binding['contract_digest'],
          'raw':copy.deepcopy(binding['raw']),'programme':copy.deepcopy(alt['registry']),
          'seconds_allocated':seconds}
        frozen=digest(request);row['attempted']=True
        out['used_attempts']+=1;out['allocated_seconds']+=seconds
        try:
            response=test_adapter(request)
            if digest(request)!=frozen:raise ValueError('ADAPTER_MUTATED_INPUT')
            receipt=_synthetic_result(response,request)
            after=_clock_value(clock,last);last=after
            if after-now>seconds or after-started>limits['wall_seconds']:
                row.update(state='BUDGET_OVERRUN',reason='Synthetic callback exceeded allocation; receipt not retained as witness.')
            else:row.update(state=receipt['state'],synthetic_receipt=receipt)
        except Exception as ex:
            row.update(state='ATTEMPT_FAILED_CLOSED',error={'type':type(ex).__name__,'detail':str(ex)})
        if digest([binding,alts,limits])!=initial:raise ValueError('SCHEDULER_INPUT_CHANGED')
    end=_clock_value(clock,last)
    out['elapsed_seconds']=end-started
    out['transition_policy_status']='DEFERRED_TASK_1_4_NOT_EXHAUSTIVENESS_REQUIREMENT'
    return out
