import copy,json,unittest
from threshold_check118 import examine
from named_checks118 import partition_ledger
class ThresholdTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.load(open('evidence/finish_threshold118_saved_geometry.json'))['model']
 def test_positive(self):self.assertEqual(examine(self.m)['errors'],[]);self.assertEqual(partition_ledger(self.m)['status'],'PASS_LIMITED')
 def test_mutations(self):
  changes=[lambda m:m['threshold_ownership']['allocations'][0].update(owner='unit:B'),lambda m:m['threshold_ownership']['allocations'][0]['rect'].__setitem__(2,'6.5'),lambda m:m['threshold_ownership']['allocations'][0]['reference_axis'].update(coordinate='10.54'),lambda m:m['threshold_ownership']['allocations'].pop(),lambda m:m['walls'].update(fake_solid=m['openings'][0]['rect']),lambda m:m['threshold_ownership']['allocations'][0].update(host_wall_id='core.lift.left')]
  for i,f in enumerate(changes):
   m=copy.deepcopy(self.m)
   if i==4:m['walls']['fake_solid']=next(o['rect']for o in m['openings']if o['id']=='A.entry')
   else:f(m)
   self.assertTrue(examine(m)['errors'],i)
 def test_ledger_owner_swap(self):
  m=copy.deepcopy(self.m);g=m['spatial_accounting']['plot_partition'];a=next(v for v in g if v['role'].startswith('threshold_A.entry_minus'));b=next(v for v in g if v['role'].startswith('threshold_A.entry_plus'));a['regions'],b['regions']=b['regions'],a['regions'];self.assertEqual(partition_ledger(m)['status'],'FAIL')
if __name__=='__main__':unittest.main()
