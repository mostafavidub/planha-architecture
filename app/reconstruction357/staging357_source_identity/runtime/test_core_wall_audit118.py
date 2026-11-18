import json,unittest,copy
from pathlib import Path
from core_wall_audit118 import ADAPTERS
P=Path(__file__).parent
class Audit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.models=[json.loads((P/f'evidence/q11_whole118_case{i}.json').read_text())['model']for i in(1,2)]
 def test_actual_core_and_hosts(self):
  for m in self.models:
   for name in('core_concept','opening_hosts'):self.assertEqual(ADAPTERS[name](m)['status'],'PASS_LIMITED')
 def test_network_existing_failure_kept(self):
  for m in self.models:
   r=ADAPTERS['wall_network'](m);self.assertEqual(r['status'],'FAIL');self.assertIn('DISCONNECTED_PARTITION_HOST_NETWORK',r['witness']['errors']);self.assertIn('MISSING_PER_HOST_FINISHED_FACE_PROFILE',r['witness']['pending'])
 def test_block_common_route(self):
  m=copy.deepcopy(self.models[0]);m['walls']['malicious_block']=['5.4','6','6.2','7'];self.assertEqual(ADAPTERS['core_concept'](m)['status'],'FAIL')
 def test_missing_lift(self):
  m=copy.deepcopy(self.models[0]);del m['common_spaces']['lift'];self.assertEqual(ADAPTERS['core_concept'](m)['status'],'FAIL')
 def test_lobby_overlaps_stair(self):
  m=copy.deepcopy(self.models[0]);m['common_spaces']['lobby'].append(m['common_spaces']['stair']);self.assertEqual(ADAPTERS['core_concept'](m)['status'],'FAIL')
 def test_false_connects(self):
  m=copy.deepcopy(self.models[0]);m['openings'][0]['connects']=['lobby','A.bed1'];self.assertEqual(ADAPTERS['opening_hosts'](m)['status'],'FAIL')
 def test_missing_host_is_unknown(self):
  m=copy.deepcopy(self.models[0]);m['openings'][0]['host_wall_id']='missing';self.assertEqual(ADAPTERS['opening_hosts'](m)['status'],'NOT_EVALUATED')
 def test_block_opening(self):
  m=copy.deepcopy(self.models[0]);m['walls']['block']=m['openings'][0]['rect'];self.assertEqual(ADAPTERS['opening_hosts'](m)['status'],'FAIL')
 def test_duplicate_wall(self):
  m=copy.deepcopy(self.models[0]);m['walls']['duplicate']=m['walls']['front'];self.assertTrue(any('DUPLICATE_SOLID'in x for x in ADAPTERS['wall_network'](m)['witness']['errors']))
 def test_window_missing_host(self):
  m=copy.deepcopy(self.models[0]);m['concept_windows'][0]['host_wall_id']='missing';self.assertEqual(ADAPTERS['opening_hosts'](m)['status'],'NOT_EVALUATED')
 def test_window_wrong_room(self):
  m=copy.deepcopy(self.models[0]);m['concept_windows'][0]['room']='B.bed1';self.assertEqual(ADAPTERS['opening_hosts'](m)['status'],'FAIL')
 def test_zero_wall(self):
  m=copy.deepcopy(self.models[0]);m['walls']['front'][2]=m['walls']['front'][0];self.assertEqual(ADAPTERS['wall_network'](m)['status'],'FAIL')
 def test_fake_finish_no_pass(self):
  m=copy.deepcopy(self.models[0]);m['wall_finish_profile']={k:{'finished':True}for k in m['wall_hosts']};r=ADAPTERS['wall_network'](m);self.assertTrue(any('FINISH_PROFILE_SCHEMA_OR_DATA' in x for x in r['witness']['pending']))
if __name__=='__main__':unittest.main()
