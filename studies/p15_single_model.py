"""One P15 construction attempt; safe metadata only, no uploaded model."""
import copy,json,os,signal,subprocess,sys,tempfile,time,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app/local_integration'))
import single_model_p15 as p
from single_access_p15 import assess
def save(path,v):path.write_text(json.dumps(v,sort_keys=True,ensure_ascii=False,allow_nan=False))
def worker(folder):
 req=json.loads((folder/'request.json').read_text());body=bytes.fromhex(req['body_hex'])
 before=p.snapshot();pf=p.preflight(body);p.require(pf['execution_ready'],'PREFLIGHT')
 out={'schema':'P15_ACTUAL_CONSTRUCTION_V1','nonce':req['nonce'],'request_digest':p.digest(req),
      'state':'STARTED','attempts':1,'source_snapshot_digest':p.digest(before),'programme_digest':p.digest(pf['programme']),
      'geometry_source':'New nonpersonal dimensions; no archived model input',**{k:False for k in p.AUTH}}
 save(folder/'summary.json',out)
 import search114,checker114
 try:
  proposal=search114.propose(p.core(pf['raw']),2,time_limit=30,variant=0,sleep_roles=['double','twin'])
  proposal,transport=p.proposal_transport(proposal)
  save(folder/'proposal.json',proposal)
  out['producer_status']=proposal['status'];out['solver_status']=proposal.get('solver_status')
  out['solver_seconds']=proposal.get('solver_seconds');out['proposal_digest']=p.digest(proposal)
  if proposal['status']!='PROPOSAL_ONLY':out['state']='NO_MODEL_IN_THIS_ATTEMPT';return
  m=p.construct(pf['raw'],proposal);save(folder/'model.json',m)
  out['model_digest']=p.digest(m)
  replay=p.replay(m,pf['raw'],proposal);save(folder/'replay.json',replay)
  report=assess(m);save(folder/'access.json',report)
  # Retain the unmodified historical checker as diagnostic, never suppress n2-domain failures.
  historical=checker114.evaluate(m);historical,_=p.transport(historical);save(folder/'historical.json',historical)
  out.update(replay_digest=p.digest(replay),access_digest=p.digest(report),historical_digest=p.digest(historical),
   replay_verified=replay['verified'],access_state=report['state'],access_error_codes=[e['code']for e in report['errors']],
   historical_status=historical['status'],historical_errors=len(historical['errors']),historical_pending=len(historical['pending']),
   historical_scope='Unmodified pair checker is not a supported n1 admission evaluator; original complete report retained',
   actual_units=len(m['units']),fixture_count=len(m['units'][0]['fixtures']),four_current='NOT_EVALUATED',
   raw_archive_durable=False)
  p.require(replay['verified'],'REPLAY')
  p.require(report['state']=='PASS_SCOPED_OWNERSHIP_ACCESS','ACCESS_NOT_VERIFIED')
  # Actual-model negatives are applied only to copies, never to the emitted model.
  tests={}
  for name,mutate in [
   ('pair',lambda z:z['units'].append(copy.deepcopy(z['units'][0]))),
   ('hidden',lambda z:z['logical_regions'].update({'B.hidden':{'unit':'B'}})),
   ('empty_common',lambda z:z['common_routes'].update(stair_A=[])),
   ('empty_internal',lambda z:z['units'][0].update(routes={})),
   ('wrong_owner',lambda z:z['units'][0].update(ownership=[['0','0','18','20']])),
   ('wrong_count_type',lambda z:z['inputs'].__setitem__(2,True))]:
   z=copy.deepcopy(m);mutate(z);tests[name]=assess(z)['state']=='FAIL'
  p.require(all(tests.values())and len(tests)==6,'ACTUAL_NEGATIVE')
  p.require(p.digest(m)==out['model_digest'],'ACTUAL_MUTATION')
  out['actual_negatives']=tests;out['state']='ACTUAL_SINGLE_UNIT_MODEL_ACCESS_VERIFIED_NOT_QUALIFIED'
 finally:
  out['source_unchanged']=p.snapshot()==before
  if not out['source_unchanged']:out['state']='SOURCE_CHANGED'
  save(folder/'summary.json',out)
def run():
 start=time.monotonic()
 with tempfile.TemporaryDirectory()as d:
  folder=Path(d);req={'nonce':uuid.uuid4().hex,'body_hex':b'{"W":"18","L":"20","n":1}'.hex()}
  save(folder/'request.json',req)
  proc=subprocess.Popen([sys.executable,'-B',__file__,'--worker',d],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
  timed=False
  try:_,err=proc.communicate(timeout=240)
  except subprocess.TimeoutExpired:
   timed=True
   try:os.killpg(proc.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   _,err=proc.communicate()
  out=json.loads((folder/'summary.json').read_text())if(folder/'summary.json').exists()else{'state':'NO_SUMMARY'}
  # Full bytes read before cleanup; no solver/evaluator rerun in parent.
  if not timed and out.get('state')=='ACTUAL_SINGLE_UNIT_MODEL_ACCESS_VERIFIED_NOT_QUALIFIED':
   raw={k:json.loads((folder/(k+'.json')).read_text())for k in('model','proposal','access','replay','historical')}
   for key in raw:p.require(p.digest(raw[key])==out[key+'_digest'],'READBACK_'+key)
   p.require(out['nonce']==req['nonce']and out['request_digest']==p.digest(req),'REQUEST_BINDING')
   p.require(raw['access']['model_digest']==out['model_digest']==raw['replay']['model_digest'],'REPORT_MODEL')
   p.require(raw['access']['state']==out['access_state']and raw['replay']['verified']is True,'REPORT_SUMMARY')
   out['full_file_readback_verified']=True
  out.update(timed_out=timed,returncode=proc.returncode,wait_completed=proc.poll()is not None,elapsed_seconds=time.monotonic()-start,
             scope='One new single-unit model and necessary ownership/access; not qualified or API enabled',raw_archive_durable=False)
  print(json.dumps(out,sort_keys=True,ensure_ascii=False))
  return 0 if not timed and proc.returncode==0 and out.get('full_file_readback_verified')is True else 1
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--worker':worker(Path(sys.argv[2]))
 elif len(sys.argv)==1:raise SystemExit(run())
 else:raise SystemExit('ARGUMENTS')
