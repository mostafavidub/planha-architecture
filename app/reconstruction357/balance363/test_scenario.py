import unittest,copy
from assessor import entry_open_scenario

def model():
 o={'opening_id':'A.entry','kind':'sliding_linear','closed_panel':['0','0','1','.1'],'open_panel':['1','0','2','.1'],'translation':['1','0'],'states':[{'fraction':'1','panel_rect':['1','0','2','.1']}]}
 return {'units':[{'id':'A'}],'operations':{'doors':[o]}}
class Tests(unittest.TestCase):
 def test_bound_open(self):self.assertEqual(len(entry_open_scenario(model())[0]),1)
 def test_wrong_translation(self):
  m=model();m['operations']['doors'][0]['translation']=['2','0']
  with self.assertRaises(ValueError):entry_open_scenario(m)
 def test_missing_actual_open_state(self):
  m=model();m['operations']['doors'][0]['states']=[]
  with self.assertRaises(ValueError):entry_open_scenario(m)
if __name__=='__main__':unittest.main()
