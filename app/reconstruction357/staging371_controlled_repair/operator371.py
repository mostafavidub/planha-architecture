"""Isolated balanced365 seating-source repair proposal, NOT live authority.

No verdict mutation, cached PASS, source overwrite, solver, or fresh review.
The changed source compound must be reconstructed and reviewed by a NEW
registered source adapter; legacy365 replay and fixed368 binding cannot do it.
"""
import copy
import hashlib
import json
from fractions import Fraction as F

SCHEMA = 'ROW_BALANCED_PORTALS365_SOURCE_TRACE_V1'
PUBLIC = {'sofa1', 'sofa2', 'armchair1', 'armchair2', 'armchair3', 'armchair4'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()

def rect(value):
    if type(value) is not list or len(value) != 4 or any(type(x) not in (str, int) for x in value):
        raise ValueError('EXACT_RECT_REQUIRED')
    r = tuple(map(F, value))
    if r[2] <= r[0] or r[3] <= r[1]:
        raise ValueError('RECT_EXTENT')
    return r

def overlap(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])

def moved(r, dx, dy):
    return (r[0] + dx, r[1] + dy, r[2] + dx, r[3] + dy)

def union_contains(r, rectangles):
    """Exact finite rectangular ownership union, no bounding-box shortcut."""
    xs = sorted({r[0], r[2]} | {x for q in rectangles for x in (q[0], q[2]) if r[0] < x < r[2]})
    ys = sorted({r[1], r[3]} | {y for q in rectangles for y in (q[1], q[3]) if r[1] < y < r[3]})
    return all(any(q[0] <= (a+b)/2 <= q[2] and q[1] <= (c+d)/2 <= q[3] for q in rectangles)
               for a,b in zip(xs,xs[1:]) for c,d in zip(ys,ys[1:]))

def protected(record):
    c = record['candidate']; p = c['packet']; m = c['model']
    if c['request_digest'] != digest(c['request']) or c['model_digest'] != digest(m):
        raise ValueError('CANDIDATE_DIGEST')
    if digest(p['world_model']) != digest(m):
        raise ValueError('PACKET_MODEL')
    return copy.deepcopy({'request': c['request'], 'family': p['family'], 'core': p['core'],
        'frames': {name: {'inputs': p[name]['inputs'], 'program': p[name]['program'],
          'profile': p[name]['profile'], 'units': [
           {'id': u['id'], 'ownership': u['ownership'],
            'room_ids': sorted(u['rooms']), 'fixture_ids': sorted(u['fixtures']),
            'activity_ids': sorted(u['activities'])} for u in p[name]['units']]}
          for name in ('local_model','world_model')}})

def validate_failure(record, fresh, binding):
    """Evidence consistency for proposal preparation, NOT authenticity/live authority."""
    if record['trace'].get('schema') not in (SCHEMA,'DERIVED_BALANCED_SOURCE369_TRACE_V1'):
        raise ValueError('UNSUPPORTED_CURRENT_FAMILY_SOURCE')
    c = record['candidate']; m = c['model']; t = record['trace']
    protected(record)
    if t['candidate_digest'] != digest(c) or t['model_digest'] != digest(m):
        raise ValueError('TRACE_DIGEST')
    for k in ('run_id','candidate_id','review_id'):
        if type(binding.get(k)) is not str or not binding[k]:
            raise ValueError('MISSING_ID:'+k)
    if binding.get('model_digest') != digest(m) or binding.get('record_digest') != digest(record):
        raise ValueError('BINDING_CHANGED')
    if binding.get('fresh_digest') != digest(fresh):
        raise ValueError('FRESH_DIGEST')
    if fresh.get('fresh_checker_executed') is not True or fresh.get('source_unchanged') is not True:
        raise ValueError('FRESH_NOT_EXECUTED')
    if fresh.get('provenance',{}).get('verified') is not True:
        raise ValueError('PROVENANCE_UNVERIFIED')
    if fresh.get('expected_method_registry',{}).get('built_before_evaluate') is not True:
        raise ValueError('REGISTRY_UNVERIFIED')
    if fresh.get('input_record_digest') != digest(record) or fresh.get('outer_trace_digest') != digest(t) or fresh.get('model_digest') != digest(m):
        raise ValueError('FRESH_MODEL_BINDING')
    proof=fresh['provenance']
    if (proof.get('input_record_digest')!=digest(record) or proof.get('model_hash')!=digest(m)
        or proof.get('outer_trace_digest')!=digest(t) or proof.get('candidate_digest')!=digest(c)
        or proof.get('packet_digest')!=digest(c['packet']) or binding['review_id']!=fresh.get('review_id')):
        raise ValueError('CURRENT_PROVENANCE_BINDING')
    r = fresh['raw_report']
    if r.get('model_hash') != digest(m) or r.get('status') != 'FAIL' or r.get('pending') != []:
        raise ValueError('CURRENT_UNAMBIGUOUS_FAIL_REQUIRED')
    errors = r.get('errors')
    if type(errors) is not list or not errors:
        raise ValueError('DIRECT_COLLISION_REQUIRED')
    # Collateral failures remain intact; only direct collision evidence permits a proposal.
    collisions = [e for e in errors if type(e) is dict and e.get('code') == 'FIXTURE_COLLISION']
    if not collisions:
        raise ValueError('DIRECT_COLLISION_REQUIRED')
    error = collisions[0]
    if set(error) != {'code','fixtures'}:
        raise ValueError('UNSUPPORTED_COLLISION_SHAPE')
    pair = error['fixtures']
    if type(pair) is not list or len(pair) != 2 or len(set(pair)) != 2 or not set(pair) <= PUBLIC:
        raise ValueError('UNSUPPORTED_COLLISION_PAIR')
    if any(set(e) != {'code','fixtures'} or type(e['fixtures']) is not list or sorted(e['fixtures']) != sorted(pair) for e in collisions):
        raise ValueError('ONLY_SAME_PAIR_DIRECT_COLLISIONS_SUPPORTED')
    # The source checker also compares units. Never authorize cross-unit repair.
    units = m['units']; witnesses=[]
    for i,u in enumerate(units):
        for v in units[i+1:]:
            for a,b in (pair,pair[::-1]):
                if overlap(rect(u['fixtures'][a]),rect(v['fixtures'][b])):
                    raise ValueError('CROSS_UNIT_COLLISION')
        if overlap(rect(u['fixtures'][pair[0]]),rect(u['fixtures'][pair[1]])):
            witnesses.append(u['id'])
    if 'A' not in witnesses:
        raise ValueError('NO_CURRENT_SOURCE_COLLISION')
    if len(collisions) != len(witnesses):
        raise ValueError('COLLISION_WITNESS_COUNT')
    return pair, witnesses

def propose(record, fresh, binding):
    """Finite exact four-direction source-compound translation, no output-model patch."""
    before = digest(record); pair,witnesses = validate_failure(record,fresh,binding)
    source = record['trace']['proposal']; unit = next(u for u in record['candidate']['model']['units'] if u['id']=='A')
    owners = list(map(rect,unit['ownership'])); options=[]
    for fid,other in (pair,pair[::-1]):
        key = (fid if fid.startswith('sofa') else 'chair'+fid[len('armchair'):])+'_use'
        fx = rect(unit['fixtures'][fid]); front = rect(unit['activities'][fid+'_front'])
        compound = (min(fx[0],front[0]),min(fx[1],front[1]),max(fx[2],front[2]),max(fx[3],front[3]))
        if rect(source['rectangles'][key]) != compound:
            raise ValueError('SOURCE_COMPOUND_NOT_BOUND')
        obstacle = rect(unit['fixtures'][other])
        shifts = [(obstacle[0]-fx[2],F(0)),(obstacle[2]-fx[0],F(0)),
                  (F(0),obstacle[1]-fx[3]),(F(0),obstacle[3]-fx[1])]
        for dx,dy in shifts:
            q = moved(compound,dx,dy); f = moved(fx,dx,dy)
            if not (dx or dy) or abs(dx)+abs(dy)>4 or not union_contains(q,owners): continue
            if any(overlap(f,rect(v)) for k,v in unit['fixtures'].items() if k!=fid): continue
            options.append((abs(dx)+abs(dy),fid,key,dx,dy,q))
    if not options:
        return {'status':'NO_ELIGIBLE_TRANSLATION','accepted':False,'delivery_allowed':False,
                'live_authority':False,'attempt_count':0}
    _,fid,key,dx,dy,q = min(options)
    proposal = copy.deepcopy(source)
    proposal['rectangles'][key] = list(map(str,q))
    # Do not retain a solver-success claim on an engineered proposal.
    for k in ('solver_status','solver_message','variables','constraints','seconds'):
        proposal.pop(k,None)
    proposal['status']='ENGINEERING_SOURCE_REPAIR_PROPOSAL'
    proposal['generation_method']='BALANCED365_SEATING_COMPOUND_TRANSLATION369'
    result={'schema':'CURRENT_FAMILY_SOURCE_PROPOSAL369','status':'RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED',
      'kind':'balanced','parent_record_digest':before,'parent_binding':copy.deepcopy(binding),
      'parent_fresh_digest':digest(fresh),'protected_snapshot_digest':digest(protected(record)),
      'source_inventory':copy.deepcopy(record['trace']['source_inventory']),
      'operator':{'name':'EXACT_SEATING_COMPOUND_TRANSLATION','fixture_id':fid,'source_key':key,
                  'dx':str(dx),'dy':str(dy),'collision_units':witnesses,'pair':pair},
      'proposal':proposal,'proposal_digest':digest(proposal),'solver_used':False,
      'accepted':False,'delivery_allowed':False,'live_authority':False,'attempt_count':1,
      'scope':'SOURCE_PROPOSAL_ONLY; ROUTES_OPERATIONS_ALL_RULES_NOT_RECHECKED'}
    result['proposal_authorization_version']='371_COLLATERAL_PRESERVED_NOT_WAIVED'
    result['before_raw_report']=copy.deepcopy(fresh['raw_report'])
    result['before_raw_digest']=digest(fresh['raw_report'])
    if digest(record)!=before: raise ValueError('PARENT_MUTATED')
    return result

def bind_reconstructed(parent, plan, child, run_id):
    """Pure preservation and new candidate lineage; does not mint a review ID."""
    if plan.get('status') != 'RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED' or plan['parent_record_digest'] != digest(parent):
        raise ValueError('PLAN_PARENT_MISMATCH')
    if plan['proposal_digest'] != digest(plan['proposal']): raise ValueError('PLAN_CHANGED')
    if run_id != plan['parent_binding']['run_id']: raise ValueError('RUN_CHANGED')
    trace=child.get('trace',{})
    if (trace.get('schema') not in ('BALANCED_SOURCE_REPAIR369_TRACE_V1','DERIVED_BALANCED_SOURCE369_TRACE_V1')
        or trace.get('parent_record_digest')!=digest(parent)
        or trace.get('proposal_digest')!=plan['proposal_digest']
        or trace.get('candidate_digest')!=digest(child['candidate'])
        or trace.get('model_digest')!=digest(child['candidate']['model'])):
        raise ValueError('NEW_SOURCE_TRACE_REQUIRED')
    if digest(protected(child)) != plan['protected_snapshot_digest']:
        raise ValueError('PROTECTED_DATA_CHANGED')
    model_digest=digest(child['candidate']['model'])
    if model_digest==plan['parent_binding']['model_digest']: raise ValueError('NO_MODEL_CHANGE')
    candidate_id=digest({'run_id':run_id,'parent_candidate_id':plan['parent_binding']['candidate_id'],
                         'model_digest':model_digest,'operator_digest':digest(plan['operator'])})
    if candidate_id==plan['parent_binding']['candidate_id']: raise ValueError('CANDIDATE_ID_REUSED')
    return {'schema':'REPAIR_LINEAGE369','run_id':run_id,'candidate_id':candidate_id,
       'model_digest':model_digest,'record_digest':digest(child),
       'parent_candidate_id':plan['parent_binding']['candidate_id'],
       'parent_review_id':plan['parent_binding']['review_id'],
       'parent_fresh_digest':plan['parent_fresh_digest'],
       'input_record_digest':plan['parent_record_digest'],'operator_digest':digest(plan['operator']),
       'request_digest':child['candidate']['request_digest'],'review_id':None,
       'fresh_review_required':True,'source_replay_required':True,
       'accepted':False,'delivery_allowed':False,'live_authority':False}

def execute_live(*args, **kwargs):
    return {'status':'BLOCKED','reason':'CURRENT_FAMILY_REPLAY_AND_FRESH_AUTHORITY_ADAPTER_NOT_REGISTERED',
            'accepted':False,'delivery_allowed':False,'repair_attempted':False}
