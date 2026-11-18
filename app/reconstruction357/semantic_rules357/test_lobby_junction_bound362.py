import unittest,copy
import lobby_junction_bound362 as b
from common import digest
class Tests(unittest.TestCase):
 def fixture(self):
  m={'common_spaces':{'lobby':[['0','0','4','3']]},'profile':{'body_m':'.7'},'openings':[{'id':i,'rect':r,'connects':['lobby',i]}for i,r in [('L',['-.1','1','0','2']),('R',['4','1','4.1','2']),('B',['1','-.1','2','0']),('T',['1','3','2','3.1'])]]}
  return {'candidate':{'model':m,'model_digest':digest(m),'packet':{'core':{'lobby':m['common_spaces']['lobby']}}}}
 def test_bound(self):
  x=b.analyze(self.fixture());self.assertEqual(x['area_m2'],'12');self.assertFalse(x['parent_complete']);self.assertTrue(x['missing'])
 def test_missing_face(self):
  r=self.fixture();r['candidate']['model']['openings'].pop();r['candidate']['model_digest']=digest(r['candidate']['model']);self.assertEqual(b.analyze(r)['verdict'],'UNKNOWN')
 def test_duplicate(self):
  r=self.fixture();r['candidate']['model']['openings'].append(copy.deepcopy(r['candidate']['model']['openings'][0]));r['candidate']['model_digest']=digest(r['candidate']['model']);self.assertEqual(b.analyze(r)['verdict'],'UNKNOWN')
 def test_stale(self):
  r=self.fixture();r['candidate']['model']['profile']['body_m']='1';self.assertEqual(b.analyze(r)['verdict'],'UNKNOWN')
 def test_too_narrow(self):
  r=self.fixture();r['candidate']['model']['profile']['body_m']='1.1';r['candidate']['model_digest']=digest(r['candidate']['model']);self.assertEqual(b.analyze(r)['verdict'],'UNKNOWN')
if __name__=='__main__':unittest.main()
