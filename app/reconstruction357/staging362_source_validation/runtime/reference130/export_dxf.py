"""Stdlib DXF, exact same window sidecar as SVG; no new runtime dependency."""
from fractions import Fraction as F
import json
names={"bedroom":"اتاق خواب","bathroom":"حمام و سرویس","internal_corridor":"راهرو","public_kitchen":"نشیمن و آشپزخانه"}
def unicode_dxf(s):return "".join(c if ord(c)<130 else "\\U+%04X"%ord(c)for c in s)
def encode(c,source_revision):
 from .render import admitted
 import copy
 original,g=admitted(c);candidate=copy.deepcopy(original)
 cv=lambda r:[float(F(str(v)))for v in r]
 candidate['inputs']=cv(candidate['inputs'])
 candidate['walls']={k:cv(v)for k,v in candidate['walls'].items()}
 candidate['common_spaces']={k:[cv(r)for r in v]if isinstance(v[0],list)else cv(v)for k,v in candidate['common_spaces'].items()}
 for o in candidate['openings']:o['rect']=cv(o['rect'])
 for w in candidate['concept_windows']:w['plan_rect']=cv(w['plan_rect'])
 """Deterministic serialization; caller must have validated this same model."""
 out=[];handle=256
 def entity(kind,layer):
  nonlocal handle
  handle+=1
  for k,v in [(0,kind),(5,format(handle,'X')),(330,'10'),(100,'AcDbEntity'),(8,layer)]:pair(k,v)
 def pair(k,v):out.extend((str(k),str(v)))
 def number(v):return format(float(F(v)),'.12g')
 def rect(r,layer):
  x,y,X,Y=r
  for a,b in [((x,y),(X,y)),((X,y),(X,Y)),((X,Y),(x,Y)),((x,Y),(x,y))]:
   entity('LINE',layer)
   for k,v in [(100,'AcDbLine'),(10,number(a[0])),(20,number(a[1])),(30,0),(11,number(b[0])),(21,number(b[1])),(31,0)]:pair(k,v)
 pair(999,'SCHEMATIC ONLY; METRES; DECIMAL DISPLAY PRECISION 12 SIGNIFICANT DIGITS; FIXED FURNITURE; SITE DETAILS SEPARATE');pair(0,'SECTION');pair(2,'HEADER');pair(9,'$ACADVER');pair(1,'AC1015');pair(9,'$INSUNITS');pair(70,6);pair(9,'$MEASUREMENT');pair(70,1);pair(0,'ENDSEC')
 pair(0,'SECTION');pair(2,'TABLES');pair(0,'TABLE');pair(2,'LAYER');pair(5,'8');pair(100,'AcDbSymbolTable');layers=['LOT','CORE','ROOMS','WALLS','DOORS','WINDOWS_ELEVATED','SPACE_NAMES','NOTES'];pair(70,len(layers))
 for i,layer in enumerate(layers):
  for k,v in [(0,'LAYER'),(5,format(32+i,'X')),(330,'8'),(100,'AcDbSymbolTableRecord'),(100,'AcDbLayerTableRecord'),(2,layer),(70,0),(62,7),(6,'CONTINUOUS')]:pair(k,v)
 pair(0,'ENDTAB')
 pair(0,'TABLE');pair(2,'BLOCK_RECORD');pair(5,'9');pair(100,'AcDbSymbolTable');pair(70,2)
 for name,h in [('*Model_Space','10'),('*Paper_Space','11')]:
  for k,v in [(0,'BLOCK_RECORD'),(5,h),(330,'9'),(100,'AcDbSymbolTableRecord'),(100,'AcDbBlockTableRecord'),(2,name)]:pair(k,v)
 pair(0,'ENDTAB');pair(0,'TABLE');pair(2,'APPID');pair(5,'A');pair(100,'AcDbSymbolTable');pair(70,1);pair(0,'APPID');pair(5,'F0');pair(330,'A');pair(100,'AcDbSymbolTableRecord');pair(100,'AcDbRegAppTableRecord');pair(2,'PLANHA130');pair(70,0);pair(0,'ENDTAB');pair(0,'ENDSEC');pair(0,'SECTION');pair(2,'BLOCKS')
 for name,h in [('*Model_Space','10'),('*Paper_Space','11')]:
  for k,v in [(0,'BLOCK'),(5,'A'+h),(330,h),(100,'AcDbEntity'),(8,'0'),(100,'AcDbBlockBegin'),(2,name),(70,0),(10,0),(20,0),(30,0),(3,name),(1,''),(0,'ENDBLK'),(5,'B'+h),(330,h),(100,'AcDbEntity'),(8,'0'),(100,'AcDbBlockEnd')]:pair(k,v)
 pair(0,'ENDSEC');pair(0,'SECTION');pair(2,'ENTITIES')
 rect([0,0,*candidate['inputs'][:2]],'LOT')
 # Display-only wall faces: cut actual apertures and elevated window symbols.
 # Source floor walls remain in the model; this is not a walk-through opening claim.
 def sub(r,b):
  x,y,X,Y=map(F,map(str,r));a,b0,A,B=map(F,map(str,b));a=max(x,a);b0=max(y,b0);A=min(X,A);B=min(Y,B)
  if a>=A or b0>=B:return [[x,y,X,Y]]
  return [q for q in [[x,y,a,Y],[A,y,X,Y],[a,y,A,b0],[a,B,A,Y]]if q[0]<q[2]and q[1]<q[3]]
 masks=[o['rect']for o in candidate['openings']]+[w['plan_rect']for w in candidate['concept_windows']]
 for r in candidate['walls'].values():
  pieces=[r]
  for mask in masks:pieces=[v for q in pieces for v in sub(q,mask)]
  for q in pieces:rect(q,'WALLS')
 for key,rs in candidate['common_spaces'].items():
  for r in (rs if isinstance(rs[0],list)else[rs]):rect(r,'CORE')
 for op in original.get('operations',{}).get('doors',[]):
  rect(cv(op['closed_panel']),'DOORS')
 # Visible names share the SVG's coordinates, including its responsive header offset.
 from .render import encode as svg
 from xml.etree import ElementTree as ET
 root=ET.fromstring(svg(c,source_revision));scale=float(root.attrib['data-scale']);offset_x=float(root.attrib['data-offset-x']);offset_y=float(root.attrib['data-offset-y'])
 for t in root.iter('{http://www.w3.org/2000/svg}text'):
  px,py=float(t.attrib['x']),float(t.attrib['y'])
  if not offset_y<=py<=offset_y+scale*candidate['inputs'][1]:continue
  entity('TEXT','SPACE_NAMES')
  for k,v in [(100,'AcDbText'),(10,number((px-offset_x)/scale)),(20,number(candidate['inputs'][1]-(py-offset_y)/scale)),(30,0),(40,float(t.attrib['font-size'])/scale),(1,unicode_dxf(t.text or ''))]:pair(k,v)
 for w in candidate['concept_windows']:
  x,y,X,Y=w['plan_rect'];entity('LWPOLYLINE','WINDOWS_ELEVATED')
  for k,v in [(100,'AcDbPolyline'),(90,4),(70,1),(38,number(w['sill_m']))]:pair(k,v)
  for a,b in [(x,y),(X,y),(X,Y),(x,Y)]:pair(10,number(a));pair(20,number(b))
  for k,v in [(1001,'PLANHA130'),(1000,w['id']),(1000,w.get('host_wall_id',w.get('hostwall_id','UNSPECIFIED'))),(1040,number(w['sill_m'])),(1040,number(w['head_m'])),(1070,0)]:pair(k,v)
 entity('TEXT','NOTES')
 for k,v in [(100,'AcDbText'),(10,0),(20,-1),(30,0),(40,.25),(1,'GENERAL130 LIMITED DRAFT; NOT ACCEPTED; SEE PROGRAM/SEARCH/GATE EVIDENCE; LIGHT/VENTILATION EXCLUDED FROM MVP ASSESSMENT; NOT TECHNICAL APPROVAL')]:pair(k,v)
 pair(999,'MODEL_SHA256 '+g['model_hash']);pair(999,'CHECKER_VERSION '+g['checker_version']);pair(999,'SOURCE_REVISION '+source_revision);pair(999,'GATE_STATUS '+g['status']);pair(999,'CONCEPT_DRAFT_ONLY_NOT_EXECUTION_OR_TECHNICAL_APPROVAL');pair(999,'UNVERIFIED_LIMITATIONS '+unicode_dxf(json.dumps({'out_of_scope':g.get('out_of_scope',[]),'not_evaluated':g.get('not_evaluated',[]),'limitations':g.get('limitations',[])},ensure_ascii=False)))
 pair(999,'CIRCULATION_COMPARISON_IS_REVIEW_PREFERENCE_NOT_GLOBAL_OPTIMALITY; SEE_SAME_MODEL_SOURCE_BOUND_REPORT_FOR_TRADEOFFS')
 pair(0,'ENDSEC');pair(0,'EOF')
 return ('\r\n'.join(out)+'\r\n').encode('ascii')
