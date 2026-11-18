import unittest
from unittest.mock import patch
import engine129 as e
class Scheduling(unittest.TestCase):
 def test_both_families_before_explicit_fallback(self):
  raw={'W':'30.95','L':'21.37','n':2,'requested_count':6};calls=[]
  def frame(raw,family):calls.append(family);return {},(1,1)
  empty={'attempts':[],'internal_proposals':[],'candidates':[],'search_seconds':0,'assembly_seconds':0,'validation_seconds':0,'full_gate_calls':0}
  with patch.object(e,'frame',frame),patch.object(e,'propose',return_value={'status':'UNSUPPORTED_BUNDLE_FIT'}),patch('engine127.run',return_value=empty)as lower:
   result=e.runtime(raw)
  self.assertEqual(calls,['FRONT_REAR','LEFT_RIGHT']);self.assertEqual(lower.call_count,1)
  self.assertEqual(result['shortfall'],6);self.assertEqual(len(result['fallback_reason']),2)
 def test_invalid_input_does_not_search(self):
  with patch.object(e,'propose')as p:
   with self.assertRaises(ValueError):e.runtime({'W':'30.95','L':'21.37','n':2,'requested_count':6,'program':3})
   p.assert_not_called()
if __name__=='__main__':unittest.main()
