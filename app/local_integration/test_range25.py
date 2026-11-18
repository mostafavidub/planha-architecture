import unittest,json
from unittest.mock import patch
from dimension_contract import parse,InputError
import generation_gateway as generation
import repair_saved_run as repair
from run_history import summary
class Range25(unittest.TestCase):
 def body(self,axis,value):
  r={'W':'25','L':'25','n':2,'requested_count':1};r[axis]=value;return json.dumps(r,ensure_ascii=False).encode()
 def test_each_inclusive_boundary_and_persian(self):
  for axis in ('W','L'):
   for value in ('5','25','۵','۲۵','۲۵٫۰۰۰۰'):
    with self.subTest(axis=axis,value=value):parse(self.body(axis,value))
 def test_every_outside_rejected_before_dispatch(self):
  with patch.object(generation.subprocess,'Popen')as worker:
   for axis in ('W','L'):
    for value in ('25.0001','۲۵٫۰۰۰۱','45','۴۵','4.9999'):
     with self.subTest(axis=axis,value=value):
      status,r=generation.generate(self.body(axis,value));self.assertEqual(status,422);self.assertEqual(r['code'],'DIMENSION_OUT_OF_OWNER_RANGE');self.assertEqual(r['field'],axis);self.assertNotIn('run_id',r)
   worker.assert_not_called()
 def test_direct_repair_also_rejects_before_worker(self):
  with patch.object(repair.subprocess,'Popen')as worker:
   self.assertEqual(repair.execute('x','y',self.body('L','25.0001'))[0],422);worker.assert_not_called()
 def test_historical_record_kept_but_repair_disallowed(self):
  run='74157a4c-fa28-441c-a56b-38c716fd2a6c';record=summary(run);self.assertTrue(record['historical_only']);self.assertFalse(record['within_current_owner_range'])
  c=next(c for c in record['candidates']if c['state']=='REJECTED_PHYSICAL')
  with patch.object(repair.subprocess,'Popen')as worker:
   status,r=repair.repair(json.dumps({'run_id':run,'candidate_id':c['candidate_id']}).encode());self.assertEqual(status,422);self.assertEqual(r['code'],'DIMENSION_OUT_OF_OWNER_RANGE');worker.assert_not_called()
if __name__=='__main__':unittest.main()
