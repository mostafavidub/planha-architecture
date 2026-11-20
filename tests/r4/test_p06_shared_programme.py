"""P06 synthetic ledger/receipt/source controls only; never start a solver."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'studies'))
import p06_shared_programme_study as p

class Clock:
 def __init__(self):self.v=100.0
 def __call__(self):return self.v

def request():
 return {'body_hex':p.BODY.hex(),'request_sha256':p.sha(p.BODY),'core_digest':'b'*64,'canonical_raw_digest':p.digest(p.CASE),
  'programme_digests':{p.P2:'c'*64,p.P1:'d'*64},'p2_preflight_digest':'e'*64,'p2_binding_digest':'f'*64,'p1_request_digest':'1'*64}
def cfg():
 b=p.Budget(Clock());return p.task_config('a'*32,p.P2,b.lease(p.P2),request(),{'source':'synthetic'})
def success(folder,v):
 h=p.sha(p.read(folder/'config.json'))
 return {'schema':'P06_WORKER_COMPLETION_V1','config_sha256':h,'programme':v['programme'],'account_id':v['account_id'],
  'starts':{'producer':1,'milp':1,'highs':1},'returns':{'producer':1,'milp':1,'highs':1},
  'guards':[],'finished_clock':105.0,'source_still_matches':True,'synthetic_prebody_guard_verified':True,'solver_status':1,'incumbent':True}
PROC={'wait_completed':True,'timed_out':False,'returncode':0,'kill_sent':False,'observed_terminal_clock':106.0}
class Controls(unittest.TestCase):
 def test_common_deadline_no_reset_and_programme_order(self):
  k=Clock();b=p.Budget(k)
  with self.assertRaisesRegex(ValueError,'ORDER'):b.lease(p.P1)
  a=b.lease(p.P2);self.assertEqual(a['child_deadline'],280)
  k.v=252;d=b.lease(p.P1)
  self.assertEqual((d['ordinal'],d['common_deadline'],d['child_deadline']),(2,a['common_deadline'],400))
  self.assertEqual(b.ledger('a',k.v)['used_seconds'],152)
  k.v-=1
  with self.assertRaisesRegex(ValueError,'CLOCK'):b.now()
 def test_remaining_and_timeout_cannot_authorize_p1(self):
  k=Clock();b=p.Budget(k);b.lease(p.P2)
  timed={'result':'VERIFIED_SOLVER_TIMEOUT_NO_WITNESS','p1_eligible':True,'model_digest':None}
  self.assertFalse(p.transition_gate(b,'a',timed)['study_p1_allowed'])
  verdict={'result':'VERIFIED_WITH_WITNESS_NOT_QUALIFIED','p1_eligible':True,'model_digest':'a'*64}
  x=p.transition_gate(b,'a',verdict)
  self.assertTrue(x['study_p1_allowed']);self.assertFalse(x['policy_record']['execute_lower_program'])
  self.assertEqual([r['state']for r in x['policy_record']['stage_dispositions']],
     ['NOT_ENUMERATED','NOT_ENUMERATED','ATTEMPTED_WITH_WITNESS','NOT_IMPLEMENTED'])
  k.v=370;self.assertFalse(p.transition_gate(b,'a',verdict)['study_p1_allowed'])
  with self.assertRaisesRegex(ValueError,'INSUFFICIENT'):b.lease(p.P1)
 def test_typed_worker_receipts_reject_edited_or_fake_success(self):
  for kind,err in [('wrong_program','IDENTITY'),('fake_count','COUNTS'),('stale_hash','IDENTITY'),
   ('late','SOURCE_TIME'),('guard_trip','SOURCE_TIME'),('missing_return','UNRETURNED_CALL'),('timed_parent','PROCESS_TERMINAL')]:
   with self.subTest(kind=kind),tempfile.TemporaryDirectory()as td:
    f=Path(td);v=cfg();p.write(f/'config.json',v);proof=success(f,v);proc=copy.deepcopy(PROC)
    if kind=='wrong_program':proof['programme']=p.P1
    elif kind=='fake_count':proof['starts']['milp']=True
    elif kind=='stale_hash':proof['config_sha256']='0'*64
    elif kind=='late':proof['finished_clock']=281
    elif kind=='guard_trip':proof['guards']=['P06_ALTERNATIVE_PRODUCER']
    elif kind=='missing_return':proof['returns'].update(milp=0,highs=0)
    else:proc['timed_out']=True
    p.write(f/'worker-proof.json',proof)
    with self.assertRaisesRegex(ValueError,err):p.worker_proof(f,v,proc)
  with tempfile.TemporaryDirectory()as td:
   f=Path(td);v=cfg();p.write(f/'config.json',v);p.write(f/'worker-proof.json',success(f,v))
   self.assertEqual(p.worker_proof(f,v,PROC)['programme'],p.P2)
 def test_same_body_core_and_registered_programmes_in_actual_pure_preflight(self):
  import search114
  with patch.object(search114,'propose',side_effect=AssertionError('NO_SOLVER'))as no,patch('subprocess.Popen',side_effect=AssertionError('NO_CHILD'))as child:
   r=p.prepare(p.BODY)
   self.assertEqual(r['canonical_raw_digest'],p.digest(p.CASE));self.assertEqual(r['request_sha256'],p.sha(p.BODY))
   self.assertNotEqual(r['programme_digests'][p.P2],r['programme_digests'][p.P1])
   self.assertTrue(all(not a['dispatch_authorized'] and not a['fit_verified'] for a in r['p05_advisory'].values()))
   for a in r['p05_advisory'].values():
    if a['state']=='MEASURED_SCOPED_NO_FIT_CLAIM':self.assertEqual(a['core_digest'],r['core_digest'])
   with self.assertRaisesRegex(ValueError,'EXACT_SAME_REQUEST'):p.prepare(b'{"W":"18","L":"20","n":1}')
   no.assert_not_called();child.assert_not_called()
 def test_crossed_model_and_changed_core_before_any_evaluation(self):
  r=request();model={'inputs':['18','20',2],'profile':{'body_m':'.7'},
   'units':[{'id':uid,'rooms':{'bed1':[],'bed2':[]},'public_program':{'capacity':{'residents':4}}}for uid in 'AB'],
   'program':{'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin'],'design_occupants_per_unit':4}}
  core={'fixture_core':True};r['core_digest']=p.digest(core);mh=p.digest(model)
  prop={'bedrooms':2,'sleep_roles':['double','twin'],'status':'PROPOSAL_ONLY'}
  b={'packet':{'family':'FRONT_REAR','admission_claim':False,'core':core,'world_model':model,'local_model':model},
   'context':{'inputs':['18','20',2],'construction_trace':{'schema':'CONSTRUCTION_TRACE127_PAIR_V1','family':'FRONT_REAR','raw':p.CASE,'core_hash':r['core_digest'],'model_hash':mh,'local_model_hash':mh,
    'proposals':{'A':prop,'B':prop}}},'model_digest':mh,**p.DENIED}
  self.assertEqual(p.bound_model(b,r,p.P2),mh)
  with self.assertRaisesRegex(ValueError,'MODEL_PROGRAMME'):p.bound_model(b,r,p.P1)
  b['context']['inputs']=['18','20',2.0]
  with self.assertRaisesRegex(ValueError,'MODEL_IDENTITY'):p.bound_model(b,r,p.P2)
  b['context']['inputs']=['18','20',2]
  b['packet']['core']={'fixture_core':1}
  with self.assertRaisesRegex(ValueError,'FRAME_CORE'):p.bound_model(b,r,p.P2)
 def test_status_incumbent_matrix_for_no_witness(self):
  def probe(label,status,incumbent):
   return p.proposal_evidence({'status':label,'solver_status':status,'budget_seconds':30},
       {'starts':{'milp':1},'solver_status':status,'incumbent':incumbent})
  self.assertEqual(probe('NO_PROPOSAL_IN_THIS_TOPOLOGY',2,False),'BOUNDED_NO_WITNESS')
  self.assertEqual(probe('NO_PROPOSAL_IN_THIS_TOPOLOGY',4,False),'SOLVER_FAULT')
  self.assertEqual(probe('SEARCH_TIMEOUT_NO_WITNESS',1,False),'SOLVER_TIMEOUT')
  self.assertEqual(probe('ROUNDED_PROPOSAL_REJECTED',1,True),'ROUNDED_REJECTED')
  self.assertEqual(p.proposal_evidence({'status':'NO_PROPOSAL_IN_THIS_PROGRAM','reason':'ROOM_OR_CORE_BOUND_CONFLICT'},{'starts':{'milp':0}}),'BOUND_CONFLICT_NO_SOLVER')
  for label,status,incumbent in (('NO_PROPOSAL_IN_THIS_TOPOLOGY',2,True),('SEARCH_TIMEOUT_NO_WITNESS',0,False),('ROUNDED_PROPOSAL_REJECTED',1,False)):
   with self.assertRaisesRegex(ValueError,'INCUMBENT_CONFLICT'):probe(label,status,incumbent)
 def test_p1_stock_index_rejects_missing_and_tampered_original(self):
  with tempfile.TemporaryDirectory()as td:
   f=Path(td);h=p.write(f/'physical-original.json',{'state':'FAIL'})
   block={'files':{'physical-original.json':{'bytes':len(p.read(f/'physical-original.json')),'sha256':h}},**p.DENIED}
   self.assertIsNone(p.stock_index(f,block,{'physical-original.json'}))
   with self.assertRaisesRegex(ValueError,'FILE_SET'):p.stock_index(f,block,{'physical-original.json','replay-original.json'})
   block['files']['physical-original.json']['sha256']='0'*64
   with self.assertRaisesRegex(ValueError,'STOCK_INDEX'):p.stock_index(f,block,{'physical-original.json'})
 def test_child_timeout_kill_and_wait_no_actual_process(self):
  import subprocess
  from unittest.mock import Mock
  with tempfile.TemporaryDirectory()as td:
   proc=Mock(pid=123456)
   proc.poll.side_effect=[None,-9]
   proc.wait.side_effect=[subprocess.TimeoutExpired('synthetic',1),-9]
   proc.returncode=-9
   with patch('subprocess.Popen',return_value=proc)as spawn,patch('os.killpg')as kill,patch.object(p.time,'monotonic',return_value=100):
    status=p.run_child(Path(td),101)
   spawn.assert_called_once()
   kill.assert_called_once_with(123456,p.signal.SIGKILL)
   self.assertEqual(proc.wait.call_count,2)
   self.assertEqual(status,{'returncode':-9,'timed_out':True,'kill_sent':True,'wait_completed':True,'observed_terminal_clock':100})
 def test_fake_process_success_without_native_receipt_never_attempts_p1(self):
  with tempfile.TemporaryDirectory()as td,patch.object(p,'source_state',return_value={'source':'synthetic'}),patch.object(p,'prepare',return_value=request()),patch.object(p,'run_child',return_value=PROC)as child:
   result=p.execute(Path(td),p.Budget(Clock()))
   self.assertEqual(result['state'],'SCOPED_PARTIAL_OR_FAILED_CLOSED')
   self.assertTrue(result['attempts'][0]['attempted']);self.assertFalse(result['attempts'][0]['verified'])
   self.assertFalse(result['attempts'][1]['attempted']);child.assert_called_once()
if __name__=='__main__':unittest.main()
