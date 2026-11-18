"""No generation: source completeness cannot be bypassed by naming or flags."""
import unittest
from q11_boundary118 import examine,PENDING
class Q11(unittest.TestCase):
 def test_producer_claim_does_not_prove(self):
  r=examine({'walls':{},'q11_functional_boundary_verified':True,'q11_proof':{'status':'PASS'}})
  self.assertIn(PENDING,r['pending']);self.assertFalse(r['evidence']['functional_boundary_proof_implemented'])
 def test_names_and_removal_are_not_certificate(self):
  for name in ['privacy_screen','useful_hall','closet_boundary']:
   self.assertIn(PENDING,examine({'walls':{name:[0,0,1,.1]}})['pending'])
  self.assertIn(PENDING,examine({'walls':{}})['pending'])
 def test_not_outscope(self):
  from scope117 import reduce_scope117
  r=reduce_scope117({'checker_version':'GENERAL117_INDEPENDENT_CONCEPT_V1','errors':[],'pending':[PENDING,'VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED']})
  self.assertIn(PENDING,r['pending']);self.assertNotIn(PENDING,r['not_evaluated']);self.assertFalse(r['eligible_for_draft_export'])
if __name__=='__main__':unittest.main()
