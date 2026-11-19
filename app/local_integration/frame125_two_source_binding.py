"""Separate FRAME125 explicit-two study. No SIDE contract/production changes.
Executable source-derived shape, not an independent declarative semantic schema.
"""
import copy,hashlib,inspect,types
from fractions import Fraction as F
from pathlib import Path
import left_right_two_source_binding as common
from left_right_two_source_binding import (ROOT,ENGINE,ENGINE_PIN,STATUS,PROPOSAL_KEYS,exact,ensure,clean_json,raw_check,canonical_json,digest,inventory,check_transport,source_state)
CONTRACT_ID='FRAME125_SERVICE_SIDE_EXPLICIT_TWO_SOURCE_D4_STUDY_V1'
TOPOLOGY='FRAME125_SERVICE_SIDE'
def own_sources():
    paths=[Path(__file__).resolve(),Path(common.__file__).resolve()]
    ensure(paths[1]==(ROOT/'app/local_integration/left_right_two_source_binding.py').resolve(),'SHARED_HELPER_IMPORT')
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
def topology_check(p,core):
    """Exact decimal rational constraints in original search114, not admission."""
    clean_json([p,core])
    ensure(p['organization_topology']==TOPOLOGY,'FRAME_TOPOLOGY_LABEL')
    bath=p['rectangles']['bath'];kitchen=p['rectangles']['kitchen']
    b=list(map(lambda v:F(str(v)),bath));k=list(map(lambda v:F(str(v)),kitchen))
    unit=list(map(lambda v:F(str(v)),core['units']['A']))
    ensure(b[2]==unit[2],'FRAME_BATH_RIGHT_SOURCE_SIDE')
    ensure(k[2]==b[0]-F('0.15'),'FRAME_KITCHEN_BATH_SHARED_WALL')
    ensure(k[1]+(k[3]-k[1])==b[1]+(b[3]-b[1]),'FRAME_SERVICE_TOP_ALIGNMENT')
    return {'bath_right':str(b[2]),'unit_right':str(unit[2]),'shared_wall_gap':str(b[0]-k[2]),'service_top':str(k[3]),'source_lines':{'search114.py':[54,55,56,57,104,105,106,107,108,109]},'scope':'Three exact source topology constraints only; no floor, operation or capacity approval.'}
def proposal_check(p,core):
    clean_json(p)
    ensure(type(p)is dict and set(p)==PROPOSAL_KEYS,'FRAME_PROPOSAL_FIELDS')
    for k,v in {'status':'PROPOSAL_ONLY','capacity_profile':'LEGACY_SOURCE_PROGRAM','organization_profile':'UNRESTRICTED','organization_topology':TOPOLOGY,'bedrooms':2,'variant':0,'sleep_roles':['double','twin'],'no_global_infeasibility_claim':True}.items():ensure(exact(p[k],v),'FRAME_PROPOSAL_'+k)
    for k in ('solver_status','variables','binary_separation_variables','constraints'):ensure(type(p[k])is int,'FRAME_INTEGER:'+k)
    for k in ('solver_seconds','budget_seconds'):ensure(type(p[k])in(int,float) and p[k]>=0,'FRAME_TIME:'+k)
    for k in ('objective_profile','solver_message','private_module_contract','network_scope'):ensure(type(p[k])is str,'FRAME_TEXT:'+k)
    roles={'bed1':'private_room','bed2':'private_room','bath':'service','kitchen':'open_room','dining':'open_room','sofa1_use':'furniture_use','sofa2_use':'furniture_use','chair1_use':'furniture_use','chair2_use':'furniture_use','entry_apron':'reserved_entry'}
    ensure(exact(p['roles'],roles),'FRAME_ROLE_INVENTORY')
    ensure(type(p['rectangles'])is dict and set(p['rectangles'])==set(roles),'FRAME_RECTANGLE_INVENTORY')
    for q in p['rectangles'].values():
        ensure(type(q)is list and len(q)==4 and all(type(v)in(int,float) for v in q),'FRAME_RECTANGLE_TYPE')
        ensure(q[0]<q[2] and q[1]<q[3],'FRAME_RECTANGLE_EXTENT')
    ensure(exact(p['bed_door_sides'],{'bed1':'right','bed2':'left'}),'FRAME_PAIR_DOORS')
    names={'bed1','bed2','bath','kitchen','dining_front','dining_back','dining_west','dining_east','sofa1_use','sofa2_use','chair1_use','chair2_use'}
    ensure(type(p['network_paths'])is dict and set(p['network_paths'])==names,'FRAME_NETWORK_INVENTORY')
    for path in p['network_paths'].values():
        ensure(type(path)is list and len(path)==5,'FRAME_PATH_LENGTH')
        for q in path:ensure(type(q)is list and len(q)==2 and all(type(v)in(int,float) for v in q),'FRAME_PATH_POINT')
    return topology_check(p,core)
def verify(packet,ctx):
    report={'contract_id':CONTRACT_ID,'status':STATUS,'scoped_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'whole_physical_verified':False,'whole_functional_verified':False,'historical_schema_replaced':False,'production_supported':False,'errors':[],'pending':['WHOLE_FUNCTIONAL_UNKNOWN','HISTORICAL_WORLD_RECORD_SCHEMA_UNSUPPORTED_REMAINS'],'source_dependency':'Pinned original constructor/frame/assemble/modules and ledger functions; shared explicit-field D4 helper. Not independent declarative semantic grammar; not production admission.'}
    try:
        before=source_state();own=own_sources();clean_json([packet,ctx]);frozen=digest([packet,ctx])
        ensure(type(packet)is dict and set(packet)=={'family','local_model','world_model','core','unit_proposal_hashes','admission_claim'},'FRAME_PACKET_FIELDS')
        ensure(exact(packet['family'],'LEFT_RIGHT') and packet['admission_claim']is False,'FRAME_FAMILY_AUTHORITY')
        ensure(type(ctx)is dict and set(ctx)=={'operation','inputs','baseline_model_hash','existing_plan_id','source_files','construction_trace'},'FRAME_CONTEXT_FIELDS')
        t=ctx['construction_trace'];raw=t['raw'];raw_check(raw)
        from constructor127 import frame,build,context
        for fn in (frame,build,context):
            ensure(Path(inspect.getsourcefile(fn)).resolve()==(ENGINE/'constructor127.py').resolve(),'FRAME_CONSTRUCTOR_IMPORT')
        core,_=frame(raw,'LEFT_RIGHT')
        ensure(set(t['proposals'])=={'A','B'},'FRAME_PROPOSAL_ASSIGNMENTS')
        report['topology_evidence']={u:proposal_check(p,core) for u,p in t['proposals'].items()}
        rebuilt=canonical_json(build(copy.deepcopy(raw),'LEFT_RIGHT',copy.deepcopy(t['proposals']['A']),copy.deepcopy(t['proposals']['B'])))
        ensure(exact(packet['local_model'],rebuilt['local_model']),'FRAME_SOURCE_LOCAL_TYPED_MISMATCH')
        ensure(exact(packet['core'],rebuilt['core']),'FRAME_SOURCE_CORE_TYPED_MISMATCH')
        ensure(exact(packet['unit_proposal_hashes'],rebuilt['unit_proposal_hashes']),'FRAME_SOURCE_PROPOSAL_HASHES')
        ensure(exact(ctx,canonical_json(context(raw,rebuilt,t['proposals']))),'FRAME_SOURCE_CONTEXT_TYPED_MISMATCH')
        inventory(packet['local_model'])
        d4=check_transport(packet['local_model'],packet['world_model'],packet['core']);report['independent_d4']=d4
        ensure(d4['verified'],'FRAME_INDEPENDENT_D4_FAILED:'+str(d4['errors']))
        ensure(digest(packet['world_model'])==t['model_hash'],'FRAME_TRACE_WORLD_HASH')
        ensure(digest([packet,ctx])==frozen,'FRAME_INPUT_MUTATION')
        ensure(source_state()==before and own_sources()==own,'FRAME_SOURCE_CHANGED')
        report.update(scoped_verified=True,source_files=before,own_source_files=own,engine_revision=ENGINE_PIN,local_model_hash=digest(packet['local_model']),model_hash=digest(packet['world_model']),context_hash=digest(ctx),canonical_type_policy='Exact JSON types; source decimal-rational topology equality without tolerance.')
    except (ValueError,TypeError,KeyError,IndexError) as ex:report['errors'].append(str(ex))
    return report
