"""Pure gates and negative joins only; no semantic kernel execution."""
import unittest,json,copy,sys,ast,types
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;W=R.parent
sys.path[:0]=[str(H),str(R/'staging378_finite_portals'),str(R/'semantic_rules357')]
import gate384 as g
from cohort384 import bind_intrinsic,verify_historical
class Tests(unittest.TestCase):
 def test_actual_gate(self):
  i=g.load_inputs();self.assertEqual(g.validate(i['record'],i['fresh'])['model_digest'],'389e1c34b481d13ab08cf178e58d49fcf2cceffb24bea05c58bf8a19b1f5c0dc')
 def test_forged_record(self):
  i=g.load_inputs();r=copy.deepcopy(i['record']);r['trace']['selection_rank']=1
  with self.assertRaises(ValueError):g.validate(r,i['fresh'])
 def test_rank1_not_rank2(self):
  r=json.loads((W/'independent379actual/evidence/review379_actual_v1/runs/02dc5f92-93b6-4466-be6c-5114e96bc636/record.json').read_text())
  with self.assertRaises(ValueError):g.validate(r,g.load_inputs()['fresh'])
 def test_eight_historical_receipts(self):
  h=json.loads((W/'review382_actual_v1/result.json').read_text());r=json.loads((W/'independent379actual/evidence/review379_actual_v1/runs/02dc5f92-93b6-4466-be6c-5114e96bc636/record.json').read_text());self.assertEqual(len(verify_historical(h,r)),8)
  h['pairs'][1]['historical_eligibility']['fresh_digest']='wrong'
  with self.assertRaises(ValueError):verify_historical(h,r)
 def test_wrong_intrinsic(self):
  i=g.load_inputs();p=json.loads((W/'review381_actual_v1/result.json').read_text())['evidence']['essential']['evidence']['intrinsic_eligibility']
  with self.assertRaises(ValueError):bind_intrinsic(i['record'],i['fresh'],p)
 def test_unchanged_eligibility_predicate(self):
  def tree(p):
   t=ast.parse(p.read_text());f=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='evaluate');return ast.dump(f,include_attributes=False)
  self.assertEqual(tree(H/'eligibility384.py'),tree(R/'staging381_role_semantics/eligibility381.py'))
 def test_wrong_join_binding(self):
  from final_join384 import join
  i=g.load_inputs();roles=json.loads((W/'review381_actual_v1/result.json').read_text())
  with self.assertRaises(ValueError):join(i['record'],i['fresh'],roles,{'binding':roles['binding']})
 def test_rank0_nonrectangular_and_core_negative(self):
  from cohort384 import source_equivalence_checks
  base=json.loads((R/'staging365_balanced_portals/actual365.json').read_text());alt=g.load_inputs()['record'];zero=copy.deepcopy(base['candidate']['packet']['core'])
  self.assertTrue(all(source_equivalence_checks(base,alt,zero).values()))
  forged=copy.deepcopy(alt);forged['trace']['proposal']['network_scope']='FORGED'
  self.assertFalse(source_equivalence_checks(base,forged,zero)['full_proposal'])
  zero['entry_centers']['A'][1]='999'
  self.assertFalse(source_equivalence_checks(base,alt,zero)['all_nonselector_core_fields'])
 def test_retained_terminal_forgery(self):
  from cohort384 import retained_terminals
  h=json.loads((W/'review382_actual_v1/result.json').read_text());r=json.loads((W/'independent379actual/evidence/review379_actual_v1/runs/02dc5f92-93b6-4466-be6c-5114e96bc636/record.json').read_text());h['full_band_current']['rows'][0]['loss_exact_m2']='0'
  self.assertFalse(retained_terminals(h,r)['closed_in_declared_conditional_domain'])
 def test_omitted_wall_and_wrong_origin(self):
  from final_join384 import validate_wall_inventory
  r={'candidate':{'model':{'walls':{'a':[],'b':[]}}}};f={'raw_report':{}};w={'rows':[{'wall_id':'a'},{'wall_id':'b'}],'source_origin_record_digest':g.D(r),'base_fresh_digest':g.D(f['raw_report'])}
  self.assertEqual(validate_wall_inventory(r,f,w),['a','b'])
  missing=copy.deepcopy(w);missing['rows'].pop()
  with self.assertRaises(ValueError):validate_wall_inventory(r,f,missing)
  w['source_origin_record_digest']='wrong'
  with self.assertRaises(ValueError):validate_wall_inventory(r,f,w)
 def test_module_origin(self):
  from adapters384 import require_origin
  with self.assertRaises(ValueError):require_origin(types.SimpleNamespace(__file__='/tmp/fake.py'),'groups384')
if __name__=='__main__':unittest.main()
