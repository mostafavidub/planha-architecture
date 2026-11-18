import unittest,sys,json,copy,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'runtime'))
import source_identity_joint367 as identity
from project_input_audit118 import PINS
from notch_grammar_joint367 import allowed_walls,checked_integrity
R=json.loads((P.parent/'review367_joint_attempt2/actual367.json').read_text());M=R['candidate']['model'];C=R['candidate']['packet']['core']
class Tests(unittest.TestCase):
 def test_exact_original_deltas(self):
  for n,h in PINS.items():identity.check_one(n,(identity.CANONICAL/n).read_bytes(),(identity.HERE/n).read_bytes(),h)
 def test_mutation_rejected(self):
  n='named_checks118.py';o=(identity.CANONICAL/n).read_bytes()
  self.assertRaises(ValueError,identity.check_one,n,o,(identity.HERE/n).read_bytes()+b'x',hashlib.sha256(o).hexdigest())
 def test_actual_geometry_only(self):self.assertEqual(allowed_walls(M,C),{'core.notch367.A_separator'})
 def test_separator_tamper(self):
  m=copy.deepcopy(M);m['wall_hosts']['core.notch367.A_separator'][0]='0';self.assertRaises(ValueError,allowed_walls,m,C)
 def test_ownership_tamper(self):
  m=copy.deepcopy(M);m['units'][0]['ownership']=[];self.assertRaises(ValueError,allowed_walls,m,C)
 def test_receipt_not_authority(self):self.assertRaises(ValueError,checked_integrity,M,{'verified':True},lambda *a,**k:True)
 def test_registry_precedes_checker(self):
  s=(P/'evaluate367.py').read_text();self.assertLess(s.index('registry={'),s.index('raw=evaluate('))
 def test_producer_is_attempt2(self):
  s=(P/'replay_worker.py').read_text();self.assertIn('staging367_service_joint_attempt2',s);self.assertIn('FULL_REPLAY_MISMATCH',s)
if __name__=='__main__':unittest.main()
