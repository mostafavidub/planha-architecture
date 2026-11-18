"""JOINT367 prepared closed dispatcher. Requires own frozen modules and audited closures; no delivery or fresh authority."""
import builtins,hashlib,json,types,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
RULE_IDS=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY','DISTINCTNESS_AND_FAIRNESS')
def evaluate(model,raw,*,post_fresh=None,source_profile='SOURCE_JOINT367',registered_artifact=None):
 manifest_bytes=(HERE/'frozen_modules367_v4.json').read_bytes();manifest=json.loads(manifest_bytes);loaded={}
 def check_outer_sources():
  if (HERE/'frozen_modules367_v4.json').read_bytes()!=manifest_bytes:raise ValueError('OUTER_MANIFEST_CHANGED')
  for name,sha in manifest['files'].items():
   if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=sha:raise ValueError('OUTER_SOURCE_CHANGED:'+name)
 check_outer_sources()
 def load(name):
  if name in loaded:return loaded[name]
  filename=name+'.py';data=(HERE/filename).read_bytes()
  if hashlib.sha256(data).hexdigest()!=manifest['files'].get(filename):raise ValueError('MODULE_SOURCE_CHANGED:'+name)
  mod=types.ModuleType(name);mod.__file__=str(HERE/filename)
  def imp(n,g=None,l=None,fromlist=(),level=0):
   if level==0 and n+'.py' in manifest['files']:return load(n)
   return builtins.__import__(n,g,l,fromlist,level)
  mod.__dict__['__builtins__']={**vars(builtins),'__import__':imp};loaded[name]=mod
  exec(compile(data,mod.__file__,'exec'),mod.__dict__);return mod
 common=load('common')
 registries={'SOURCE_JOINT367':'method_registry_source367.json'}
 if source_profile not in registries:raise ValueError('UNREGISTERED_SOURCE_PROFILE')
 registry_name=registries[source_profile];common.REGISTRY_NAME=registry_name
 registry=(HERE/registry_name).read_bytes()
 if hashlib.sha256(registry).hexdigest()!=manifest['files'].get(registry_name):raise ValueError('REGISTRY_SOURCE_CHANGED')
 before=common.digest([model,raw]);out={};closures={};registered=False
 try:
  common.rows(model,raw)
  if registered_artifact is not None:
   if post_fresh is not None or type(registered_artifact)is not dict or set(registered_artifact)!={'record','result'}:raise ValueError('CLOSED_REGISTERED_ARTIFACT_INPUT')
   view=load('group_readsets367').build(registered_artifact['record'],registered_artifact['result'],source_profile=source_profile,seconds=8)
   post_fresh={k:view[k]for k in ('envelope','result','groups')};post_fresh['seconds']=10
   author_bytes=(HERE/'author_source.json').read_bytes()
   if hashlib.sha256(author_bytes).hexdigest()!=manifest['files']['author_source.json']:raise ValueError('AUTHOR_MANIFEST_CHANGED')
   author=json.loads(author_bytes);workspace=HERE.parents[1]
   if hashlib.sha256((workspace/'owner_four_steps233.html').read_bytes()).hexdigest()!=author['html_sha256']or hashlib.sha256((workspace/'recovered233_rendered/sections.json').read_bytes()).hexdigest()!=author['sections_sha256']:raise ValueError('AUTHOR_SOURCE_CHANGED')
   registered=True
  for module in ('modules_structure','modules_spatial','modules_comparison'):
   for rid,res in load(module).evaluate(model,raw).items():
    if rid in out or rid not in RULE_IDS:raise ValueError('DISPATCH_ID')
    if res['verdict']=='PASS' and res.get('missing'):raise ValueError('PASS_WITH_MISSING')
    out[rid]=res
  if set(out)!=set(RULE_IDS):raise ValueError('DISPATCH_INCOMPLETE')
  opening=load('closure_openings').evaluate(model,raw);closures['openings']=opening
  out['OPENINGS_REAL']['source_closure']=opening
  if post_fresh is not None:
   if type(post_fresh)is not dict or set(post_fresh)!={'envelope','result','groups','seconds'}:raise ValueError('CLOSED_POST_FRESH_CONTEXT')
   env,res,groups=(post_fresh[k]for k in ('envelope','result','groups'));budget=post_fresh['seconds']
   if type(budget)not in(int,float)or not 0<budget<=10:raise ValueError('POST_FRESH_BUDGET')
   if common.digest(env['packet']['world_model'])!=common.digest(model) or common.digest(res['raw_fresh_report'])!=common.digest(raw):raise ValueError('POST_FRESH_MODEL_RAW_BINDING')
   deadline=time.monotonic()+budget
   for name in ('living_closure','guest_closure','kitchen_closure'):
    remaining=deadline-time.monotonic()
    if remaining<=0:closures[name]={'verdict':'UNKNOWN','missing':['POST_FRESH_BUDGET_EXHAUSTED']};continue
    c=load(name+'367').evaluate(env,res,groups,seconds=min(remaining,8));closures[name]=c
    # Intrinsic scoped positives are evidence only until authoritative parent
    # applicability and every required subclaim are independently closed.
    rid=c.get('rule_id')
    if rid in out:out[rid]['reconstructed_source_closure']=c

 except (ValueError,KeyError,TypeError) as e:
  out={k:common.result(codes=['BINDING_OR_DISPATCH_BLOCKED',str(e)],missing=['VERIFIED_SOURCE_INPUT'])for k in RULE_IDS}
 if registered and closures.get('openings',{}).get('scope_complete')is True and closures['openings'].get('codes')==[] and closures['openings'].get('missing')==['INDEPENDENT_AUDIT_BEFORE_PARENT_ENABLE'] and not any(v.get('codes',[None])[0:1]==['BINDING_OR_DISPATCH_BLOCKED']for v in out.values()):
  out['OPENINGS_REAL']={'verdict':'PASS','codes':['CURRENT_REGISTERED_SOURCE_OPENING_PROFILE_COMPLETE'],'missing':[],'scope':'Source233 H08/H10/H11 opening-host, aperture, window geometry and required source operation profile only; no technical core or light/ventilation approval','source_closure':closures['openings'],'contract_source_sha256':author['html_sha256'],'model_hash':common.digest(model),'artifact_reassessment_only':True}
 if registered and not any(v.get('codes',[None])[0:1]==['BINDING_OR_DISPATCH_BLOCKED']for v in out.values()):
  spatial_mapping=load('author233_spatial_mapping').evaluate(post_fresh['envelope'],closures.get('living_closure',{}),closures.get('guest_closure',{}))
  if spatial_mapping['source_html_sha256']!=author['html_sha256']or spatial_mapping['extracted_sections_sha256']!=author['sections_sha256']:raise ValueError('AUTHOR_MAPPING_BINDING')
  for parent,rule,closure,scope in (
   ('LIVING_USEFUL_CONTIGUITY','Q02','living_closure','Required source seating/use/access connected by verified source body sweeps; no whole residual-use or aesthetic optimum claim; R-LIV exact trigger N_A'),
   ('GUEST_ROUTE_INDEPENDENCE','Q06','guest_closure','All four required source guest relations per unit, complete source private exclusion and conservative source kitchen operations; source open-transit profile only; H07 separate')):
   mapping=spatial_mapping['rules'][rule]
   if mapping.get('audit_recommendation')=='ELIGIBLE_CURRENT_PROFILE_PARENT_CLOSURE_PENDING_INDEPENDENT_AUDIT':
    out[parent]={'verdict':'PASS','codes':['CURRENT_REGISTERED_SOURCE_PROFILE_COMPLETE'],'missing':[],'scope':scope,'source_closure':closures[closure],'source_mapping':mapping,'contract_source_sha256':author['html_sha256'],'model_hash':common.digest(model),'artifact_reassessment_only':True}
  kitchen=closures.get('kitchen_closure',{})
  if kitchen.get('verdict')=='PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS' and kitchen.get('evidence',{}).get('model_hash')==common.digest(model):
   out['KITCHEN_PROXIMITY']={'verdict':'PASS','codes':['CURRENT_REGISTERED_ESSENTIAL_KITCHEN_USE_COMPLETE'],'missing':[],'scope':'Q07 required source cooking-to-dining and living essential-use relations with protected guest/private access; sequential source operation profile; optional proximity ranking not claimed','source_closure':kitchen,'contract_source_sha256':author['html_sha256'],'model_hash':common.digest(model),'artifact_reassessment_only':True}
  room=load('closure_room_program367').evaluate(registered_artifact['record'],registered_artifact['result'],source_profile='SOURCE_JOINT367');closures['room']=room
  if room.get('proofscopecomplete')is True and room.get('missing')==[] and room.get('evidence',{}).get('model_hash')==common.digest(model)and room.get('evidence',{}).get('raw_hash')==common.digest(raw):
   out['ROOM_PROGRAM_CAPACITY']={'verdict':'PASS','codes':['CURRENT_REGISTERED_REQUIRED_PROGRAM_COMPLETE'],'missing':[],'scope':'H12/H13/Q01 current source required bedroom/closet/program counts, rigid assets, usable operations and access per unit; R-LIV trigger N_A; no IR-P13 comparative grouping or alternative furnishing optimum claim','source_closure':room,'contract_source_sha256':author['html_sha256'],'model_hash':common.digest(model),'artifact_reassessment_only':True}
 for rid in ('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','DISTINCTNESS_AND_FAIRNESS'):
  if registered:
   out[rid]={'verdict':'UNKNOWN','codes':['OWN_JOINT_CANDIDATE_PROOF_NOT_INTEGRATED'],'missing':['CURRENT_JOINT367_REQUIRED_ROLE_COMPARISON_OR_SELECTION_PROOF'],'model_hash':common.digest(model)}
 if registered and not any(v.get('codes',[None])[0:1]==['BINDING_OR_DISPATCH_BLOCKED']for v in out.values()):
  try:
   grouping=load('bedroom_grouping367').evaluate(registered_artifact['record'],registered_artifact['result']);closures['bedroom_grouping']=grouping
   proof=grouping.get('evidence',{})
   if grouping.get('verdict')=='PASS_SCOPED_REVIEWED_TRADEOFF_PENDING_AUDIT' and grouping.get('proofscopecomplete')is True and grouping.get('missing')==['INDEPENDENT_SCOPE_AUDIT_PENDING'] and proof.get('model_digest')==common.digest(model) and proof.get('record_digest')==common.digest(registered_artifact['record']) and proof.get('result_digest')==common.digest(registered_artifact['result']):
    out['BEDROOM_GROUPING']={'verdict':'PASS','codes':['OWN_JOINT_IRP13_FINITE_REVIEW_INDEPENDENTLY_AUDITED'],'missing':[],'scope':grouping['scope'],'source_closure':grouping,'model_hash':common.digest(model),'artifact_reassessment_only':True,'independent_audit_basis':'Source module sections and 100 own-source task paths; two exact-source-module local longitudinal privacy counterexamples; explicit per-unit smaller-room and route tradeoffs. Historical pending-audit receipt preserved. Not dominance, all alternatives, or nonshrink repair.'}
  except Exception as error:
   out['BEDROOM_GROUPING']={'verdict':'UNKNOWN','codes':['OWN_JOINT_GROUPING_FAILED_CLOSED',type(error).__name__],'missing':['CURRENT_PINNED_JOINT_GROUPING_PROOF'],'model_hash':common.digest(model)}
 if registered and not any(v.get('codes',[None])[0:1]==['BINDING_OR_DISPATCH_BLOCKED']for v in out.values()):
  try:
   final=load('final_role_artifact_gate367').evaluate(registered_artifact['record'],registered_artifact['result']);closures['final_role']=final
   for rid in ('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','PRIVACY_WITHOUT_FAKE_BAFFLE','COMMON_CORE_COMPACTNESS','SERVICE_COMPACTNESS'):
    proof=final['parent_evidence'][rid]
    out[rid]={'verdict':'PASS','codes':['OWN_AUDITED_SEALED_ROLE_ARTIFACT_COMPLETE'],'missing':[],'scope':proof['scope'],'source_closure':proof,'model_hash':common.digest(model),'artifact_reassessment_only':True}
   out['DISTINCTNESS_AND_FAIRNESS']={'verdict':'UNKNOWN','codes':['REQUESTED_SET_NOT_ESTABLISHED'],'missing':['ACTUAL_REQUESTED_SELECTION_SET_NOT_SUPPLIED'],'source_closure':final['parent_evidence']['DISTINCTNESS_AND_FAIRNESS'],'model_hash':common.digest(model)}
  except (ValueError,KeyError,TypeError) as error:
   for rid in ('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','PRIVACY_WITHOUT_FAKE_BAFFLE','COMMON_CORE_COMPACTNESS','SERVICE_COMPACTNESS'):
    out[rid]={'verdict':'UNKNOWN','codes':['FINAL_ARTIFACT_BINDING_FAILED',type(error).__name__],'missing':['CURRENT_SEALED_FINAL_ROLE'],'model_hash':common.digest(model)}
 check_outer_sources()
 if common.digest([model,raw])!=before:raise ValueError('INPUT_MUTATED')
 return {'schema':'SEMANTIC_JOINT367_CURRENT_SOURCE_V4_FINAL_AUDITED_ARTIFACT','source_profile':source_profile,'registered_artifact_verified':registered,'quality':[dict(rule_id=k,**out[k])for k in RULE_IDS],'source_closures':closures,'model_hash':common.digest(model),'raw_report_hash':common.digest(raw),'fresh_executed':False,'accepted':False,'delivery_allowed':False,'scope':'CURRENT_BOUND_ARTIFACT_REVIEW_NOT_NEW_FRESH','source_manifest_digest':common.digest(manifest)}
