import unittest
from gate_cache118 import GateCache,digest
class C(unittest.TestCase):
 def setUp(self):self.c=GateCache(2);self.model={'x':1};self.context={'mode':'fresh'};self.calls=0
 def ev(self,m,c):self.calls+=1;return {'model_hash':digest(m),'status':'TEST_ONLY_NO_GEOMETRY'}
 def test_once_then_hash_bound(self):
  a=self.c.evaluate(self.model,self.context,'v1',self.ev);b=self.c.evaluate(self.model,self.context,'v1',self.ev);self.assertEqual(a,b);self.assertEqual(self.calls,1)
  self.c.evaluate({'x':2},self.context,'v1',self.ev);self.c.evaluate(self.model,{'mode':'changed'},'v1',self.ev);self.c.evaluate(self.model,self.context,'v2',self.ev);self.assertEqual(self.calls,4)
 def test_no_receipt_injection_or_mutation(self):
  r=self.c.evaluate(self.model,self.context,'v1',self.ev);r['status']='FAKE';self.assertNotEqual(self.c.evaluate(self.model,self.context,'v1',self.ev)['status'],'FAKE')
 def test_force_independent_review(self):
  self.c.evaluate(self.model,self.context,'v1',self.ev);self.c.evaluate(self.model,self.context,'v1',self.ev,force=True);self.assertEqual(self.calls,2)
 def test_bad_evaluator_never_cached(self):
  with self.assertRaises(ValueError):self.c.evaluate(self.model,self.context,'v1',lambda m,c:{'model_hash':'wrong'})
  self.assertFalse(self.c._entries)
 def test_bounded_and_cleared(self):
  for i in range(4):self.c.evaluate({'x':i},self.context,'v1',self.ev)
  self.assertEqual(len(self.c._entries),2);self.c.clear();self.assertFalse(self.c._entries)
if __name__=='__main__':unittest.main()
