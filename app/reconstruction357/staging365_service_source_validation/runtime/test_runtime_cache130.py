import unittest
from unittest.mock import patch
from copy import deepcopy
import engine130 as e
from contract114 import digest
class CacheBinding(unittest.TestCase):
 def test_computed_reports_and_invalidation(self):
  e._CACHE.clear();calls=[];p={'world_model':{'value':1},'local_model':{'value':1}};c={'construction_trace':{'schema':'CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1'}}
  def evaluate(p,c):calls.append(1);return {'model_hash':digest(p['world_model']),'errors':[],'computed':len(calls)}
  with patch('evaluate_hierarchical129.evaluate',evaluate),patch.object(e,'revision',return_value='rev1'):
   a=e.evaluate_current(p,c);a['errors'].append('caller forged');self.assertEqual(e.evaluate_current(p,c)['errors'],[]);self.assertEqual(len(calls),1)
   e.evaluate_current(p,c,force=True);self.assertEqual(len(calls),2)
   q=deepcopy(p);q['local_model']['value']=2;e.evaluate_current(q,c);self.assertEqual(len(calls),3)
   q=deepcopy(p);q['world_model']['value']=2;e.evaluate_current(q,c);self.assertEqual(len(calls),4)
   q=deepcopy(c);q['caller_receipt']={'status':'PASS'};e.evaluate_current(p,q);self.assertEqual(len(calls),5)
  with patch('evaluate_hierarchical129.evaluate',evaluate),patch.object(e,'revision',return_value='rev2'):
   e.evaluate_current(p,c);self.assertEqual(len(calls),6)
 def test_false_report_rejected(self):
  e._CACHE.clear();p={'world_model':{'v':1}};c={'construction_trace':{'schema':'CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1'}}
  with patch('evaluate_hierarchical129.evaluate',return_value={'model_hash':'forged','status':'PASS'}):
   with self.assertRaisesRegex(ValueError,'REPORT_MODEL_BINDING'):e.evaluate_current(p,c)
if __name__=='__main__':unittest.main()
