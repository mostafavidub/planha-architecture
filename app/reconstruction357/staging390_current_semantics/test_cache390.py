"""Pure canonical-cache regressions; no semantic execution."""
import unittest,tempfile,json,hashlib,sys
from pathlib import Path
from unittest.mock import patch
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import frozen390 as f
D=lambda b:hashlib.sha256(b).hexdigest()
class CacheTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.w=Path(self.tmp.name);self.p=self.w/'a';self.p.write_bytes(b'original');self.man=self.w/'freeze.json';self.original=(f.W,f.MANIFEST,f._EXPECTED,f._CACHE);f.W=self.w;f.MANIFEST=self.man;f._EXPECTED=None;f._CACHE={}
 def tearDown(self):f.W,f.MANIFEST,f._EXPECTED,f._CACHE=self.original;self.tmp.cleanup()
 def manifest(self,files=None):
  self.man.write_text(json.dumps({'files':files or {'a':D(b'original')}}));return D(self.man.read_bytes())
 def test_cache_index_once_and_every_read_verifies_bytes(self):
  sha=self.manifest()
  with patch.object(f.json,'loads',wraps=json.loads)as parse:
   f.configure(sha);self.assertEqual(f.bytes_for(self.p),b'original');f.bytes_for(self.p);self.assertEqual(parse.call_count,1)
  self.p.write_bytes(b'tampered')
  with self.assertRaisesRegex(ValueError,'DEPENDENCY_CHANGED'):f.bytes_for(self.p)
 def test_changed_manifest_rejected_even_after_cache(self):
  f.configure(self.manifest());self.man.write_text(self.man.read_text()+' ')
  with self.assertRaisesRegex(ValueError,'FREEZE_CHANGED'):f.bytes_for(self.p)
 def test_same_hash_canonical_alias_allowed(self):
  f.configure(self.manifest({'a':D(b'original'),'./a':D(b'original')}));self.assertEqual(f.bytes_for(self.w/'./a'),b'original')
 def test_conflicting_alias_rejected(self):
  with self.assertRaisesRegex(ValueError,'CONFLICTING'):f.configure(self.manifest({'a':D(b'original'),'./a':'0'*64}))
 def test_manifest_path_escape_rejected(self):
  with self.assertRaisesRegex(ValueError,'OUTSIDE'):f.configure(self.manifest({'../a':'0'*64}))
 def test_requested_path_escape_rejected(self):
  f.configure(self.manifest())
  with self.assertRaisesRegex(ValueError,'OUTSIDE'):f.bytes_for(self.w/'../a')
 def test_unregistered_file_rejected(self):
  f.configure(self.manifest());p=self.w/'other';p.write_bytes(b'original')
  with self.assertRaisesRegex(ValueError,'UNREGISTERED'):f.bytes_for(p)
 def test_wrong_initial_manifest_and_reconfigure_rejected(self):
  sha=self.manifest()
  with self.assertRaisesRegex(ValueError,'FREEZE_CHANGED'):f.configure('0'*64)
  f._EXPECTED=None;f.configure(sha)
  with self.assertRaisesRegex(ValueError,'ALREADY_CONFIGURED'):f.configure('0'*64)
 def test_symlink_escape_rejected(self):
  (self.w/'escape').symlink_to('/tmp')
  with self.assertRaisesRegex(ValueError,'OUTSIDE'):f.configure(self.manifest({'escape/outside':'0'*64}))

if __name__=='__main__':unittest.main()
