"""Pure source-binding helpers; synthetic fixtures do not prove real programme adequacy."""
import unittest,copy
from current_programme_evaluator import placed,rect,inventory,proven_capacity_violation
from program_profile_registry import lookup
class ProgrammeHelpers(unittest.TestCase):
 def test_shortfall_not_malformed(self):
  for code,expected in [('ACTUAL_CAPACITY_SHORTFALL',True),('CAPACITY_AUDIT_MALFORMED',False),('LIVING_ACCESS_COLLISION',False)]:
   self.assertIs(proven_capacity_violation({'errors':[{'code':code}],'evidence':{'units':[]}}),expected)
 def test_actual_sleep_below_approved(self):
  self.assertTrue(proven_capacity_violation({'errors':[],'evidence':{'units':[{'actual_places':{'sleeping_places':2}}]}}))
 def test_missing_evidence_not_vacuous_pass(self):
  self.assertFalse(proven_capacity_violation({'errors':[],'evidence':{'units':[]}}))
  # False means no proven violation; overall criterion remains UNKNOWN, never PASS.
 def test_identity(self):self.assertEqual(placed(['0','1','2','3'],{'matrix':[[1,0],[0,1]],'translation':['4','5']}),rect(['4','6','6','8']))
 def test_reflection(self):self.assertEqual(placed(['0','1','2','3'],{'matrix':[[-1,0],[0,-1]],'translation':['4','5']}),rect(['2','2','4','4']))
 def test_rotation(self):self.assertEqual(placed(['0','1','2','3'],{'matrix':[[0,-1],[1,0]],'translation':['4','5']}),rect(['1','5','3','7']))
 def test_bad_isometry(self):
  for m in ([[2,0],[0,1]],[[1,1],[0,1]],[[True,0],[0,1]],[[1.0,0],[0,1]]):
   with self.assertRaises(ValueError):placed(['0','0','1','1'],{'matrix':m,'translation':['0','0']})
 def test_rect_invalid(self):
  for q in ([1,2,0,3],[0,0,0,1],[0,0,1],[0,0,'nan',1]):
   with self.assertRaises((ValueError,TypeError)):rect(q)
 def test_typed_programme(self):
  base={'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin'],'design_occupants_per_unit':4,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True}
  for k,v in [('units',2.0),('provisional',1),('design_occupants_per_unit',False),('bedrooms_per_unit',1)]:
   p=copy.deepcopy(base);p[k]=v
   with self.assertRaisesRegex(ValueError,'PROGRAM_IDENTITY'):inventory({'program':p},lookup('PROGRAM_2BED_V1'),{})
 def test_registry_no_fallback(self):
  base={'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin'],'design_occupants_per_unit':4,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True}
  with self.assertRaisesRegex(ValueError,'REGISTRY_APPROVAL'):inventory({'program':base},lookup('PROGRAM_1BED_V1'),{})
if __name__=='__main__':unittest.main()
