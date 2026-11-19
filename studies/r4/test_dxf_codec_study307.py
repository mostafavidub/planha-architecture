import copy,hashlib,io,unittest
import ezdxf
from fractions import Fraction as F
from dxf_codec_study307 import encode,parity,observe,precision_observation,validate,AUTH,source_guard
def fixture():
 return {'schema':'SYNTHETIC_DXF_CODEC_V1','units':'m','lot':['10','8'],
  'walls':[{'id':'wall1','rect':['1','1','9','1.5']}],
  'openings':[{'id':'door1','host':'wall1','rect':['4','1','5','1.5']}],
  'rooms':[{'id':'room1','name':'اتاق خواب','rect':['1','2','4','6']},{'id':'room2','name':'نشیمن','rect':['5','2','9','6']}]}
def modified(data,fn):
 doc=ezdxf.read(io.StringIO(data.decode('ascii'),newline=None));fn(doc)
 out=io.StringIO();doc.write(out);return out.getvalue().encode('ascii','backslashreplace')
class CodecStudy(unittest.TestCase):
 def setUp(self):self.s=fixture();self.b=encode(self.s)
 def test_roundtrip_independent_reader(self):
  r=parity(self.s,self.b);self.assertEqual(r['state'],'EXACT_SYNTHETIC_CODEC_PARITY_ONLY')
  self.assertTrue(all(r[k] is False for k in AUTH));self.assertFalse(r['product_snapshot_bound'])
 def test_known_aperture_geometry_not_self_oracle(self):
  boxes,names=observe(self.b)
  self.assertEqual(boxes['W__wall1__0'],tuple(map(F,['1','1','4','1.5'])))
  self.assertEqual(boxes['W__wall1__1'],tuple(map(F,['5','1','9','1.5'])))
  self.assertEqual(names['N__room1'][0],'اتاق خواب')
 def test_crlf_and_lf_streams_have_same_semantics(self):
  self.assertIn(b'\r\n',self.b)
  self.assertEqual(observe(self.b),observe(self.b.replace(b'\r\n',b'\n')))
 def test_deterministic_source_and_input_unchanged(self):
  old=copy.deepcopy(self.s);pin=source_guard()
  self.assertEqual(self.b,encode(self.s));parity(self.s,self.b)
  self.assertEqual(self.s,old);self.assertEqual(source_guard(),pin)
 def test_wrong_units(self):
  b=modified(self.b,lambda d:d.header.__setitem__('$INSUNITS',4))
  with self.assertRaisesRegex(ValueError,'DXF_UNITS_OR_VERSION'):parity(self.s,b)
 def test_scale_ten(self):
  from ezdxf.math import Matrix44
  b=modified(self.b,lambda d:[e.transform(Matrix44.scale(10))for e in d.modelspace()])
  with self.assertRaisesRegex(ValueError,'LOT_PARITY'):parity(self.s,b)
 def test_missing_opening(self):
  def change(d):
   for e in list(d.modelspace()):
    if e.dxf.layer=='O__door1':d.modelspace().delete_entity(e)
  with self.assertRaisesRegex(ValueError,'OBJECT_PARITY'):parity(self.s,modified(self.b,change))
 def test_wall_fills_aperture(self):
  # Complete closed rectangle across the missing gap, not mere ID/hash tamper.
  def change(d):
   m=d.modelspace()
   for e in list(m):
    if e.dxf.layer.startswith('W__'):m.delete_entity(e)
   for a,b in [((1,1),(9,1)),((9,1),(9,1.5)),((9,1.5),(1,1.5)),((1,1.5),(1,1))]:
    m.add_line(a,b,dxfattribs={'layer':'W__wall1__0'})
  with self.assertRaisesRegex(ValueError,'WALL_MINUS_OPENING_PARITY'):parity(self.s,modified(self.b,change))
 def test_corrupt_persian_name(self):
  def change(d):
   for e in d.modelspace().query('TEXT'):e.dxf.text='CORRUPT'
  with self.assertRaisesRegex(ValueError,'NAME_OR_LOCATION_PARITY'):parity(self.s,modified(self.b,change))
 def test_wrong_layer(self):
  def change(d):
   for e in d.modelspace():
    if e.dxf.layer=='O__door1':e.dxf.layer='WRONG'
  with self.assertRaises(ValueError):parity(self.s,modified(self.b,change))
 def test_other_fixture(self):
  s=fixture();s['rooms'][0]['rect'][0]='1.25'
  with self.assertRaisesRegex(ValueError,'OBJECT_PARITY'):parity(s,self.b)
 def test_missing_edge_is_not_closed(self):
  def change(d):d.modelspace().delete_entity(next(iter(d.modelspace())))
  with self.assertRaisesRegex(ValueError,'RECT_EDGE_COUNT'):parity(self.s,modified(self.b,change))
 def test_extra_entity(self):
  b=modified(self.b,lambda d:d.modelspace().add_circle((2,3),1))
  with self.assertRaisesRegex(ValueError,'UNSUPPORTED_ENTITY'):parity(self.s,b)
 def test_precision_exact_and_loss_reported(self):
  self.assertTrue(precision_observation('1.25')['exact'])
  r=precision_observation('1.23456789012345')
  self.assertEqual(r['serialized'],'1.23456789012');self.assertFalse(r['exact']);self.assertFalse(r['tolerance_assumed'])
  s=fixture();s['rooms'][0]['rect'][0]='1.23456789012345'
  with self.assertRaisesRegex(ValueError,'OBJECT_PARITY'):parity(s,encode(s))
 def test_invalid_types_and_authority_fields(self):
  for value in [True,1.25,float('nan'),float('inf'),'NaN','1/3']:
   s=fixture();s['lot'][0]=value
   with self.assertRaises(ValueError):encode(s)
  s=fixture();s['qualified']=True
  with self.assertRaisesRegex(ValueError,'FIXTURE_FIELDS'):encode(s)
 def test_duplicate_and_bad_host(self):
  s=fixture();s['walls'][0]['id']='a__b'
  with self.assertRaisesRegex(ValueError,'ID_REQUIRED'):encode(s)
  s=fixture();s['rooms'].append(copy.deepcopy(s['rooms'][0]))
  with self.assertRaisesRegex(ValueError,'DUPLICATE_ID'):encode(s)
  s=fixture();s['openings'][0]['host']='absent'
  with self.assertRaisesRegex(ValueError,'OPENING_HOST'):encode(s)
 def test_more_than_224_layers_have_unique_handles(self):
  s=fixture();s['rooms']=[{'id':'room'+str(i),'name':'اتاق','rect':['1','2','4','6']}for i in range(230)]
  data=encode(s);rows=data.decode('ascii').splitlines()
  handles=[rows[i+1]for i in range(0,len(rows),2)if rows[i]=='5']
  self.assertEqual(len(handles),len(set(handles)))
  self.assertGreater(len(handles),224);parity(s,data)
 def test_boundary_and_unknown_schema(self):
  for v in ['5','25']:
   s=fixture();s['lot'][0]=v
   if v=='5':
    s['walls'][0]['rect'][2]='5';s['rooms']=s['rooms'][:1]
   parity(s,encode(s))
  for v in ['4.999','25.001']:
   s=fixture();s['lot'][0]=v
   with self.assertRaisesRegex(ValueError,'LOT_DOMAIN'):encode(s)
if __name__=='__main__':unittest.main()
