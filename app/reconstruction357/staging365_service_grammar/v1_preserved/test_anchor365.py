import unittest,copy
from service_anchor365 import anchors,choose,validate_rectangles
class Tests(unittest.TestCase):
 def module(self):return {'input_program':{'width':'2','depth':'2'},'walls':{'left':['-.1','0','0','2'],'right':['2','0','2.1','2']},'wall_hosts':{'left':['-.1','0','0','2'],'right':['2','0','2.1','2']},'unit':{'fixtures':{'f':['.5','.5','1','1']},'activities':{'a':['.5','1','1','1.5']},'rooms':{'room':[['0','0','2','2']]}},'operations':{}}
 def test_source_anchor(self):
  a=anchors(self.module(),{'parts':[['.5','-.7','1.2','0']]},['0','0','10','10']);self.assertEqual(a['left']['x'],'1/10');self.assertEqual(a['right']['x'],'79/10');self.assertEqual(a['left']['y_min'],'7/10')
 def test_no_fake_contact(self):
  m=self.module();m['wall_hosts']={'interior':['.5','0','.6','2']};self.assertFalse(anchors(m,{'parts':[]},['0','0','10','10']))
 def test_source_outside_extent(self):self.assertFalse(anchors(self.module(),{'parts':[]},['0','0','2','2']))
 def test_missing_source(self):
  m=self.module();del m['unit']['activities']
  with self.assertRaises(KeyError):anchors(m,{'parts':[]},['0','0','10','10'])
 def test_unregistered_side(self):
  with self.assertRaises(ValueError):choose(self.module(),self.module(),{},['0','0','10','10'],'ANY')
 def test_quantized_or_resized_rejected(self):
  c=choose(self.module(),self.module(),{'bath':{'parts':[]},'kitchen':{'parts':[]}},['0','0','10','10'],'BATH_RIGHT_KITCHEN_LEFT');rs={'bath':['7.9','1','9.9','3'],'kitchen':['.1','1','2.1','3']};self.assertTrue(validate_rectangles(rs,c));rs['bath'][2]='10'
  with self.assertRaises(ValueError):validate_rectangles(rs,c)
if __name__=='__main__':unittest.main()
