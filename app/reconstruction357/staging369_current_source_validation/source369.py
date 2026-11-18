"""Exact derived balanced source: immutable parent plus one seating translation.

No solver claim. CONTROLLED_TEST_FIXTURE records remain test-only throughout
their descendants. A repaired record proves reconstruction, not quality.
"""
import copy,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT.parent/'staging369_current_family_repair'))
from operator369 import digest,protected
SCHEMA='DERIVED_BALANCED_SOURCE369_TRACE_V1'
ANCHOR='ROW_BALANCED_PORTALS365_SOURCE_TRACE_V1'
KEYS={'sofa1_use','sofa2_use','chair1_use','chair2_use','chair3_use','chair4_use'}

def _check_inventory(inventory):
    if not inventory:raise ValueError('EMPTY_SOURCE_INVENTORY')
    for n,h in inventory.items():
        p=(ROOT/n).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:
            raise ValueError('SOURCE_CHANGED:'+n)

def _imports():
    for rel in ('staging359_hall_clamp','planha_general150_runtime_work','staging365_balanced_portals'):
        sys.path.insert(0,str(ROOT/rel))
    from adapter365 import replay
    from constructor365 import build
    if Path(sys.modules['adapter365'].__file__).resolve()!=ROOT/'staging365_balanced_portals/adapter365.py':
        raise ValueError('ADAPTER_IMPORT_COLLISION')
    if Path(sys.modules['constructor365'].__file__).resolve()!=ROOT/'staging365_balanced_portals/constructor365.py':
        raise ValueError('CONSTRUCTOR_IMPORT_COLLISION')
    return replay,build

def replay(record,depth=0):
    if depth>2:raise ValueError('SOURCE_LINEAGE_DEPTH')
    t=record['trace'];_check_inventory(t['source_inventory'])
    if t['schema']==ANCHOR:
        old_replay,_=_imports();built=old_replay(t)
    elif t['schema']==SCHEMA:
        parent=record['parent_record']
        if digest(parent)!=t['parent_record_digest']:raise ValueError('PARENT_RECORD_CHANGED')
        replay(parent,depth+1)
        built=_construct(parent,t['source_key'],t['dx'],t['dy'],t['purpose'])
    else:raise ValueError('UNREGISTERED_SOURCE_SCHEMA')
    if digest(built)!=digest(record):raise ValueError('EXACT_REPLAY_MISMATCH')
    return built

def _construct(parent,key,dx,dy,purpose):
    if key not in KEYS or type(dx) not in (str,int) or type(dy) not in (str,int):
        raise ValueError('EXACT_SEATING_TRANSLATION_REQUIRED')
    dx,dy=F(dx),F(dy)
    if bool(dx)==bool(dy) or abs(dx)+abs(dy)>4:raise ValueError('ONE_AXIS_NONZERO_MAX_4M')
    if purpose not in ('CONTROLLED_TEST_FIXTURE','CURRENT_REPAIR_PROPOSAL'):
        raise ValueError('EXPLICIT_PURPOSE_REQUIRED')
    _,build=_imports();source=parent['trace']['proposal'];proposal=copy.deepcopy(source)
    r=list(map(F,proposal['rectangles'][key]));proposal['rectangles'][key]=list(map(str,[r[0]+dx,r[1]+dy,r[2]+dx,r[3]+dy]))
    for k in ('solver_status','solver_message','variables','constraints','seconds'):proposal.pop(k,None)
    proposal['status']='ENGINEERING_SOURCE_REPAIR_PROPOSAL'
    proposal['generation_method']='BALANCED365_SEATING_COMPOUND_TRANSLATION369'
    raw=copy.deepcopy(parent['candidate']['request']);packet=build(raw,'FRONT_REAR',proposal);model=packet['world_model']
    test_only=(purpose=='CONTROLLED_TEST_FIXTURE' or parent.get('test_only') is True)
    context={'schema':'EXPLICIT_DERIVED_SOURCE369_CONTEXT','parent_record_digest':digest(parent),
             'source_key':key,'dx':str(dx),'dy':str(dy),'solver_used':False,'legacy_context_used':False}
    c={'request':raw,'request_digest':digest(raw),'packet':packet,'model':model,'model_digest':digest(model),
       'generation_context':context}
    trace={'schema':SCHEMA,'source_inventory':copy.deepcopy(parent['trace']['source_inventory']),
           'raw':raw,'proposal':proposal,'proposal_digest':digest(proposal),'parent_record_digest':digest(parent),
           'parent_model_digest':parent['candidate']['model_digest'],'candidate_digest':digest(c),
           'model_digest':digest(model),'packet_digest':digest(packet),'source_key':key,
           'dx':str(dx),'dy':str(dy),'purpose':purpose,'solver_used':False}
    result={'candidate':c,'trace':trace,'parent_record':copy.deepcopy(parent),'test_only':test_only,
            'accepted':False,'delivery_allowed':False}
    if digest(protected(parent))!=digest(protected(result)):raise ValueError('PROTECTED_INPUT_PROGRAM_IDS_CHANGED')
    return result

def construct(parent,key,dx,dy,*,purpose):
    initial=digest(parent);replay(parent);result=_construct(parent,key,dx,dy,purpose)
    _check_inventory(parent['trace']['source_inventory'])
    if digest(parent)!=initial:raise ValueError('PARENT_MUTATED')
    return result

def proof(record):
    replay(record);c=record['candidate'];t=record['trace']
    return {'verified':True,'schema':SCHEMA,'input_record_digest':digest(record),
       'outer_trace_digest':digest(t),'candidate_digest':digest(c),'model_hash':digest(c['model']),
       'packet_digest':digest(c['packet']),'raw':c['request'],'parent_record_digest':t['parent_record_digest'],
       'protected_snapshot_digest':digest(protected(record)),'test_only':record['test_only'],
       'scope':'DERIVED_SOURCE_RECONSTRUCTION_ONLY_NOT_REPAIR_AUTHORITY_OR_QUALITY'}

if __name__=='__main__':
    try:print(json.dumps(proof(json.load(sys.stdin))))
    except Exception as e:print(json.dumps({'verified':False,'error':type(e).__name__+':'+str(e)}));sys.exit(1)
