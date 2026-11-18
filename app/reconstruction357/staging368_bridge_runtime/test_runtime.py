import unittest,tempfile,json,uuid,hashlib
from pathlib import Path
from unittest.mock import patch
import bootstrap as b
class RuntimeTests(unittest.TestCase):
 def test_completed(self):
  s={'reason':'COMPLETED','worker_returncode':0,'cleanup_verified':True,'worker_reaped':True,'unresolved':[]};self.assertTrue(b.completed(s))
  for k,v in [('reason','TIMEOUT'),('worker_returncode',False),('worker_returncode',1),('cleanup_verified',False),('unresolved',[1])]:self.assertFalse(b.completed(dict(s,**{k:v})))
 def test_run_path(self):
  with tempfile.TemporaryDirectory()as d,patch.object(b,'ROOT',Path(d)):
   rid=str(uuid.uuid4());p=Path(d)/'review368_runs'/rid;p.mkdir(parents=True);self.assertEqual(b.run_folder(rid),p)
   for x in('../x',rid.upper(),'notuuid'):
    with self.assertRaises((ValueError,AttributeError)):b.run_folder(x)
 def test_inputs(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d);r=str(uuid.uuid4());request={'run_id':r,'envelope':{}};raw={'schema':'FINAL_PIPELINE368_RUN','generation_run_id':r,'status':'REVIEWED_NOT_QUALIFIED'}
   b.write_once(p/'request.json',request);b.write_once(p/'result.json',raw);self.assertEqual(b.read_inputs(p,r)[:2],(request,raw))
   raw['generation_run_id']=str(uuid.uuid4());(p/'result.json').write_text(json.dumps(raw))
   with self.assertRaises(ValueError):b.read_inputs(p,r)
 def test_write_once(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'x';b.write_once(p,{'a':1})
   with self.assertRaises(FileExistsError):b.write_once(p,{'a':2})
   self.assertEqual(json.loads(p.read_text()),{'a':1})
 def test_unreleased_freeze(self):
  with self.assertRaisesRegex(ValueError,'NOT_RELEASED'):b.verify_freeze('PENDING')
 def test_source_mutation(self):
  with tempfile.TemporaryDirectory()as d,patch.object(b,'ROOT',Path(d)),patch.object(b,'HERE',Path(d)):
   p=Path(d);(p/'source.py').write_text('ORIGINAL');f={'files':{'source.py':hashlib.sha256(b'ORIGINAL').hexdigest()}};(p/'source_freeze.json').write_text(json.dumps(f));h=hashlib.sha256((p/'source_freeze.json').read_bytes()).hexdigest();b.verify_freeze(h);(p/'source.py').write_text('MUTATED')
   with self.assertRaisesRegex(ValueError,'SOURCE_DRIFT'):b.verify_freeze(h)
if __name__=='__main__':unittest.main()
