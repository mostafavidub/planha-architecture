import copy,unittest,json
from xml.etree import ElementTree as ET
import paired_codec308 as p
from test_dxf_codec_study307 import fixture
class Paired(unittest.TestCase):
 def setUp(self):
  self.s=fixture();self.svg=p.svg.encode(self.s);self.dxf=p.dxf.encode(self.s);self.report=p.make_report(self.s)
 def check(self,**kw):
  return p.assess(kw.get('s',self.s),kw.get('svg',self.svg),kw.get('dxf',self.dxf),kw.get('report',self.report))
 def test_actual_pair_table(self):
  r=self.check();self.assertEqual(len(r['rows']),8);self.assertEqual(r['mismatch_count'],0)
  self.assertEqual(r['extent_m'],['10','8']);self.assertTrue(all(r[k]is False for k in p.AUTH))
  self.assertEqual({r['kind']for r in r['rows']},{'lot','room','wall','opening','label'})
  print(json.dumps({k:r[k]for k in ('schema','state','fixture_digest','svg_sha256','dxf_sha256','report_digest','mismatch_count','source_snapshot','visual_reviewed','product_snapshot_bound')},sort_keys=True))
 def test_receipt_roundtrip(self):
  c=p.receipt(self.s,self.svg,self.dxf,self.report)
  self.assertEqual(p.verify(self.s,self.svg,self.dxf,self.report,c),self.check())
 def test_cross_snapshot_bytes(self):
  other=fixture();other['rooms'][0]['name']='اتاق دیگر'
  with self.assertRaises(ValueError):self.check(dxf=p.dxf.encode(other))
  with self.assertRaises(ValueError):self.check(svg=p.svg.encode(other))
 def test_cross_snapshot_report(self):
  other=fixture();other['lot'][0]='11'
  with self.assertRaisesRegex(ValueError,'REPORT_BINDING'):self.check(report=p.make_report(other))
 def test_missing_opening_and_room(self):
  for id in ('opening_door1','room_room1'):
   root=ET.fromstring(self.svg);root.remove(next(e for e in root if e.attrib['id']==id))
   with self.assertRaises(ValueError):self.check(svg=ET.tostring(root))
 def test_changed_entity(self):
  root=ET.fromstring(self.svg);root[1].set('x','61')
  with self.assertRaises(ValueError):self.check(svg=ET.tostring(root))
 def test_rehashed_receipt_geometry(self):
  c=p.receipt(self.s,self.svg,self.dxf,self.report);c['body']['rows'][0]['state']='PASS'
  c['digest']=p.digest(c['body'])
  with self.assertRaisesRegex(ValueError,'PAIRED_RECEIPT_MISMATCH'):p.verify(self.s,self.svg,self.dxf,self.report,c)
 def test_rehashed_receipt_byte_identity(self):
  c=p.receipt(self.s,self.svg,self.dxf,self.report)
  b=self.dxf.replace(b'\r\n',b'\n')
  self.assertEqual(self.check(dxf=b)['rows'],c['body']['rows'])
  with self.assertRaisesRegex(ValueError,'PAIRED_RECEIPT_MISMATCH'):p.verify(self.s,self.svg,b,self.report,c)
 def test_fake_positive_report(self):
  for field,value in [('state','PASS'),('qualified',True),('architectural_evaluation','PASS')]:
   r=copy.deepcopy(self.report);r[field]=value
   with self.assertRaisesRegex(ValueError,'REPORT_BINDING'):self.check(report=r)
 def test_report_inventory_tamper(self):
  r=copy.deepcopy(self.report);r['objects']['rooms'].pop()
  with self.assertRaisesRegex(ValueError,'REPORT_BINDING'):self.check(report=r)
 def test_wrong_units(self):
  b=self.dxf.replace(b'$INSUNITS\r\n70\r\n6',b'$INSUNITS\r\n70\r\n4')
  with self.assertRaises(ValueError):self.check(dxf=b)
 def test_wrong_frame(self):
  root=ET.fromstring(self.svg);root.set('data-scale','4')
  with self.assertRaises(ValueError):self.check(svg=ET.tostring(root))
 def test_typed_receipt(self):
  c=p.receipt(self.s,self.svg,self.dxf,self.report);c['body']['mismatch_count']=False;c['digest']=p.digest(c['body'])
  with self.assertRaises(ValueError):p.verify(self.s,self.svg,self.dxf,self.report,c)
 def test_report_detached(self):
  r=p.make_report(self.s);before=copy.deepcopy(r);self.s['lot'][0]='11'
  self.assertEqual(r,before)
 def test_source_and_inputs_unchanged(self):
  before=copy.deepcopy((self.s,self.report));pins=p.guard();self.check()
  self.assertEqual(before,(self.s,self.report));self.assertEqual(pins,p.guard())
if __name__=='__main__':unittest.main()
