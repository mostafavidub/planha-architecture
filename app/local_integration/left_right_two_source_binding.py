"""Study-only source-derived shape plus independent swap-XY binding.
NOT a declarative semantic schema, physical checker, or production registry.
The entire current engine is pinned. Executable shape depends on unchanged
constructor/frame/assemble/module sources; historical schema errors remain.
"""
import copy,hashlib,inspect,json,math,re,types
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
ENGINE_PIN='faada6a8a1106adfe8a24a5f18dfdf6b550f20a6ecc93d81ce07d47a20d6a279'
STATUS='SOURCE_DERIVED_SHAPE_AND_INDEPENDENT_D4_BINDING_ONLY'
RECT=set('rect plan_rect closed_panel open_panel pocket rail_envelope panel_rect actor_rect actor_start actor_end closed_rect open_rect occupied_body standing_body closed_tray open_tray body_rect front_rect region'.split())
POINT=set('hand_point hand_start hand_end center hinge closed_actor open_actor open_access shelf_target held_target grip_closed grip_open storage_target workpoint access_point point target actor hand translation actor_offset_m normal front_normal'.split())
RECTS=set('shell_rects motion_envelopes regions parts'.split())
PATHS=set('path egress_route route open_transfer_points'.split())
INVARIANT_NUMERIC_LISTS=set('angle_range_degrees source_size_m size_m opaque_skin_m'.split())
SHAPE_PATHS=['root.walls','root.wall_hosts','root.source_wall_hosts','root.units[].rooms','root.units[].fixtures','root.units[].fixture_metadata','root.units[].activities','root.units[].routes','root.units[].route_targets','root.room_metadata','root.proposal_network_paths','root.module_aprons','root.physical_wall_network.source_aliases','root.wall_finish_profile']
PROPOSAL_KEYS=set('organization_profile organization_topology objective_profile capacity_profile sleep_roles status solver_status solver_message solver_seconds budget_seconds bedrooms variant variables binary_separation_variables constraints no_global_infeasibility_claim rectangles roles network_paths bed_door_sides private_module_contract network_scope'.split())

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def canonical_json(x):
    # Explicit JSON transport serialization, never semantic number/string coercion.
    return json.loads(json.dumps(x,ensure_ascii=False,allow_nan=False))

def exact(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a)is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def ensure(ok,reason):
    if not ok:raise ValueError(reason)

def clean_json(v):
    if type(v)is dict:
        ensure(all(type(k)is str for k in v),'NONSTRING_KEY')
        for x in v.values():clean_json(x)
    elif type(v)is list:
        for x in v:clean_json(x)
    else:ensure(type(v)in(str,int,float,bool,type(None)) and (type(v)is not float or math.isfinite(v)),'NONCANONICAL_JSON_TYPE')

def raw_check(raw):
    ensure(type(raw)is dict and set(raw)=={'W','L','n','requested_count'},'RAW_FIELDS')
    for axis in ('W','L'):
        v=raw[axis];ensure(type(v)is str and re.fullmatch(r'(?:0|[1-9][0-9]*)(?:\.[0-9]+)?',v) is not None,'RAW_DECIMAL_TYPE')
        ensure(F(5)<=F(v)<=F(25),'RAW_RANGE')
        # Canonical decimal output of prepare; no alternate zero-padding.
        ensure(not('.' in v and v.endswith('0')),'RAW_NONCANONICAL_DECIMAL')
    ensure(type(raw['n'])is int and raw['n']==2,'RAW_N')
    ensure(type(raw['requested_count'])is int and 1<=raw['requested_count']<=12,'RAW_COUNT')

def proposal_check(p):
    ensure(type(p)is dict and set(p)==PROPOSAL_KEYS,'PROPOSAL_FIELDS')
    ensure(type(p['bedrooms'])is int and p['bedrooms']==2,'PROPOSAL_PROGRAM')
    ensure(exact(p['sleep_roles'],['double','twin']),'PROPOSAL_SLEEP_ROLES')
    for k,v in {'status':'PROPOSAL_ONLY','capacity_profile':'LEGACY_SOURCE_PROGRAM','organization_profile':'UNRESTRICTED','organization_topology':'SIDE_ROOTED_SERVICES'}.items():ensure(exact(p[k],v),'PROPOSAL_'+k)
    ensure(type(p['variant'])is int and p['variant']==0,'PROPOSAL_VARIANT')
    ensure(p['no_global_infeasibility_claim']is True,'PROPOSAL_INFEASIBILITY')
    for k in ('solver_status','variables','binary_separation_variables','constraints'):ensure(type(p[k])is int,'PROPOSAL_INTEGER:'+k)
    for k in ('solver_seconds','budget_seconds'):ensure(type(p[k])in(int,float) and p[k]>=0,'PROPOSAL_TIME:'+k)
    for k in ('objective_profile','solver_message','private_module_contract','network_scope'):ensure(type(p[k])is str,'PROPOSAL_TEXT:'+k)
    roles={'bed1':'private_room','bed2':'private_room','bath':'service','kitchen':'open_room','dining':'open_room','sofa1_use':'furniture_use','sofa2_use':'furniture_use','chair1_use':'furniture_use','chair2_use':'furniture_use','entry_apron':'reserved_entry'}
    ensure(exact(p['roles'],roles),'PROPOSAL_ROLE_INVENTORY')
    ensure(type(p['rectangles'])is dict and set(p['rectangles'])==set(roles),'PROPOSAL_RECTANGLE_INVENTORY')
    for q in p['rectangles'].values():
        ensure(type(q)is list and len(q)==4 and all(type(v)in(int,float) for v in q),'PROPOSAL_RECTANGLE_TYPE')
        ensure(q[0]<q[2] and q[1]<q[3],'PROPOSAL_RECTANGLE_EXTENT')
    ensure(exact(p['bed_door_sides'],{'bed1':'right','bed2':'left'}),'PROPOSAL_PAIR_DOORS')
    names={'bed1','bed2','bath','kitchen','dining_front','dining_back','dining_west','dining_east','sofa1_use','sofa2_use','chair1_use','chair2_use'}
    ensure(type(p['network_paths'])is dict and set(p['network_paths'])==names,'PROPOSAL_NETWORK_INVENTORY')
    for path in p['network_paths'].values():
        ensure(type(path)is list and len(path)==5,'PROPOSAL_PATH_LENGTH')
        for q in path:ensure(type(q)is list and len(q)==2 and all(type(v)in(int,float) for v in q),'PROPOSAL_PATH_POINT')

def source_state():
    import engine114,constructor127,wall_union118,spatial_roles118
    import assemble114,world_transform125,frame_contract125,common_core125,geometry114,space_accounting118
    bindings=[(constructor127,'assemble',assemble114,'assemble'),(constructor127,'to_world',world_transform125,'to_world'),(constructor127,'local_core',frame_contract125,'local_core'),(frame_contract125,'build',common_core125,'build'),(spatial_roles118,'ledger',space_accounting118,'ledger'),(spatial_roles118,'cells',geometry114,'cells'),(wall_union118,'cells',geometry114,'cells')]
    for owner,alias,module,name in bindings:
        fn=getattr(owner,alias);ensure(fn is getattr(module,name),'IMPORTED_CALLABLE_IDENTITY:'+alias)
        path=ENGINE/(module.__name__+'.py');ensure(Path(inspect.getsourcefile(fn)).resolve()==path.resolve(),'DEPENDENCY_IMPORT:'+alias)
        compiled=compile(path.read_text(),str(path),'exec',dont_inherit=True)
        expected=next(x for x in compiled.co_consts if isinstance(x,types.CodeType) and x.co_name==name)
        ensure(fn.__code__==expected,'DEPENDENCY_CODE_CHANGED:'+alias)
    functions=[(engine114.revision,'engine114.py'),(constructor127.frame,'constructor127.py'),(constructor127.build,'constructor127.py'),(constructor127.context,'constructor127.py'),(wall_union118.bind_physical_wall_union,'wall_union118.py'),(spatial_roles118.attach,'spatial_roles118.py')]
    for fn,name in functions:ensure(Path(inspect.getsourcefile(fn)).resolve()==(ENGINE/name).resolve(),'SOURCE_IMPORT:'+name)
    ensure(engine114.revision()==ENGINE_PIN,'ENGINE_PIN')
    paths={name for _,name in functions}|{'assemble114.py','frame_contract125.py','common_core125.py','world_transform125.py','bedroom_module116.py','twin_module118.py','dining_module118.py','bathroom_module117.py','kitchen_module117.py','world_record_schema129.json'}
    return {name:hashlib.sha256((ENGINE/name).read_bytes()).hexdigest() for name in sorted(paths)}

def S(v):
    from decimal import Decimal,localcontext
    v=F(v)
    with localcontext() as ctx:
        ctx.prec=max(60,len(str(v.numerator))+len(str(v.denominator))+5)
        return format(Decimal(v.numerator)/Decimal(v.denominator),'f')

def scalar(v,role='source_geometry_string'):
    if role=='proposal_network_coordinate':
        ensure(type(v)in(int,float) and (type(v)is not float or math.isfinite(v)),'PROPOSAL_NETWORK_COORDINATE_TYPE:'+type(v).__name__)
        return F(str(v))
    ensure(type(v)is str,'GEOMETRY_COORDINATE_TYPE:'+role+':'+type(v).__name__)
    return F(v)

def swap_point(q,role='source_geometry_string'):
    ensure(type(q)is list and len(q)==2,'POINT_SHAPE:'+role)
    return [S(scalar(q[1],role)),S(scalar(q[0],role))]

def swap_rect(q):
    ensure(type(q)is list and len(q)==4,'RECT_SHAPE')
    v=list(map(scalar,q));return [S(v[1]),S(v[0]),S(v[3]),S(v[2])]

def isometry(t,mode):
    ensure(type(t)is dict and set(t)=={'matrix','translation'},'ISOMETRY_FIELDS')
    a=t['matrix'];ensure(type(a)is list and len(a)==2 and all(type(r)is list and len(r)==2 and all(type(v)is int and v in(-1,0,1) for v in r) for r in a),'ISOMETRY_MATRIX_TYPE')
    ensure(all(sum(a[k][i]*a[k][j] for k in range(2))==int(i==j) for i in range(2) for j in range(2)),'ISOMETRY_NOT_D4')
    ensure(type(t['translation'])is list and len(t['translation'])==2 and all(type(v)is str for v in t['translation']),'ISOMETRY_TRANSLATION')
    if mode=='placement':return {'matrix':[a[1][:],a[0][:]],'translation':swap_point(t['translation'])}
    return {'matrix':[[a[0][1],a[0][0]],[a[1][1],a[1][0]]],'translation':copy.deepcopy(t['translation'])}

def transport(v,key='',path='root'):
    if key in ('module','source_contract'):return copy.deepcopy(v)
    if type(v)is dict:
        if key in ('canonical_isometry','canonical_transform'):return isometry(v,'canonical')
        z={k:transport(x,k,path+'.'+k) for k,x in v.items()}
        for k in ('axis','front_axis'):
            if z.get(k)in('x','y'):z[k]={'x':'y','y':'x'}[z[k]]
        if z.get('orientation')in('horizontal','vertical'):z['orientation']={'horizontal':'vertical','vertical':'horizontal'}[z['orientation']]
        return z
    if type(v)is list:
        if key in RECT:return swap_rect(v)
        if key in POINT:return swap_point(v)
        if key in RECTS:return [swap_rect(x) for x in v]
        if key in PATHS:return [swap_point(x) for x in v]
        if v and all(type(x)in(str,int,float) for x in v):
            try:[F(str(x)) for x in v]
            except ValueError:pass
            else:ensure(key in INVARIANT_NUMERIC_LISTS,'UNKNOWN_NUMERIC_FIELD:'+path)
        return [transport(x,'',path+'[]') for x in v]
    return copy.deepcopy(v)

LOCAL_TOP=set('schema contract_version inputs scope_declaration ordered_macro status accepted release_allowed profile program walls wall_hosts source_wall_hosts common_spaces openings concept_windows units room_metadata common_routes fixture_catalog_hash fixture_catalog fixture_catalog_digest openedge_assumptions route_failures proposal_network_paths network_scope logical_regions operations pending module_ports module_aprons module_placements quality_unverified source_geometry_contract physical_wall_network wall_finish_profile threshold_ownership spatial_accounting'.split())

def expected_world(local,core):
    from wall_union118 import bind_physical_wall_union
    from spatial_roles118 import attach
    ensure(type(local)is dict and set(local)==LOCAL_TOP,'UNKNOWN_OR_MISSING_LOCAL_TOP_FIELD')
    ensure(local.get('ordered_macro')is None and 'private_domains'not in local,'OUTSIDE_EXPLICIT_TWO_TOPOLOGY')
    ensure(exact(core['world_from_local'],{'matrix':[[0,1],[1,0]],'translation':['0','0']}),'WORLD_FRAME')
    e=copy.deepcopy(local);e['inputs']=[S(F(v)) for v in core['physical_core_model']['inputs'][:2]]+[2];e['schema']='GENERAL125_WORLD_FRAME_STUDY'
    for key in ('walls','wall_hosts','source_wall_hosts'):e[key]={n:swap_rect(q) for n,q in local[key].items()}
    e['common_spaces']={k:([swap_rect(q) for q in v] if type(v[0])is list else swap_rect(v)) for k,v in local['common_spaces'].items()}
    e['common_routes']={n:[swap_point(q,'common_route') for q in path] for n,path in local['common_routes'].items()}
    # search114 emits JSON numeric local proposal network coordinates only.
    # Their known physical point role transports to canonical world strings;
    # all other source coordinates stay strictly string-typed.
    e['proposal_network_paths']={n:[swap_point(q,'proposal_network_coordinate') for q in path] for n,path in local['proposal_network_paths'].items()}
    for key in ('openings','concept_windows','operations','module_ports','logical_regions','wall_finish_profile','threshold_ownership'):e[key]=transport(local[key],key,key)
    for w in e['concept_windows']:
        if 'destination'in w:w['destination']['edge']={'bottom':'left','top':'right','left':'bottom','right':'top'}[w['destination']['edge']]
    e['module_aprons']={k:[swap_rect(q) for q in v] for k,v in local['module_aprons'].items()}
    for rec in e['module_placements']:rec['transform']=isometry(rec['transform'],'placement')
    for u in e['units']:
        u['ownership']=[swap_rect(q) for q in u['ownership']]
        u['rooms']={k:[swap_rect(q) for q in v] for k,v in u['rooms'].items()}
        for key in ('fixtures','activities'):u[key]={k:swap_rect(q) for k,q in u[key].items()}
        for key in ('routes','scenario_routes'):u[key]={k:[swap_point(q) for q in v] for k,v in u[key].items()}
        u['route_targets']={k:swap_point(q) for k,q in u['route_targets'].items()};u['entry_point']=swap_point(u['entry_point'])
        for md in u['fixture_metadata'].values():md['rotation_deg']=(90-md.get('rotation_deg',0))%180
        u['dining_module_placement']['transform']=isometry(u['dining_module_placement']['transform'],'placement')
        u['public_program']=transport(u['public_program'],'public_program','unit.public_program')
        u['public_floor_classification']['route_geometry_hash']=digest({**u['routes'],**{'scenario:'+k:v for k,v in u['scenario_routes'].items()}})
    e['openedge_assumptions']={'rights':'UNVERIFIED','assessment':'LIGHT_VENTILATION_EXCLUDED','geometric_frame_transform':'swapXY; optional opening physical hosts retained'}
    e=attach(bind_physical_wall_union(e))
    e['quality_unverified']=[s for s in e['quality_unverified'] if 'ventilation'not in s and 'daylight'not in s]
    e['frame_binding125']={'schema':'ACTUAL_LOCAL_TO_WORLD_D4_V1','local_model_hash':digest(local),'core_contract_hash':digest(core),'world_from_local':copy.deepcopy(core['world_from_local']),'not_a_receipt_of_whole_acceptance':True,'rotation_deg_scope':'Axis footprint only, not a world-facing heading; full source module placement D4 retains orientation binding.','operation_angle_scope':'Kitchen angle ranges are source canonical study parameters, not world polar angles; canonical_transform binds their physical geometry.'}
    return canonical_json(e)

def check_transport(local,world,core):
    try:
        before=source_state();clean_json([local,world,core]);expected=expected_world(local,core)
        ensure(exact(expected,world),'INDEPENDENT_D4_TYPED_WORLD_MISMATCH')
        ensure(source_state()==before,'SOURCE_CHANGED')
        return {'verified':True,'errors':[],'accepted':False,'scope':'Internal source-bound-only transport helper, not an origin or semantic schema verifier. Full verify must first reconstruct and exactly compare all source-local records. Explicit-field swapXY plus pinned source-derived ledger rebuild only.'}
    except (ValueError,TypeError,KeyError,IndexError) as ex:return {'verified':False,'errors':[str(ex)],'accepted':False}

def inventory(local):
    ensure(exact([u['id'] for u in local['units']],['A','B']),'UNIT_ORDER')
    ensure(local['program']['bedrooms_per_unit']==2 and type(local['program']['bedrooms_per_unit'])is int and exact(local['program']['sleep_roles'],['double','twin']),'ACTUAL_PROGRAM')
    expected_fx=set('WC_iranian shower_floor basin fridge sink prep cooker sofa1 sofa2 armchair1 armchair2 dining_table dining_chair_front dining_chair_back dining_chair_west dining_chair_east bed1.bed bed1.closet bed2.bedA bed2.bedB bed2.closet'.split())
    for u in local['units']:
        ensure(set(u['fixtures'])==expected_fx and set(u['fixture_metadata'])==expected_fx,'ACTUAL_FIXTURE_INVENTORY')
        ensure(set(u['rooms'])=={'bed1','bed2','bath','kitchen','dining','living','entry_circulation'},'ACTUAL_ROOM_INVENTORY')
        seats=u['dining_module_placement']['module']['seating']['instances']
        ensure(len(seats)==4,'ACTUAL_FOUR_SEAT_PROGRAM')
    ensure(set(local['physical_wall_network']['source_aliases'])==set(local['walls']),'SOURCE_WALL_ALIAS_INVENTORY')

def verify(packet,ctx):
    report={'status':STATUS,'scoped_verified':False,'errors':[],'accepted':False,'delivery_allowed':False,'qualified':False,'whole_physical_verified':False,'whole_functional_verified':False,'historical_schema_replaced':False,
        'pending':['WHOLE_FUNCTIONAL_UNKNOWN','HISTORICAL_WORLD_RECORD_SCHEMA_UNSUPPORTED_REMAINS'],'source_dependency':'Pinned executable constructor/frame/assemble/modules and source ledger functions. No independent declarative semantic grammar. Not a production evaluator replacement.','shape_paths':SHAPE_PATHS}
    try:
        before=source_state();clean_json([packet,ctx]);frozen=digest([packet,ctx])
        ensure(type(packet)is dict and set(packet)=={'family','local_model','world_model','core','unit_proposal_hashes','admission_claim'},'PACKET_FIELDS')
        ensure(packet['family']=='LEFT_RIGHT' and packet['admission_claim']is False,'PACKET_FAMILY_AUTHORITY')
        ensure(type(ctx)is dict and set(ctx)=={'operation','inputs','baseline_model_hash','existing_plan_id','source_files','construction_trace'},'CONTEXT_FIELDS')
        t=ctx['construction_trace'];raw=t['raw'];raw_check(raw)
        ensure(set(t['proposals'])=={'A','B'},'PROPOSAL_ASSIGNMENTS')
        for p in t['proposals'].values():proposal_check(p)
        from constructor127 import build,context
        rebuilt=canonical_json(build(copy.deepcopy(raw),'LEFT_RIGHT',copy.deepcopy(t['proposals']['A']),copy.deepcopy(t['proposals']['B'])))
        ensure(exact(packet['local_model'],rebuilt['local_model']),'SOURCE_DERIVED_LOCAL_TYPED_MISMATCH')
        ensure(exact(packet['core'],rebuilt['core']),'SOURCE_DERIVED_CORE_TYPED_MISMATCH')
        ensure(exact(packet['unit_proposal_hashes'],rebuilt['unit_proposal_hashes']),'SOURCE_PROPOSAL_HASHES')
        ensure(exact(ctx,canonical_json(context(raw,rebuilt,t['proposals']))),'SOURCE_DERIVED_CONTEXT_TYPED_MISMATCH')
        inventory(packet['local_model'])
        d4=check_transport(packet['local_model'],packet['world_model'],packet['core']);report['independent_d4']=d4
        ensure(d4['verified'],'INDEPENDENT_D4_FAILED:'+str(d4['errors']))
        ensure(digest(packet['world_model'])==t['model_hash'],'TRACE_WORLD_HASH')
        ensure(digest([packet,ctx])==frozen,'INPUT_MUTATION')
        ensure(source_state()==before,'SOURCE_CHANGED')
        report.update(scoped_verified=True,source_files=before,engine_revision=ENGINE_PIN,local_model_hash=digest(packet['local_model']),model_hash=digest(packet['world_model']),context_hash=digest(ctx),canonical_type_policy='Exact JSON type/value equality; bool is not int, numbers are not strings.')
    except (ValueError,TypeError,KeyError,IndexError) as ex:report['errors'].append(str(ex))
    return report
