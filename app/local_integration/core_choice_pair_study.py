"""Two source-selected central-core assemblies. Study only; no active API wiring.
Original replay/checker reports are retained unchanged, even when their compact-only
contract cannot validate the full-band choice. No private artifacts are consumed.
"""
import copy,inspect,json,os,re,subprocess,sys,tempfile,time,uuid
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
from front_rear_runtime_adapter import transport,proposal_transport,proposal_disposition,preserve_report,verify_reports
from same_version_front_rear_contract import digest,ENGINE_REVISION,FREEZE
from one_bed_pair_source_study import code_counts,stop_process
CHOICES={'FRONT_REAR_COMPACT118':'core_first','FRONT_REAR_FULL_BAND114':'full_band_core_first'}
def need(ok,code):
 if not ok:raise ValueError(code)
def selected_core(raw,choice):
 import contract114
 need(type(raw)is dict and set(raw)=={'W','L','n','requested_count'},'RAW_FIELDS')
 need(type(raw['n'])is int and raw['n']==2 and type(raw['requested_count'])is int and raw['requested_count']==1,'RAW_COUNTS')
 vals=[]
 for key in ('W','L'):
  need(type(raw[key])is str and re.fullmatch(r'[0-9]+(?:[.][0-9]+)?',raw[key])is not None,'RAW_DIMENSION_TOKEN')
  v=F(raw[key]);need(5<=v<=25,'RAW_DIMENSION_DOMAIN');vals.append(v)
 need(type(choice)is str and choice in CHOICES,'CORE_CHOICE')
 core=getattr(contract114,CHOICES[choice])(*vals)
 need(core is not None,'CURRENT_CORE_METHOD_NO_FIT_NOT_INFEASIBLE')
 return core,vals
def bind_profile(profile):
 need(type(profile)is dict and profile.get('approval',{}).get('status')=='APPROVED_DESIGN_PROGRAM','PROFILE_APPROVAL')
 for k,v in {'id':'PROGRAM_2BED_V1','version':1,'bedrooms_per_unit':2,'design_persons_per_unit':4,'sleep_roles':['double','twin'],'capacity_means_actual_population':False}.items():
  need(digest(profile.get(k))==digest(v),'PROFILE_FIELD')
def bind_program(model,profile):
 bind_profile(profile)
 for k,v in {'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin'],'design_occupants_per_unit':4,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True}.items():
  need(digest(model['program'].get(k))==digest(v),'MODEL_PROGRAM')
 need([u['id']for u in model['units']]==['A','B'],'PAIR_UNITS')
 need(model.get('accepted')is False and model.get('release_allowed')is False,'MODEL_AUTHORITY')
def make_receipt(raw,choice,profile,core,proposals,model,sources,nonce):
 need(type(nonce)is str and re.fullmatch('[0-9a-f]{32}',nonce)is not None,'RUN_NONCE')
 return {'run_nonce':nonce,'schema':'CORE_CHOICE_ORIGIN_V1','choice':choice,'raw_digest':digest(raw),'profile_digest':digest(profile),
 'core_digest':digest(core),'proposals_digest':digest(proposals),'model_digest':digest(model),'source_digest':digest(sources),'accepted':False,'qualified':False}
def bind_receipt(receipt,raw,choice,profile,core,proposals,model,sources,nonce):
 need(digest(receipt)==digest(make_receipt(raw,choice,profile,core,proposals,model,sources,nonce)),'ORIGIN_RECEIPT_MISMATCH')
def core_geometry(model,core):
 from core_wall_audit118 import q,hit,inside,covered
 errors=[];common=model['common_spaces'];units=model['units']
 if set(common)!={'stair','lift','lobby'}:errors.append('CORE_COMPONENT_INVENTORY')
 if digest(common)!=digest({k:core[k]for k in ('stair','lift','lobby')}):errors.append('SOURCE_CORE_GEOMETRY_CHANGED')
 if [u['id']for u in units]!=['A','B']:errors.append('UNIT_INVENTORY')
 ownership={u['id']:[q(r)for r in u['ownership']]for u in units}
 for uid in ('A','B'):
  if digest(next(u['ownership']for u in units if u['id']==uid))!=digest(core.get('unit_ownership',{}).get(uid,[core['units'][uid]])):errors.append('SOURCE_OWNERSHIP_CHANGED')
 if any(hit(a,b)for a in ownership['A']for b in ownership['B']):errors.append('UNIT_OWNERSHIP_OVERLAP')
 W,L=map(F,model['inputs'][:2]);frame=(F(0),F(0),W,L)
 if any(not inside(r,frame)for rs in ownership.values()for r in rs):errors.append('OWNERSHIP_OUTSIDE_FRAME')
 if set(common)=={'stair','lift','lobby'}:
  stair,lift=q(common['stair']),q(common['lift']);lobby=[q(r)for r in common['lobby']]
  if [stair[2]-stair[0],stair[3]-stair[1]]!=[F('4.55'),F('2.45')]or[lift[2]-lift[0],lift[3]-lift[1]]!=[F('1.65'),F('1.65')]:errors.append('SOURCE_CLEAR_SIZES_CHANGED')
  if hit(stair,lift)or any(hit(r,stair)or hit(r,lift)for r in lobby):errors.append('LOBBY_NOT_INDEPENDENT')
  if any(hit(r,c)for rs in ownership.values()for r in rs for c in [stair,lift]+lobby):errors.append('OWNERSHIP_COMMON_OVERLAP')
  # Positive shared-edge or interior connection, not a point-touch graph.
  todo={0};seen=set()
  while todo:
   i=todo.pop();seen.add(i)
   for j,b in enumerate(lobby):
    a=lobby[i];dx=min(a[2],b[2])-max(a[0],b[0]);dy=min(a[3],b[3])-max(a[1],b[1])
    if j not in seen and dx>=0 and dy>=0 and(dx>0 or dy>0):todo.add(j)
  if len(seen)!=len(lobby):errors.append('LOBBY_GRAPH_DISCONNECTED')
 entries=[]
 for uid in ('A','B'):
  os_=[o for o in model['openings']if o.get('id')==uid+'.entry']
  if len(os_)!=1 or digest(os_[0].get('connects'))!=digest(['lobby',uid+'.entry_circulation']):errors.append('INDEPENDENT_LOBBY_ENTRY_REQUIRED')
  else:entries.append(os_[0]['id'])
 return {'status':'FAIL'if errors else'PASS_SOURCE_CORE_PARTITION_ONLY','errors':sorted(set(errors)),'pending':[],
 'independent_entry_count':len(entries),'scope':'Source core/ownership/entry relations only; body routes independently assessed; no technical or quality approval'}
def child(folder,choice,nonce):
 from program_profile_registry import lookup
 from producer_provenance import snapshot,require_unchanged
 import engine114,guard400,search114,contract114,assemble114,constructor127,construction_replay127,evaluate_pair127,core_wall_audit118
 folder=Path(folder);folder.mkdir(exist_ok=False)
 out={'run_nonce':nonce,'schema':'CORE_CHOICE_STUDY_V1','choice':choice,'state':'STARTED','completed':False,'construction_observed':False,
 'independent_origin_verified':False,'integrity_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
 'current_four':'NOT_EVALUATED_CORE_CHOICE_ADAPTER_MISSING','technical_core':'POST_MVP_NOT_EVALUATED','internal_count_is_product_count':False}
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
  paths=['app/local_integration/'+n for n in ('core_choice_pair_study.py','one_bed_pair_source_study.py','program_profile_registry.py','front_rear_runtime_adapter.py','same_version_front_rear_contract.py')]
  paths+=['app/reconstruction357/planha_general150_runtime_work/'+m.__name__+'.py'for m in (contract114,assemble114,search114,constructor127,construction_replay127,evaluate_pair127,core_wall_audit118)]
  snap=snapshot(ROOT,paths)
  need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'ENGINE_GUARD')
  for mod,names in ((contract114,('core_first','full_band_core_first')),(assemble114,('assemble',)),(search114,('propose',)),(constructor127,('context',)),(construction_replay127,('verify',)),(evaluate_pair127,('evaluate',)),(core_wall_audit118,('core_concept','opening_hosts'))):
   for name in names:need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ENGINE/(mod.__name__+'.py'),'ACTUAL_IMPORT_PATH')
  audited=True;raw={'W':'18','L':'20','n':2,'requested_count':1};profile=lookup('PROGRAM_2BED_V1');bind_profile(profile)
  pin('raw',raw);pin('profile',profile);core,(W,L)=selected_core(raw,choice);pin('core',core)
  out.update(stage='PROPOSE',raw_digest=digest(raw),profile_digest=digest(profile),core_digest=digest(core),source_digest=digest(snap),solver_limit_seconds=30);save()
  p=search114.propose(core,2,time_limit=30,variant=0,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES');check()
  state=proposal_disposition(p);out['producer_status']=state
  if state!='PROPOSAL_ONLY':out.update(state='NO_PROPOSAL_NO_INFEASIBILITY_CLAIM',completed=True);return
  p,tr=proposal_transport(p)
  need(type(p.get('bedrooms'))is int and p['bedrooms']==2 and digest(p.get('sleep_roles'))==digest(['double','twin']),'PROPOSAL_PROGRAM')
  proposals={'A':p,'B':copy.deepcopy(p)};pin('proposals',proposals)
  out.update(stage='ASSEMBLE',proposal_digest=digest(proposals),coordinate_conversion_count=len(tr['coordinate_conversions']));save()
  model=assemble114.assemble(W,L,core,proposals['A'],unit_proposals=proposals);out['construction_observed']=True;check()
  model,_=transport(model);bind_program(model,profile)
  packet={'family':'FRONT_REAR','local_model':model,'world_model':model,'core':core,'unit_proposal_hashes':{k:digest(v)for k,v in proposals.items()},'admission_claim':False}
  # This original trace is deliberately NOT a claim that legacy127 supports corechoice.
  ctx=constructor127.context(raw,packet,proposals);check()
  bundle,_=transport({'packet':packet,'context':ctx});bp=digest(bundle);packet=bundle['packet'];ctx=bundle['context'];model=packet['world_model']
  receipt=make_receipt(raw,choice,profile,core,proposals,model,snap,nonce);pin('receipt',receipt)
  out.update(stage='INDEPENDENT_REPLAY',model_digest=digest(model),receipt_digest=digest(receipt),program_digest=digest(model['program']));save()
  again,(w,l)=selected_core(raw,choice);need(digest(again)==inputpins['core'],'CORE_REPLAY_MISMATCH')
  replay_model=assemble114.assemble(w,l,again,proposals['A'],unit_proposals=proposals);replay_model,_=transport(replay_model);check()
  bind_receipt(receipt,raw,choice,profile,again,proposals,replay_model,snap,nonce)
  out.update(independent_origin_verified=True,independent_origin_scope='Same selected source function and exact full reassembly; not original127 approval or quality')
  retain('independent_replay',{'verified':True,'model_hash':digest(model),'receipt_digest':digest(receipt),'authority':False})
  out['stage']='ORIGINAL_REPLAY_AND_FULL_PHYSICAL';save()
  retain('original_replay',construction_replay127.verify(model,ctx))
  retain('physical',evaluate_pair127.evaluate(packet,ctx))
  need(originals['physical']['model_hash']==digest(model),'PHYSICAL_MODEL_BINDING')
  out['stage']='CORE_CHECKERS';save()
  retain('core_partition',core_geometry(model,core))
  retain('core_concept',core_wall_audit118.core_concept(model))
  retain('opening_hosts',core_wall_audit118.opening_hosts(model))
  out.update(state='FULL_REPORTS_RETAINED_NOT_QUALIFIED',completed=True,legacy_replay_verified=originals['original_replay'].get('verified')is True,
   core_geometry_status=originals['core_partition']['status'],core_concept_status=originals['core_concept']['status'],opening_hosts_status=originals['opening_hosts']['status'],
   physical_status=originals['physical'].get('status'),physical_error_counts=code_counts(originals['physical'].get('errors',[])),
   physical_pending_counts=code_counts(originals['physical'].get('pending',[])),legacy_replay_error_counts=code_counts(originals['original_replay'].get('errors',[])),
   original_not_evaluated_count=len(originals['physical'].get('not_evaluated',[])),original_out_of_scope_count=len(originals['physical'].get('out_of_scope',[])),
   unit_count=len(model['units']),core_route_count=len(model['common_routes']),independent_entry_count=originals['core_partition']['independent_entry_count'],
   core_metrics_scope='Geometry only, no quality winner',lobby_rectangle_count=len(core['lobby']),
   ownership_piece_counts={u['id']:len(u['ownership'])for u in model['units']},
   original_adapter_scope='COMPACT_ONLY_ORIGINAL_REPLAY_AND_GRAMMAR_UNCHANGED')
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
 for choice in CHOICES:
  remaining=(datetime(2026,11,19,14,10,2,tzinfo=timezone.utc)-datetime.now(timezone.utc)).total_seconds()
  budget=min(240,remaining-5);need(budget>0,'TASK_TIMEBOX_EXPIRED')
  with tempfile.TemporaryDirectory(prefix='core-choice-')as tmp:
   dest=Path(tmp)/'run';start=time.monotonic();nonce=uuid.uuid4().hex
   proc=subprocess.Popen([sys.executable,'-B',__file__,'--child',str(dest),choice,nonce],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True);timed=False
   try:proc.wait(timeout=budget)
   except subprocess.TimeoutExpired:timed=True;stop_process(proc)
   try:result=json.loads((dest/'summary.json').read_text())if(dest/'summary.json').exists()else{'state':'NO_SUMMARY'}
   except(ValueError,OSError):result={'state':'SUMMARY_PARSE_FAILED_CLOSED'}
   if type(result)is not dict:result={'state':'SUMMARY_TYPE_FAILED_CLOSED'}
   if result.get('run_nonce')!=nonce:result.update(state='NONCE_BINDING_FAILED',completed=False,independent_origin_verified=False)
   result.update(choice=choice,outer_timeout=timed,wait_completed=proc.poll()is not None,returncode=proc.returncode,elapsed_seconds=time.monotonic()-start,outer_budget_seconds=budget,full_model_uploaded=False)
   if timed or proc.returncode!=0:result.update(completed=False,origin_observed_at_checkpoint=result.get('independent_origin_verified',False),independent_origin_verified=False,state='OUTER_TIMEOUT_PARTIAL_OBSERVATION'if timed else'PROCESS_FAILED_CLOSED')
   print(json.dumps(result,sort_keys=True,allow_nan=False),flush=True);results.append(result)
 need(all(r.get('completed')is True and r.get('integrity_verified')is True and not r['outer_timeout']and r['returncode']==0 for r in results),'STUDY_NOT_COMPLETED')
if __name__=='__main__':main()
