"""Synthetic references only; no path admissibility or generated plan."""
import copy,hashlib,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2];ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path.insert(0,str(ROOT/'app/local_integration'))
from source_wall_record_contract_study import ROOT_KEYS
from source_activity_target_reference_study import assess,digest
def fixture():
 m=dict.fromkeys(ROOT_KEYS);m.update(schema='GENERAL125_WORLD_FRAME_STUDY',inputs=['20','25',2],accepted=False,release_allowed=False,ordered_macro=None,program={'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin']},route_failures=[],units=[])
 for uid in ('A','B'):
  m['units'].append({'id':uid,'activities':{'use':['1','1','3','3'],'kitchen_work':['4','4','6','6']},'route_targets':{'use':['2','2'],'kitchen_work':['5','5']},'routes':{'use':[['0','0'],['2','2']]}})
 return m
class Targets(unittest.TestCase):
 def good(self,m):return assess(m,digest(m))
 def bad(self,m):self.assertEqual(self.good(m)['state'],'INVALID_TARGET_REFERENCE')
 def test_pinned_target_sources(self):
  for name,pin in [('assemble114.py','6e19b12c62820e015055765e0fe56d6339cd4312'),('public_witness118.py','36f49057da712f29953bbc940a0dd8e9285ee64b'),('world_transform125.py','b7e02236a057316998ae3c7d14cb0ddf94bd4879')]:
   b=(ENGINE/name).read_bytes();self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin)
 def test_references_missing_route_not_architecture_fail(self):
  m=fixture();m['route_failures']=[{'unit':'A','route':'kitchen_work','reason':'synthetic no witness'}]
  o=self.good(m);self.assertEqual(o['state'],'ACTIVITY_TARGET_REFERENCES_BOUND_ONLY')
  states={r['evidence_state']for r in o['bindings']}
  self.assertIn('MISSING_PATH_WITH_MATCHED_LEDGER_RECORD',states);self.assertIn('MISSING_PATH_WITHOUT_FAILURE_RECORD',states)
  self.assertIs(o['route_geometry_verified'],False);self.assertIs(o['accepted'],False)
 def test_missing_extra_and_wrong_target_center(self):
  for mode in range(3):
   m=fixture();t=m['units'][0]['route_targets']
   if mode==0:del t['use']
   elif mode==1:t['unknown']=['2','2']
   else:t['use']=['3','2']
   self.bad(m)
 def test_endpoint_and_numeric_types(self):
  for value in (['3','2'],[2,'2'],[False,'2'],('2','2')):
   m=fixture();m['units'][0]['routes']['use'][-1]=value;self.bad(m)
 def test_dangling_route_and_empty_path(self):
  for mode in range(2):
   m=fixture();m['units'][0]['routes']['unknown'if mode==0 else'use']=[];self.bad(m)
 def test_kitchen_alias_source_rule(self):
  m=fixture();u=m['units'][0];u['routes']['kitchen_work']=[['5','5']];u['routes']['kitchen']=copy.deepcopy(u['routes']['kitchen_work'])
  self.assertEqual(self.good(m)['state'],'ACTIVITY_TARGET_REFERENCES_BOUND_ONLY')
  u['routes']['kitchen'][0]=['4','5'];self.bad(m)
 def test_failure_records_retained_not_cleared_by_path(self):
  m=fixture();m['route_failures']=[{'unit':'A','route':'use','reason':'earlier failure'}]
  before=digest(m);o=self.good(m);self.assertEqual(o['original_failure_ledger_digest'],digest(m['route_failures']));self.assertEqual(before,digest(m));self.assertEqual(o['bindings'][0]['matched_failure_count'],1);self.assertEqual(o['bindings'][0]['matched_reason_text_present'],[True])
 def test_matched_record_without_reason_is_not_reason_evidence(self):
  m=fixture();m['route_failures']=[{'unit':'A','route':'kitchen_work'}]
  o=self.good(m);r=next(r for r in o['bindings']if r['unit']=='A'and r['activity_id']=='kitchen_work')
  self.assertEqual(r['matched_reason_text_present'],[False]);self.assertEqual(r['evidence_state'],'MISSING_PATH_WITH_MATCHED_LEDGER_RECORD')
 def test_hash_binding(self):
  m=fixture();self.assertEqual(assess(m,'f'*64)['state'],'INVALID_TARGET_REFERENCE')
if __name__=='__main__':unittest.main()
