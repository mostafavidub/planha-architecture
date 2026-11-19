"""Paired synthetic codec consistency, not admission, authenticity or visual QA."""
import copy,hashlib,pathlib
from fractions import Fraction as F
from xml.etree import ElementTree as ET
import preview_codec_study306 as svg
import dxf_codec_study307 as dxf
from dxf_codec_study307 import require,digest,AUTH
PINS={'preview_codec_study306.py':'bda5dd060c044b33e94742b2de246c846a861351',
 'dxf_codec_study307.py':'5b922b484b27f3792748b2a4bf5faaa7e221112f'}
def guard():
 out={}
 for name,pin in PINS.items():
  p=pathlib.Path(__file__).with_name(name);b=p.read_bytes()
  require(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin,'PAIRED_SOURCE_CHANGED')
  mod=svg if name.startswith('preview') else dxf
  require(pathlib.Path(mod.__file__).resolve()==p.resolve(),'PAIRED_IMPORT_PATH')
  out[name]=hashlib.sha256(b).hexdigest()
 return out
def sha(b):return hashlib.sha256(b).hexdigest()
def rational(q):return [str(x)for x in q]
def make_report(s):
 # Nonarchitectural report derived from the fixture, never caller PASS flags.
 dxf.validate(s)
 return {'schema':'SYNTHETIC_INVENTORY_REPORT308_V1','fixture_digest':digest(s),
  'state':'SYNTHETIC_INVENTORY_ONLY','units':s['units'],'extent':copy.deepcopy(s['lot']),
  'objects':{k:copy.deepcopy(s[k])for k in ('rooms','walls','openings')},
  'architectural_evaluation':'NOT_RUN',**AUTH}
def assess(s,svgb,dxfb,report):
 pins=guard();original=digest(s)
 require(digest(report)==digest(make_report(s)),'REPORT_BINDING_OR_SEMANTICS')
 sr=svg.inspect(s,svgb);dr=dxf.parity(s,dxfb)
 boxes,names=dxf.observe(dxfb);root=ET.fromstring(svgb)
 L=dxf.num(s['lot'][1]);rows=[];seen=set()
 for e in root:
  a=e.attrib;kind=a['data-kind'];sid=a['data-source-id']
  if kind=='label':
   key='N__'+sid
   observed=(e.text,((F(a['x'])-svg.PAD)/svg.S,L-(F(a['y'])-svg.PAD)/svg.S))
   require(names.get(key)==observed,'PAIRED_LABEL')
   value={'name':observed[0],'point_m':rational(observed[1])}
  else:
   key={'lot':'LOT','room':'R__'+sid,'opening':'O__'+sid}.get(kind)
   if kind=='wall':key='W__'+sid+'__'+a['id'].rsplit('_',1)[1]
   x,y,w,h=[F(a[k])for k in ('x','y','width','height')]
   q=((x-svg.PAD)/svg.S,L-(y-svg.PAD+h)/svg.S,(x-svg.PAD+w)/svg.S,L-(y-svg.PAD)/svg.S)
   require(boxes.get(key)==q,'PAIRED_RECTANGLE')
   value={'rect_m':rational(q)}
  require(key not in seen,'PAIRED_DUPLICATE');seen.add(key)
  rows.append({'kind':kind,'source_id':sid,'svg_id':a['id'],'dxf_layer':key,'value':value,'state':'EXACT'})
 require(seen==set(boxes)|set(names),'PAIRED_INVENTORY')
 rows.sort(key=lambda r:r['dxf_layer'])
 require(guard()==pins and digest(s)==original,'PAIRED_SOURCE_CHANGED')
 return {'schema':'SYNTHETIC_PAIRED308_V1','state':'PAIRED_CODEC_CONSISTENCY_ONLY',
  'fixture_digest':original,'svg_sha256':sha(svgb),'dxf_sha256':sha(dxfb),
  'report_digest':digest(report),'source_snapshot':pins,'units':'m',
  'extent_m':rational(map(dxf.num,s['lot'])),'rows':rows,'mismatch_count':0,
  'frame':'SVG_Y_INVERTED_TO_DXF_CARTESIAN_METRES',
  'svg_observation_digest':digest(sr),'dxf_observation_digest':digest(dr),
  'not_checked':['pixel_review','DXF_visibility_text_style','complete_DXF_audit',
   'product_snapshot_admission','architectural_quality','source_authenticity'],
  'visual_reviewed':False,'product_snapshot_bound':False,**AUTH}
def receipt(s,svgb,dxfb,report):
 body=assess(s,svgb,dxfb,report)
 return {'body':body,'digest':digest(body)}
def verify(s,svgb,dxfb,report,claimed):
 expected=receipt(s,svgb,dxfb,report)
 require(digest(claimed)==digest(expected),'PAIRED_RECEIPT_MISMATCH')
 return expected['body']
