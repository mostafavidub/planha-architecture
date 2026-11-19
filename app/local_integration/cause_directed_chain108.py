"""One fresh nonpersonal parent and at most one cause-selected child.
No private artifacts, uploads, API admission, error filtering or minimality claim.
"""
import copy,inspect,json,re,subprocess,sys,tempfile,time,uuid
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
from same_version_front_rear_contract import digest,ENGINE_REVISION,FREEZE
from front_rear_runtime_adapter import transport,proposal_transport,proposal_disposition,preserve_report,verify_reports,packet_binding,observed_digest,observed_copy
from one_bed_pair_source_study import code_counts,stop_process
from core_choice_pair_study import selected_core,bind_profile,bind_program
from cause_directed_contract108 import diagnose,freeze,bind_parent,check_child,resolution,validate_current_report
from precision_boundary208 import prepare
def need(ok,code):
 if not ok:raise ValueError(code)
def child(folder,nonce,request=None):
 from producer_provenance import snapshot,require_unchanged
 from program_profile_registry import lookup
 import engine114,guard400,search114,constructor127,construction_replay127,evaluate_pair127,cause_directed_candidate108
 import cause_directed_contract108,source_fit_profile207
 import current_programme_evaluator,source_guest_route_evaluator,source_living_evaluator,source_wall_function_evaluator
 folder=Path(folder);folder.mkdir(exist_ok=False)
 out={'schema':'CAUSE_DIRECTED_CHAIN108_V1','run_nonce':nonce,'state':'STARTED','completed':False,'integrity_verified':False,
  'parent_observed':False,'child_observed':False,'cause_repair_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
  'solver_limit_per_attempt':30,'maximum_attempts':2,'attempt_count':0,'whole_dependencies':'PRIOR_FUNCTIONAL_STUDIES_PARTIAL',
  'scope':'Cause-directed resynthesis with fixed dimensions and protected state, not minimal geometric repair'}
 originals={};live={};pins={};objects={};opins={};snap=None;audited=False
 out['stage_trace']=[]
 def save():
  stage=out.get('stage',out['state'])
  if not out['stage_trace'] or out['stage_trace'][-1]['stage']!=stage:out['stage_trace'].append({'stage':stage,'utc':datetime.now(timezone.utc).isoformat()})
  out['report_digests']=copy.deepcopy(pins)
  for name,value in (('reports.json',originals),('summary.json',out)):
   tmp=folder/(name+'.tmp');tmp.write_text(json.dumps(value,sort_keys=True,allow_nan=False));tmp.replace(folder/name)
 def pin(k,v):objects[k]=v;opins[k]=digest(v)
 def check():
  need(snap is not None,'SNAPSHOT_NOT_ESTABLISHED');require_unchanged(ROOT,snap)
  for k,v in objects.items():need(digest(v)==opins[k],'INPUT_OR_MODEL_MUTATION')
  verify_reports(originals,pins);verify_reports(live,pins)
 def retain(k,v):preserve_report(originals,live,pins,k,v);check();save()
 def collect(label,p,raw,profile,core):
  out['stage']=label+'_CONSTRUCT';save()
  p,tr=proposal_transport(p);proposals={'A':p,'B':copy.deepcopy(p)};pin(label+'_proposals',proposals)
  packet=constructor127.build(raw,'FRONT_REAR',proposals['A'],proposals['B']);check()
  packet=transport(packet)[0];pin(label+'_packet',packet)
  out[label+'_observed']=True;save()
  ctx=constructor127.context(raw,packet,proposals);check();ctx=transport(ctx)[0];pin(label+'_context',ctx)
  model=packet['world_model'];bind_program(model,profile);packet_binding(packet,ctx,raw,p)
  need(digest(packet['core'])==digest(core),'CORE_CHANGED')
  out[label+'_model_digest']=digest(model);save()
  out['stage']=label+'_FULL_ORIGINAL_REPORTS';save()
  retain(label+'_replay',construction_replay127.verify(model,ctx))
  retain(label+'_physical',evaluate_pair127.evaluate(packet,ctx))
  physical=originals[label+'_physical']
  need(physical['model_hash']==digest(model),'PHYSICAL_MODEL')
  need(originals[label+'_replay'].get('verified')is True,'ORIGINAL_REPLAY_NOT_VERIFIED')
  out[label+'_physical']={'status':physical.get('status'),'errors':code_counts(physical.get('errors',[])),'pending':code_counts(physical.get('pending',[])),
   'not_evaluated_count':len(physical.get('not_evaluated',[])),'out_of_scope_count':len(physical.get('out_of_scope',[]))}
  evidence={'packet':packet,'context':ctx,'model_digest':digest(model),'reports':{'physical':copy.deepcopy(physical),'original_replay':copy.deepcopy(originals[label+'_replay'])},
   'report_digests':{'physical':pins[label+'_physical'],'original_replay':pins[label+'_replay']}}
  pin(label+'_evidence',evidence);out[label+'_current']={}
  for mod in (current_programme_evaluator,source_guest_route_evaluator,source_living_evaluator,source_wall_function_evaluator):
   out['stage']=label+'_CURRENT_'+mod.__name__;save()
   key=label+'_current_'+mod.__name__;report=None
   summary={'state':'EVALUATOR_ERROR','integrity_verified':False,'missing_count':0,'evaluator_error_count':1}
   try:
    report=mod.assess(evidence)
    # Save returned evidence before validating binding or downstream mutation.
    preserve_report(originals,live,pins,key,report);save()
    check();validate_current_report(report,digest(model))
    errors=sum(v.get('kind')in('EVALUATOR_OR_SOURCE_BINDING_ERROR','INTEGRITY_ERROR')for v in report.get('findings',[]))
    errors+=sum(r.get('state')in('UNKNOWN_EVALUATOR_OR_BINDING_ERROR','EVALUATOR_ERROR')for u in report.get('units',[])for r in u.get('routes',[]))
    errors+=sum(r.get('state')=='EVALUATOR_ERROR'for u in report.get('units',[])for st in u.get('studies',[])for r in st.get('routes',[]))
    summary={'state':report['state'],'integrity_verified':report.get('integrity_verified')is True,'missing_count':len(report.get('missing',[])),'evaluator_error_count':errors}
   except Exception as ex:
    marker={'state':'EVALUATOR_ERROR','exception_type':type(ex).__name__,'returned_report_retained':key in originals,
     'returned_report_observed_digest':observed_digest(report),'authority':False}
    if key not in originals:marker['unverified_observation']=observed_copy(report)
    preserve_report(originals,live,pins,key+'_validation_error',marker);save()
   out[label+'_current'][mod.__name__]=summary;save()
  need(all(r['integrity_verified']and r['state']in('PASS','FAIL','UNKNOWN','NOT_EVALUATED')and not r['missing_count']and not r['evaluator_error_count']for r in out[label+'_current'].values()),'CURRENT_EVALUATION_BLOCKED')
  return packet,ctx,proposals,physical
 try:
  local=['cause_directed_chain108.py','cause_directed_contract108.py','cause_directed_candidate108.py','source_fit_candidate207.py','source_fit_profile207.py','precision_boundary208.py','public_wln_contract.py','dimension_contract.py','core_choice_pair_study.py','protected_repair_contract.py','explicit_pair_redirection.py','front_rear_runtime_adapter.py','same_version_front_rear_contract.py','program_profile_registry.py','guest_route_certificate_study.py','current_programme_evaluator.py','source_guest_route_evaluator.py','source_living_evaluator.py','source_wall_function_evaluator.py']
  paths=['app/local_integration/'+n for n in local]+['app/reconstruction357/planha_general150_runtime_work/'+n for n in('search114.py','constructor127.py','construction_replay127.py','evaluate_pair127.py','checker114.py','typed_public_access120.py','public_program_audit118.py')]
  if request is not None:
   from request_trace109 import validate_request
   validate_request(request,digest(request));pin('http_request',request)
   paths+=['app/local_integration/'+n for n in ('request_trace109.py','request_trace_server109.py','repair_attempt_control.py')]
   out.update(request_digest=digest(request),request_account_id=request['account_id'],request_source_digest=digest(request['source_snapshot']),request_mode='PARENT_ONLY')
  snap=snapshot(ROOT,paths)
  need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'ENGINE_GUARD')
  for mod,names in ((search114,('propose',)),(constructor127,('build','context')),(construction_replay127,('verify',)),(evaluate_pair127,('evaluate',))):
   for name in names:need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ENGINE/(mod.__name__+'.py'),'ENGINE_IMPORT')
  for mod,names in ((cause_directed_candidate108,('propose',)),(cause_directed_contract108,('diagnose','freeze','bind_parent','check_child')),(current_programme_evaluator,('assess',)),(source_guest_route_evaluator,('assess',)),(source_living_evaluator,('assess',)),(source_wall_function_evaluator,('assess',))):
   for name in names:need(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ROOT/'app/local_integration'/(mod.__name__+'.py'),'LOCAL_IMPORT')
  source_fit_profile207.source_check();audited=True
  raw=prepare(bytes.fromhex(request['body_hex'])if request is not None else b'{"W":"18","L":"22","n":2}')['raw'];profile=lookup('PROGRAM_2BED_V1');bind_profile(profile)
  core,_=selected_core(raw,'FRONT_REAR_COMPACT118')
  for k,v in (('raw',raw),('profile',profile),('core',core)):pin(k,v)
  out.update(raw_digest=digest(raw),profile_digest=digest(profile),core_digest=digest(core),source_digest=digest(snap),stage='PARENT_PROPOSAL',attempt_count=1);save()
  p=search114.propose(core,2,time_limit=30,variant=0,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES');check()
  out['parent_producer_status']=proposal_disposition(p);save()
  if out['parent_producer_status']!='PROPOSAL_ONLY':retain('parent_no_witness',p);out.update(state='BLOCKED_NO_PARENT_PROPOSAL',completed=True);return
  pp,pc,ps,pr=collect('parent',p,raw,profile,core)
  out['stage']='ACTUAL_PARENT_CAUSE';save()
  cause=diagnose(pp['world_model'],ps,raw['L'],pr);retain('parent_cause',cause)
  out['selected_causes']=cause['selected_causes']
  out['parent_cause_rows']=[{k:r[k]for k in('unit','cause','established')}for r in cause['rows']];save()
  if not cause['selected_causes']:out.update(state='BLOCKED_NO_SUPPORTED_CAUSE',completed=True);return
  if request is not None:out.update(state='BLOCKED_REPAIR_CONTROLLER_ADAPTER',completed=True);return
  contract=freeze(raw,pp,pc,ps,pr,cause,snap,nonce);pin('parent_contract',contract);retain('parent_contract',contract)
  rejected=0
  for field in('rectangle_dimensions','enabled_causes','run_nonce','protected'):
   bad=copy.deepcopy(contract)
   if field=='rectangle_dimensions':bad[field]['bed1']['width']='1'
   elif field=='enabled_causes':bad[field]=[]
   elif field=='run_nonce':bad[field]='0'*32
   else:bad[field]['unit_count']=True
   try:bind_parent(bad,raw,pp,pc,ps,pr,cause,snap,nonce)
   except ValueError:rejected+=1
  out['actual_parent_contract_negative_rejections']=rejected;need(rejected==4,'CONTRACT_NEGATIVE_NOT_REJECTED')
  bind_parent(contract,raw,pp,pc,ps,pr,cause,snap,nonce);check()
  out.update(stage='CAUSE_SELECTED_CHILD_PROPOSAL',attempt_count=2);save()
  p=cause_directed_candidate108.propose(core,2,time_limit=30,variant=0,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES',parent_contract=contract,enabled_causes=contract['enabled_causes']);check()
  out['child_producer_status']=proposal_disposition(p);save()
  if out['child_producer_status']!='PROPOSAL_ONLY':retain('child_no_witness',p);out.update(state='BLOCKED_BOUNDED_CHILD_NO_WITNESS',completed=True);return
  cp,cc,cs,cr=collect('child',p,raw,profile,core)
  preservation=check_child(contract,cp,cs);retain('child_preservation',preservation)
  childcause=diagnose(cp['world_model'],cs,raw['L'],cr);retain('child_cause',childcause)
  resolved=resolution(cause,childcause);retain('cause_resolution',resolved)
  bind_parent(contract,raw,pp,pc,ps,pr,cause,snap,nonce);check()
  out.update(state='CAUSE_RESOLVED_NOT_QUALIFIED'if resolved['all_target_causes_resolved']and not resolved['new_supported_causes']else'CHILD_TARGET_CAUSE_UNRESOLVED',
   completed=True,cause_repair_verified=resolved['all_target_causes_resolved']and not resolved['new_supported_causes'],protected_verified=True,
   resolution_rows=resolved['rows'],new_supported_causes=resolved['new_supported_causes'])
 except Exception as ex:
  out.update(state='FAILED_CLOSED',completed=False,error_type=type(ex).__name__,error_code=str(ex)if re.fullmatch(r'[A-Z0-9_:]+',str(ex))else'NONPUBLIC_DETAIL_NOT_PRINTED')
 finally:
  try:
   need(audited and snap is not None,'INITIAL_AUDIT_NOT_ESTABLISHED');check()
   need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'FINAL_ENGINE_GUARD');out['integrity_verified']=True
  except Exception as ex:out.update(state='INTEGRITY_ERROR',completed=False,integrity_verified=False,cause_repair_verified=False,protected_verified=False,integrity_error_type=type(ex).__name__)
  out.update(original_reports_retained_job_temporarily=True,durable_archive_created=False);save()
def main():
 if len(sys.argv)==5 and sys.argv[1]=='--request-child':
  from request_trace109 import validate_request
  request=json.loads(Path(sys.argv[3]).read_text());validate_request(request,sys.argv[4])
  child(sys.argv[2],request['nonce'],request);return
 if len(sys.argv)==4 and sys.argv[1]=='--child':child(sys.argv[2],sys.argv[3]);return
 need(len(sys.argv)==1,'NO_EXTRA_STUDY_MODES')
 budget=min(480,(datetime(2026,11,19,15,40,2,tzinfo=timezone.utc)-datetime.now(timezone.utc)).total_seconds()-5);need(budget>0,'TASK_TIMEBOX_EXPIRED')
 with tempfile.TemporaryDirectory(prefix='cause-directed-')as tmp:
  dest=Path(tmp)/'run';nonce=uuid.uuid4().hex;start=time.monotonic()
  proc=subprocess.Popen([sys.executable,'-B',__file__,'--child',str(dest),nonce],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True);timed=False
  try:proc.wait(timeout=budget)
  except subprocess.TimeoutExpired:timed=True;stop_process(proc)
  try:result=json.loads((dest/'summary.json').read_text())if(dest/'summary.json').exists()else{'state':'NO_SUMMARY'}
  except(ValueError,OSError):result={'state':'SUMMARY_PARSE_FAILED_CLOSED'}
  if type(result)is not dict:result={'state':'SUMMARY_TYPE_FAILED_CLOSED'}
  if result.get('run_nonce')!=nonce:result.update(state='NONCE_BINDING_FAILED',completed=False,cause_repair_verified=False)
  result.update(outer_timeout=timed,wait_completed=proc.poll()is not None,returncode=proc.returncode,elapsed_seconds=time.monotonic()-start,outer_budget_seconds=budget,full_model_uploaded=False)
  if timed or proc.returncode!=0:result.update(state='OUTER_TIMEOUT_PARTIAL_OBSERVATION'if timed else'PROCESS_FAILED_CLOSED',completed=False,cause_repair_verified=False,protected_verified=False)
  print(json.dumps(result,sort_keys=True,allow_nan=False),flush=True)
 need(result.get('completed')is True and result.get('integrity_verified')is True and not result['outer_timeout']and result['returncode']==0,'STUDY_NOT_COMPLETED')
if __name__=='__main__':main()
