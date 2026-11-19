"""Two nonpersonal dimensions; source-derived fit constraints before original construction.
No private artifact inputs or uploads. Full original reports remain job-temporary.
"""
import copy,inspect,json,os,re,subprocess,sys,tempfile,time,uuid
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
from source_fit_profile207 import source_fit,profiles,installation_expectations,verify_installed_subset,installation_negatives,door_side_negative
CASES={'20x18':('20','18'),'18x22':('18','22')}
def need(ok,code):
 if not ok:raise ValueError(code)
def child(folder,case,nonce):
 from program_profile_registry import lookup
 from producer_provenance import snapshot,require_unchanged
 import engine114,guard400,source_fit_candidate207,contract114,constructor127,construction_replay127,evaluate_pair127
 import source_fit_profile207
 folder=Path(folder);folder.mkdir(exist_ok=False)
 out={'run_nonce':nonce,'schema':'SOURCE_FIT_PAIR_STUDY207_V1','case':case,'state':'STARTED','completed':False,'construction_observed':False,
 'independent_origin_verified':False,'integrity_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
 'current_four':'NOT_EVALUATED_FRESH_CURRENT_CRITERIA_NOT_RUN','technical_core':'POST_MVP_NOT_EVALUATED','internal_count_is_product_count':False}
 originals={};live={};pins={};inputs={};inputpins={};bundle=None;bp=None;snap=None;audited=False
 def save():
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
  paths=['app/local_integration/'+n for n in ('source_fit_pair_study207.py','source_fit_candidate207.py','source_fit_profile207.py','core_choice_pair_study.py','one_bed_pair_source_study.py','program_profile_registry.py','front_rear_runtime_adapter.py','same_version_front_rear_contract.py')]
  paths+=['app/reconstruction357/planha_general150_runtime_work/'+m.__name__+'.py'for m in (contract114,constructor127,construction_replay127,evaluate_pair127)]+['app/reconstruction357/planha_general150_runtime_work/entry117.py']
  snap=snapshot(ROOT,paths)
  need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'ENGINE_GUARD')
  for mod,names in ((contract114,('core_first',)),(constructor127,('frame','build','context')),(construction_replay127,('verify',)),(evaluate_pair127,('evaluate',))):
   for name in names:need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ENGINE/(mod.__name__+'.py'),'ACTUAL_IMPORT_PATH')
  for mod,name in ((source_fit_candidate207,'propose'),(source_fit_profile207,'source_fit')):
   need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ROOT/'app/local_integration'/(mod.__name__+'.py'),'STUDY_IMPORT_PATH')
  need(Path(inspect.getsourcefile(lookup)).resolve()==ROOT/'app/local_integration/program_profile_registry.py','REGISTRY_IMPORT_PATH')
  audited=True;need(case in CASES,'STUDY_CASE');w,l=CASES[case];raw={'W':w,'L':l,'n':2,'requested_count':1};profile=lookup('PROGRAM_2BED_V1');bind_profile(profile)
  pin('raw',raw);pin('profile',profile);core,(W,L)=selected_core(raw,'FRONT_REAR_COMPACT118');pin('core',core)
  out.update(stage='PROPOSE',raw_digest=digest(raw),profile_digest=digest(profile),core_digest=digest(core),source_digest=digest(snap),solver_limit_seconds=30);save()
  p=source_fit_candidate207.propose(core,2,time_limit=30,variant=0,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES');check()
  state=proposal_disposition(p);out['producer_status']=state
  if state!='PROPOSAL_ONLY':out.update(state='NO_PROPOSAL_NO_INFEASIBILITY_CLAIM',completed=True);return
  p,tr=proposal_transport(p)
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
  ctx=constructor127.context(raw,packet,proposals);check()
  bundle,_=transport({'packet':packet,'context':ctx});bp=digest(bundle);packet=bundle['packet'];ctx=bundle['context'];model=packet['world_model']
  need(digest(ctx['construction_trace']['raw'])==digest(raw)and digest(ctx['construction_trace']['proposals'])==digest(proposals),'CONTEXT_ASSIGNMENTS')
  packet_binding(packet,ctx,raw,p);check()
  out.update(model_digest=digest(model),program_digest=digest(model['program']),fit_state=originals['preconstruction_fit']['state']);save()
  out['stage']='ORIGINAL_REPLAY_AND_FULL_PHYSICAL';save()
  retain('original_replay',construction_replay127.verify(model,ctx))
  retain('physical',evaluate_pair127.evaluate(packet,ctx))
  need(originals['physical']['model_hash']==digest(model),'PHYSICAL_MODEL_BINDING')
  out.update(physical_status=originals['physical'].get('status'),physical_error_counts=code_counts(originals['physical'].get('errors',[])),
   physical_pending_counts=code_counts(originals['physical'].get('pending',[])),legacy_replay_verified=originals['original_replay'].get('verified')is True);save()
  out['stage']='INSTALLED_SUBSET_CHECK';save()
  expected=installation_expectations(proposals,L);pin('expected_installation',expected);check()
  retain('installed_source_subset',verify_installed_subset(model,expected))
  retain('actual_source_negatives',installation_negatives(model,expected))
  out.update(installed_subset_state=originals['installed_source_subset']['state'],installed_record_count=originals['installed_source_subset']['checked_record_count'],
   actual_negative_count=len(originals['actual_source_negatives']['rows']),actual_negatives_detected=originals['actual_source_negatives']['all_detected'])
  need(out['installed_subset_state']=='PASS_SOURCE_SUBSET_ONLY'and out['actual_negatives_detected']is True,'INSTALLATION_STUDY_NOT_VERIFIED')
  retain('door_side_negative',door_side_negative(model))
  out['door_side_negative_states']=[r['state']for r in originals['door_side_negative']['rows']]
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
   need(audited and snap is not None,'INITIAL_AUDIT_NOT_ESTABLISHED');check()
   need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'FINAL_ENGINE_GUARD');out['integrity_verified']=True
  except Exception as ex:out.update(state='INTEGRITY_ERROR',completed=False,integrity_verified=False,origin_observed_at_checkpoint=out.get('independent_origin_verified',False),independent_origin_verified=False,integrity_error_type=type(ex).__name__)
  out.update(report_digests=pins,original_reports_retained_job_temporarily=True,durable_archive_created=False);save()
def main():
 if len(sys.argv)==5 and sys.argv[1]=='--child':child(sys.argv[2],sys.argv[3],sys.argv[4]);return
 results=[]
 for case in CASES:
  remaining=(datetime(2026,11,19,14,35,44,tzinfo=timezone.utc)-datetime.now(timezone.utc)).total_seconds()
  budget=min(240,remaining-5);need(budget>0,'TASK_TIMEBOX_EXPIRED')
  with tempfile.TemporaryDirectory(prefix='source-fit-')as tmp:
   dest=Path(tmp)/'run';start=time.monotonic();nonce=uuid.uuid4().hex
   proc=subprocess.Popen([sys.executable,'-B',__file__,'--child',str(dest),case,nonce],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True);timed=False
   try:proc.wait(timeout=budget)
   except subprocess.TimeoutExpired:timed=True;stop_process(proc)
   try:result=json.loads((dest/'summary.json').read_text())if(dest/'summary.json').exists()else{'state':'NO_SUMMARY'}
   except(ValueError,OSError):result={'state':'SUMMARY_PARSE_FAILED_CLOSED'}
   if type(result)is not dict:result={'state':'SUMMARY_TYPE_FAILED_CLOSED'}
   if result.get('run_nonce')!=nonce:result.update(state='NONCE_BINDING_FAILED',completed=False,independent_origin_verified=False)
   result.update(case=case,outer_timeout=timed,wait_completed=proc.poll()is not None,returncode=proc.returncode,elapsed_seconds=time.monotonic()-start,outer_budget_seconds=budget,full_model_uploaded=False)
   if timed or proc.returncode!=0:result.update(completed=False,origin_observed_at_checkpoint=result.get('independent_origin_verified',False),independent_origin_verified=False,state='OUTER_TIMEOUT_PARTIAL_OBSERVATION'if timed else'PROCESS_FAILED_CLOSED')
   print(json.dumps(result,sort_keys=True,allow_nan=False),flush=True);results.append(result)
 need(all(r.get('completed')is True and r.get('integrity_verified')is True and not r['outer_timeout']and r['returncode']==0 for r in results),'STUDY_NOT_COMPLETED')
if __name__=='__main__':main()
