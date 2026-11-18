"""Pure WSGI transport tests with explicitly test-only fake execution; no generator."""
import unittest,tempfile,json,io,sys,copy,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from request_contract368 import parse_json
from server import Application
from state_machine import redesign_decision,event_view,final_view
BODY=json.dumps({'W':'۲۶','L':'28.0','n':'2','requested_count':'2'})
class Tests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.calls=[]
 def tearDown(self):self.tmp.cleanup()
 def make(self,bad=False):
  def invoke(envelope,run_id,folder):
   self.calls.append((envelope,run_id));return {'state':'REVIEWED_NOT_QUALIFIED','generation_run_id':run_id,'canonical_request_digest':envelope['canonical_request_digest'],'raw_digest':'wrong'if bad else envelope['raw_digest'],'test_only':True}
  return Application(_test_parser=parse_json,_test_invoke=invoke,_test_root=Path(self.tmp.name),_test_synchronous=True)
 def request(self,app,path='/api/runs',method='POST',body=BODY):
  status=[];res=b''.join(app({'PATH_INFO':path,'REQUEST_METHOD':method,'CONTENT_TYPE':'application/json','CONTENT_LENGTH':str(len(body.encode())),'wsgi.input':io.BytesIO(body.encode())},lambda s,h:status.append(s)));return status[0],json.loads(res)
 def test_cross_origin_not_submitted(self):
  app=self.make();statuses=[];result=b''.join(app({'PATH_INFO':'/api/runs','REQUEST_METHOD':'POST','CONTENT_TYPE':'application/json','HTTP_ORIGIN':'https://untrusted.example','CONTENT_LENGTH':str(len(BODY.encode())),'wsgi.input':io.BytesIO(BODY.encode())},lambda s,h:statuses.append(s)))
  self.assertEqual(statuses,['403 Forbidden']);self.assertFalse(self.calls)
 def test_exact_typed_request_reaches_execution(self):
  app=self.make();status,post=self.request(app);self.assertEqual(status,'202 Accepted');_,out=self.request(app,post['status_url'],'GET','');self.assertEqual(out['state'],'REVIEWED_NOT_QUALIFIED');self.assertEqual(self.calls[0][0]['received_types']['W'],'str');self.assertEqual(self.calls[0][0]['normalized_raw']['W'],'26');self.assertNotEqual(out['canonical_request_digest'],out['raw_digest'])
 def test_unsupported_no_execute(self):
  app=self.make();s,x=self.request(app,body=BODY.replace('28.0','29'));self.assertEqual(x['state'],'CAPABILITY_UNAVAILABLE');self.assertFalse(self.calls)
 def test_exact_unsupported_dimension(self):
  for w in ('27','26.0000000000000000000000000001'):
   app=self.make();raw=json.loads(BODY);raw['W']=w;_,x=self.request(app,body=json.dumps(raw));self.assertEqual(x['state'],'CAPABILITY_UNAVAILABLE');self.assertFalse(self.calls)
 def test_nan_malformed_invalid(self):
  for w in ('NaN','26e0','nonsense'):
   app=self.make();raw=json.loads(BODY);raw['W']=w;_,x=self.request(app,body=json.dumps(raw));self.assertEqual(x['state'],'INPUT_INVALID');self.assertFalse(self.calls)
 def test_boolean_no_execute(self):
  app=self.make();_,x=self.request(app,body='{"W":"26","L":"28","n":true,"requested_count":2}');self.assertEqual(x['state'],'INPUT_INVALID');self.assertFalse(self.calls)
 def test_duplicate_no_execute(self):
  app=self.make();_,x=self.request(app,body='{"W":"26","W":"26","L":"28","n":2,"requested_count":2}');self.assertEqual(x['state'],'INPUT_INVALID');self.assertFalse(self.calls)
 def test_no_caller_model_or_proof(self):
  app=self.make();raw=json.loads(BODY);raw['accepted']=True;_,x=self.request(app,body=json.dumps(raw));self.assertEqual(x['state'],'INPUT_INVALID');self.assertFalse(self.calls)
 def test_wrong_result_request_not_promoted(self):
  app=self.make(True);_,p=self.request(app);_,x=self.request(app,p['status_url'],'GET','');self.assertEqual(x['state'],'UNKNOWN');self.assertFalse(x['delivery_allowed'])
 def test_repeat_new_run_not_cache(self):
  app=self.make();_,a=self.request(app);_,b=self.request(app);self.assertNotEqual(a['generation_run_id'],b['generation_run_id']);self.assertEqual(len(self.calls),2)
 def test_busy_reject(self):
  app=self.make();app.active=True;s,x=self.request(app);self.assertEqual(s,'409 Conflict');self.assertFalse(self.calls)
 def test_foreign_job_404(self):
  app=self.make();s,x=self.request(app,'/api/runs/'+str(uuid.uuid4()),'GET','');self.assertEqual(s,'404 Not Found')
 def test_unknown_does_not_repair(self):self.assertEqual(redesign_decision({'verdict':'UNKNOWN'},['FIXTURE_COLLISION']),'STOP_NOT_PROVEN_FAIL')
 def test_unsupported_fail_stops(self):self.assertEqual(redesign_decision({'verdict':'FAIL','candidate_id':'c','review_id':'r','model_digest':'h','errors':[{'code':'OTHER'}]},[]),'STOP_UNSUPPORTED_REJECTION')
 def test_event_wrong_run_rejected(self):
  with self.assertRaises(ValueError):event_view({'generation_run_id':'other','phase':'review','status':'COMPLETED'},'current')
 def test_qualified_state_needs_set_witness(self):
  e=parse_json(BODY);x={'state':'QUALIFIED_CONCEPTUAL_SET','generation_run_id':'x','canonical_request_digest':e['canonical_request_digest'],'raw_digest':e['raw_digest']}
  with self.assertRaises(ValueError):final_view(x,e,'x')
if __name__=='__main__':unittest.main()
