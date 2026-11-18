import unittest
from operationalization import compare
class Test(unittest.TestCase):
 def setUp(self):
  self.d={f'{u}/s/t/path':{'metric':'path_length_m','role':'objective','unit':u,'scenario':'s','source_pointer':'233/Q04'} for u in ['A','B']}
  self.a={k:{'value':'5','readset_digest':'synthetic-test-only','definition':v} for k,v in self.d.items()}
 def test_equal(self):self.assertFalse(compare(self.a,self.a,self.d)['strictly_dominates'])
 def test_improve(self):
  import copy
  b=copy.deepcopy(self.a);b['A/s/t/path']['value']='4';self.assertTrue(compare(self.a,b,self.d)['strictly_dominates'])
 def test_no_average(self):
  import copy
  b=copy.deepcopy(self.a);b['A/s/t/path']['value']='1';b['B/s/t/path']['value']='6';self.assertFalse(compare(self.a,b,self.d)['strictly_dominates'])
 def test_missing(self):self.assertEqual(compare({},self.a,self.d)['state'],'UNKNOWN')
 def test_null(self):
  import copy
  b=copy.deepcopy(self.a);b['A/s/t/path']['value']=None;self.assertEqual(compare(self.a,b,self.d)['state'],'UNKNOWN')
 def test_no_authority(self):self.assertFalse(compare(self.a,self.a,self.d)['rule_acceptance'])
if __name__=='__main__':unittest.main()

class PartialTests(unittest.TestCase):
 def test_known_worse_refutes_with_missing_protected(self):
  from operationalization import partial_dominance
  ds={'p':{'metric':'path_length_m','role':'objective','unit':'A','scenario':'entry_to_WC','source_pointer':'233/Q04'},'capacity':{'metric':'functional_capacity','role':'protected','unit':'B','scenario':'required_use','source_pointer':'233/IR-P13'}}
  a={'p':{'value':'4','definition':ds['p'],'readset_digest':'synthetic'}};b={'p':{'value':'5','definition':ds['p'],'readset_digest':'synthetic'}}
  o=partial_dominance(a,b,ds);self.assertEqual(o['dominance'],'FALSE');self.assertEqual(len(o['unknown_dimensions']),1);self.assertFalse(o['rule_acceptance'])
 def test_improvement_not_enough_when_missing(self):
  from operationalization import partial_dominance
  d={'metric':'path_length_m','role':'objective','unit':'A','scenario':'s','source_pointer':'233/Q04'}
  a={'x':{'value':'5','definition':d,'readset_digest':'synthetic'}};b={'x':{'value':'4','definition':d,'readset_digest':'synthetic'}}
  self.assertEqual(partial_dominance(a,b,{'x':d,'missing':d})['dominance'],'UNKNOWN')
 def test_unknown_is_not_failure(self):
  from operationalization import partial_dominance
  self.assertEqual(partial_dominance({}, {}, {})['dominance'],'UNKNOWN')
