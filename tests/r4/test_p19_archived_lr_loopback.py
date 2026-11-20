"""Control-only HTTP tests: no replay, geometry, optimizer, archive asset."""
import copy,http.client,io,json,os,sys,tempfile,threading,time,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'studies'))
import p19_archived_lr_loopback as p
import http_withholding_x04 as x04

BODY=b'{"W":"20","L":"25","n":2}'
def control(_):
 return {'source_integrity_verified':True,'attempts':[{'receipt_verified':True}],
  'receipt_sha256':'f'*64,'archived_model_reused':True,'physical_status':'FAIL',
  'decision':{'state':'BLOCKED','blockers':['PHYSICAL_FAIL','CURRENT_UNKNOWN']},
  'private_key':'private:/wrong/row','generation_started':True}
def post(s,body=BODY,**headers):
 conn=http.client.HTTPConnection('127.0.0.1',s.server_port,timeout=8)
 try:
  conn.request('POST',p.ROUTE,body=body,headers={'Content-Type':'application/json',**headers})
  r=conn.getresponse();return r.status,json.loads(r.read())
 finally:conn.close()

def fixture():
 model={'inputs':p.CASE_SCOPE,'logical_regions':{'z':{},'a':{}}}
 mp=p.digest(model);core={'solver_inputs':['25','20',2]};local={'inputs':['25','20',2]};proposal={'status':'PROPOSAL_ONLY'}
 trace={'family':'LEFT_RIGHT','model_hash':mp,'core_hash':p.digest(core),'local_model_hash':p.digest(local),'raw':p.RAW,
  'proposals':{'A':proposal,'B':proposal},'source_revision':p.ENGINE_REVISION}
 ctx={'construction_trace':trace,'inputs':p.CASE_SCOPE}
 packet={'family':'LEFT_RIGHT','admission_claim':False,'core':core,'local_model':local,'world_model':model}
 row={'packet':packet,'context':ctx,'raw':p.RAW,'proposal':proposal,'world_model_digest':mp,'replay':{'verified':True},
  'historical_report':{'status':'FAIL'},'current_report':{},'source_binding':{'scoped_verified':True}}
 h=p.digest([row[k]for k in ('raw','proposal','packet','context')]);row.update(input_bundle_digest=h,input_bundle_digest_after=h)
 row['completed_report_digests']={k:p.digest(row[k])for k in ('replay','historical_report','current_report','source_binding')}
 return {'engine_revision':p.ENGINE_REVISION,'cases':[row]},mp

def zipbytes(doc):
 d=io.BytesIO()
 with zipfile.ZipFile(d,'w')as z:z.writestr(p.ARCHIVE_MEMBER,json.dumps(doc))
 return d.getvalue()

class ArchivePathTests(unittest.TestCase):
 def test_native_archive_order_and_exact_pin(self):
  doc,mp=fixture();b=zipbytes(doc);r=p.archive_row(b,p.sha(b),mp)
  self.assertEqual(list(r['packet']['world_model']['logical_regions']),['z','a'])
  for pin,model in [('0'*64,mp),(p.sha(b),'0'*64)]:
   with self.assertRaises(ValueError):p.archive_row(b,pin,model)
 def test_rehashed_family_and_report_rejected(self):
  for target,key,value,code in [('packet','family','FRONT_REAR','ARCHIVE_FAMILY'),('historical_report','status','PASS','ARCHIVE_ORIGINAL_REPORT')]:
   doc,mp=fixture();doc['cases'][0][target][key]=value;b=zipbytes(doc)
   with self.assertRaisesRegex(ValueError,code):p.archive_row(b,p.sha(b),mp)
 def test_file_exclusivity_and_private_mode(self):
  with tempfile.TemporaryDirectory()as d:
   out=p.private_directory(Path(d)/'private')
   self.assertEqual(p.write(out,'x.json',b'private'),p.sha(b'private'))
   with self.assertRaises(FileExistsError):p.write(out,'x.json',b'replace')
   link=out/'symlink';link.symlink_to(out/'x.json')
   with self.assertRaises(ValueError):p.private_read(link)
   (out/'x.json').chmod(0o644)
   with self.assertRaisesRegex(ValueError,'PRIVATE_FILE_REQUIRED'):p.private_read(out/'x.json')

class HTTPTests(unittest.TestCase):
 def open(self,run):
  s=p.server(run);t=threading.Thread(target=s.serve_forever);t.start()
  self.addCleanup(s.server_close);self.addCleanup(t.join,6);self.addCleanup(s.shutdown)
  return s
 def safe(self,body):
  for k,v in p.ZERO.items():self.assertIs(body[k],v) if type(v)is bool else self.assertEqual(body[k],v)
  self.assertNotIn('private',json.dumps(body).lower().replace('p19_private_archive_http_v1','').replace('operator_only_archived_model_study',''))
 def test_invalid_unsupported_wire_othercase_no_worker(self):
  calls=[]
  s=self.open(lambda b:(calls.append(b),control(b))[1])
  for b,code in [(b'{"W":"20","L":"25","n":3}',422),(b'{"W":20.0,"L":"25","n":2}',409),(b'{"W":"25","L":"20","n":2}',409),(b'{"W":"20","L":"25","n":1}',409),(b'{"W":"20","L":"25","n":2,"archive":"wrong"}',422)]:
   status,row=post(s,b);self.assertEqual(status,code);self.assertFalse(row['archived_evaluation_started'])
  self.assertFalse(calls)
  self.assertEqual(post(s,Host='example.invalid')[0],403)
  self.assertEqual(post(s,Origin='https://example.invalid')[0],403)
 def test_one_real_http_archive_worker_and_projection(self):
  calls=[]
  s=self.open(lambda b:(calls.append(b),control(b))[1]);status,row=post(s)
  self.assertEqual(status,200);self.safe(row)
  self.assertEqual(calls,[BODY]);self.assertTrue(row['archived_evaluation_started']);self.assertTrue(row['archived_model_reused'])
  self.assertFalse(row['outer_observation']['receipt_verified']);self.assertEqual(row['archive_report_receipt_sha256'],'f'*64)
  self.assertEqual(row['decision']['state'],'BLOCKED')
  self.assertEqual(post(s)[1]['status'],'ARCHIVE_ONE_SHOT_ALREADY_USED');self.assertEqual(calls,[BODY])
 def test_failure_does_not_expose_exception(self):
  def run(_):raise ValueError('private host/file/payload')
  s=self.open(run);status,row=post(s)
  self.assertEqual(status,500);self.safe(row);self.assertTrue(row['archived_evaluation_started']);self.assertFalse(row['archived_model_reused'])
  self.assertNotIn('archive_report_receipt_sha256',row)
 def test_unverified_and_forged_projection_fail_closed(self):
  invalid=[{'attempts':[]},{'attempts':[{'receipt_verified':1}]},{'source_integrity_verified':False},
   {'decision':{'state':'NO_VERIFIED_DECISION','blockers':[]}},{'decision':{'state':'BLOCKED','blockers':['PRIVATE_PAYLOAD']}},
   {'physical_status':'PRIVATE_PATH'}]
  for fields in invalid:
   runtime={**control(BODY),**fields}
   s=self.open(lambda _:runtime)
   status,row=post(s);self.assertEqual(status,500);self.safe(row)
   self.assertFalse(row['archived_model_reused']);self.assertNotIn('archive_report_receipt_sha256',row)
  projected=p.project(control(BODY))
  projected.update(decision={'state':'NO_VERIFIED_DECISION','blockers':[]},http_lifecycle={'response_state':'ON_TIME_OBSERVED'})
  self.assertEqual(p.safe_response(200,projected)['status'],'ARCHIVE_RECEIPT_UNAVAILABLE')
 def test_deadline_withholds_and_worker_retains_lock(self):
  entered=threading.Event();release=threading.Event()
  def run(body):
   entered.set();release.wait(6);return control(body)
  with patch.object(x04,'LIMIT_SECONDS',.35):
   s=self.open(run)
   try:
    status,row=post(s);self.assertTrue(entered.is_set());self.assertEqual(status,504);self.safe(row)
    self.assertTrue(row['archived_evaluation_started']);self.assertFalse(row['archived_model_reused']);self.assertNotIn('archive_report_receipt_sha256',row)
    self.assertTrue(s.private_worker_lock.locked())
    self.assertEqual(post(s)[1]['status'],'ARCHIVE_WORKER_BUSY')
   finally:release.set()
   stop=time.monotonic()+5
   while s.private_worker_lock.locked() and time.monotonic()<stop:time.sleep(.02)
   self.assertFalse(s.private_worker_lock.locked())
   self.assertEqual(s.private_boundary.snapshot()[0]['response_state'],'WITHHELD')

if __name__=='__main__':unittest.main()
