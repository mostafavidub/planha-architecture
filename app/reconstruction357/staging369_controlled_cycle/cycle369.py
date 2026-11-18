"""Single test-only controlled cycle, one shared240s deadline, no retry."""
import copy,hashlib,json,sys,time,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;WORKSPACE=ROOT.parent
folder=Path(sys.argv[1]);run_id=sys.argv[2]
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from supervisor import supervise
sys.path.insert(0,str(WORKSPACE/'staging369_current_family_repair'))
from operator369 import digest,protected
start=time.monotonic();deadline=start+240;phases=[]
def read(n):return json.loads((folder/n).read_text())
def emit(event):
 with(folder/'events.jsonl').open('a')as f:f.write(json.dumps({'run_id':run_id,**event})+'\n')
def stage(name,cap=None):
 remaining=deadline-time.monotonic()
 if remaining<=0:raise ValueError('SHARED240_DEADLINE')
 budget=min(remaining,cap)if cap else remaining
 emit({'phase':name,'status':'STARTED','budget_seconds':budget})
 evidence=folder/(name+'_supervision_evidence');evidence.mkdir()
 s=supervise([sys.executable,'-B',str(HERE/'phase_worker369.py'),name,str(folder),str(budget),run_id],budget,evidence_directory=evidence)
 (folder/(name+'_supervision.json')).write_text(json.dumps(s,indent=2));phases.append({'phase':name,'supervision':s})
 if s.get('reason')!='COMPLETED'or s.get('worker_returncode')!=0 or not s.get('cleanup_verified')or not s.get('worker_reaped')or s.get('unresolved'):
  emit({'phase':name,'status':'STOPPED'});raise ValueError('PHASE_NOT_COMPLETED:'+name)
 emit({'phase':name,'status':'COMPLETED'})
out={'schema':'CONTROLLED_CURRENT_FAMILY369_CYCLE','run_id':run_id,'test_only':True,
     'natural_generation_failure':False,'form_path_executed':False,'retry':False,
     'repair_attempted':False,'fresh_count':0,'accepted':False,'delivery_allowed':False,
     'semantic_qualification':'UNKNOWN_NEW_GEOMETRY_NOT_REPROVEN'}
request=json.loads((HERE/'request368.json').read_text());request_hash=digest(request)
out['request_envelope_digest']=request_hash
out['input_digests']={k:request[k]for k in ('received_digest','raw_digest','canonical_request_digest')}
try:
 stage('construct',45)
 fixture=read('fixture_record.json')
 if fixture.get('test_only')is not True or digest(fixture['candidate']['request'])!=request['raw_digest']:
  raise ValueError('FIXTURE_INPUT_OR_SCOPE_CHANGED')
 stage('fresh_first',90);out['fresh_count']=1
 first=read('fresh_first.json');out['first_raw_status']=first['raw_report']['status']
 out['first_review_id']=first['review_id'];out['first_model_digest']=first['model_digest']
 stage('propose',3);proposal=read('proposal_result.json')
 if proposal['status']!='PROPOSAL_PREPARED'or proposal['plan'].get('status')!='RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED':
  out['status']='STRICT_REJECTION_GATE_BLOCKED';out['reason']=proposal.get('reason',proposal.get('status'))
 else:
  out['repair_attempted']=True;stage('reconstruct_repair',90)
  child=read('repaired_record.json');lineage=read('repair_lineage.json')
  if child.get('test_only')is not True or digest(protected(child))!=digest(protected(fixture)):
   raise ValueError('REPAIR_PROGRAM_OR_TEST_SCOPE_CHANGED')
  stage('fresh_second',90);out['fresh_count']=2;second=read('fresh_second.json')
  if first['review_id']==second['review_id']or first['model_digest']==second['model_digest']:
   raise ValueError('REVIEW_OR_MODEL_ID_REUSED')
  if second['input_record_digest']!=digest(child)or second['model_digest']!=lineage['model_digest']:
   raise ValueError('CHILD_REVIEW_LINEAGE_CHANGED')
  lineage=copy.deepcopy(lineage);lineage.update(review_id=second['review_id'],fresh_digest=digest(second),
       source_replay_required=False,fresh_review_required=False,raw_review_status=second['raw_report']['status'],
       semantic_qualification='UNKNOWN_NEW_GEOMETRY_NOT_REPROVEN',test_only=True)
  with(folder/'lineage_after_review.json').open('x')as f:json.dump(lineage,f,indent=2)
  out.update(status='CONTROLLED_CYCLE_EXECUTED_NOT_LIVE_END_TO_END',second_review_id=second['review_id'],
      second_model_digest=second['model_digest'],second_raw_status=second['raw_report']['status'],
      protected_snapshot_digest=digest(protected(child)),lineage=lineage)
except Exception as error:
 out.update(status='STOPPED',reason=type(error).__name__+':'+str(error))
if digest(json.loads((HERE/'request368.json').read_text()))!=request_hash:raise ValueError('IMMUTABLE_REQUEST_CHANGED')
out.update(phases=phases,seconds=time.monotonic()-start)
with(folder/'cycle_result.json').open('x')as f:json.dump(out,f,ensure_ascii=False,indent=2)
