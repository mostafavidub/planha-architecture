import unittest,copy
from private_domain121 import examine
class Scope(unittest.TestCase):
 def model(self):
  return {'inputs':['10','10',1],'profile':{'body_m':'.7'},'walls':{},'wall_hosts':{},'openings':[],'module_ports':[],'units':[{'id':'A','ownership':[['0','0','10','10']],'rooms':{'bed1':[['0','0','1','1']],'bed2':[['1','0','2','1']],'bed3':[['2','0','3','1']],'living':[['0','1','10','10']]},'fixtures':{},'routes':{},'scenario_routes':{}}]}
 def test_no_domain_not_owner_failure(self):
  r=examine(self.model());self.assertEqual(r['errors'],[]);self.assertTrue(any('UNSUPPORTED_DOMAIN_VERIFICATION'in x for x in r['pending']))
 def test_multiple_domains_not_impossible(self):
  m=self.model();m['private_domains']=[{'unit':'A'},{'unit':'A'}];r=examine(m);self.assertEqual(r['errors'],[]);self.assertTrue(r['pending'])
 def test_real_collision_remains_error(self):
  m=self.model();m['units'][0]['fixtures']['table']=['4','4','5','5'];m['private_domains']=[{'unit':'A','bedrooms':['A.bed1','A.bed2','A.bed3'],'parts':[['4','4','6','6']],'public_interface':{'rect':['4','5.65','6','6.35'],'open_side':'top'},'paths':{}}];r=examine(m);self.assertIn('A:DOMAIN_NOT_ACTUAL_FREE_FLOOR',r['errors'])
if __name__=='__main__':unittest.main()
