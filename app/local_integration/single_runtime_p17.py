"""One n1 HTTP attempt, fixed P15 family; full temporary evidence, no public raw."""
import copy,hashlib,json,math,os,signal,subprocess,sys,tempfile,time,uuid
from pathlib import Path
import single_model_p15 as p
import single_evaluation_p17 as binding
import single_decision_p17 as decision
AUTH=p.AUTH
def save(path,value):
 data=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
 tmp=path.with_suffix('.tmp');tmp.write_bytes(data);tmp.replace(path)
def read(path):
 p.require(not path.is_symlink(),'P17_FILE_SYMLINK');data=path.read_bytes()
 p.require(len(data)<=32*1024*1024,'P17_FILE_LIMIT')
 def pairs(items):
  out={}
  for k,v in items:
   p.require(k not in out,'P17_DUPLICATE_KEY');out[k]=v
  return out
 value=json.loads(data,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in()).throw(ValueError('P17_NONFINITE')))
 p.digest(value)
 return value,hashlib.sha256(data).hexdigest()
def worker(folder):
 request,_=read(folder/'request.json');body=bytes.fromhex(request['body_hex']);deadline=request['deadline']
 start=time.monotonic();before=binding.source_audit();pf=p.preflight(body)
 p.require(pf['execution_ready'],'P17_PREFLIGHT')
 out={'schema':'SINGLE_RUNTIME_P17_V1','nonce':request['nonce'],'request_digest':p.digest(request),'state':'STARTED','stage':'SETUP',
      'attempts':0,'report_digests':{},'source_snapshot':before,'source_integrity_verified':False,**{k:False for k in AUTH}}
 def stage(name):
  out['stage']=name;save(folder/'summary.json',out);p.require(time.monotonic()<deadline,'P17_BUDGET_EXHAUSTED')
 save(folder/'summary.json',out)
 try:
  import search114,checker114,single_physical_p17,single_access_p15
  stage('PROPOSE');out['attempts']=1;save(folder/'summary.json',out)
  proposal=search114.propose(p.core(pf['raw']),2,time_limit=min(30,max(.001,deadline-time.monotonic())),variant=0,sleep_roles=['double','twin'])
  proposal,_=p.proposal_transport(proposal);save(folder/'proposal.json',proposal)
  out['producer_status']=proposal['status']
  for key in ('solver_status','solver_seconds','budget_seconds'):
   v=proposal.get(key)
   p.require(v is None or type(v)in(int,float) and math.isfinite(v),'P17_SOLVER_METADATA')
   out[key]=v
  if proposal['status']!='PROPOSAL_ONLY':out['state']='NO_MODEL_IN_THIS_ATTEMPT';return
  stage('CONSTRUCT');m=p.construct(pf['raw'],proposal);save(folder/'model.json',m)
  out['model_digest']=p.digest(m);context=binding.context(pf['raw'],proposal)
  reports={};live={};pins={}
  def retain(name,value):
   p.digest(value);live[name]=value;reports[name]=copy.deepcopy(value);pins[name]=p.digest(value)
   save(folder/'originals.json',reports);out['report_digests']=copy.deepcopy(pins)
   p.require(p.digest(m)==out['model_digest'],'P17_MODEL_MUTATION')
   for k,v in live.items():p.require(p.digest(v)==pins[k],'P17_REPORT_MUTATION')
  stage('REPLAY');retain('replay',binding.verify(m,context))
  stage('ACCESS');retain('access',single_access_p15.assess(m))
  stage('HISTORICAL_PHYSICAL');r=checker114.evaluate(m);r,_=p.transport(r);retain('historical_physical',r)
  stage('SINGLE_PHYSICAL');r=single_physical_p17.evaluate(m,pf['raw'],proposal);r,_=p.transport(r);retain('physical',r)
  bundle={'schema':'SINGLE_EVALUATION_BUNDLE_P17_V1','packet':{'world_model':m},'context':context,'model_digest':out['model_digest'],
          'reports':reports,'report_digests':pins}
  save(folder/'bundle.json',bundle)
  import single_current_programme_evaluator_p17 as programme
  import single_source_guest_route_evaluator_p17 as guest
  import single_source_living_evaluator_p17 as living
  import single_source_wall_function_evaluator_p17 as walls
  modules=[programme,guest,living,walls];current={};current_live={};cpins={}
  for mod in modules:
   stage('CURRENT_'+mod.__name__)
   report=mod.assess(bundle);p.digest(report);cid=report['criterion']
   current_live[cid]=report;current[cid]=copy.deepcopy(report);cpins[cid]=p.digest(report)
   save(folder/'current.json',current)
   for k,v in current_live.items():p.require(p.digest(v)==cpins[k],'P17_CURRENT_MUTATION')
   for k,v in live.items():p.require(p.digest(v)==pins[k],'P17_ORIGINAL_MUTATION')
  stage('DECISION');d=decision.assemble(bundle,current,cpins);save(folder/'decision.json',d)
  # Actual-model negative contracts, no generation or altered original reports.
  negatives={}
  for name,change in [('n2_request',lambda z:z['context']['raw'].update(n=2)),('core',lambda z:z['context']['core']['stair'].__setitem__(0,'.5')),
                      ('numeric_type',lambda z:z['packet']['world_model']['inputs'].__setitem__(2,1.0)),('old_report',lambda z:z['reports']['physical'].update(schema='GENERAL117'))]:
   z=copy.deepcopy(bundle);change(z)
   if name=='old_report':z['report_digests']['physical']=p.digest(z['reports']['physical'])
   try:binding.bind_bundle(z)
   except ValueError:negatives[name]=True
   else:negatives[name]=False
  p.require(all(negatives.values()),'P17_NEGATIVE_ACCEPTED')
  stage('FINAL_BIND')
  p.require(p.digest(bundle['packet']['world_model'])==out['model_digest'],'P17_FINAL_MODEL')
  out.update(state='FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED',current_digests=cpins,decision_digest=p.digest(d),bundle_digest=p.digest(bundle),
             negatives=negatives,current_states={r['criterion']:r['state']for r in d['criteria']},
             physical_status=reports['physical']['status'],physical_errors=len(reports['physical']['errors']),physical_pending=len(reports['physical']['pending']),
             historical_status=reports['historical_physical']['status'],historical_errors=len(reports['historical_physical']['errors']),
             access_state=reports['access']['state'],raw_archive_durable=False)
 except Exception as ex:
  out.update(state='FAILED_CLOSED',error_type=type(ex).__name__)
  raise
 finally:
  out['source_integrity_verified']=binding.source_audit()==before
  out['within_budget']=time.monotonic()<deadline
  if not out['source_integrity_verified']:out['state']='SOURCE_CHANGED'
  if not out['within_budget']:out['state']='BUDGET_EXHAUSTED'
  out['elapsed_seconds']=time.monotonic()-start;save(folder/'summary.json',out)
def run_bound(body,deadline):
 started=time.monotonic();before=binding.source_audit();pf=p.preflight(body)
 p.require(pf['execution_ready'],'P17_UNSUPPORTED')
 p.require(type(deadline)in(int,float) and math.isfinite(deadline) and 0<deadline-started<=180,'P17_DEADLINE')
 request={'schema':'SINGLE_REQUEST_P17_V1','nonce':uuid.uuid4().hex,'body_hex':body.hex(),'deadline':deadline}
 with tempfile.TemporaryDirectory(prefix='p17-')as name:
  folder=Path(name);save(folder/'request.json',request)
  p.require(time.monotonic()<deadline,'P17_PRESPAWN_DEADLINE')
  proc=subprocess.Popen([sys.executable,'-B',__file__,'--worker',name],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  timed=False
  try:_,err=proc.communicate(timeout=max(.001,deadline-time.monotonic()))
  except subprocess.TimeoutExpired:
   timed=True
   try:os.killpg(proc.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   _,err=proc.communicate()
  summary,_=read(folder/'summary.json')if(folder/'summary.json').exists()else({'state':'NO_SUMMARY','attempts':0},None)
  observed={};data={}
  for key in ('request','summary','bundle','current','decision','originals','proposal','model'):
   path=folder/(key+'.json')
   if path.exists():
    value,h=read(path);observed[key]=h;data[key]=value
  usable=False;d=None
  if not timed and proc.returncode==0 and summary['state']=='FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED':
   p.require(summary['nonce']==request['nonce'] and summary['request_digest']==p.digest(request) and p.digest(data['request'])==p.digest(request),'P17_REQUEST_BINDING')
   b=data['bundle'];current=data['current'];d=data['decision']
   p.require(p.digest(b)==summary['bundle_digest'] and p.digest(b['context']['raw'])==p.digest(pf['raw']),'P17_BUNDLE_READBACK')
   p.require(p.digest(data['model'])==b['model_digest']==summary['model_digest'] and p.digest(data['proposal'])==p.digest(b['context']['proposal']),'P17_MODEL_READBACK')
   p.require(p.digest(data['originals'])==p.digest(b['reports']),'P17_ORIGINAL_READBACK')
   rebuilt=decision.assemble(b,current,summary['current_digests'])
   p.require(p.digest(rebuilt)==p.digest(d)==summary['decision_digest'],'P17_DECISION_READBACK')
   p.require(summary['current_states']=={r['criterion']:r['state']for r in d['criteria']},'P17_SUMMARY_CURRENT')
   ph=b['reports']['physical']
   p.require([summary['physical_status'],summary['physical_errors'],summary['physical_pending']]==[ph['status'],len(ph['errors']),len(ph['pending'])],'P17_SUMMARY_PHYSICAL')
   for key,h in observed.items():p.require(read(folder/(key+'.json'))[1]==h,'P17_FILE_CHANGED')
   usable=True
  source_ok=binding.source_audit()==before and summary.get('source_integrity_verified')is True
  usable=usable and source_ok and time.monotonic()<deadline
  row={'nonce':request['nonce'],'state':summary['state'],'model_digest':summary.get('model_digest'),'runtime_digest':p.digest(summary),
       'receipt_verified':usable,'solver_status':summary.get('solver_status'),'solver_seconds':summary.get('solver_seconds'),
       'stage':summary.get('stage'),'physical_status':summary.get('physical_status'),'physical_errors':summary.get('physical_errors'),
       'physical_pending':summary.get('physical_pending'),'historical_status':summary.get('historical_status'),'historical_errors':summary.get('historical_errors'),
       'current_states':summary.get('current_states'),'actual_negatives':summary.get('negatives'),
       'timed_out':timed,'returncode':proc.returncode,'wait_completed':proc.poll()is not None,
       'observed_file_hashes':observed,'stderr_digest':hashlib.sha256(err).hexdigest()}
  return {'schema':'SINGLE_HTTP_RESULT_P17_V1','state':'BLOCKED'if usable else summary['state'],'preflight':pf,'attempts':[row]if summary.get('attempts')==1 else[],
          'fresh_model_executed':bool(summary.get('model_digest')),'source_integrity_verified':source_ok,
          'current_decision':d['decision'] if usable else None,'http_full_evidence':{'schema':'SINGLE_READBACK_P17_V1','binding_verified':usable,'raw_archive_durable':False,
          'scope':'Same request/source/full-report readback and decision rederivation, not producer authenticity or P25 admission'},
          'elapsed_seconds':time.monotonic()-started,**{k:False for k in AUTH}}
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--worker':worker(Path(sys.argv[2]))
 else:raise SystemExit('P17_INTERNAL_WORKER_ARGUMENTS')
