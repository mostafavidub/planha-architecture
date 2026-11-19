"""Nonpersonal precision study; full reports are temporary, no uploads.
Public V3 input validation reused, not a claim of public runtime readiness.
"""
import copy,inspect,json,math,os,signal,re,subprocess,sys,tempfile,time,uuid,hashlib
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
from front_rear_runtime_adapter import transport,proposal_transport,proposal_disposition,preserve_report,verify_reports,packet_binding
from same_version_front_rear_contract import digest,ENGINE_REVISION,FREEZE
from one_bed_pair_source_study import code_counts,stop_process
from core_choice_pair_study import selected_core,bind_profile,bind_program
from source_fit_profile207 import source_fit
from precision_boundary208 import prepare,gated_propose,roundtrip,coordinate_receipt
CASES={'V0':('18','20'),'V2':('18','20')}
VARIANTS={'V0':0,'V2':2}
CURRENT=('current_programme_evaluator','source_guest_route_evaluator','source_living_evaluator','source_wall_function_evaluator')
SCHEMAS={"current_programme_evaluator":"CURRENT_PROGRAMME_SOURCE_EVALUATION_V1","source_guest_route_evaluator":"SOURCE_BOUND_FOUR_GUEST_ROUTES_V1","source_living_evaluator":"CURRENT_LIVING_SOURCE_EVIDENCE_V1","source_wall_function_evaluator":"SOURCE_WALL_FUNCTION_EVIDENCE_V1"}
SOURCES={"current_programme_evaluator":["app/local_integration/current_entry_boundary_x03.py","app/local_integration/current_programme_evaluator.py","app/local_integration/program_profile_registry.py","specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json"],"source_guest_route_evaluator":["app/local_integration/current_entry_boundary_x03.py","app/local_integration/source_guest_route_evaluator.py","app/local_integration/current_programme_evaluator.py","app/local_integration/kitchen_guest_review.py","app/local_integration/guest_four_route_diagnostic.py"],"source_living_evaluator":["app/local_integration/current_entry_boundary_x03.py","app/local_integration/source_living_evaluator.py","app/local_integration/source_guest_route_evaluator.py","app/local_integration/living_connectivity_diagnostic.py","app/local_integration/fixed_route_clearance_diagnostic.py","app/local_integration/kitchen_guest_review.py"],"source_wall_function_evaluator":["app/local_integration/current_entry_boundary_x03.py","app/local_integration/source_wall_function_evaluator.py","app/local_integration/source_wall_counterfactual.py","app/local_integration/current_programme_evaluator.py"]}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
DEADLINE=datetime(2026,11,19,21,3,20,tzinfo=timezone.utc)
def eligibility(body):
 from public_wln_contract import parse_public,verify_public
 e=parse_public(body);verify_public(body,e)
 if e['canonical_request']['unit_count']!=2:
  return {'state':'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT','dispatch':False,'envelope_digest':digest(e)}
 p=prepare(body)
 return {'state':'SUPPORTED_STUDY_INPUT','dispatch':True,'prepared':p}
def slot(remaining):
 need(type(remaining)in(int,float) and remaining>=0,'REMAINING_TYPE')
 return 240 if remaining>=250 else 0

def need(ok,code):
 if not ok:raise ValueError(code)
def current_report_binding(name,r,bundle):
 from producer_provenance import snapshot
 need(type(r)is dict and r.get('schema')==SCHEMAS[name]and r.get('current_domain_policy')=='CURRENT_ENTRY_DOMAIN_X03_V1','CURRENT_SCHEMA_POLICY')
 need(type(r)is dict and digest(r.get('source_snapshot'))==digest(snapshot(ROOT,SOURCES[name])),'CURRENT_SOURCE_SNAPSHOT')
 mh=bundle['model_digest'];physical=bundle['reports']['physical'];ph=bundle['report_digests']['physical']
 need(r.get('integrity_verified')is True and all(r.get(k)is False for k in('accepted','qualified','display_allowed','delivery_allowed')),'CURRENT_INTEGRITY_AUTHORITY')
 need(r.get('model_digest')==mh and r.get('state')in('PASS','FAIL','UNKNOWN','NOT_EVALUATED'),'CURRENT_MODEL_STATE')
 need(not r.get('report_mutations')and not r.get('integrity_error')and not r.get('missing'),'CURRENT_ERROR_OR_MUTATION')
 if name=='current_programme_evaluator':
  need(not any(x.get('kind')in('EVALUATOR_OR_SOURCE_BINDING_ERROR','INTEGRITY_ERROR')for x in r['findings']),'PROGRAMME_EVALUATOR_ERROR')
  replay=r['reports']['replay']
  need(r['historical_physical_digest']==ph and digest(r['historical_physical_report'])==digest(physical),'PROGRAMME_PHYSICAL_BINDING')
  need(all(digest(v)==r['report_digests'][k]for k,v in r['reports'].items()),'PROGRAMME_REPORT_HASH')
 else:
  replay=r['replay']
  need(r['original_physical_digest']==ph and digest(r['original_physical_report'])==digest(physical),'CURRENT_PHYSICAL_BINDING')
 def error_states(v):
  if type(v)is dict:
   return v.get('state')in('EVALUATOR_ERROR','UNKNOWN_EVALUATOR_OR_BINDING_ERROR')or any(error_states(x)for x in v.values())
  return any(error_states(x)for x in v)if type(v)is list else False
 need(not error_states(r.get('units',[]))and not error_states(r.get('walls',[])),'CURRENT_SUBREPORT_ERROR')
 need(replay['verified']is True and replay['model_hash']==mh,'CURRENT_REPLAY_BINDING')


def json_types(v):
 if v is None or type(v)in(str,bool,int):return
 if type(v)is float:
  need(math.isfinite(v),'NONFINITE_REPORT');return
 if type(v)is list:
  for x in v:json_types(x)
  return
 if type(v)is dict:
  need(all(type(k)is str for k in v),'REPORT_KEY_TYPE')
  for x in v.values():json_types(x)
  return
 raise ValueError('NONJSON_REPORT')
def capture_returned(result):
 try:json_types(result)
 except (ValueError,RecursionError):
  return {'schema':'NONJSON_REPORT_OBSERVATION302_V1','state':'EVALUATOR_ERROR','raw_value_type':type(result).__name__ if type(result)in(dict,list,tuple,str,int,float,bool,type(None))else'OTHER','raw_preserved_as_json':False},False
 return copy.deepcopy(result),True
def recheck_reports(r,reports):
 need(type(reports)is dict,'REPORT_TYPE')
 need(all(k in reports and digest(reports[k])==v for k,v in r.get('report_digests',{}).items()),'REPORT_FILE_DIGEST')
 if r.get('state')!='FULL_REPORTS_RETAINED_NOT_QUALIFIED'or r.get('completed')is not True:return
 physical=reports['physical'];replay=reports['original_replay'];mh=r['model_digest']
 need(physical['model_hash']==mh and replay['verified']is True and replay['model_hash']==mh,'RETAINED_MODEL_REPLAY')
 need(r['physical_status']==physical['status']and digest(r['physical_error_counts'])==digest(code_counts(physical.get('errors',[])))and digest(r['physical_pending_counts'])==digest(code_counts(physical.get('pending',[]))),'PHYSICAL_SUMMARY')
 binding={'model_digest':mh,'reports':{'physical':physical},'report_digests':{'physical':r['report_digests']['physical']}}
 for name in CURRENT:
  raw=reports['current_'+name];current_report_binding(name,raw,binding)
  need(r['current_assessments'][name]['state']==raw['state']and r['current_assessments'][name]['integrity_verified']is raw['integrity_verified'],'CURRENT_SUMMARY')

def capture_equivalence(a,b):
 import numpy as np
 for key in('lower','upper','integrality'):
  need(np.array_equal(a[key],b[key]),'CAPTURE_'+key.upper())
 for key in('lb','ub'):
  need(np.array_equal(getattr(a['bounds'],key),getattr(b['bounds'],key)),'CAPTURE_BOUNDS')
 need(a['matrix'].shape==b['matrix'].shape,'CAPTURE_MATRIX_SHAPE')
 for key in('data','indices','indptr'):
  need(np.array_equal(getattr(a['matrix'],key),getattr(b['matrix'],key)),'CAPTURE_CSR')
 need(digest(a['specs'])==digest(b['specs'])and digest(a['row_metadata'])==digest(b['row_metadata']),'CAPTURE_SCHEMA')
 names=[r[0]for r in a['specs']];ki=4*names.index('kitchen')+1;di=4*names.index('dining')
 need(np.flatnonzero(a['objective']!=b['objective']).tolist()==sorted([ki,di]),'CAPTURE_OBJECTIVE_PATHS')
 need(a['objective'][ki]==.006 and b['objective'][ki]==-.006 and a['objective'][di]==.003 and b['objective'][di]==-.003,'CAPTURE_OBJECTIVE_VALUES')
 return {'state':'SAME_HARD_CONSTRAINTS_DIFFERENT_DECLARED_OBJECTIVE','structural_difference_proven':False}
def dependency_guard():
 pins={'app/local_integration/source_fit_candidate207.py':'be98c37a0827f23b34d6110182c582177532217c','app/local_integration/precision_boundary208.py':'e1ece20ad40d7d17e268fc9e1c2fe701ca383548','studies/r4/actual_descriptor301.py':'02c3126479b9fee410d985afb7e58205bb55c0b3','studies/r4/semantic_descriptor301.py':'8bdcf838386ea798405b8bc3d43b355fe0957777'}
 for path,sha in pins.items():
  b=(ROOT/path).read_bytes();need(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==sha,'DEPENDENCY_PIN')
 return pins
def child(folder,case,nonce):
 from program_profile_registry import lookup
 from producer_provenance import snapshot,require_unchanged
 import engine114,guard400,source_fit_candidate207,search114,contract114,constructor127,construction_replay127,evaluate_pair127
 import source_fit_profile207
 folder=Path(folder);folder.mkdir(exist_ok=False)
 out={'run_nonce':nonce,'schema':'STRUCTURAL_PAIR302_CASE_V1','case':case,'state':'STARTED','completed':False,'construction_observed':False,
 'independent_origin_verified':False,'integrity_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
 'current_assessment_attempted':False,'current_four':'NOT_EVALUATED_FRESH_CURRENT_CRITERIA_NOT_RUN','technical_core':'POST_MVP_NOT_EVALUATED','internal_count_is_product_count':False}
 originals={};live={};pins={};inputs={};inputpins={};bundle=None;bp=None;snap=None;audited=False
 def save():
  out['report_digests']=copy.deepcopy(pins)
  for n,v in (('reports.json',originals),('summary.json',out)):
   p=folder/(n+'.tmp');p.write_text(json.dumps(v,sort_keys=True,allow_nan=False));p.replace(folder/n)
 def pin(k,v):inputs[k]=v;inputpins[k]=digest(v)
 def check():
  for k,v in inputs.items():need(digest(v)==inputpins[k],'INPUT_MUTATION')
  verify_reports(live,pins);verify_reports(originals,pins)
  if bundle is not None:need(digest(bundle)==bp,'BUNDLE_MUTATION')
  require_unchanged(ROOT,snap)
 def retain(k,r):preserve_report(originals,live,pins,k,r);check();save()
 try:
  paths=['app/local_integration/'+n for n in ('structural_pair302.py','precision_pair_study208.py','precision_boundary208.py','public_wln_contract.py','dimension_contract.py','source_fit_candidate207.py','source_fit_profile207.py','core_choice_pair_study.py','one_bed_pair_source_study.py','program_profile_registry.py','front_rear_runtime_adapter.py','same_version_front_rear_contract.py')]
  paths+=['app/reconstruction357/planha_general150_runtime_work/'+m.__name__+'.py'for m in (contract114,search114,constructor127,construction_replay127,evaluate_pair127)]+['app/reconstruction357/planha_general150_runtime_work/entry117.py']
  paths+=['app/local_integration/'+n+'.py'for n in CURRENT]+['app/local_integration/current_entry_boundary_x03.py','studies/r4/actual_descriptor301.py','studies/r4/semantic_descriptor301.py']
  snap=snapshot(ROOT,paths)
  from front_rear_runtime_adapter import source_audit
  source_audit();audit_pin=snapshot(ROOT,paths)
  need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'ENGINE_GUARD')
  for mod,names in ((search114,('propose',)),(contract114,('core_first',)),(constructor127,('frame','build','context')),(construction_replay127,('verify',)),(evaluate_pair127,('evaluate',))):
   for name in names:need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ENGINE/(mod.__name__+'.py'),'ACTUAL_IMPORT_PATH')
  for mod,name in ((source_fit_candidate207,'propose'),(source_fit_profile207,'source_fit')):
   need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ROOT/'app/local_integration'/(mod.__name__+'.py'),'STUDY_IMPORT_PATH')
  need(Path(inspect.getsourcefile(lookup)).resolve()==ROOT/'app/local_integration/program_profile_registry.py','REGISTRY_IMPORT_PATH')
  import precision_boundary208,public_wln_contract
  for mod,names in ((precision_boundary208,('prepare','gated_propose','roundtrip','coordinate_receipt')),(public_wln_contract,('parse_public','engine_raw'))):
   for name in names:need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ROOT/'app/local_integration'/(mod.__name__+'.py'),'PRECISION_IMPORT_PATH')
  dependency_guard()
  audited=True;need(case in CASES,'STUDY_CASE');w,l=CASES[case];body=json.dumps({'W':w,'L':l,'n':2}).encode();eligible=eligibility(body);need(eligible['dispatch'],'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT');prepared=eligible['prepared'];raw=prepared['raw'];profile=lookup('PROGRAM_2BED_V1');bind_profile(profile)
  pin('prepared',prepared);reread,rt=roundtrip(prepared);retain('input_roundtrip',rt);need(digest(reread)==digest(prepared),'INPUT_REREAD')
  out['input_ratios']=prepared['ratios'];out['input_schema']=prepared['envelope']['schema']
  pin('raw',raw);pin('profile',profile);core,(W,L)=selected_core(raw,'FRONT_REAR_COMPACT118');pin('core',core)
  out.update(stage='PROPOSE',raw_digest=digest(raw),profile_digest=digest(profile),core_digest=digest(core),source_digest=digest(snap),solver_limit_seconds=30);save()
  out['producer_scope']='ADDITIVE_SOURCE_FIT_STUDY';save()
  again=prepare(body);again_core,_=selected_core(again['raw'],'FRONT_REAR_COMPACT118')
  p=source_fit_candidate207.propose(again_core,2,time_limit=30,variant=VARIANTS[case],sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES');check()
  need(digest(again)==digest(prepared)and digest(again_core)==digest(core),'PREPARED_DISPATCH_BINDING')
  state=proposal_disposition(p);out['producer_status']=state
  out.update(solver_status=p.get('solver_status'),emitted_constraint_count=p.get('constraints'),solver_seconds=p.get('solver_seconds'))
  if state!='PROPOSAL_ONLY':
   retain('producer_no_witness',p);out.update(state='NO_PROPOSAL_NO_INFEASIBILITY_CLAIM',completed=True);return
  original_proposal=p;p,tr=proposal_transport(original_proposal)
  retain('coordinate_precision',coordinate_receipt(original_proposal,p,tr))
  p,rt=roundtrip(p);retain('proposal_roundtrip',rt)
  need(type(p.get('variant'))is int and p['variant']==VARIANTS[case],'PROPOSAL_VARIANT')
  need(type(p.get('bedrooms'))is int and p['bedrooms']==2 and digest(p.get('sleep_roles'))==digest(['double','twin']),'PROPOSAL_PROGRAM')
  proposals={'A':p,'B':copy.deepcopy(p)};pin('proposals',proposals)
  retain('preconstruction_fit',source_fit(p,core))
  if originals['preconstruction_fit']['state']!='PASS_LIMITED_CONSTRAINTS':
   out.update(state='EXACT_FIT_REJECTED_NO_GLOBAL_INFEASIBILITY',completed=True,fit_state=originals['preconstruction_fit']['state']);return
  out.update(stage='CONSTRUCT',proposal_digest=digest(proposals),coordinate_conversion_count=len(tr['coordinate_conversions']));save()
  packet=constructor127.build(raw,'FRONT_REAR',proposals['A'],proposals['B']);out['construction_observed']=True;check()
  packet,_=transport(packet);pin('packet',packet)
  need(digest(packet['core'])==digest(core),'CORE_BINDING')
  need(digest(packet['unit_proposal_hashes'])==digest({k:digest(v)for k,v in proposals.items()}),'PROPOSAL_ASSIGNMENTS')
  model=packet['world_model'];bind_program(model,profile)
  reread,rt=roundtrip(packet);retain('packet_roundtrip',rt);need(digest(reread)==digest(packet),'PACKET_REREAD')
  need(all(F(model['inputs'][i])==F(raw[k])for i,k in enumerate(('W','L'))),'MODEL_INPUT_RATIO')
  ctx=constructor127.context(raw,packet,proposals);check()
  bundle,_=transport({'packet':packet,'context':ctx});bp=digest(bundle);packet=bundle['packet'];ctx=bundle['context'];model=packet['world_model']
  need(digest(ctx['construction_trace']['raw'])==digest(raw)and digest(ctx['construction_trace']['proposals'])==digest(proposals),'CONTEXT_ASSIGNMENTS')
  packet_binding(packet,ctx,raw,p);check()
  out.update(variant=VARIANTS[case],model_digest=digest(model),program_digest=digest(model['program']),fit_state=originals['preconstruction_fit']['state']);save()
  out['stage']='ORIGINAL_REPLAY_AND_FULL_PHYSICAL';save()
  retain('original_replay',construction_replay127.verify(model,ctx))
  retain('physical',evaluate_pair127.evaluate(packet,ctx))
  need(originals['physical']['model_hash']==digest(model),'PHYSICAL_MODEL_BINDING')
  out.update(physical_status=originals['physical'].get('status'),physical_error_counts=code_counts(originals['physical'].get('errors',[])),
   physical_pending_counts=code_counts(originals['physical'].get('pending',[])),legacy_replay_verified=originals['original_replay'].get('verified')is True);save()
  out['stage']='REPORT_AND_CONTEXT_ROUNDTRIP';save()
  for key,value in (('context',ctx),('physical',originals['physical']),('replay',originals['original_replay'])):
   reread,rt=roundtrip(value);retain(key+'_roundtrip',rt);need(digest(reread)==digest(value),'REPORT_REREAD')
  out['stage']='CURRENT_ASSESSMENTS';save()
  evidence={'packet':packet,'context':ctx,'model_digest':digest(model),'reports':{'physical':copy.deepcopy(originals['physical']),'original_replay':copy.deepcopy(originals['original_replay'])},'report_digests':{k:pins[k]for k in ('physical','original_replay')}}
  pin('current_evidence',evidence)
  out['current_assessments']={};out['current_assessment_attempted']=True;out['current_assessment_call_count']=0
  for name in CURRENT:
   out['stage']='ASSESS_'+name;save()
   mod=__import__(name);path=ROOT/'app/local_integration'/(name+'.py')
   need(Path(mod.__file__).resolve()==path and Path(inspect.getsourcefile(mod.assess)).resolve()==path,'CURRENT_IMPORT_PATH')
   out['current_assessment_call_count']+=1;save()
   result=mod.assess(evidence)
   # Preserve returned report before validation, including errors or malformed JSON-shaped evidence.
   captured,json_ok=capture_returned(result)
   originals['current_'+name]=captured;pins['current_'+name]=digest(captured);live['current_'+name]=result if json_ok else copy.deepcopy(captured);save()
   need(json_ok,'NONJSON_CURRENT_RETURNED_REPORT')
   current_report_binding(name,result,evidence);check()
   out['current_assessments'][name]={'state':result['state'],'integrity_verified':result['integrity_verified'],'report_digest':digest(result)}
  out['current_assessment_attempted']=True;out['current_four']='FOUR_CURRENT_RETAINED_NOT_QUALIFIED'
  need(set(out['current_assessments'])==set(CURRENT),'CURRENT_SET')
  source_audit();require_unchanged(ROOT,audit_pin)
  out['stage']='ACTUAL_DESCRIPTOR';out['descriptor_state']='STARTED';save()
  descriptor_module=descriptor_import()
  projection=descriptor_module.project(model);check()
  desc=descriptor_module.descriptor(projection)
  need(desc['model_digest']==digest(model)and all(desc[k]is False for k in AUTH),'DESCRIPTOR_MODEL_BINDING')
  retain('actual_descriptor',desc)
  pth=folder/'projection.json.tmp';pth.write_text(json.dumps(projection,sort_keys=True,allow_nan=False));pth.replace(folder/'projection.json')
  out.update(descriptor_state='ACTUAL_MODEL_BOUND_DESCRIPTOR',descriptor_digest=digest(desc),projection_digest=digest(projection),descriptor_signature=desc['signature'])
  source_audit();require_unchanged(ROOT,audit_pin)
  out['roundtrip_verified']=True
  out['coordinate_conversion_count']=originals['coordinate_precision']['conversion_count']
  out['coordinate_ratio_record_digest']=originals['coordinate_precision']['record_digest']
  out.update(state='FULL_REPORTS_RETAINED_NOT_QUALIFIED',completed=True,independent_origin_verified=originals['original_replay'].get('verified')is True,
   legacy_replay_verified=originals['original_replay'].get('verified')is True,
   physical_status=originals['physical'].get('status'),physical_error_counts=code_counts(originals['physical'].get('errors',[])),
   physical_pending_counts=code_counts(originals['physical'].get('pending',[])),legacy_replay_error_counts=code_counts(originals['original_replay'].get('errors',[])),
   original_not_evaluated_count=len(originals['physical'].get('not_evaluated',[])),original_out_of_scope_count=len(originals['physical'].get('out_of_scope',[])),
   unit_count=len(model['units']),no_quality_claim=True)
 except Exception as ex:
  out.update(state='FAILED_CLOSED',completed=False,error_type=type(ex).__name__,error_code=str(ex)if re.fullmatch(r'[A-Z0-9_:]+',str(ex))else'NONPUBLIC_DETAIL_NOT_PRINTED')
 finally:
  try:
   need(audited and snap is not None,'INITIAL_AUDIT_NOT_ESTABLISHED');dependency_guard();check()
   need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'FINAL_ENGINE_GUARD');out['integrity_verified']=True
  except Exception as ex:out.update(state='INTEGRITY_ERROR',completed=False,integrity_verified=False,origin_observed_at_checkpoint=out.get('independent_origin_verified',False),independent_origin_verified=False,roundtrip_verified=False,integrity_error_type=type(ex).__name__)
  out.update(current_assessment_completed_count=len(out.get('current_assessments',{})),report_digests=pins,original_reports_retained_job_temporarily=True,durable_archive_created=False,evidence_usable=out.get('completed')is True and out.get('integrity_verified')is True);save()

def read_summary(path,case,nonce):
 need(path.stat().st_size<=1048576,'SUMMARY_SIZE')
 r=json.loads(path.read_text())
 need(type(r)is dict and r.get('case')==case and r.get('run_nonce')==nonce,'SUMMARY_BINDING')
 need(all(r.get(k)is False for k in AUTH),'SUMMARY_AUTHORITY')
 need(r.get('state')in('FULL_REPORTS_RETAINED_NOT_QUALIFIED','NO_PROPOSAL_NO_INFEASIBILITY_CLAIM','EXACT_FIT_REJECTED_NO_GLOBAL_INFEASIBILITY','FAILED_CLOSED','INTEGRITY_ERROR'),'SUMMARY_STATE')
 if r.get('state')=='FULL_REPORTS_RETAINED_NOT_QUALIFIED' and r.get('completed')is True:
  need(r.get('independent_origin_verified')is True and r.get('integrity_verified')is True,'SUMMARY_ORIGIN')
  q=r.get('current_assessments')
  need(type(q)is dict and set(q)==set(CURRENT),'SUMMARY_CURRENT_SET')
  need(all(v.get('state')in('PASS','FAIL','UNKNOWN','NOT_EVALUATED')and v.get('integrity_verified')is True and v.get('report_digest')==r['report_digests']['current_'+k]for k,v in q.items()),'SUMMARY_CURRENT_BINDING')
 return r
def invalidate(r,state):
 r=dict(r);r.update(state=state,completed=False,independent_origin_verified=False,integrity_verified=False,roundtrip_verified=False,evidence_usable=False)
 return r
def descriptor_import():
 sys.path.insert(0,str(ROOT/'studies/r4'))
 import actual_descriptor301 as a
 need(Path(a.__file__).resolve()==ROOT/'studies/r4/actual_descriptor301.py','DESCRIPTOR_IMPORT')
 for fn in(a.project,a.descriptor,a.compare_projections):
  need(Path(inspect.getsourcefile(fn)).resolve()==ROOT/'studies/r4/actual_descriptor301.py','DESCRIPTOR_CALLABLE')
 a.guard();dependency_guard()
 return a
def pair_readback(results,folder):
 accepted=[r for r in results if r.get('completed')is True and r.get('descriptor_state')=='ACTUAL_MODEL_BOUND_DESCRIPTOR'and r.get('integrity_verified')is True]
 if len(accepted)!=2:return {'state':'NOT_COMPARABLE_MISSING_BOUND_DESCRIPTOR','reason':'NO_FALLBACK_OR_RESAMPLE','architectural_diversity_verified':False,**{k:False for k in AUTH}}
 a=descriptor_import();pin=a.guard();projections=[]
 for r in results:
  path=folder/r['case']/'projection.json';need(path.stat().st_size<=33554432,'PROJECTION_SIZE')
  p=json.loads(path.read_text());need(digest(p)==r['projection_digest']and p['model_digest']==r['model_digest'],'PROJECTION_MODEL_BINDING')
  d=a.descriptor(p);need(digest(d)==r['descriptor_digest']and d['signature']==r['descriptor_signature'],'DESCRIPTOR_REREAD')
  projections.append(p)
 result=a.compare_projections(*projections)
 result.update(model_hashes=[r['model_digest']for r in results],same_model=results[0]['model_digest']==results[1]['model_digest'],
  signatures=[r['descriptor_signature']for r in results],comparison_scope='Actual source-bound descriptor relationship difference, not quality or admission',
  canonical_difference_digest=digest([a.canonical(p)for p in projections]),**{k:False for k in AUTH})
 need(digest(a.guard())==digest(pin),'PAIR_SOURCE_CHANGED')
 return result
def run():
 start=time.monotonic()
 allocation=min(600,(DEADLINE-datetime.now(timezone.utc)).total_seconds()-5)
 need(allocation>0,'TASK_TIMEBOX_EXPIRED')
 def remaining():return max(0,allocation-(time.monotonic()-start))
 results=[]
 selfpin=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 with tempfile.TemporaryDirectory(prefix='structural302-')as tmp:
  for case in ('V0','V2'):
   budget=slot(remaining())
   if not budget:
    results.append({'case':case,'state':'NOT_RUN_INSUFFICIENT_SHARED_BUDGET','solver_attempts':0,**{k:False for k in AUTH}});continue
   nonce=uuid.uuid4().hex;dest=Path(tmp)/case;reserved=time.monotonic()-start
   proc=subprocess.Popen([sys.executable,'-B',__file__,'--child',str(dest),case,nonce],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
   timed=False
   try:proc.wait(timeout=min(budget,remaining()))
   except subprocess.TimeoutExpired:
    timed=True
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    proc.wait()
   try:r=read_summary(dest/'summary.json',case,nonce)
   except (OSError,ValueError,TypeError,RecursionError):r={'case':case,'state':'SUMMARY_FAILED_CLOSED','completed':False,**{k:False for k in AUTH}}
   # File consistency only; raw reports remain private until temporary cleanup.
   try:
    rp=dest/'reports.json';need(rp.stat().st_size<=33554432,'REPORT_FILE_SIZE')
    reports=json.loads(rp.read_text());recheck_reports(r,reports)
    r['report_file_hash']=hashlib.sha256(rp.read_bytes()).hexdigest()
   except (OSError,ValueError,TypeError,RecursionError,KeyError):r=invalidate(r,'REPORT_READBACK_FAILED')
   finished=time.monotonic()-start
   r.update(case=case,reserved_at=reserved,finished_at=finished,allocated_seconds=budget,outer_timeout=timed,wait_completed=proc.poll()is not None,returncode=proc.returncode)
   if timed or proc.returncode!=0 or finished-reserved>=budget:r=invalidate(r,'TIMEOUT_OR_PROCESS_ERROR_OBSERVED_ONLY')
   results.append(r)
  try:comparison=pair_readback(results,Path(tmp))
  except (ValueError,KeyError,TypeError,OSError,RecursionError):comparison={'state':'PAIR_BINDING_ERROR','architectural_diversity_verified':False,**{k:False for k in AUTH}}
  valid_source=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==selfpin
  if not valid_source or remaining()<=0:
   results=[invalidate(r,'GLOBAL_SOURCE_OR_BUDGET_ERROR')for r in results]
  out={'schema':'STRUCTURAL_PAIR302_BATCH_V1','rows':results,'comparison':comparison,'elapsed_seconds':time.monotonic()-start,'allocation_seconds':allocation,'source_integrity_verified':valid_source,'seed':'NOT_EXPOSED_SOURCE_DEFAULT','variants':[0,2],'retry_count':0,'fresh_four_current_case_count':sum(r.get('state')=='FULL_REPORTS_RETAINED_NOT_QUALIFIED'and r.get('completed')is True for r in results if r['case']in('V0','V2')),'subcriterion_fresh_four_current_complete':all(r.get('state')=='FULL_REPORTS_RETAINED_NOT_QUALIFIED'and r.get('completed')is True for r in results if r['case']in('V0','V2')),'durable_raw_archive_created':False,'budget_scope':'Batch600 starts before source/runtime setup, after CI dependency installation; job13min also bounded separately. Each child240 includes current evaluators; parent verification measured not preempted. Encoding/network outside cutoff; absolute taskcap retained.','qualified':False,'accepted':False,'display_allowed':False,'delivery_allowed':False}
  if not valid_source or remaining()<=0:out['comparison']={'state':'GLOBAL_INTEGRITY_ERROR','architectural_diversity_verified':False,**{k:False for k in AUTH}}
  print(json.dumps(out,sort_keys=True,allow_nan=False),flush=True)
  need(valid_source and remaining()>0,'GLOBAL_INTEGRITY')
  need(all((r.get('completed')is True and r.get('integrity_verified')is True)or r.get('state')=='NOT_RUN_INSUFFICIENT_SHARED_BUDGET'for r in results if r['case']in('V0','V2')),'BATCH_COLLECTION_ERROR')
def main():
 if len(sys.argv)==5 and sys.argv[1]=='--child':
  need(sys.argv[3]in CASES,'UNKNOWN_CASE');child(sys.argv[2],sys.argv[3],sys.argv[4]);return
 need(sys.argv[1:]==[],'UNKNOWN_MODE')
 run()
if __name__=='__main__':main()
