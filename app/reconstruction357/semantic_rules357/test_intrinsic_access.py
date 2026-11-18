import unittest,json,copy
from pathlib import Path
from intrinsic_access import evaluate,pathcheck,private_parts,rect,F
BASE=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  x=json.loads((BASE/'actual_run/actual_response.json').read_text());cls.m=x['selected'][0]['model'];cls.raw=x['central_fresh_reviews'][0]['central_fresh_review']['raw_fresh_report']
 def test_baseline(self):
  r=evaluate(self.m,self.raw);self.assertEqual(r['verdict'],'PASS_SCOPED_INTRINSIC_ACCESS');self.assertFalse(r['parent_complete']);self.assertEqual(sum(len(v['H07']['routes'])for v in r['minima'].values()),6)
 def test_new_profile(self):
  c=json.loads((BASE/'staging357_comparative/attached_service_final357.json').read_text());r=json.loads((BASE/'review357_source_identity/result.json').read_text());out=evaluate(c['candidate']['model'],r['raw_report'],'SOURCE_IDENTITY357');self.assertEqual(out['verdict'],'PASS_SCOPED_INTRINSIC_ACCESS');self.assertEqual(sum(len(v['H05_H15_Q10_ARRIVAL']['routes'])for v in out['minima'].values()),4)
 def test_wrong_registry(self):
  c=json.loads((BASE/'staging357_comparative/attached_service_final357.json').read_text());r=json.loads((BASE/'review357_source_identity/result.json').read_text());self.assertEqual(evaluate(c['candidate']['model'],r['raw_report'])['verdict'],'UNKNOWN')
 def test_stale_panel_mutation(self):
  m=copy.deepcopy(self.m);m['operations']['doors'][0]['open_panel']=['0','0','1','1'];self.assertEqual(evaluate(m,self.raw)['verdict'],'UNKNOWN')
 def test_open_panel_blocks_sweep(self):
  r=pathcheck([['1','1'],['3','1']],F('.7'),[rect(['0','0','4','4'])],[('open_panel',rect(['2','.5','2.1','1.5']))]);self.assertEqual(r['verdict'],'UNKNOWN_STORED_PATH_BLOCKED');self.assertTrue(r['collisions'])
 def test_floor_gap(self):
  r=pathcheck([['1','1'],['3','1']],F('.7'),[rect(['0','0','1.5','4']),rect(['2','0','4','4'])],[]);self.assertTrue(r['uncovered_segments'])
 def test_complete_private_deletion_includes_vestibule(self):
  m=copy.deepcopy(self.m);u=m['units'][0];u['rooms']['private_vestibule']=[['1','1','2','2']];self.assertIn(rect(['1','1','2','2']),private_parts(m,u));self.assertTrue(all(rect(p)in private_parts(m,u)for d in m['private_domains']if d['unit']==u['id']for p in d['parts']))
if __name__=='__main__':unittest.main()
