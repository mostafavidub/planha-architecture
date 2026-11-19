import copy,unittest
from explicit_pair_redirection import require_rejection,PENDING
def report():
 return {'status':'FAIL','errors':[{'code':'MISSING_REQUIRED_ACTIVITY_ROUTES','failures':[{'unit':u,'route':'guest_dining','reason':'NO_CONNECTED_BODY_ROUTE','profile':'public_all_seat_motion_occupied_and_kitchen_exclusion'} for u in ('A','B')]}],'pending':sorted(PENDING)}
class Rejection(unittest.TestCase):
 def test_exact_scope(self):require_rejection(report())
 def test_pass_not_repair_trigger(self):
  r=report();r['status']='PASS_CONCEPT_SCOPED_REVIEW'
  with self.assertRaises(ValueError):require_rejection(r)
 def test_other_error(self):
  r=report();r['errors'][0]['code']='OTHER'
  with self.assertRaises(ValueError):require_rejection(r)
 def test_error_not_filtered(self):
  r=report();r['errors'].append({'code':'OTHER'})
  with self.assertRaises(ValueError):require_rejection(r)
 def test_work_only_profile_not_same_rejection(self):
  r=report();r['errors'][0]['failures'][0]['profile']='actual_work_only'
  with self.assertRaises(ValueError):require_rejection(r)
 def test_other_pending(self):
  r=report();r['pending'].append('UNKNOWN_NEW_RULE')
  with self.assertRaises(ValueError):require_rejection(r)
 def test_other_unit(self):
  r=report();r['errors'][0]['failures'][1]['unit']='C'
  with self.assertRaises(ValueError):require_rejection(r)
 def test_typed_pending(self):
  r=report();r['pending']=[False]
  with self.assertRaises(ValueError):require_rejection(r)
if __name__=='__main__':unittest.main()
