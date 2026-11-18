"""Four isolated real source phases. Fixed scope, no admission or cached substitute."""
import json,hashlib,time,uuid,copy,sys,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
FREEZE_SHA='0698f0958a23e2e882c60ff06e58490db01ed5fcaee084eb1d64318ff51046fa'
def execute(envelope,*,deadline_seconds=440,generation_run_id=None,on_event=None):
 manifest=HERE/'source_freeze.json'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=FREEZE_SHA:raise ValueError('PIPELINE_FREEZE_ANCHOR')
 m=json.loads(manifest.read_text())
 def check():
  for n,h in m['files'].items():
   if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('PIPELINE_SOURCE_DRIFT:'+n)
 check()
 from request_contract368 import verify,digest
 e=verify(envelope)
 if type(deadline_seconds)not in(int,float)or not math.isfinite(deadline_seconds)or not 0<deadline_seconds<=440:raise ValueError('BOUNDED_PIPELINE_DEADLINE')
 run_id=str(uuid.UUID(generation_run_id))if generation_run_id is not None else str(uuid.uuid4())
 folder=ROOT/'review368_runs'/run_id;folder.mkdir(parents=True,exist_ok=False)
 (folder/'request.json').write_text(json.dumps({'run_id':run_id,'envelope':copy.deepcopy(envelope)},ensure_ascii=False,indent=2))
 from supervisor import supervise
 started=time.monotonic();events=[];members=[];callback_errors=[]
 request_sha=hashlib.sha256((folder/'request.json').read_bytes()).hexdigest()
 def check_request():
  if hashlib.sha256((folder/'request.json').read_bytes()).hexdigest()!=request_sha:raise ValueError('RUN_REQUEST_CHANGED')
 def event(**v):
  v={'generation_run_id':run_id,**v};events.append(v)
  if on_event is not None:
   try:on_event(copy.deepcopy(v))
   except Exception as error:callback_errors.append(type(error).__name__)
  check_request()
 try:
  for kind in ('balanced','joint'):
   d=folder/kind;d.mkdir();member={'kind':kind}
   for phase in ('construct','review'):
    remaining=deadline_seconds-(time.monotonic()-started)
    if remaining<=0:raise ValueError('PIPELINE_DEADLINE')
    event(kind=kind,phase=phase,status='STARTED')
    evidence=d/(phase+'_supervision');evidence.mkdir()
    cmd=[sys.executable,'-B',str(HERE/'worker368.py'),str(manifest),FREEZE_SHA,str(d),kind,phase,str(min(90,remaining))]
    supervision=supervise(cmd,min(110,remaining),evidence_directory=evidence)
    (d/(phase+'_supervision.json')).write_text(json.dumps(supervision,indent=2))
    receipt=d/(phase+'_receipt.json')
    if supervision.get('reason')!='COMPLETED'or supervision.get('worker_returncode')!=0 or supervision.get('cleanup_verified')is not True or supervision.get('worker_reaped')is not True or supervision.get('unresolved')or not receipt.exists():raise ValueError('STAGE_NOT_COMPLETED:'+kind+':'+phase)
    member[phase]=json.loads(receipt.read_text());event(kind=kind,phase=phase,status='COMPLETED',candidate_id=member[phase]['binding']['candidate_id'],review_id=member[phase].get('review_id'))
   members.append(member)
  status='REVIEWED_NOT_QUALIFIED'
 except Exception as error:status='UNKNOWN';event(phase='stopped',status='STOPPED',reason=type(error).__name__+':'+str(error))
 check();check_request();out={'schema':'FINAL_PIPELINE368_RUN','generation_run_id':run_id,'canonical_request_digest':e['canonical_request_digest'],'raw_digest':e['raw_digest'],'received_digest':e['received_digest'],'status':status,'state':status,'members':members,'events':events,'callback_errors':callback_errors,'seconds':time.monotonic()-started,'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'supported_repair_reasons':[],'repair_attempted':False,'scope':'ONLY_FIXED26X28_N2_COUNT2_REAL_RECONSTRUCTION_REPLAY_CHECKER; NO_ALL_DOMAIN_CLAIM'}
 (folder/'result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));return out
