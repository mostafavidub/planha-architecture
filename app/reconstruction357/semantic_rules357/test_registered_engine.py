import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
import engine
class Registered(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  p=Path(__file__).resolve().parents[1];cls.a=json.loads((p/'staging357_comparative/attached_service_final357.json').read_text());cls.b=json.loads((p/'review357_source_identity/result.json').read_text());cls.m=cls.a['candidate']['model'];cls.r=cls.b['raw_report']
 def runreg(self,a=None):return engine.evaluate(self.m,self.r,source_profile='SOURCE_IDENTITY357',registered_artifact={'record':self.a if a is None else a,'result':self.b})
 def test_registered_opening_only_scoped(self):
  x=self.runreg();q={v['rule_id']:v for v in x['quality']};self.assertEqual(q['OPENINGS_REAL']['verdict'],'PASS');self.assertFalse(x['delivery_allowed']);self.assertFalse(x['fresh_executed']);self.assertTrue(x['registered_artifact_verified']);self.assertTrue(all(v['verdict']=='UNKNOWN'for k,v in q.items()if k!='OPENINGS_REAL'))
 def test_raw_alone_is_not_registered_authority(self):
  x=engine.evaluate(self.m,self.r,source_profile='SOURCE_IDENTITY357');self.assertFalse(x['registered_artifact_verified']);self.assertTrue(all(v['verdict']=='UNKNOWN'for v in x['quality']))
 def test_record_tamper_blocks_every_parent(self):
  a=copy.deepcopy(self.a);a['accepted']=True;x=self.runreg(a);self.assertTrue(all(v['verdict']=='UNKNOWN'for v in x['quality']));self.assertFalse(x['registered_artifact_verified'])
 def test_author_html_tamper_blocks(self):
  original=Path.read_bytes
  def altered(p):return b'fake'if p.name=='owner_four_steps233.html'else original(p)
  with patch.object(Path,'read_bytes',altered):x=self.runreg()
  self.assertTrue(all(v['verdict']=='UNKNOWN'for v in x['quality']))
if __name__=='__main__':unittest.main()
