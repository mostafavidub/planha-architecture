import unittest,tempfile
from pathlib import Path
from copy import deepcopy
from service126 import Service,digest
from engine126 import select_scoped
class MetadataBinding(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.s=Service(str(Path(self.temp.name)/'db'),None,None,lambda:'fixed',{})
  self.raw={'W':'39','L':'7.07','n':2,'requested_count':6}
  self.base={'requested_count':6,'admitted_count':0,'distinct_count':0,'shortfall':6,'candidates':[],'organization_count':0,'organization_shortfall':6,'scoped_diversity':select_scoped([],6)[1],'verified_architectural_diversity':False}
 def tearDown(self):self.temp.cleanup()
 def test_positive(self):
  p=self.s._decorate(self.base,self.raw);self.s._validate(p,self.raw)
 def mutated(self,key,value):
  p=self.s._decorate(self.base,self.raw);p[key]=value;p['payload_hash']=digest({k:v for k,v in p.items()if k!='payload_hash'})
  with self.assertRaises(ValueError):self.s._validate(p,self.raw)
 def test_count_rehash(self):self.mutated('organization_count',6)
 def test_shortfall_rehash(self):self.mutated('organization_shortfall',0)
 def test_proof_rehash(self):self.mutated('scoped_diversity',{'scope':'SIX_PROVEN'})
 def test_claim_rehash(self):self.mutated('verified_architectural_diversity',True)
if __name__=='__main__':unittest.main()
