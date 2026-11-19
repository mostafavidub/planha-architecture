"""Nonproduct synthetic preview; no historical gate, SVG metadata or endpoint.
XML parity is coordinate/data evidence. Browser measurements are not pixel review.
"""
import hashlib,pathlib
from fractions import Fraction as F
from xml.etree import ElementTree as ET
from dxf_codec_study307 import validate,rect,num,digest,subtract,require,AUTH
ROOT=pathlib.Path(__file__).resolve().parents[2]
PINS={'app/reconstruction357/planha_general150_runtime_work/reference150/render.py':'f9681119e31394825f8b2b410a1fb893f34a59d3',
 'studies/r4/dxf_codec_study307.py':'5b922b484b27f3792748b2a4bf5faaa7e221112f'}
NS='http://www.w3.org/2000/svg'
S=F(40);PAD=F(20)
def guard():
 out={}
 for path,pin in PINS.items():
  b=(ROOT/path).read_bytes()
  require(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin,'PREVIEW_SOURCE_CHANGED')
  out[path]=hashlib.sha256(b).hexdigest()
 return out
def decimal(v):
 # Exact finite decimal only, deliberately no implicit coordinate rounding.
 v=F(v);d=v.denominator
 while d%2==0:d//=2
 while d%5==0:d//=5
 require(d==1,'NON_TERMINATING_COORDINATE')
 from decimal import Decimal,localcontext
 with localcontext()as ctx:
  ctx.prec=160
  return format(Decimal(v.numerator)/Decimal(v.denominator),'f')
def screen_rect(q,L):
 x,y,X,Y=q
 return tuple(map(decimal,(PAD+x*S,PAD+(L-Y)*S,(X-x)*S,(Y-y)*S)))
def expected(s):
 validate(s);W,L=map(num,s['lot']);rows={}
 def add(id,kind,source,q):
  rows[id]={'kind':kind,'source':source,'q':tuple(q)}
 add('lot','lot','lot',(F(0),F(0),W,L))
 for r in s['rooms']:add('room_'+r['id'],'room',r['id'],rect(r['rect']))
 for w in s['walls']:
  pieces=[rect(w['rect'])]
  for o in s['openings']:
   if o['host']==w['id']:pieces=[p for q in pieces for p in subtract(q,rect(o['rect']))]
  for i,q in enumerate(pieces):add('wall_'+w['id']+'_'+str(i),'wall',w['id'],q)
 for o in s['openings']:add('opening_'+o['id'],'opening',o['id'],rect(o['rect']))
 return rows
def encode(s):
 pin=guard();h=digest(s);rows=expected(s);W,L=map(num,s['lot'])
 ET.register_namespace('',NS)
 root=ET.Element('{'+NS+'}svg',{'width':decimal(W*S+2*PAD),'height':decimal(L*S+2*PAD),
  'viewBox':'0 0 '+decimal(W*S+2*PAD)+' '+decimal(L*S+2*PAD),
  'style':'max-width:100%;height:auto;background:white','data-study':'SYNTHETIC_PREVIEW306_V1',
  'data-fixture-digest':h,'data-scale':decimal(S),'data-offset':decimal(PAD),'data-length':decimal(L),
  'role':'img','aria-label':'Synthetic codec diagnostic, not a qualified plan'})
 for id,row in rows.items():
  x,y,w,hgt=screen_rect(row['q'],L)
  ET.SubElement(root,'{'+NS+'}rect',{'id':id,'data-kind':row['kind'],'data-source-id':row['source'],
   'x':x,'y':y,'width':w,'height':hgt,'fill':'#333333'if row['kind']=='wall'else'none',
   'stroke':'#444444','stroke-width':'1'})
 for r in s['rooms']:
  x,y,X,Y=rect(r['rect'])
  e=ET.SubElement(root,'{'+NS+'}text',{'id':'label_'+r['id'],'data-kind':'label','data-source-id':r['id'],
   'x':decimal(PAD+(x+X)/2*S),'y':decimal(PAD+(L-(y+Y)/2)*S),
   'font-family':'sans-serif','font-size':'16','direction':'rtl','unicode-bidi':'plaintext',
   'text-anchor':'middle','dominant-baseline':'middle','fill':'#000000'})
  e.text=r['name']
 data=ET.tostring(root,encoding='utf-8')
 require(guard()==pin and digest(s)==h,'PREVIEW_SOURCE_CHANGED')
 return data
def inspect(s,data):
 pin=guard();h=digest(s);validate(s);require(type(data)is bytes,'SVG_BYTES')
 root=ET.fromstring(data);W,L=map(num,s['lot']);rows=expected(s)
 require(root.tag=='{'+NS+'}svg','SVG_ROOT')
 require(root.attrib.get('data-study')=='SYNTHETIC_PREVIEW306_V1'and root.attrib.get('data-fixture-digest')==h,'SVG_FIXTURE_BINDING')
 require(root.attrib.get('data-scale')==decimal(S)and root.attrib.get('data-offset')==decimal(PAD)and root.attrib.get('data-length')==decimal(L),'SVG_FRAME')
 require(root.attrib.get('viewBox')=='0 0 '+decimal(W*S+2*PAD)+' '+decimal(L*S+2*PAD),'SVG_VIEWBOX')
 require(root.attrib.get('width')==decimal(W*S+2*PAD)and root.attrib.get('height')==decimal(L*S+2*PAD),'SVG_SIZE')
 allowed_root={'width','height','viewBox','style','data-study','data-fixture-digest','data-scale','data-offset','data-length','role','aria-label'}
 require(set(root.attrib)==allowed_root and root.attrib['style']=='max-width:100%;height:auto;background:white','SVG_ROOT_ATTRIBUTES')
 observed={};labels={}
 for e in root:
  require(len(e)==0 and e.tag in ('{'+NS+'}rect','{'+NS+'}text'),'SVG_ELEMENT')
  id=e.attrib.get('id');require(type(id)is str and id not in observed and id not in labels,'SVG_ID')
  if e.tag.endswith('rect'):
   require(set(e.attrib)=={'id','data-kind','data-source-id','x','y','width','height','fill','stroke','stroke-width'},'SVG_RECT_ATTRIBUTES')
   require(id in rows,'SVG_EXTRA_OBJECT');row=rows[id]
   require(e.attrib['data-kind']==row['kind'] and e.attrib['data-source-id']==row['source'],'SVG_SOURCE_ID')
   # Invert SVG coordinates independently; no forward-screen equality shortcut.
   px,py,w,hgt=[F(e.attrib[k])for k in ('x','y','width','height')]
   q=((px-PAD)/S,L-(py-PAD+hgt)/S,(px-PAD+w)/S,L-(py-PAD)/S)
   require(q==row['q'],'SVG_GEOMETRY')
   require(e.attrib['fill']==('#333333'if row['kind']=='wall'else'none') and e.attrib['stroke']=='#444444' and e.attrib['stroke-width']=='1','SVG_STYLE')
   observed[id]=q
  else:
   require(set(e.attrib)=={'id','data-kind','data-source-id','x','y','font-family','font-size','direction','unicode-bidi','text-anchor','dominant-baseline','fill'},'SVG_TEXT_ATTRIBUTES')
   rid=e.attrib['data-source-id'];r=next((r for r in s['rooms']if r['id']==rid),None)
   require(r is not None and id=='label_'+rid and e.attrib['data-kind']=='label','SVG_LABEL_ID')
   q=rect(r['rect']);point=((F(e.attrib['x'])-PAD)/S,L-(F(e.attrib['y'])-PAD)/S)
   require(point==((q[0]+q[2])/2,(q[1]+q[3])/2) and e.text==r['name'],'SVG_LABEL_PARITY')
   require({k:e.attrib[k]for k in ('font-family','font-size','direction','unicode-bidi','text-anchor','dominant-baseline','fill')}=={'font-family':'sans-serif','font-size':'16','direction':'rtl','unicode-bidi':'plaintext','text-anchor':'middle','dominant-baseline':'middle','fill':'#000000'},'SVG_TEXT_STYLE')
   labels[id]=point
 require(set(observed)==set(rows) and len(labels)==len(s['rooms']),'SVG_MISSING_OBJECT')
 require(pin==guard() and h==digest(s),'PREVIEW_SOURCE_CHANGED')
 return {'schema':'SYNTHETIC_PREVIEW306_PARITY','state':'XML_EXACT_SYNTHETIC_PARITY_ONLY',
  'fixture_digest':h,'svg_sha256':hashlib.sha256(data).hexdigest(),'rectangle_count':len(observed),
  'label_count':len(labels),'product_snapshot_bound':False,'visual_reviewed':False,
  'source_snapshot':pin,**AUTH}
# Executes in a browser after fonts.ready. Uses rendered glyph bounding boxes,
# not character-count estimates; only this font/rendering/viewport is observed.
MEASURE_JS=r"""() => {
 const svg=document.querySelector('svg'), labels=[...svg.querySelectorAll('text')];
 const box=e=>{const b=e.getBBox();return {x:b.x,y:b.y,w:b.width,h:b.height};};
 const outside=(a,b)=>a.x<b.x||a.y<b.y||a.x+a.w>b.x+b.w||a.y+a.h>b.y+b.h;
 const rs=labels.map(e=>({id:e.id,b:box(e),room:box(document.getElementById('room_'+e.dataset.sourceId))}));
 const overflow=rs.filter(r=>outside(r.b,r.room)).map(r=>r.id),overlap=[];
 for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){
  const a=rs[i].b,b=rs[j].b;
  if(Math.min(a.x+a.w,b.x+b.w)>Math.max(a.x,b.x)&&Math.min(a.y+a.h,b.y+b.h)>Math.max(a.y,b.y))overlap.push([rs[i].id,rs[j].id]);
 }
 const v=svg.getBoundingClientRect(),pageFits=v.left>=0&&v.right<=innerWidth;
 return {state:overflow.length||overlap.length||!pageFits?'LAYOUT_DEFECT_OBSERVED':'NO_MEASURED_LABEL_DEFECT_IN_THIS_RENDER',
 overflow,overlap,pageFits,labelCount:rs.length,visual_reviewed:false,qualified:false,display_allowed:false,delivery_allowed:false};
}"""
