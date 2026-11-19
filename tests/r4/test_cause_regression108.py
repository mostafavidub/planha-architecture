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
 def test_removed_source_line_detected(self):
  original=(s.ENGINE/'search114.py').read_text()
  fork=(ROOT/'app/local_integration/cause_parent_witness108.py').read_text()
  self.assertEqual(s.strip_selector(fork),original)
  self.assertNotEqual(s.strip_selector(fork.replace('lo=y0/scale','lo=0',1)),original)
if __name__=='__main__':unittest.main()
