import tempfile,hashlib,json,unittest
from pathlib import Path
from bootstrap import verify
class Tests(unittest.TestCase):
 def test_tamper_before_project_import(self):
  with tempfile.TemporaryDirectory()as d:
   r=Path(d);p=r/'server.py';p.write_text("raise Exception('must never import')")
   m=r/'manifest.json';m.write_text(json.dumps({'files':{'server.py':hashlib.sha256(p.read_bytes()).hexdigest()}}));h=hashlib.sha256(m.read_bytes()).hexdigest()
   p.write_text("open('SIDE_EFFECT','w').write('bad')")
   with self.assertRaisesRegex(ValueError,'BOOTSTRAP_SOURCE_CHANGED'):verify(r,m,h)
   self.assertFalse((r/'SIDE_EFFECT').exists())
 def test_manifest_tamper(self):
  with tempfile.TemporaryDirectory()as d:
   r=Path(d);m=r/'m.json';m.write_text('{"files":{}}')
   with self.assertRaisesRegex(ValueError,'MANIFEST_CHANGED'):verify(r,m,'0'*64)
if __name__=='__main__':unittest.main()
