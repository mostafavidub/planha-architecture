"""Fresh central source evaluator supports both pair127 and hierarchical129.
No current native composition or repair capability is implied.
"""
from pathlib import Path
import hashlib,types,copy,threading,uuid,json
ROOT=Path(__file__).resolve().parents[1]
ADAPTER=ROOT/'staging274_evaluator_transport_fix/adapter.py'
ADAPTER_SHA='cf5d31e86b0093b7794bb8438eed2d00d2ccc6a56a2fe12279834553cd5630fc'
def load():
 data=ADAPTER.read_bytes()
 if hashlib.sha256(data).hexdigest()!=ADAPTER_SHA:raise ValueError('EVALUATOR_SOURCE_DRIFT')
 m=types.ModuleType('_selected263_evaluator');m.__file__=str(ADAPTER);exec(compile(data,str(ADAPTER),'exec'),m.__dict__);return m

def envelope(selected,evaluator):
 raw=selected['request'];ctx=selected['generation_context'];packet=selected['packet']
 if _digest_model282(selected['model'])!=_digest_model282(packet.get('world_model')):raise ValueError('SELECTED_MODEL_CHANGED')
 if selected['request_digest']!=evaluator.digest(raw)or selected['model_digest']!=evaluator.digest(selected['model']):raise ValueError('SELECTED_BINDING_CHANGED')
 lock=evaluator.check_source()
 e={'schema':evaluator.SCHEMA,'candidate_id':str(uuid.uuid4()),'raw':copy.deepcopy(raw),'packet':copy.deepcopy(packet),'generation_context':copy.deepcopy(ctx),'producer_source_hash':lock['producer_inventory_digest'],'producer_revision':lock['revision']}
 evaluator.validate_envelope(e);return e

INVENTORY_SHA='69fddea156406a5531551131d2194d3eab9840835edaa4bc755ffbbdcfdeb5c2'
def _digest_model282(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def model_preflight282(selected):
 # The same source-pinned inventory inspector, not a geometry/repair authority.
 path=Path(__file__).with_name('model_inventory.py');data=path.read_bytes()
 if hashlib.sha256(data).hexdigest()!=INVENTORY_SHA:raise ValueError('MODEL_INVENTORY_SOURCE_CHANGED')
 m=types.ModuleType('_model_inventory282');m.__file__=str(path);exec(compile(data,str(path),'exec'),m.__dict__)
 rows={};inspection_error=None
 before=_digest_model282(selected);packet=selected['packet']
 if type(packet)is not dict or _digest_model282(selected['model'])!=_digest_model282(packet.get('world_model'))or selected['model_digest']!=_digest_model282(selected['model'])or selected['request_digest']!=_digest_model282(selected['request']):raise ValueError('MODEL_PREFLIGHT_INPUT_BINDING')
 try:
  for frame in ('local_model','world_model'):
   model=packet.get(frame);rows[frame]={'model_hash':_digest_model282(model),'inventory':m.inspect(model)}
 except (ValueError,KeyError,TypeError,OverflowError,RecursionError)as exc:
  inspection_error={'reason':'MODEL_INSPECTION_UNKNOWN','data_status':'UNKNOWN','error_type':type(exc).__name__,'detail':str(exc),'frames':rows,'fresh_started':False,'fresh_started_semantics':'EVALUATOR_INVOKED_NOT_PROCESS_SPAWN','evaluator_invoked':False,'process_spawned':False,'central_fresh_completed':False,'physical_verdict':'NOT_EVALUATED','geometry_repair_authority':False,'accepted':False,'delivery_allowed':False}
 if before!=_digest_model282(selected)or path.read_bytes()!=data:raise ValueError('MODEL_PREFLIGHT_MUTATION')
 if inspection_error is not None:return inspection_error
 statuses=[v['inventory']['status']for v in rows.values()]
 status='INVALID'if 'INVALID'in statuses else'INCOMPLETE'if 'INCOMPLETE'in statuses else'UNKNOWN'if 'UNKNOWN'in statuses else'COMPLETE_FOR_LISTED_FIELDS'
 return {'reason':'MODEL_DATA_INVALID'if status=='INVALID'else'UNKNOWN_MODEL_DATA_INCOMPLETE'if status=='INCOMPLETE'else'UNKNOWN_UNSUPPORTED_MODEL_DATA'if status=='UNKNOWN'else'MODEL_DATA_PREFLIGHT_READY','data_status':status,'frames':rows,'selected_digest':before,'inventory_sha256':INVENTORY_SHA,'fresh_started':False,'fresh_started_semantics':'EVALUATOR_INVOKED_NOT_PROCESS_SPAWN','evaluator_invoked':False,'process_spawned':False,'central_fresh_completed':False,'physical_verdict':'NOT_EVALUATED','geometry_repair_authority':False,'accepted':False,'delivery_allowed':False}

def _phase293(name):pass # Replaced only by the captured server-owned worker, never request JSON.

def review(selected,seconds=60):
 import time
 started=time.monotonic();evaluator=load()
 _phase293('envelope.begin')
 e=envelope(selected,evaluator) # Binding/source errors remain terminal, not schema UNKNOWN.
 _phase293('envelope.end');_phase293('preflight.begin')
 preflight=model_preflight282(selected)
 _phase293('preflight.end')
 if preflight['data_status']!='COMPLETE_FOR_LISTED_FIELDS':return preflight
 if _digest_model282(selected)!=preflight['selected_digest']:raise ValueError('MODEL_PREFLIGHT_TO_ENVELOPE_MUTATION')
 origin_path=Path(__file__).with_name('origin_join.py');origin_bytes=origin_path.read_bytes()
 if hashlib.sha256(origin_bytes).hexdigest()!='9acdfc577e30744fdbdf3e480750b23e76e9aa24e41bf035e2231f007a8d6368':raise ValueError('PAIR_ORIGIN_JOIN_SOURCE_CHANGED')
 origin=types.ModuleType('_origin267');origin.__file__=str(origin_path);exec(compile(origin_bytes,str(origin_path),'exec'),origin.__dict__)
 region_path=ROOT/'staging239_region_domain/regions.py';region_bytes=region_path.read_bytes()
 if hashlib.sha256(region_bytes).hexdigest()!='4d17da17635445e39f46e14fcf40201304ae6edd0bb954cc056648333962a7f7':raise ValueError('REGION_SOURCE_CHANGED')
 region=types.ModuleType('_region267');region.__file__=str(region_path);exec(compile(region_bytes,str(region_path),'exec'),region.__dict__)
 _group_sources285();_network_sources288()
 source_binding=evaluator.digest({'network288':_digest_model282(NETWORK288_PINS),'groups285':_digest_model282(GROUP285_SOURCE_PINS),'origin':hashlib.sha256(origin_bytes).hexdigest(),'region':hashlib.sha256(region_bytes).hexdigest(),'evaluator':ADAPTER_SHA,'inventory':INVENTORY_SHA})
 session=origin._FixedFreshSession(e,e['producer_revision'],source_binding)
 if hashlib.sha256(Path(__file__).with_name('model_inventory.py').read_bytes()).hexdigest()!=INVENTORY_SHA:raise ValueError('MODEL_INVENTORY_SOURCE_CHANGED')
 remaining=seconds-(time.monotonic()-started)
 if remaining<=0:return dict(preflight,reason="MODEL_PREFLIGHT_DEADLINE",data_status="UNKNOWN")
 _phase293('fresh_evaluate.begin')
 result=evaluator.ProductionEvaluatorAdapter().evaluate(e,remaining_budget_seconds=remaining,cancel_token=threading.Event(),permit_execution=True)
 _phase293('fresh_evaluate.end')
 # Never reuse selector's cached receipt. Require exact freshly checked identity.
 if result.get('candidate_digest')!=evaluator.digest(e):return {'reason':'FRESH_REVIEW_UNBOUND_OR_INCOMPLETE','raw_review':result,'model_preflight':preflight,'fresh_started':True,'fresh_started_semantics':'EVALUATOR_INVOKED_NOT_PROCESS_SPAWN','evaluator_invoked':True,'process_spawned':None,'central_fresh_completed':False,'accepted':False,'delivery_allowed':False}
 _phase293('bind.begin')
 facts=session.bind_after_fixed_evaluator(e,result,source_binding)
 fresh_digest=evaluator.digest(result)
 if fresh_digest!=facts._data['fresh_result_digest']:raise ValueError('POST_FRESH_RESULT_BINDING')
 if hashlib.sha256(Path(__file__).with_name('model_inventory.py').read_bytes()).hexdigest()!=INVENTORY_SHA:raise ValueError('MODEL_INVENTORY_SOURCE_CHANGED')
 _phase293('bind.end');_phase293('groups.begin')
 groups=source_groups285(origin,facts,e,result,source_binding,remaining_seconds=max(0,seconds-(time.monotonic()-started)))
 _phase293('groups.end');_phase293('region239.begin')
 native={}
 for frame in('local_model','world_model'):
  origin.verify_native_immutability(facts,e,source_binding)
  if evaluator.digest(result)!=fresh_digest or _digest_model282(selected)!=preflight['selected_digest']:raise ValueError('FRESH_OR_SELECTED_MUTATION')
  native[frame]={'model_digest':evaluator.digest(e['packet'][frame]),'evaluation':region.evaluate(e['packet'][frame],remaining_budget_seconds=2),'scope':'DECLARED_REGION_DOMAIN239_ONLY_NOT_FULL_NATIVE_OR_H03'}
  origin.verify_native_immutability(facts,e,source_binding)
  if evaluator.digest(result)!=fresh_digest or _digest_model282(selected)!=preflight['selected_digest']:raise ValueError('FRESH_OR_SELECTED_MUTATION')
 _phase293('region239.end')
 return {'source_groups285':groups,'current_review_status':groups['review_verdict'],'review_stop_reason':groups['stop_reason'],'model_preflight':preflight,'fresh_started':True,'fresh_started_semantics':'EVALUATOR_INVOKED_NOT_PROCESS_SPAWN','evaluator_invoked':True,'process_spawned':True,'central_envelope':e,'native_scoped_region239':native,'origin_binding':facts.private_summary(),'schema':'SELECTED_PROGRAM_FRESH267','request_digest':selected['request_digest'],'model_digest':selected['model_digest'],'central_fresh_review':result,'central_fresh_completed':True,'current_native_review':'REGION239_EIGHT_SOURCE_GROUPS_AND_STORED_NETWORK_FULL_NATIVE_UNKNOWN','redesign':'UNKNOWN_NO_PAIR_PROGRAM_PRESERVING_OPERATOR'if selected['family']=='PAIR_2_OR_1'else'UNKNOWN_SERVICE_OPERATOR_NOT_CONNECTED_TO_SELECTED_RESULT','accepted':False,'delivery_allowed':False}

GROUP285_SOURCE_PINS={'named_checks118.py': 'e8a846186900c5fb1597defde9186ffb39a83ad0310cc96c90d462c8ae924002', 'rule_contract118.py': '970b45b413f02be0d4c470bd582a6451fd64ec39155506c0c3b6d23d3083fa83', 'rule_contract118.json': 'b286c31d09fd58b962e0af1a81ee0e5c79c43c17271c40580ff6ee5b7ce3a1ac', 'checker114.py': '30de230316e9f3856433961651326f362ffe98ee7ceec4e813eb0bde1a7d1a02', 'operation_check114.py': 'ac73b6a13c73f60c513de19c5faa60fb6a9f445e4ad4b2f836fd945df006ce6b', 'partition_audit118.py': '373c924c15f8bf4ba687ac0e48185c201e2140421059b322f5c429f28124e41c', 'program_capacity_audit118.py': '6bc9e739abe05d4606a5c026537c8f37ae76bc9e714ba91022191784cdc0c8ba', 'public_program_audit118.py': 'aa282091606bbdfc3cd91b58567d2757edb6f2959ce8c0fbc62d593af4f82c99'}
GROUP285_SOURCE_PINS.update({'privacy116.py': 'c0636bc7b1a42833bfc19e40718723d8db1002a94d99ce8e0426695331fd79f7', 'privacy115.py': '5526b1d9c4339f6ca79272645364299b101e7de1d7cea3ba4ac94498e740bf6e', 'q11_boundary118.py': '4a7f86ac4d3b088f465435a8b2d0e03df239d20ce2c55018e3ea14fe549d384c'})
GROUP285_IDS=('partition_ledger','door_operation','fixture_inventory_use','closet_operation','kitchen_essential_operation','bath_service_operation','program_functional_roles','privacy_scenarios')
def _group_sources285():
 # Compile declarations only to obtain the identical inspect.getsource domain;
 # never invoke a source checker or import its transitive runtime here.
 import ast,inspect
 app=ROOT/'planha_general150_runtime_work';captured={}
 for name,sha in GROUP285_SOURCE_PINS.items():
  data=(app/name).read_bytes()
  if hashlib.sha256(data).hexdigest()!=sha:raise ValueError('GROUP285_SOURCE_CHANGED:'+name)
  captured[name]=data
 contract=json.loads(captured['rule_contract118.json']);text=captured['named_checks118.py'].decode();tree=ast.parse(text);methods={}
 for node in tree.body:
  if isinstance(node,ast.FunctionDef)and node.name in GROUP285_IDS:
   if node.decorator_list:raise ValueError('GROUP285_UNSUPPORTED_METHOD_WRAPPER')
   ns={'__name__':'named_checks118'}
   exec(compile(ast.Module(body=[node],type_ignores=[]),str(app/'named_checks118.py'),'exec'),ns)
   lines,start=inspect.getsourcelines(ns[node.name]);src=''.join(lines)
   if src!=''.join(text.splitlines(True)[start-1:start-1+len(lines)]):raise ValueError('GROUP285_SOURCE_CACHE_DRIFT')
   methods[node.name]={'name':'named_checks118.'+node.name,'code_sha256':hashlib.sha256(src.encode()).hexdigest()}
 if set(methods)!=set(GROUP285_IDS):raise ValueError('GROUP285_METHOD_INVENTORY')
 for name,data in captured.items():
  if (app/name).read_bytes()!=data:raise ValueError('GROUP285_SOURCE_MUTATION')
 return contract,methods

def source_groups285(origin,facts,envelope,result,source_binding,*,remaining_seconds=2):
 import time
 group_started=time.monotonic()
 # Only the fixed fresh callsite passes its sealed Origin and result here.
 origin.verify_native_immutability(facts,envelope,source_binding)
 full_digest=_digest_model282(result)
 if facts._data['fresh_result_digest']!=full_digest:raise ValueError('GROUP285_FRESH_DIGEST')
 contract,methods=_group_sources285();model=envelope['packet']['world_model'];mh=_digest_model282(model)
 if facts._data['world_model_hash']!=mh:raise ValueError('GROUP285_FRAME_BINDING')
 raw=result['raw_fresh_report'];audit=raw.get('rule_contract_evidence')
 ch=GROUP285_SOURCE_PINS['rule_contract118.json'];summaries=[]
 def require(ok,reason):
  if not ok:raise ValueError('GROUP285_'+reason)
 def exact(a,b):return _digest_model282(a)==_digest_model282(b)
 def lists(x):return type(x)is dict and type(x.get('errors'))is list and type(x.get('pending'))is list
 def clean_result(x):return lists(x)and x['errors']==[]and x['pending']==[]
 def placement(p):
  require(clean_result(p)and type(p.get('evidence'))is list,'PLACEMENT_SHAPE')
  expected=[{'unit':v['unit_id'],'room':v['room_id'],'module_hash':_digest_model282(v['module'])}for v in model.get('module_placements',[])]
  got=[{k:v.get(k)for k in ('unit','room','module_hash')}for v in p['evidence']]
  require(exact(got,expected),'PLACEMENT_INVENTORY')
  require(p.get('whole_model_pass')is False,'PLACEMENT_SCOPE')
  require(p.get('status')=='PASS_PLACEMENT_SCOPED'and all(v.get('local_status')=='PASS_MODULE_SCOPED'for v in p['evidence']),'PLACEMENT_STATUS')
 def operation(w,component):
  require(w.get('model_hash')==mh and w.get('operation_component')==component,'OPERATION_BINDING')
  expected=[o.get('opening_id',o.get('fixture_id',o.get('unit')))for o in model['operations'].get(component,[])]
  require(exact(w.get('actual_operation_ids'),expected),'OPERATION_INVENTORY')
 def bath(w):
  require(type(w.get('modules'))is list,'BATH_SHAPE');placement(w.get('placement'))
  expected=[_digest_model282(v['module'])for v in model.get('module_placements',[])if v['module'].get('schema')=='BATHROOM_MODULE117']
  require(exact([v.get('module_hash')for v in w['modules']],expected),'BATH_INVENTORY')
  require(all(v.get('status')=='PASS_MODULE_SCOPED'and clean_result(v)for v in w['modules']),'BATH_STATUS')
 def capacity(c):
  require(clean_result(c)and type(c.get('evidence'))is dict,'CAPACITY_SHAPE')
  require(c['evidence'].get('model_hash')==mh,'CAPACITY_MODEL')
 def privacy(w):
  p=w.get('privacy')
  if not lists(p)or type(p.get('evidence'))is not dict or type(w.get('actual_private_rooms'))is not list:return False
  require(clean_result(p),'PRIVACY_PENDING_OR_ERRORS')
  pe=p['evidence'];require(pe.get('whole_model_hash')==mh,'PRIVACY_WHOLE_MODEL')
  require(pe.get('status')=='PASS_SCOPED_PRIVACY'and pe.get('accepted')is False,'PRIVACY_SCOPE_STATUS')
  targets=pe.get('targets')
  if type(targets)is not list:return False
  expected=sorted((u['id'],room)for u in model['units']for room in u['rooms']if room.startswith('bed')or room=='bath')
  require(exact(w['actual_private_rooms'],[list(x)for x in expected]),'PRIVACY_DECLARED_ROOM_INVENTORY')
  require(all(type(t)is dict for t in targets),'PRIVACY_TARGET_SHAPE')
  require(exact(sorted([[t.get('unit'),t.get('room')]for t in targets]),[list(x)for x in expected]),'PRIVACY_ACTUAL_ROOM_INVENTORY')
  placement(w.get('placement'))
  units={u['id']:u for u in model['units']}
  for t in targets:
   uid=t['unit'];room=t['room'];u=units[uid]
   openings=[o['id']for o in model['openings']if uid+'.'+room in o['connects']]
   if room=='bath':
    require(t.get('kind')=='actual_necessary_inner_boundary_face','PRIVACY_BATH_KIND');records=t.get('evidence');names=['WC_use','shower_use','shower_floor']
    expected_pairs=[(name,oid)for name in names for oid in openings]
   else:
    require(t.get('kind')=='full_actual_aperture_strict_bedroom','PRIVACY_SLEEP_KIND');bed=t.get('evidence')
    if type(bed)is not dict:return False
    require(bed.get('status')=='PASS_SCOPED_MODULE_PRIVACY'and bed.get('accepted')is False and bed.get('release_allowed')is False,'PRIVACY_SLEEP_SCOPE')
    require(bed.get('checker_sha256')==GROUP285_SOURCE_PINS['privacy116.py'],'PRIVACY_SLEEP_CHECKER')
    records=bed.get('targets');names=[k for k in u['fixtures']if k.startswith(room+'.')and u['fixture_metadata'].get(k,{}).get('kind')in('bed','single_bed')]+['changing']
    expected_pairs=[(name,oid)for oid in openings for name in names]
   if type(records)is not list:return False
   require(all(type(v)is dict for v in records),'PRIVACY_CERTIFICATE_ROWS')
   require(exact([[v.get('target'),v.get('opening')]for v in records],[list(x)for x in expected_pairs]),'PRIVACY_TARGET_APERTURE_INVENTORY')
   for v in records:
    require('counterexample'in v and v['counterexample']is None,'PRIVACY_COUNTEREXAMPLE')
    if room=='bath':
     cert=v.get('strict')or v.get('conditional_closed_boundary');require(type(v.get('necessary_actual_boundary_face'))is list and len(v['necessary_actual_boundary_face'])==4,'PRIVACY_BOUNDARY_FACE')
     require(type(cert)is dict and cert.get('conditional_closed_boundary')is (False if v.get('strict')is not None else True),'PRIVACY_BATH_CERTIFICATE')
    else:
     cert=v.get('strict_certificate');require(type(cert)is dict and cert.get('conditional_closed_boundary')is False,'PRIVACY_STRICT_CERTIFICATE')
    # Certificate structure only; no separator/sightline geometry recomputation.
    require(type(cert.get('wall'))is str and bool(cert['wall'])and type(cert.get('axis'))is int and cert['axis']in(0,1)and type(cert.get('projected_interval'))is list and len(cert['projected_interval'])==2,'PRIVACY_CERTIFICATE_SHAPE')
    from fractions import Fraction
    values=[cert.get('plane'),*cert['projected_interval']]+(v['necessary_actual_boundary_face']if room=='bath'else[])
    require(all(type(x)in(str,int)for x in values),'PRIVACY_CERTIFICATE_NUMBERS')
    try:[Fraction(x)for x in values]
    except (ValueError,ZeroDivisionError):raise ValueError('GROUP285_PRIVACY_CERTIFICATE_NUMBERS')
  return True
 if audit is None:
  rows=[]
 else:
  require(type(audit)is dict and audit.get('model_hash')==mh and audit.get('contract_hash')==ch and audit.get('contract_schema')==contract['schema'],'CONTRACT_BINDING')
  rows=audit.get('requirements');require(type(rows)is list,'ROWS_SHAPE')
 requirements={v['id']:v for v in contract['requirements']}
 for rid in GROUP285_IDS:
  matches=[(i,v)for i,v in enumerate(rows)if type(v)is dict and v.get('requirement_id')==rid]
  require(len(matches)<=1,'DUPLICATE_ROW:'+rid)
  if not matches:
   summaries.append({'requirement_id':rid,'verdict':'UNKNOWN','reason':'NAMED_ROW_MISSING'});continue
  index,row=matches[0];spec=requirements[rid]
  require(row.get('mandatory')is True and spec.get('mandatory',True)is True and exact(row.get('source_rule_ids'),spec['source_rule_ids']),'RULE_SCOPE:'+rid)
  require(spec['condition']=='always'and row.get('applicability')=={'condition':'always'},'APPLICABILITY:'+rid)
  status=row.get('status');require(status in ('PASS_LIMITED','FAIL','NOT_EVALUATED'),'STATUS:'+rid)
  if 'method'not in row and status=='NOT_EVALUATED':
   summaries.append({'requirement_id':rid,'verdict':'UNKNOWN','reason':'NAMED_METHOD_UNAVAILABLE','row_index':index,'row_hash':_digest_model282(row)});continue
  require(row.get('model_hash')==mh and row.get('contract_hash')==ch and exact(row.get('method'),methods[rid]),'METHOD_MODEL_BINDING:'+rid)
  ev=row.get('evidence');require(type(ev)is dict and ev.get('status')==status and type(ev.get('witness'))is dict and type(ev.get('scope'))is str and bool(ev['scope']),'EVIDENCE_SHAPE:'+rid)
  w=ev['witness'];verdict='FAIL'if status=='FAIL'else'UNKNOWN'
  if status=='PASS_LIMITED':
   require(clean_result(w),'CONTRADICTORY_PASS:'+rid)
   if rid in ('door_operation','closet_operation','kitchen_essential_operation'):
    operation(w,{'door_operation':'doors','closet_operation':'closets','kitchen_essential_operation':'kitchen'}[rid])
   elif rid=='bath_service_operation':bath(w)
   elif rid=='partition_ledger':
    require(w.get('model_hash')==mh and type(w.get('groups'))is list and type(w.get('exact_role_cells'))is int and w['exact_role_cells']>=0,'PARTITION_SHAPE')
    expected=[{'role':g['role'],'regions':len(g['regions'])}for g in model['spatial_accounting']['plot_partition']]
    require(exact([{k:g.get(k)for k in ('role','regions')}for g in w['groups']],expected),'PARTITION_INVENTORY')
    from fractions import Fraction
    for got,given in zip(w['groups'],model['spatial_accounting']['plot_partition']):
     require(type(got.get('area_m2'))in(str,int)and type(given.get('area_m2'))in(str,int)and Fraction(got['area_m2'])==Fraction(given['area_m2']),'PARTITION_AREA_BINDING')
    require(w.get('declared_footprints_are_not_capacity_proof')is True,'PARTITION_SCOPE')
   elif rid=='fixture_inventory_use':
    capacity(w.get('capacity'));placement(w.get('source_placement'));sub=w.get('fresh_functional_components')
    require(type(sub)is list and len(sub)==5,'FUNCTIONAL_COMPONENTS_SHAPE')
    for x in sub:require(type(x)is dict and x.get('status')=='PASS_LIMITED'and clean_result(x.get('witness')),'FUNCTIONAL_COMPONENT_STATUS')
    for x,comp in zip(sub[:3],('doors','closets','kitchen')):operation(x['witness'],comp)
    bath(sub[3]['witness'])
   elif rid=='program_functional_roles':
    capacity(w.get('actual_capacity'));pub=w.get('public_scenarios');require(clean_result(pub)and type(pub.get('evidence'))is dict and pub['evidence'].get('model_hash')==mh,'PUBLIC_SCENARIO_BINDING')
    wet=w.get('wet_service');access=w.get('nonprivate_wet_access')
    require(type(wet)is dict and wet.get('status')=='PASS_LIMITED'and clean_result(wet.get('witness')),'WET_SHAPE');bath(wet['witness'])
    require(type(access)is dict and access.get('status')=='PASS_LIMITED'and clean_result(access.get('witness'))and access['witness'].get('model_hash')==mh,'WET_ACCESS_BINDING')
   elif rid=='privacy_scenarios':
    if not privacy(w):
     summaries.append({'requirement_id':rid,'verdict':'UNKNOWN','reason':'PRIVACY_WITNESS_COVERAGE_MISSING','row_index':index,'row_hash':_digest_model282(row)});continue
   verdict='SCOPED_PASS'
  summaries.append({'requirement_id':rid,'verdict':verdict,'source_status':status,'scope':ev['scope'],'row_index':index,'row_path':'/raw_fresh_report/rule_contract_evidence/requirements/'+str(index),'row_hash':_digest_model282(row),'witness_hash':_digest_model282(w)})
 _phase293('network.begin')
 network=_network288(envelope,result,summaries,remaining_seconds-(time.monotonic()-group_started))
 _phase293('network.end')
 summaries.append(network)
 state='FAIL'if any(r['verdict']=='FAIL'for r in summaries)else'UNKNOWN'if any(r['verdict']=='UNKNOWN'for r in summaries)else'SCOPED_PASS'
 local_same=_digest_model282(envelope['packet']['local_model'])==mh
 review_state=state if local_same or state=='FAIL'else'UNKNOWN'
 origin.verify_native_immutability(facts,envelope,source_binding)
 require(_digest_model282(result)==full_digest,'RESULT_MUTATED')
 _group_sources285() # captured source identity still exact; no checker invocation
 return {'schema':'SAME_FRESH_SOURCE_GROUPS285','review_verdict':review_state,'world_verdict':state,'local_verdict':state if local_same else'UNKNOWN','local_scope':'EXACT_MODEL_IDENTITY_ALIAS_NO_SECOND_EXECUTION'if local_same else'NO_LOCAL_SOURCE_WITNESS_REUSE','rows':summaries,'model_hash':mh,'fresh_result_digest':full_digest,'source_pins_digest':_digest_model282(GROUP285_SOURCE_PINS),'scope':'EIGHT_SOURCE_SUBCLAIMS_AND_STORED_NETWORK_NOT_WHOLE_LIVING_Q11_IRP12','repair_authority':False,'parent_complete':False,'delivery_allowed':False,'stop_reason':None if review_state=='SCOPED_PASS'else'SOURCE_GROUPS285_'+review_state}

NETWORK288_PINS={'staging251_geometry/native_adapter.py': '26648a546e551737d58df2f4441c8ffa37203e0cb18a46d54823c38b4bf825b1', 'staging250_guest_serving_v2/source_checks.py': '1fc2cc79ce431137d9083f7d81d08824d0d908b671abed4d8ffa288ce2bbd09d', 'planha_general150_runtime_work/public_program_audit118.py': 'aa282091606bbdfc3cd91b58567d2757edb6f2959ce8c0fbc62d593af4f82c99', 'planha_general150_runtime_work/public_witness118.py': 'abef67400f88999dc3878e16b046ce47a8f8747b546ff25f85010e39f669b8f5', 'planha_general150_runtime_work/entry117.py': '01acc8c99e0c56b7e60f67a44ea399b8f2e1fabaa3fd9343e51f2b046ccd7d65', 'planha_general150_runtime_work/contract114.py': '8fa52a9d992cd078e7dd3356bab61de7b9687d60a4ae52fc403a3e0b2203dbcf', 'planha_general150_runtime_work/world_transform125.py': 'fa301aadbf7cf006bc030464cf6ad8ed34d13f7347a20ccad69a7838e6f40b55', 'planha_general150_runtime_work/assemble114.py': 'b12cf81eb0acdfd5c696445fe7821235012f589cac9477b865da89093c0b095e'}
def _network_sources288():
 captured={}
 for name,sha in NETWORK288_PINS.items():
  data=(ROOT/name).read_bytes()
  if hashlib.sha256(data).hexdigest()!=sha:raise ValueError('NETWORK288_SOURCE_CHANGED:'+name)
  captured[name]=data
 return captured

def _network288(envelope,result,prerequisites,remaining_seconds):
 """Same live-Origin callsite only. Reuse exact graph247; no checker/issuer."""
 import ast,time
 from fractions import Fraction as F
 from decimal import Decimal,localcontext
 start=time.monotonic();captured=_network_sources288()
 out={'requirement_id':'stored_living_network288','verdict':'UNKNOWN','scope':'GUEST_ROOT_TO_ALL_STORED_LIVING_STANDING_TARGETS_ONLY','rows':[],'repair_authority':False,'whole_living_extent_verified':False,'whole_Q11_IRP12':False,'source_pins_digest':_digest_model282(NETWORK288_PINS)}
 def tick():
  if type(remaining_seconds)not in(int,float)or remaining_seconds<=0 or time.monotonic()-start>=min(2,remaining_seconds):raise ValueError('NETWORK288_REMAINING_DEADLINE')
 def funcs(name,names,ns,constants=False):
  raw=captured[name];tree=ast.parse(raw);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in names or constants and isinstance(n,ast.Assign)and all(isinstance(t,ast.Name)and t.id.endswith('_KEYS')for t in n.targets)]
  if {n.name for n in nodes if isinstance(n,ast.FunctionDef)}!=set(names):raise ValueError('NETWORK288_SOURCE_FUNCTION_MISSING')
  exec(compile(ast.Module(body=nodes,type_ignores=[]),str(ROOT/name),'exec'),ns)
  return ns
 try:
  tick()
  if any(r['verdict']!='SCOPED_PASS'for r in prerequisites):raise ValueError('NETWORK288_SAMEFRESH_PREREQUISITES_UNPROVEN')
  pkt=envelope['packet'];model=pkt['world_model'];core=pkt['core'];family=pkt['family'];mh=_digest_model282(model)
  # Core is part of Origin267 trace and independently verified constructor replay.
  ns={'F':F,'Decimal':Decimal,'localcontext':localcontext,'deepcopy':copy.deepcopy}
  funcs('planha_general150_runtime_work/contract114.py',['S'],ns)
  funcs('planha_general150_runtime_work/public_program_audit118.py',['q','hit','covered'],ns)
  ns['Q']=ns['q'];funcs('planha_general150_runtime_work/entry117.py',['install'],ns)
  funcs('planha_general150_runtime_work/world_transform125.py',['point','rect','geometry','canonical','placement'],ns,True)
  funcs('staging251_geometry/native_adapter.py',['_stored_seat_graph247'],ns)
  if family not in('FRONT_REAR','LEFT_RIGHT'):raise ValueError('NETWORK288_UNSUPPORTED_FRAME')
  swapped=family=='LEFT_RIGHT'
  if swapped and core.get('world_from_local')!={'matrix':[[0,1],[1,0]],'translation':['0','0']}:raise ValueError('NETWORK288_FRAME_BINDING')
  units=model['units']
  if sorted(u['id']for u in units)!=['A','B']:raise ValueError('NETWORK288_UNIT_INVENTORY')
  rows=result['raw_fresh_report']['rule_contract_evidence']['requirements']
  w=next(r for r in rows if r['requirement_id']=='program_functional_roles')['evidence']['witness']
  ce=w['actual_capacity']['evidence'];pub=w['public_scenarios']['evidence']
  if ce.get('status')!='PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY'or ce.get('model_hash')!=mh or pub.get('status')!='PASS_PUBLIC_SCOPED'or pub.get('model_hash')!=mh:raise ValueError('NETWORK288_SOURCE_CAPACITY_PUBLIC_STATUS')
  if sorted(x['unit']for x in ce['units'])!=['A','B']:raise ValueError('NETWORK288_CAPACITY_UNIT_INVENTORY')
  for u in units:
   tick();uid=u['id'];owner=core.get('unit_ownership',{}).get(uid,[core['units'][uid]])
   wantowner=[ns['rect'](r)for r in owner]if swapped else owner
   eq=lambda a,b:_digest_model282(a)==_digest_model282(b)
   # Numeric representation equality is source rational, never trimming identifiers.
   if [ns['q'](r)for r in u['ownership']]!=[ns['q'](r)for r in wantowner]:raise ValueError('NETWORK288_CORE_OWNERSHIP')
   cx=F(core['entry_centers']['A'][0]);y=F(core['band'][1]);yt=F(core['band'][3]);box=list(map(F,owner[0]));lo,hi=(y-F('.15'),y)if uid=='A'else(yt,yt+F('.15'))
   root=[cx,box[3]-F('.4')if uid=='A'else box[1]+F('.4')]
   opening={'id':uid+'.entry','rect':list(map(str,(cx-F('.65'),lo,cx+F('.65'),hi))),'host_wall_id':uid+'.unit_boundary','connects':['lobby',uid+'.entry_circulation'],'operation_kind':'sliding_study','operation_witness_status':'NOT_EVALUATED'}
   scratch={'openings':[opening]};ns['install'](scratch)
   wantopen=scratch['openings'][0];wantop=scratch['operations']['doors'][0]
   if swapped:root=ns['point'](root);wantopen=ns['geometry'](wantopen);wantop=ns['geometry'](wantop)
   # Source strings can be decimal or rational; structural numeric comparison.
   def same(a,b):
    if type(a)is dict:return type(b)is dict and set(a)==set(b)and all(same(a[k],b[k])for k in a)
    if type(a)is list:return type(b)is list and len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    if type(a)is str and type(b)is str:
     try:return F(a)==F(b)
     except(ValueError,ZeroDivisionError):return a==b
    return type(a)is type(b)and a==b
   opens=[o for o in model['openings']if o['id']==uid+'.entry'];ops=[o for o in model['operations']['doors']if o.get('opening_id')==uid+'.entry']
   if len(opens)!=1 or len(ops)!=1 or not same(opens[0],wantopen)or not same(ops[0],wantop):raise ValueError('NETWORK288_SOURCE_ENTRY_INSTALLATION')
   cap=u['public_program']['capacity'];seats=cap['living_seats'];crow=next(x for x in ce['units']if x['unit']==uid)
   if crow['living_occupied_instances']!=len(seats)or crow['actual_places']['living_seats']!=sum(s['places']for s in seats):raise ValueError('NETWORK288_CAPACITY_INVENTORY')
   source=types.SimpleNamespace(**ns);row=ns['_stored_seat_graph247'](model,u,root,source,tick)
   row['model_hash']=mh;out['rows'].append(row)
  out['verdict']='SCOPED_PASS'if all(r['verdict']=='PASS_STORED_SOURCE_ROUTE_NETWORK_SCOPED'for r in out['rows'])else'UNKNOWN'
  out['reason']=None if out['verdict']=='SCOPED_PASS'else'STORED_NETWORK_INCOMPLETE_NOT_GLOBAL_INFEASIBILITY'
 except(ValueError,KeyError,TypeError,IndexError,StopIteration,ZeroDivisionError,OverflowError)as exc:
  out['reason']='NETWORK288_UNVERIFIED:'+str(exc)
 if _network_sources288()!=captured:raise ValueError('NETWORK288_SOURCE_MUTATION')
 return out
