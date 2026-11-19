import copy,json,shutil,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import current_entry_inventory_x05 as inv
class InventoryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name)
  cls.manifest=inv.decode((ROOT/inv.SPEC).read_bytes())
  for name in set(cls.manifest['files'])|set(cls.manifest['top_level_paths'])|inv.SELF|{inv.OLD}:
   src=ROOT/name;dst=cls.root/name;dst.parent.mkdir(parents=True,exist_ok=True)
   if src.is_symlink():dst.symlink_to(src.readlink())
   else:shutil.copyfile(src,dst)
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_actual_snapshot(self):
  out=inv.scan();self.assertEqual(out['file_count'],243);self.assertFalse(out['new_dispatch'])
  self.assertTrue(out['old_x03_failure_retained']);self.assertFalse(out['self_hash_closure'])
 def test_changed_blob(self):
  p=self.root/'app/local_integration/report_lifecycle112.py';old=p.read_bytes()
  try:
   p.write_bytes(old+b'\n# changed\n')
   with self.assertRaisesRegex(ValueError,'^STALE_SNAPSHOT_SOURCE_CHANGED$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_missing_path(self):
  p=self.root/'app/local_integration/request_trace109.py';old=p.read_bytes()
  try:
   p.unlink()
   with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_unknown_not_auto_registered(self):
  p=self.root/'app/local_integration/unreviewed_candidate.py'
  try:
   p.write_text('raise RuntimeError("must not import")')
   with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan(self.root)
  finally:p.unlink()
 def test_unknown_workflow(self):
  p=self.root/'.github/workflows/unreviewed.yml'
  try:
   p.write_text('name: unreviewed')
   with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan(self.root)
  finally:p.unlink()
 def test_missing_non_surface_record(self):
  name=next(p for p in self.manifest['files'] if p not in self.manifest['top_level_paths'])
  p=self.root/name;old=inv.read(self.root,name);link=p.readlink() if p.is_symlink() else None
  try:
   p.unlink()
   with self.assertRaisesRegex(ValueError,'^MISSING_REVIEWED_PATH$'):inv.scan(self.root)
  finally:
   if link is not None:p.symlink_to(link)
   else:p.write_bytes(old)
 def test_drop_addition_rejected(self):
  m=copy.deepcopy(self.manifest);m['reviewed_additions'].pop()
  with self.assertRaisesRegex(ValueError,'^REVIEWED_ADDITIONS_REQUIRED$'):inv.reconcile(m,inv.decode((ROOT/inv.OLD).read_bytes()))
 def test_no_dispatch_escalation(self):
  m=copy.deepcopy(self.manifest);m['reviewed_additions'][0]['new_dispatch']=True
  with self.assertRaisesRegex(ValueError,'^ADDITION_CLASSIFICATION$'):inv.reconcile(m,inv.decode((ROOT/inv.OLD).read_bytes()))
 def test_changed_provenance_tamper(self):
  m=copy.deepcopy(self.manifest);m['changed_source_tasks']['app/local_integration/request_trace109.py']['task']='R4-X.04'
  with self.assertRaisesRegex(ValueError,'^CHANGED_PROVENANCE_MISMATCH$'):inv.reconcile(m,inv.decode((ROOT/inv.OLD).read_bytes()))
 def test_addition_commit_tamper(self):
  for value in ('z'*40,'0'*40):
   m=copy.deepcopy(self.manifest);m['reviewed_additions'][0]['source_change_commit']=value
   with self.assertRaisesRegex(ValueError,'^ADDITION_PROVENANCE(_MISMATCH)?$'):inv.reconcile(m,inv.decode((ROOT/inv.OLD).read_bytes()))
 def test_self_scope_not_wildcard(self):
  m=copy.deepcopy(self.manifest);m['self_paths_unhashed'].append('tests/**')
  with self.assertRaisesRegex(ValueError,'^SELF_SCOPE_CHANGED$'):inv.reconcile(m,inv.decode((ROOT/inv.OLD).read_bytes()))
 def test_old_manifest_pinned(self):
  p=self.root/inv.OLD;old=p.read_bytes()
  try:
   p.write_bytes(old+b' ')
   with self.assertRaisesRegex(ValueError,'^OLD_MANIFEST_CHANGED$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_old_failure_not_rewritten(self):
  import current_entry_inventory_x03 as historical
  with self.assertRaisesRegex(ValueError,'^INVENTORY_SOURCE_CHANGED$'):historical.scan()
 def test_changed_during_read(self):
  real=inv.read;target='app/local_integration/report_lifecycle112.py';calls=[0]
  def changing(root,path):
   data=real(root,path)
   if path==target:
    calls[0]+=1
    if calls[0]>1:return data+b' '
   return data
  with patch.object(inv,'read',side_effect=changing):
   with self.assertRaisesRegex(ValueError,'^SOURCE_CHANGED_DURING_READ$'):inv.scan(self.root)
if __name__=='__main__':unittest.main()
