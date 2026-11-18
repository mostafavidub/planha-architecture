import unittest,sys,json,copy
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;W=R.parent
sys.path[:0]=[str(H),str(R/'staging381_role_semantics')]
from gate381 import load_inputs,views,D
from final_join386 import validate_semantic_views,validate_wall_inventory
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  i=load_inputs();cls.r=i['record'];cls.f=i['fresh'];cls.v=views(cls.r,cls.f);cls.w=json.loads((W/'review381_actual_v1/result.json').read_text())['evidence']['spatial']['wall_purpose']
 def test_exact_actual_view(self):self.assertEqual(validate_semantic_views(self.r,self.f,self.v),self.w['base_fresh_digest'])
 def test_exact_wall(self):self.assertEqual(set(validate_wall_inventory(self.r,self.f,self.w,self.v)),set(self.r['candidate']['model']['walls']))
 def test_omitted_wall(self):
  w=copy.deepcopy(self.w);w['rows'].pop()
  with self.assertRaises(ValueError):validate_wall_inventory(self.r,self.f,w,self.v)
 def test_raw_digest_wrong(self):
  w=copy.deepcopy(self.w);w['base_fresh_digest']=D(self.f['raw_report'])
  with self.assertRaises(ValueError):validate_wall_inventory(self.r,self.f,w,self.v)
 def test_forged_view_raw(self):
  v=copy.deepcopy(self.v);v[1]['raw_fresh_report']['status']='FORGED'
  with self.assertRaises(ValueError):validate_semantic_views(self.r,self.f,v)
 def test_forged_packet(self):
  v=copy.deepcopy(self.v);v[0]['packet']['world_model']['inputs']=['1','1',2];v[1]['candidate_digest']=D(v[0])
  with self.assertRaises(ValueError):validate_semantic_views(self.r,self.f,v)
 def test_wrong_producer(self):
  v=copy.deepcopy(self.v);v[2]['record_digest']='wrong'
  with self.assertRaises(ValueError):validate_semantic_views(self.r,self.f,v)
 def test_run_metadata_preserved(self):
  v=copy.deepcopy(self.v);v[0]['schema']='CURRENT385_SEMANTIC_VIEW';v[1]['schema']='CURRENT385_SEMANTIC_RESULT';v[0]['same_pipeline_run']=True;v[1]['same_pipeline_run']=True;v[1]['candidate_digest']=D(v[0]);self.assertEqual(validate_semantic_views(self.r,self.f,v),D(v[1]))
if __name__=='__main__':unittest.main()
