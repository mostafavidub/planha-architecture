"""X05 V2 scoped reconciliation and independent real HTTP rejection; no solver."""
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
  cls.manifest=inv.decode((ROOT/inv.SPEC_V2).read_bytes())
  cls.previous=inv.decode((ROOT/inv.SPEC).read_bytes());cls.old=inv.decode((ROOT/inv.OLD).read_bytes())
  for name in set(cls.manifest['files'])|set(cls.manifest['top_level_paths'])|inv.SELF_V2|{inv.OLD,inv.SPEC}:
   src=ROOT/name;dst=cls.root/name;dst.parent.mkdir(parents=True,exist_ok=True)
   if src.is_symlink():dst.symlink_to(src.readlink())
   else:shutil.copyfile(src,dst)
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def reconcile(self,m):return inv.reconcile_current(m,self.previous,self.old)
 def test_actual_snapshot(self):
  out=inv.scan();self.assertEqual((out['file_count'],out['top_level_surface_count'],out['presence_only_count']),(274,313,51))
  self.assertEqual((out['added_count'],out['changed_count'],out['missing_count']),(31,4,0))
  self.assertFalse(out['new_dispatch']);self.assertFalse(out['qualification_allowed']);self.assertFalse(out['self_hash_closure'])
 def test_changed_blob(self):
  p=self.root/'app/local_integration/public_wln_server.py';old=p.read_bytes()
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
 def test_unknown_source_not_auto_registered(self):
  p=self.root/'app/local_integration/unreviewed_candidate.py'
  try:
   p.write_text('raise RuntimeError("must not import")')
   with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan(self.root)
  finally:p.unlink()
 def test_unknown_presence_only_test_not_auto_registered(self):
  p=self.root/'app/local_integration/test_unreviewed_presence.py'
  try:
   p.write_text('raise RuntimeError("must not import")')
   with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE
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
 def test_missing_presence_only_path(self):
  p=self.root/self.manifest['presence_only_paths'][0];old=p.read_bytes()
  try:
   p.unlink()
   with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_provenance_commit_tamper(self):
  m=copy.deepcopy(self.manifest);m['provenance'][0]['source_change_commit']='0'*40
  with self.assertRaisesRegex(ValueError,'^CURRENT_PROVENANCE_MISMATCH$'):self.reconcile(m)
 def test_provenance_task_tamper(self):
  m=copy.deepcopy(self.manifest);m['provenance'][0]['task']='INVENTED_APPROVAL'
  with self.assertRaisesRegex(ValueError,'^CURRENT_PROVENANCE_MISMATCH$'):self.reconcile(m)
 def test_rehashed_record_not_auto_approved(self):
  m=copy.deepcopy(self.manifest);r=m['provenance'][0];r['blob']='0'*40;m['files'][r['path']]['blob']=r['blob']
  with self.assertRaisesRegex(ValueError,'^CURRENT_PROVENANCE_MISMATCH$'):self.reconcile(m)
 def test_drop_delta(self):
  m=copy.deepcopy(self.manifest);m['delta']['added'].pop()
  with self.assertRaisesRegex(ValueError,'^CURRENT_DIFF_SET$'):self.reconcile(m)
 def test_no_dispatch_escalation(self):
  m=copy.deepcopy(self.manifest);m['new_dispatch']=True
  with self.assertRaisesRegex(ValueError,'^NO_NEW_AUTHORITY$'):self.reconcile(m)
 def test_self_scope_not_wildcard(self):
  m=copy.deepcopy(self.manifest);m['self_paths_unhashed'].append('tests/**')
  with self.assertRaisesRegex(ValueError,'^SELF_SCOPE_CHANGED$'):self.reconcile(m)
 def test_self_symlink_rejected(self):
  p=self.root/'tests/r4/test_current_entry_inventory_x05.py';old=p.read_bytes()
  try:
   p.unlink();p.symlink_to(self.root/inv.SPEC)
   with self.assertRaisesRegex(ValueError,'^SELF_PATH_REQUIRED$'):inv.scan(self.root)
  finally:p.unlink();p.write_bytes(old)
 def test_snapshot_ref_stale(self):
  m=copy.deepcopy(self.manifest);m['reviewed_ref']=inv.REVIEWED
  with self.assertRaisesRegex(ValueError,'^WRONG_CURRENT_SNAPSHOT_VERSION$'):self.reconcile(m)
 def test_snapshot_downgrade_and_bool_version(self):
  for field,value in [('schema','CURRENT_SOURCE_INVENTORY_X05_V1'),('version',True),('version',1)]:
   m=copy.deepcopy(self.manifest);m[field]=value
   with self.assertRaisesRegex(ValueError,'^WRONG_CURRENT_SNAPSHOT_VERSION$'):self.reconcile(m)
 def test_previous_manifest_bytes_pinned(self):
  p=self.root/inv.SPEC;old=p.read_bytes()
  try:
   p.write_bytes(old+b' ')
   with self.assertRaisesRegex(ValueError,'^PREVIOUS_MANIFEST_CHANGED$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_old_manifest_pinned(self):
  p=self.root/inv.OLD;old=p.read_bytes()
  try:
   p.write_bytes(old+b' ')
   with self.assertRaisesRegex(ValueError,'^OLD_MANIFEST_CHANGED$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_historical_reconciliation_still_exact(self):
  files,tops=inv.reconcile(self.previous,self.old);self.assertEqual(len(files),243);self.assertEqual(len(tops),280)
 def test_historical_x05_not_current_success(self):
  with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan_historical()
 def test_old_x03_failure_not_rewritten(self):
  import current_entry_inventory_x03 as historical
  with self.assertRaisesRegex(ValueError,'^INVENTORY_SOURCE_CHANGED$'):historical.scan()
 def test_changed_during_read(self):
  real=inv.read;target='app/local_integration/public_wln_server.py';calls=[0]
  def changing(root,path):
   data=real(root,path)
   if path==target:
    calls[0]+=1
    if calls[0]>1:return data+b' '
   return data
  with patch.object(inv,'read',side_effect=changing):
   with self.assertRaisesRegex(ValueError,'^SOURCE_CHANGED_DURING_READ$'):inv.scan(self.root)
class CurrentBoundaryHTTP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import threading
  import public_wln_server
  cls.server=public_wln_server
  cls.dispatch=patch.object(cls.server,'run_bound',side_effect=AssertionError('NO_DISPATCH')).start();cls.addClassCleanup(patch.stopall)
  cls.spawn=patch('subprocess.Popen',side_effect=AssertionError('NO_PROCESS')).start()
  cls.inventory=patch.object(inv,'scan',side_effect=AssertionError('SCANNER_MUST_NOT_GATE_HTTP_TEST')).start()
  cls.s=cls.server.server(0);cls.addClassCleanup(cls.s.server_close)
  cls.t=threading.Thread(target=cls.s.serve_forever,daemon=True);cls.t.start();cls.addClassCleanup(cls.s.shutdown)
 @classmethod
 def tearDownClass(cls):
  cls.dispatch.assert_not_called();cls.spawn.assert_not_called();cls.inventory.assert_not_called()
 def post(self,body):
  import http.client
  c=http.client.HTTPConnection('127.0.0.1',self.s.server_address[1],timeout=5)
  try:
   c.request('POST','/api/public/plan',body,{'Content-Type':'application/json'});r=c.getresponse();return r.status,json.loads(r.read())
  finally:c.close()
 def test_real_invalid_boundaries_no_dispatch(self):
  for axis in ('W','L'):
   for value in ('4.999','25.001'):
    raw={'W':'18','L':'20','n':2};raw[axis]=value
    status,out=self.post(json.dumps(raw).encode())
    self.assertEqual((status,out['code']),(422,'DIMENSION_OUT_OF_OWNER_RANGE'))
    for k in self.server.AUTH:self.assertIs(out[k],False)
 def test_real_invalid_units_and_hidden_field(self):
  for n in (3,4,'1.5',''):
   status,out=self.post(json.dumps({'W':'18','L':'20','n':n}).encode());self.assertEqual(status,422)
  status,out=self.post(b'{"W":"18","L":"20","n":2,"requested_count":6}')
  self.assertEqual((status,out['code']),(422,'UNEXPECTED_PUBLIC_FIELD'))
 def test_real_wire_decimal_separate(self):
  status,out=self.post(b'{"W":18.5,"L":"20","n":2}')
  self.assertEqual((status,out['code']),(409,'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION'))
 def test_real_valid_unsupported_not_invalid(self):
  status,out=self.post(b'{"W":"17","L":"20","n":1}')
  self.assertEqual(status,409);self.assertIs(out['input_valid'],True);self.assertEqual(out['actual_live_attempts'],0)
  for k in self.server.AUTH:self.assertIs(out[k],False)
if __name__=='__main__':unittest.main()
):inv.scan(self.root)
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
 def test_missing_presence_only_path(self):
  p=self.root/self.manifest['presence_only_paths'][0];old=p.read_bytes()
  try:
   p.unlink()
   with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_provenance_commit_tamper(self):
  m=copy.deepcopy(self.manifest);m['provenance'][0]['source_change_commit']='0'*40
  with self.assertRaisesRegex(ValueError,'^CURRENT_PROVENANCE_MISMATCH$'):self.reconcile(m)
 def test_provenance_task_tamper(self):
  m=copy.deepcopy(self.manifest);m['provenance'][0]['task']='INVENTED_APPROVAL'
  with self.assertRaisesRegex(ValueError,'^CURRENT_PROVENANCE_MISMATCH$'):self.reconcile(m)
 def test_rehashed_record_not_auto_approved(self):
  m=copy.deepcopy(self.manifest);r=m['provenance'][0];r['blob']='0'*40;m['files'][r['path']]['blob']=r['blob']
  with self.assertRaisesRegex(ValueError,'^CURRENT_PROVENANCE_MISMATCH$'):self.reconcile(m)
 def test_drop_delta(self):
  m=copy.deepcopy(self.manifest);m['delta']['added'].pop()
  with self.assertRaisesRegex(ValueError,'^CURRENT_DIFF_SET$'):self.reconcile(m)
 def test_no_dispatch_escalation(self):
  m=copy.deepcopy(self.manifest);m['new_dispatch']=True
  with self.assertRaisesRegex(ValueError,'^NO_NEW_AUTHORITY$'):self.reconcile(m)
 def test_self_scope_not_wildcard(self):
  m=copy.deepcopy(self.manifest);m['self_paths_unhashed'].append('tests/**')
  with self.assertRaisesRegex(ValueError,'^SELF_SCOPE_CHANGED$'):self.reconcile(m)
 def test_self_symlink_rejected(self):
  p=self.root/'tests/r4/test_current_entry_inventory_x05.py';old=p.read_bytes()
  try:
   p.unlink();p.symlink_to(self.root/inv.SPEC)
   with self.assertRaisesRegex(ValueError,'^SELF_PATH_REQUIRED$'):inv.scan(self.root)
  finally:p.unlink();p.write_bytes(old)
 def test_snapshot_ref_stale(self):
  m=copy.deepcopy(self.manifest);m['reviewed_ref']=inv.REVIEWED
  with self.assertRaisesRegex(ValueError,'^WRONG_CURRENT_SNAPSHOT_VERSION$'):self.reconcile(m)
 def test_snapshot_downgrade_and_bool_version(self):
  for field,value in [('schema','CURRENT_SOURCE_INVENTORY_X05_V1'),('version',True),('version',1)]:
   m=copy.deepcopy(self.manifest);m[field]=value
   with self.assertRaisesRegex(ValueError,'^WRONG_CURRENT_SNAPSHOT_VERSION$'):self.reconcile(m)
 def test_previous_manifest_bytes_pinned(self):
  p=self.root/inv.SPEC;old=p.read_bytes()
  try:
   p.write_bytes(old+b' ')
   with self.assertRaisesRegex(ValueError,'^PREVIOUS_MANIFEST_CHANGED$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_old_manifest_pinned(self):
  p=self.root/inv.OLD;old=p.read_bytes()
  try:
   p.write_bytes(old+b' ')
   with self.assertRaisesRegex(ValueError,'^OLD_MANIFEST_CHANGED$'):inv.scan(self.root)
  finally:p.write_bytes(old)
 def test_historical_reconciliation_still_exact(self):
  files,tops=inv.reconcile(self.previous,self.old);self.assertEqual(len(files),243);self.assertEqual(len(tops),280)
 def test_historical_x05_not_current_success(self):
  with self.assertRaisesRegex(ValueError,'^UNREVIEWED_SURFACE$'):inv.scan_historical()
 def test_old_x03_failure_not_rewritten(self):
  import current_entry_inventory_x03 as historical
  with self.assertRaisesRegex(ValueError,'^INVENTORY_SOURCE_CHANGED$'):historical.scan()
 def test_changed_during_read(self):
  real=inv.read;target='app/local_integration/public_wln_server.py';calls=[0]
  def changing(root,path):
   data=real(root,path)
   if path==target:
    calls[0]+=1
    if calls[0]>1:return data+b' '
   return data
  with patch.object(inv,'read',side_effect=changing):
   with self.assertRaisesRegex(ValueError,'^SOURCE_CHANGED_DURING_READ$'):inv.scan(self.root)
class CurrentBoundaryHTTP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import threading
  import public_wln_server
  cls.server=public_wln_server
  cls.dispatch=patch.object(cls.server,'run_bound',side_effect=AssertionError('NO_DISPATCH')).start();cls.addClassCleanup(patch.stopall)
  cls.spawn=patch('subprocess.Popen',side_effect=AssertionError('NO_PROCESS')).start()
  cls.inventory=patch.object(inv,'scan',side_effect=AssertionError('SCANNER_MUST_NOT_GATE_HTTP_TEST')).start()
  cls.s=cls.server.server(0);cls.addClassCleanup(cls.s.server_close)
  cls.t=threading.Thread(target=cls.s.serve_forever,daemon=True);cls.t.start();cls.addClassCleanup(cls.s.shutdown)
 @classmethod
 def tearDownClass(cls):
  cls.dispatch.assert_not_called();cls.spawn.assert_not_called();cls.inventory.assert_not_called()
 def post(self,body):
  import http.client
  c=http.client.HTTPConnection('127.0.0.1',self.s.server_address[1],timeout=5)
  try:
   c.request('POST','/api/public/plan',body,{'Content-Type':'application/json'});r=c.getresponse();return r.status,json.loads(r.read())
  finally:c.close()
 def test_real_invalid_boundaries_no_dispatch(self):
  for axis in ('W','L'):
   for value in ('4.999','25.001'):
    raw={'W':'18','L':'20','n':2};raw[axis]=value
    status,out=self.post(json.dumps(raw).encode())
    self.assertEqual((status,out['code']),(422,'DIMENSION_OUT_OF_OWNER_RANGE'))
    for k in self.server.AUTH:self.assertIs(out[k],False)
 def test_real_invalid_units_and_hidden_field(self):
  for n in (3,4,'1.5',''):
   status,out=self.post(json.dumps({'W':'18','L':'20','n':n}).encode());self.assertEqual(status,422)
  status,out=self.post(b'{"W":"18","L":"20","n":2,"requested_count":6}')
  self.assertEqual((status,out['code']),(422,'UNEXPECTED_PUBLIC_FIELD'))
 def test_real_wire_decimal_separate(self):
  status,out=self.post(b'{"W":18.5,"L":"20","n":2}')
  self.assertEqual((status,out['code']),(409,'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION'))
 def test_real_valid_unsupported_not_invalid(self):
  status,out=self.post(b'{"W":"17","L":"20","n":1}')
  self.assertEqual(status,409);self.assertIs(out['input_valid'],True);self.assertEqual(out['actual_live_attempts'],0)
  for k in self.server.AUTH:self.assertIs(out[k],False)
if __name__=='__main__':unittest.main()
