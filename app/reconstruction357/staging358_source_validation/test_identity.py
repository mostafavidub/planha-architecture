import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'runtime'))
from source_identity358 import check_one,expected,CANONICAL,HERE,verify_identity
from project_input_audit118 import PINS
class IdentityTests(unittest.TestCase):
 def test_all279(self):
  rows=[check_one(n,(CANONICAL/n).read_bytes(),(HERE/n).read_bytes(),h)for n,h in PINS.items()]
  self.assertEqual(len(rows),279);self.assertEqual(sum(r['relation']!='EXACT_BYTES'for r in rows),3)
 def test_unknown_geometry_delta(self):
  n='geometry114.py'
  n=next(k for k in PINS if k.startswith('assemble114'))
  x=(CANONICAL/n).read_bytes();self.assertRaises(ValueError,check_one,n,x,x+b'\n',PINS[n])
 def test_unknown_seam_delta(self):
  n='named_checks118.py';x=(CANONICAL/n).read_bytes();self.assertRaises(ValueError,check_one,n,x,expected(n,x)+b'\n',PINS[n])
 def test_canonical_tamper(self):
  n='named_checks118.py';x=(CANONICAL/n).read_bytes();self.assertRaises(ValueError,check_one,n,x+b'\n',expected(n,x),PINS[n])
 def test_json_receipt(self):self.assertRaises(ValueError,verify_identity,{}, {'verified':True},PINS)
if __name__=='__main__':unittest.main()
