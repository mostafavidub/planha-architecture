import unittest,copy,sys,ast
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parent/'semantic_rules357')]
import gate380 as g
class Tests(unittest.TestCase):
 def setUp(self):self.i=g.load_inputs()
 def test_pinned_gate(self):self.assertEqual(g.validate(**self.i)['model_digest'],'e7fe5a247adda70eb9fd400e3118f20c0c0a13d03df2d98c64b846555f031055')
 def test_tampered_record(self):
  self.i['record']['candidate']['request']['W']='27'
  with self.assertRaises(ValueError):g.validate(**self.i)
 def test_forged_self_consistent_model(self):
  r=self.i['record'];f=self.i['fresh'];r['candidate']['model']['inputs'][0]='27';r['candidate']['packet']['world_model']=copy.deepcopy(r['candidate']['model']);r['candidate']['model_digest']=g.D(r['candidate']['model']);f['model_digest']=r['candidate']['model_digest'];f['raw_report']['model_hash']=f['model_digest']
  with self.assertRaises(ValueError):g.validate(**self.i)
 def test_tampered_review(self):
  self.i['fresh']['review_id']='fake'
  with self.assertRaises(ValueError):g.validate(**self.i)
 def test_view_tamper(self):
  e,r,_=g.views(**self.i);g.validate_views(e,r);e['raw']['W']='27'
  with self.assertRaises(ValueError):g.validate_views(e,r)
 def test_no_old_gate_adapter(self):
  from adapters380 import MAP
  self.assertEqual(MAP['group_readsets365_v2'],'groups380');self.assertEqual(MAP['closure_room_program365'],'room380')
 def test_forged_module_origin(self):
  import types
  from unittest.mock import patch
  from adapters380 import load
  with patch.dict(sys.modules,{'groups380':types.SimpleNamespace(__file__='/tmp/groups380.py')}):
   with self.assertRaisesRegex(ValueError,'SEMANTIC_MODULE_ORIGIN'):load('group_readsets365_v2')
 def test_no_source_fresh_calls(self):
  for p in HERE.glob('*.py'):
   if p.name.startswith('test'):continue
   tree=ast.parse(p.read_text())
   for n in ast.walk(tree):
    if isinstance(n,ast.ImportFrom):self.assertNotIn(n.module,('source378','evaluate378','checker114'))
 def test_closed_scope(self):
  s=(HERE/'semantic380.py').read_text();self.assertIn('CURRENT_FINAL_ROLE_DAG_NOT_PORTED',s);self.assertIn("'accepted':False",s)
if __name__=='__main__':unittest.main()
