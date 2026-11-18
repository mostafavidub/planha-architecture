import unittest,copy,json,sys,types
from pathlib import Path
from applicability import rliv_applicability,digest
from modules_structure import inspect,rectangle,evaluate
P=Path(__file__).resolve().parents[1]/'actual_run/actual_response.json'
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.model=json.loads(P.read_text())['selected'][0]['model']
 def test_real_saved_source_binding(self):
  x=json.loads(P.read_text());report=x["central_fresh_reviews"][0]["central_fresh_review"]["raw_fresh_report"]
  from common import rows
  self.assertEqual(len(rows(self.model,report)),38)
  result=evaluate(self.model,report)
  self.assertTrue(all(v["verdict"]=="UNKNOWN" and v["evidence"].get("model_digest")==digest(self.model) for v in result.values()))
 def test_actual_inventory(self):
  x=inspect(self.model);self.assertEqual(len(x['units']),2);self.assertEqual(len(x['opening_ids']),18)
 def test_actual_rliv_not_applicable(self):self.assertEqual(rliv_applicability(self.model)['state'],'NOT_APPLICABLE')
 def test_trigger_missing_brief(self):
  m=copy.deepcopy(self.model);m['inputs'][:2]=['12.5','20'];self.assertEqual(rliv_applicability(m)['state'],'UNKNOWN')
 def test_bound_brief(self):
  m=copy.deepcopy(self.model);m['inputs'][:2]=['20','12.5'];b={'model_hash':digest(m),'source_ref':'PRD111','requested_count':6};self.assertEqual(rliv_applicability(m,b)['state'],'APPLIES');b['requested_count']=True;self.assertEqual(rliv_applicability(m,b)['state'],'UNKNOWN')
 def test_bad_inputs(self):
  for value in (True,None,12.5):
   m=copy.deepcopy(self.model);m['inputs'][0]=value;self.assertEqual(rliv_applicability(m)['state'],'UNKNOWN')
 def test_duplicate_opening(self):
  m=copy.deepcopy(self.model);m['openings'].append(copy.deepcopy(m['openings'][0]));self.assertRaises(ValueError,inspect,m)
 def test_program_null(self):
  m=copy.deepcopy(self.model);m['program']['sleep_roles'][0]=None;self.assertRaises(ValueError,inspect,m)
 def test_count_bool(self):
  m=copy.deepcopy(self.model);m['program']['units']=True;self.assertRaises(ValueError,inspect,m)
 def test_rect_negative(self):
  for r in ([0,0,0,1],[0,0,True,1],[0,0,1.0,1]):self.assertRaises(ValueError,rectangle,r)
 def test_semantic_no_inherited_pass(self):
  # Test seam only, not a real report or source-binding proof.
  old=sys.modules.get('common');stub=types.ModuleType('common');stub.rows=lambda m,r:{};sys.modules['common']=stub
  try:
   result=evaluate(self.model,{})
   self.assertTrue(all(v['verdict']=='UNKNOWN' for v in result.values()))
   self.assertTrue(any('IR_P13' in x for x in result['BEDROOM_GROUPING']['missing']))
  finally:
   if old is None:del sys.modules['common']
   else:sys.modules['common']=old
if __name__=='__main__':unittest.main()
