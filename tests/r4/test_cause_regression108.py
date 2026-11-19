"""Source master/selector extraction and real report-binding reuse. No solver."""
import copy,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import cause_regression_support108 as s
import search114,cause_parent_witness108 as w
from core_choice_pair_study import selected_core
class Regression108(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.core,_=selected_core({'W':'18','L':'22','n':2,'requested_count':1},'FRONT_REAR_COMPACT118')
  opts={'sleep_roles':['double','twin'],'variant':0,'topology':'SIDE_ROOTED_SERVICES','diagnostic_capture':lambda d:d}
  with patch.object(search114,'milp',side_effect=AssertionError('NO_SOLVER')),patch.object(w,'milp',side_effect=AssertionError('NO_SOLVER')):
   cls.a=search114.propose(cls.core,2,**opts);cls.b=w.propose(cls.core,2,**opts)
 def test_source_exact_except_selector(self):self.assertTrue(s.source_guard())
 def test_actual_matrix_retention(self):self.assertTrue(s.compare_capture(self.a,self.b)['verified'])
 def test_changed_old_coefficient_rejected(self):
  b=copy.deepcopy(self.b);b['matrix'].data[0]+=1
  with self.assertRaises(ValueError):s.compare_capture(self.a,b)
 def test_changed_old_bounds_rejected(self):
  b=copy.deepcopy(self.b);b['bounds'].lb[0]+=1
  with self.assertRaises(ValueError):s.compare_capture(self.a,b)
 def test_changed_old_objective_rejected(self):
  b=copy.deepcopy(self.b);b['objective'][0]+=1
  with self.assertRaises(ValueError):s.compare_capture(self.a,b)
 def test_changed_integrality_rejected(self):
  b=copy.deepcopy(self.b);b['integrality'][0]=1-b['integrality'][0]
  with self.assertRaises(ValueError):s.compare_capture(self.a,b)
 def test_changed_row_bound_rejected(self):
  b=copy.deepcopy(self.b);b['upper'][0]-=1
  with self.assertRaises(ValueError):s.compare_capture(self.a,b)
 def test_missing_selector_rejected(self):
  with self.assertRaises(ValueError):s.compare_capture(self.a,self.a)
 def test_source_piece_positive_and_contact_only(self):
  piece=s.profiles()['bath_apron'][0]
  p={'rectangles':{'bath':['0','0','3.15','2.25'],'dining':list(piece)}}
  self.assertTrue(s.selector_geometry(p)['positive_source_piece_overlap'])
  p['rectangles']['dining']=['10','10','11','11']
  self.assertFalse(s.selector_geometry(p)['positive_source_piece_overlap'])
 def test_exact_contact_and_subgrid_not_selected(self):
  from contract114 import GRID
  from fractions import Fraction as F
  a,b,c,d=map(F,s.profiles()['bath_apron'][0])
  for x in(c,c-GRID/2):
   p={'rectangles':{'bath':['0','0','3.15','2.25'],'dining':list(map(str,[x,b,c+1,d]))}}
   self.assertFalse(s.selector_geometry(p)['positive_source_piece_overlap'])
 def test_actual_added_rows_or_positive_contact_subgrid_and_disabled(self):
  import numpy as np
  from fractions import Fraction as F
  from contract114 import GRID
  m,n=self.a['matrix'].shape
  rows=self.b['matrix'][m:];lo=self.b['lower'][m:];hi=self.b['upper'][m:]
  bk=4*next(i for i,z in enumerate(self.a['specs'])if z[0]=='bath')
  dk=4*next(i for i,z in enumerate(self.a['specs'])if z[0]=='dining')
  pieces=s.profiles()['bath_apron']
  for index,piece in enumerate(pieces):
   a,b,c,d=map(F,piece)
   def assigned(x,right,active=True):
    v=np.zeros(self.b['matrix'].shape[1])
    v[dk]=float(x/GRID);v[dk+1]=float(b/GRID);v[dk+2]=float((right-x)/GRID);v[dk+3]=float((d-b)/GRID)
    v[n+index]=int(active)
    values=rows@v
    return np.all(values>=lo-1e-9)and np.all(values<=hi+1e-9),values
   self.assertTrue(assigned(a,c)[0])
   self.assertFalse(assigned(c,c+1)[0])
   self.assertFalse(assigned(c-GRID/2,c+1)[0])
   good,values=assigned(c,c+1,False)
   self.assertFalse(good) # OR requires at least one chosen piece.
   self.assertTrue(np.all(values[:-1]>=lo[:-1]-1e-9)) # z=0 disables overlap only.
 def test_readback_no_model_is_explicit_and_rejects_digest_change(self):
  import tempfile,json
  with tempfile.TemporaryDirectory()as tmp:
   folder=Path(tmp);report={'parent_no_witness':{'status':'NO_PROPOSAL_IN_THIS_TOPOLOGY'}}
   (folder/'reports.json').write_text(json.dumps(report))
   result={'state':'BLOCKED_NO_PARENT_PROPOSAL','parent_observed':False,'child_observed':False,'attempt_count':1,'cause_repair_verified':False,
    'report_digests':{k:s.digest(v)for k,v in report.items()}}
   self.assertEqual(s.readback(folder,result)['state'],'NO_MODEL_COLLECTION_READBACK')
   result['report_digests']['parent_no_witness']='0'*64
   with self.assertRaises(ValueError):s.readback(folder,result)
 def test_rehashed_fake_completed_missing_bundles_rejected(self):
  import tempfile,json
  with tempfile.TemporaryDirectory()as tmp:
   folder=Path(tmp);(folder/'reports.json').write_text('{}')
   result={'state':'CAUSE_RESOLVED_NOT_QUALIFIED','parent_observed':True,'child_observed':True,'attempt_count':2,'cause_repair_verified':True,'report_digests':{}}
   with self.assertRaisesRegex(ValueError,'READBACK_STATE_BUNDLE_REQUIRED'):s.readback(folder,result)
 def test_rehashed_state_and_attempt_count_rejected(self):
  import tempfile,json
  with tempfile.TemporaryDirectory()as tmp:
   folder=Path(tmp);report={'parent_no_witness':{'status':'NO_PROPOSAL_IN_THIS_TOPOLOGY'}}
   (folder/'reports.json').write_text(json.dumps(report))
   base={'state':'BLOCKED_NO_PARENT_PROPOSAL','parent_observed':False,'child_observed':False,'attempt_count':1,'cause_repair_verified':False,
    'report_digests':{k:s.digest(v)for k,v in report.items()}}
   for key,value in(('state','CAUSE_RESOLVED_NOT_QUALIFIED'),('attempt_count',True),('attempt_count',2),('cause_repair_verified',True)):
    bad=copy.deepcopy(base);bad[key]=value
    with self.assertRaises(ValueError):s.readback(folder,bad)
 def test_removed_source_line_detected(self):
  original=(s.ENGINE/'search114.py').read_text()
  fork=(ROOT/'app/local_integration/cause_parent_witness108.py').read_text()
  self.assertEqual(s.strip_selector(fork),original)
  self.assertNotEqual(s.strip_selector(fork.replace('lo=y0/scale','lo=0',1)),original)
if __name__=='__main__':unittest.main()
