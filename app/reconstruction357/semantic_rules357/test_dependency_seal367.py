import unittest,copy
from common import digest
from role_dependency_seal367 import seal,verify,order
from role_registry_balanced365_expanded367_v2 import DAG
class Tests(unittest.TestCase):
 def fixture(self):
  n={k:{'status':'PASS_TEST_ONLY','evidence':{'fixture':'TEST_ONLY'}}for k in DAG}
  n['WALL_PURPOSE']['evidence']={'closed_hall_dependency_rows':[{'source_row_digest':'test'}]}
  n['Q12_PER_UNIT']['evidence']=[{'exact_pending':[]}];n['Q12_PER_UNIT']['balanced_common_access']={'test_only':True}
  n['Q14_SELECTION_SET']['status']='UNKNOWN_SELECTION_SET_NOT_SUPPLIED';return n
 def test_positive_full_dag(self):
  n=seal(self.fixture(),DAG);self.assertTrue(verify(n,DAG));self.assertEqual(n,seal(n,DAG))
  self.assertEqual(n['Q11_WHOLE_ROLE']['evidence']['dependency_digests'],{k:digest(n[k])for k in DAG['Q11_WHOLE_ROLE']})
  self.assertEqual(n['Q05_PRIVACY']['evidence']['whole_role_digest'],digest(n['Q11_WHOLE_ROLE']))
  self.assertEqual(n['Q12_PER_UNIT']['evidence'][0]['resolved_dependency_digests']['Q04_COMPARISON'],digest(n['Q04_COMPARISON']))
 def changed(self,fn):
  n=seal(self.fixture(),DAG);fn(n)
  with self.assertRaises(ValueError):verify(n,DAG)
 def test_depends_on(self):self.changed(lambda n:n['COMMON_ROLE']['depends_on'].append('Q14_SELECTION_SET'))
 def test_blocking(self):self.changed(lambda n:n['COMMON_ROLE']['blocking_dependencies'].append('SOURCE_GATE'))
 def test_childproof(self):self.changed(lambda n:n['COMMON_ROLE']['evidence'].update(forged=True))
 def test_nested_q05(self):self.changed(lambda n:n['Q05_PRIVACY']['evidence'].update(wall_role_digest='stale'))
 def test_nested_q12(self):self.changed(lambda n:n['Q12_PER_UNIT']['evidence'][0]['resolved_dependency_digests'].update(Q04_COMPARISON='stale'))
 def test_node_status(self):self.changed(lambda n:n['COMMON_ROLE'].update(status='UNKNOWN'))
 def test_cycle(self):
  d=copy.deepcopy(DAG);d['SOURCE_GATE']=['Q11_WHOLE_ROLE']
  with self.assertRaises(ValueError):order(d)
if __name__=='__main__':unittest.main()
