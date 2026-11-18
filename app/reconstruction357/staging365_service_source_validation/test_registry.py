import sys,unittest,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'runtime'))
from source_registry_service365 import CurrentContext,verify_context,resolve,_TOKEN
from contract114 import digest
class Tests(unittest.TestCase):
 def test_external_receipt(self):self.assertFalse(verify_context({}, {'verified':True})['verified'])
 def test_token(self):self.assertRaises(ValueError,CurrentContext,object(),{},{},time.monotonic()+2)
 def test_schema(self):self.assertRaises(ValueError,resolve,{'trace':{'schema':'CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1'}},time.monotonic()+2)
 def test_mutation(self):
  c=CurrentContext(_TOKEN,{}, {'model_hash':digest({})},time.monotonic()+2);c['fake']=1;self.assertFalse(verify_context({},c)['verified'])
 def test_model_switch(self):
  c=CurrentContext(_TOKEN,{}, {'model_hash':digest({})},time.monotonic()+2);self.assertFalse(verify_context({'fake':1},c)['verified'])
 def test_expired(self):
  c=CurrentContext(_TOKEN,{}, {'model_hash':digest({})},0);self.assertFalse(verify_context({},c)['verified'])
if __name__=='__main__':unittest.main()
