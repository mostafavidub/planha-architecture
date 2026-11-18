import unittest,json
from pathlib import Path
from unittest.mock import patch
import closure_room_program_v2 as room
class NoReentry(unittest.TestCase):
 def test_baseline_without_parent_dispatch(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text())
  with patch('engine.evaluate',side_effect=AssertionError('PARENT_REENTRY')):
   r=room.evaluate(x['selected'][0],x['central_fresh_reviews'][0]);self.assertTrue(r['proofscopecomplete'],r)
 def test_identity_without_parent_dispatch(self):
  p=Path(__file__).resolve().parents[1];a=json.loads((p/'staging357_comparative/attached_service_final357.json').read_text());b=json.loads((p/'review357_source_identity/result.json').read_text())
  with patch('engine.evaluate',side_effect=AssertionError('PARENT_REENTRY')):
   r=room.evaluate(a,b,'SOURCE_IDENTITY357');self.assertTrue(r['proofscopecomplete'],r)
 def test_no_parent_import(self):
  src=Path(room.__file__).read_text();self.assertNotIn('from engine import',src)
if __name__=='__main__':unittest.main()
