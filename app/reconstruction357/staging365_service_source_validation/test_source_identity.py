import unittest,sys,hashlib,ast
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'runtime'))
import source_identity_service365 as s
from project_input_audit118 import PINS
class Tests(unittest.TestCase):
 def test_all_original_pins_and_exact_delta(self):
  for n,h in PINS.items():
   with self.subTest(n=n):s.check_one(n,(s.CANONICAL/n).read_bytes(),(s.HERE/n).read_bytes(),h)
 def test_unapproved_delta_rejected(self):
  n='named_checks118.py';old=(s.CANONICAL/n).read_bytes()
  with self.assertRaises(ValueError):s.check_one(n,old,(s.HERE/n).read_bytes()+b'\n# mutation',hashlib.sha256(old).hexdigest())
 def test_no_notch_or_balanced_grammar(self):
  self.assertEqual((s.HERE/'core_circulation_scope118.py').read_bytes(),(s.CANONICAL/'core_circulation_scope118.py').read_bytes())
  self.assertNotIn('notch_grammar',(s.HERE/'named_checks118.py').read_text())
 def test_compile_and_registry_before_evaluate(self):
  for f in P.glob('*.py'):compile(f.read_bytes(),str(f),'exec')
  body=(P/'evaluate365.py').read_text();self.assertLess(body.index('registry={'),body.index('raw=evaluate('))
if __name__=='__main__':unittest.main()
