"""Bounded one-bedroom pair source study. Not a public adapter or quality gate."""
import copy,json,math,os,re,signal,subprocess,sys,tempfile,time,inspect
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
from front_rear_runtime_adapter import transport,preserve_report,verify_reports,proposal_disposition
from same_version_front_rear_contract import digest,ENGINE_REVISION,FREEZE
RECTS={'bed1','bath','kitchen','dining','sofa1_use','sofa2_use','chair1_use','chair2_use','entry_apron'}
TERMINALS=(RECTS-{'dining','entry_apron'})|{'dining_front','dining_back','dining_west','dining_east'}
def need(ok,why):
 if not ok:raise ValueError(why)
def normalize_proposal(value):
 import numpy as np
 p=copy.deepcopy(value);need(type(p)is dict,'PROPOSAL_OBJECT')
 need(type(p.get('bedrooms'))is int and p['bedrooms']==1 and digest(p.get('sleep_roles'))==digest(['double']),'ONE_BED_PROGRAM')
 need(set(p['rectangles'])==RECTS and set(p['network_paths'])==TERMINALS,'ONE_BED_ROLES')
 changes=[]
 def number(v,path):
  if type(v)is np.float64:
   y=float(v);need(math.isfinite(y)and v.as_integer_ratio()==y.as_integer_ratio()and digest(v)==digest(y),'LOSSLESS_BINARY64')
   changes.append(path);return y
  need(type(v)in(int,float)and math.isfinite(v),'COORDINATE_TYPE');return v
 for key,q in p['rectangles'].items():
  need(type(q)is list and len(q)==4,'RECTANGLE_SHAPE');p['rectangles'][key]=[number(v,['rectangles',key,i])for i,v in enumerate(q)]
 for key,path in p['network_paths'].items():
  need(type(path)is list and len(path)==5,'PATH_SHAPE')
  for i,q in enumerate(path):
   need(type(q)is list and len(q)==2,'POINT_SHAPE');path[i]=[number(v,['network_paths',key,i,j])for j,v in enumerate(q)]
 need(type(p.get('bed_door_sides'))is dict and set(p['bed_door_sides'])=={'bed1'}and p['bed_door_sides']['bed1']in('left','right'),'BED_DOOR_SIDE')
 p,_=transport(p);need(digest(p)==digest(value),'PROPOSAL_DIGEST_CHANGE')
 return p,{'conversions':len(changes),'proposal_digest':digest(p),'scope':'Only source proposal coordinate numpy.float64 lossless binary64'}
def program_bind(model,profile):
 need(profile['id']=='PROGRAM_1BED_V1'and profile['approval']['status']=='APPROVED_DESIGN_PROGRAM','REGISTRY_PROFILE')
 for k,v in {'bedrooms_per_unit':1,'design_persons_per_unit':2,'sleep_roles':['double'],'capacity_means_actual_population':False}.items():need(digest(profile[k])==digest(v),'REGISTRY_FIELD')
 for k,v in {'units':2,'bedrooms_per_unit':1,'sleep_roles':['double'],'design_occupants_per_unit':2,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True}.items():need(digest(model['program'][k])==digest(v),'MODEL_PROGRAM')
 need([u['id']for u in model['units']]==['A','B'],'PAIR_UNITS')
 need(model['accepted']is False and model['release_allowed']is False,'MODEL_AUTHORITY')
def code_counts(items):
 counts={}
 for item in items:
  raw=item.get('code')if type(item)is dict else item
  token=raw.split(':',1)[0]if type(raw)is str else ''
  code=token if re.fullmatch(r'[A-Z][A-Z0-9_]{0,100}',token)else'UNCLASSIFIED'
  counts[code]=counts.get(code,0)+1
 return counts
def child(folder):
 from program_profile_registry import lookup
 from producer_provenance import snapshot,require_unchanged
 import engine114,guard400,search114,constructor127,construction_replay127,evaluate_pair127
 folder=Path(folder);folder.mkdir(exist_ok=False)
 out={'schema':'ONE_BED_PAIR_SOURCE_STUDY_V1','state':'STARTED','completed':False,'construction_observed':False,'fresh_model_verified':False,'integrity_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'current_four':'NOT_EVALUATED_PROGRAM_ADAPTER_MISSING','source_program_readiness':'EXPERIMENT_ONLY_NOT_PUBLIC_READY'}
 reports={};live={};pins={};bundle=None;bundlepin=None;snap=None;audited=False;inputs={};inputpins={}
 def save():
  for name,value in (('reports.json',reports),('summary.json',out)):
   temp=folder/(name+'.tmp');temp.write_text(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False));temp.replace(folder/name)
 def bind_input(name,value):
  inputs[name]=value;inputpins[name]=digest(value)
 def check_inputs():
  for name,value in inputs.items():need(digest(value)==inputpins[name],'PRECONSTRUCTION_INPUT_MUTATION:'+name)
 def check():
  check_inputs()
  verify_reports(live,pins);verify_reports(reports,pins)
  if bundle is not None:need(digest(bundle)==bundlepin,'BUNDLE_MUTATION')
  require_unchanged(ROOT,snap)
 try:
  snap=snapshot(ROOT,['app/local_integration/one_bed_pair_source_study.py','app/local_integration/program_profile_registry.py','app/local_integration/front_rear_runtime_adapter.py'])
  need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'ENGINE_GUARD')
  for mod,fn in ((search114,'propose'),(constructor127,'build'),(constructor127,'context'),(construction_replay127,'verify'),(evaluate_pair127,'evaluate')):
   need(Path(inspect.getsourcefile(getattr(mod,fn))).resolve()==(ENGINE/(mod.__name__+'.py')).resolve(),'IMPORTED_SOURCE_PATH')
  audited=True;profile=lookup('PROGRAM_1BED_V1');profilepin=digest(profile);bind_input('profile',profile)
  raw={'W':'18','L':'20','n':2,'requested_count':1};bind_input('raw',raw);core,_=constructor127.frame(raw,'FRONT_REAR');check_inputs();bind_input('core',core)
  out.update(stage='PROPOSE',raw_digest=digest(raw),registry_digest=profilepin,solver_seconds_limit=30,internal_requested_count_scope='one bounded source study attempt, not product output count');save()
  p=search114.propose(core,1,time_limit=30,variant=0,sleep_roles=['double'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES')
  check_inputs();disposition=proposal_disposition(p);out['producer_status']=disposition
  if disposition!='PROPOSAL_ONLY':
   out.update(state='NO_SOURCE_PROPOSAL_NO_INFEASIBILITY_CLAIM',completed=True);return
  p,receipt=normalize_proposal(p);assignments={'A':p,'B':copy.deepcopy(p)};bind_input('proposals',assignments);ph=digest(p)
  out['transport']=receipt;out['stage']='CONSTRUCT';save()
  packet=constructor127.build(raw,'FRONT_REAR',assignments['A'],assignments['B']);out['construction_observed']=True;check_inputs()
  need(digest(packet['unit_proposal_hashes'])==digest({'A':ph,'B':ph}),'ORIGINAL_PROPOSAL_ASSIGNMENTS')
  ctx=constructor127.context(raw,packet,assignments);check_inputs()
  need(digest(ctx['construction_trace']['raw'])==inputpins['raw'] and digest(ctx['construction_trace']['proposals'])==inputpins['proposals'],'ORIGINAL_CONTEXT_INPUTS')
  bundle,_=transport({'packet':packet,'context':ctx,'raw':raw,'proposals':{'A':p,'B':copy.deepcopy(p)}});bundlepin=digest(bundle)
  packet=bundle['packet'];ctx=bundle['context'];model=packet['world_model'];program_bind(model,profile)
  out.update(stage='REPLAY',model_digest=digest(model),program_digest=digest(model['program']));save()
  replay=construction_replay127.verify(model,ctx);preserve_report(reports,live,pins,'replay',replay);check()
  need(replay['verified']is True and replay['model_hash']==digest(model),'ORIGINAL_REPLAY_FAILED')
  out.update(stage='PHYSICAL',replay_verified=True,fresh_model_verified=True,fresh_model_verified_scope='construction origin only, not physical or quality acceptance');save()
  physical=evaluate_pair127.evaluate(packet,ctx);preserve_report(reports,live,pins,'physical',physical);check()
  need(physical['model_hash']==digest(model),'PHYSICAL_MODEL_BINDING');need(digest(profile)==profilepin,'REGISTRY_MUTATION')
  out.update(state='FRESH_ONE_BED_PAIR_FULL_REPORTS_NOT_QUALIFIED',completed=True,
   physical_status=physical.get('status'),physical_errors=len(physical.get('errors',[])),physical_pending=len(physical.get('pending',[])),physical_error_code_counts=code_counts(physical.get('errors',[])),physical_pending_code_counts=code_counts(physical.get('pending',[])),
   historical_not_evaluated_count=len(physical.get('not_evaluated',[])),historical_out_of_scope_count=len(physical.get('out_of_scope',[])),
   units=[{'id':u['id'],'fixtures':len(u['fixtures']),'activities':len(u['activities'])}for u in model['units']])
 except Exception as ex:
  out.update(state='FAILED_CLOSED',completed=False,error_type=type(ex).__name__,error_code=str(ex)if re.fullmatch(r'[A-Z0-9_:]+',str(ex))else'NONPUBLIC_DETAIL_RETAINED_ONLY_IN_PROCESS',stage=out.get('stage','SOURCE_AUDIT'))
 finally:
  try:
   need(audited and snap is not None,'INITIAL_SOURCE_AUDIT_NOT_COMPLETED');check()
   need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'FINAL_ENGINE_GUARD')
   out['integrity_verified']=True
  except Exception as ex:out.update(integrity_verified=False,completed=False,state='INTEGRITY_ERROR',origin_verified_at_checkpoint=out.get('fresh_model_verified',False),fresh_model_verified=False,integrity_error_type=type(ex).__name__)
  out['report_digests']=pins
  # Full originals remain job-private temporary evidence, never uploaded or printed.
  out['full_original_reports_retained_job_temporarily']=True
  out['durable_private_archive']='NOT_CREATED';save()
def stop_process(proc):
 try:os.killpg(proc.pid,signal.SIGKILL)
 except ProcessLookupError:pass
 finally:proc.wait()
def main():
 if len(sys.argv)==3 and sys.argv[1]=='--child':child(sys.argv[2]);return
 with tempfile.TemporaryDirectory(prefix='one-bed-pair-')as tmp:
  dest=Path(tmp)/'run'
  remaining=(datetime(2026,11,19,10,52,35,tzinfo=timezone.utc)-datetime.now(timezone.utc)).total_seconds()
  budget=min(180,remaining-5);need(budget>0,'TASK_TIMEBOX_EXPIRED')
  proc=subprocess.Popen([sys.executable,'-B',__file__,'--child',str(dest)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
  timed=False;start=time.monotonic()
  try:proc.wait(timeout=budget)
  except subprocess.TimeoutExpired:
   timed=True;stop_process(proc)
  try:result=json.loads((dest/'summary.json').read_text())if(dest/'summary.json').exists()else{'state':'NO_SUMMARY'}
  except (ValueError,OSError):result={'state':'SUMMARY_PARSE_FAILED_CLOSED','completed':False,'fresh_model_verified':False}
  if type(result)is not dict:result={'state':'SUMMARY_TYPE_FAILED_CLOSED','completed':False,'fresh_model_verified':False}
  result.update(outer_timeout=timed,wait_completed=proc.poll()is not None,returncode=proc.returncode,elapsed_seconds=time.monotonic()-start,outer_budget_seconds=budget,full_model_uploaded=False)
  if timed or proc.returncode!=0:result.update(state='OUTER_TIMEOUT_PARTIAL_OBSERVATION'if timed else'PROCESS_FAILED_CLOSED',completed=False,origin_verified_at_checkpoint=result.get('fresh_model_verified',False),fresh_model_verified=False,observations_verified_after_process=False,qualified=False,accepted=False,display_allowed=False,delivery_allowed=False)
  print(json.dumps(result,sort_keys=True,allow_nan=False))
  need(not timed and proc.returncode==0 and result.get('completed')is True and result.get('integrity_verified')is True,'STUDY_NOT_COMPLETED')
if __name__=='__main__':main()
