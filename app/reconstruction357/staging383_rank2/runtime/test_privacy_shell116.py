import unittest,copy
from privacy_shell116 import shell_certificate as cert
class Tests(unittest.TestCase):
 def setUp(self):
  self.s=[0,1,0.1,2];self.t=[4,1,5,2];self.g=[1,0,3,3]
  self.w={'bottom':[1,0,3,.1],'top':[1,2.9,3,3],'back':[2.9,0,3,3]}
 def call(self,w=None):return cert(self.s,self.t,self.g,list((w or self.w)),w or self.w)
 def test_actual_three_faces(self):self.assertIsNotNone(self.call())
 def test_no_envelope_opacity(self):self.assertIsNone(cert(self.s,self.t,self.g,['cabinet'],self.w))
 def test_missing_face(self):
  w=copy.deepcopy(self.w);del w['back'];self.assertIsNone(self.call(w))
 def test_slit(self):
  w=copy.deepcopy(self.w);w['back']=[2.9,0,3,1.49];w['back2']=[2.9,1.51,3,3];self.assertIsNone(self.call(w))
 def test_rigid_mirror(self):
  r=lambda q:[-q[2],q[1],-q[0],q[3]]
  self.assertIsNotNone(cert(r(self.s),r(self.t),r(self.g),list(self.w),{k:r(v)for k,v in self.w.items()}))
if __name__=='__main__':unittest.main()
