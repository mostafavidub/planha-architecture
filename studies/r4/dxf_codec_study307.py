"""Synthetic-only DXF codec study. Not a product exporter or admission issuer.
Historical serialization/subtraction is a read-only reference, never imported.
No model artifacts, SVG, runtime gate or server endpoint are consumed.
"""
from fractions import Fraction as F
import hashlib,io,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[2]
SOURCE='app/reconstruction357/planha_general150_runtime_work/reference150/export_dxf.py'
SOURCE_BLOB='711d37ae49c9649d381fa22f1990ee12b1598a27'
AUTH={k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')}
def require(ok,code):
 if not ok:raise ValueError(code)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()).hexdigest()
def source_guard():
 b=(ROOT/SOURCE).read_bytes()
 require(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==SOURCE_BLOB,'SOURCE_CHANGED')
 return hashlib.sha256(b).hexdigest()
def num(v):
 require(type(v)is str and re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?',v)is not None,'DECIMAL_STRING_REQUIRED')
 require(len(v)<=64,'NUMERIC_LIMIT');return F(v)
def rect(v):
 require(type(v)is list and len(v)==4,'RECT_SHAPE')
 q=tuple(map(num,v));require(q[0]<q[2] and q[1]<q[3],'RECT_POSITIVE');return q
def ident(v):require(type(v)is str and '__'not in v and re.fullmatch('[A-Za-z][A-Za-z0-9_]{0,31}',v)is not None,'ID_REQUIRED')
def validate(s):
 require(type(s)is dict and set(s)=={'schema','units','lot','walls','openings','rooms'},'FIXTURE_FIELDS')
 require(s['schema']=='SYNTHETIC_DXF_CODEC_V1' and s['units']=='m','FIXTURE_SCOPE')
 require(type(s['lot'])is list and len(s['lot'])==2,'LOT')
 W,L=map(num,s['lot']);require(5<=W<=25 and 5<=L<=25,'LOT_DOMAIN')
 for name in ('walls','openings','rooms'):
  require(type(s[name])is list and len(s[name])>0,'INVENTORY_REQUIRED')
  seen=set()
  for row in s[name]:
   required={'id','rect'}|({'host'}if name=='openings' else {'name'}if name=='rooms' else set())
   require(type(row)is dict and set(row)==required,'ROW_FIELDS')
   ident(row['id']);require(row['id']not in seen,'DUPLICATE_ID');seen.add(row['id'])
   x,y,X,Y=rect(row['rect']);require(0<=x<X<=W and 0<=y<Y<=L,'RECT_OUTSIDE_LOT')
   if name=='rooms':require(type(row['name'])is str and bool(row['name']) and len(row['name'])<=80 and all(ord(c)>=32 and ord(c)<65536 and not 0xD800<=ord(c)<=0xDFFF for c in row['name']),'NAME_REQUIRED')
 walls={w['id']:rect(w['rect'])for w in s['walls']}
 for o in s['openings']:
  require(type(o['host'])is str and o['host']in walls,'OPENING_HOST')
  a=rect(o['rect']);b=walls[o['host']]
  require(b[0]<=a[0]<a[2]<=b[2] and b[1]<=a[1]<a[3]<=b[3],'OPENING_HOST_CONTAINMENT')
 return s
def subtract(r,b):
 x,y,X,Y=r;a,c,A,C=b;a=max(x,a);c=max(y,c);A=min(X,A);C=min(Y,C)
 if a>=A or c>=C:return [r]
 return [q for q in [(x,y,a,Y),(A,y,X,Y),(a,y,A,c),(a,C,A,Y)]if q[0]<q[2]and q[1]<q[3]]
def number(v):return format(float(v),'.12g')
def ascii_text(s):return ''.join(c if ord(c)<128 else '\\U+%04X'%ord(c) for c in s)
def encode(s):
 before=digest(s);pin=source_guard();validate(s);out=[];entities=[];layers={'LOT','NOTES'}
 def add(kind,layer,data):
  layers.add(layer);entities.append((kind,layer,data))
 def outline(q,layer):
  x,y,X,Y=q
  for a,b in [((x,y),(X,y)),((X,y),(X,Y)),((X,Y),(x,Y)),((x,Y),(x,y))]:
   add('LINE',layer,[(100,'AcDbLine'),(10,number(a[0])),(20,number(a[1])),(30,0),(11,number(b[0])),(21,number(b[1])),(31,0)])
 W,L=map(num,s['lot']);outline((F(0),F(0),W,L),'LOT')
 for w in s['walls']:
  pieces=[rect(w['rect'])]
  for o in s['openings']:
   if o['host']==w['id']:pieces=[p for q in pieces for p in subtract(q,rect(o['rect']))]
  for i,q in enumerate(pieces):outline(q,'W__'+w['id']+'__'+str(i))
 for o in s['openings']:outline(rect(o['rect']),'O__'+o['id'])
 for r in s['rooms']:
  q=rect(r['rect']);outline(q,'R__'+r['id'])
  add('TEXT','N__'+r['id'],[(100,'AcDbText'),(10,number((q[0]+q[2])/2)),(20,number((q[1]+q[3])/2)),(30,0),(40,'0.25'),(1,ascii_text(r['name']))])
 def pair(k,v):out.extend((str(k),str(v)))
 for k,v in [(0,'SECTION'),(2,'HEADER'),(9,'$ACADVER'),(1,'AC1015'),(9,'$INSUNITS'),(70,6),(9,'$MEASUREMENT'),(70,1),(0,'ENDSEC'),(0,'SECTION'),(2,'TABLES'),(0,'TABLE'),(2,'LAYER'),(5,'8'),(100,'AcDbSymbolTable'),(70,len(layers))]:pair(k,v)
 for i,name in enumerate(sorted(layers)):
  for k,v in [(0,'LAYER'),(5,format(32+i,'X')),(330,'8'),(100,'AcDbSymbolTableRecord'),(100,'AcDbLayerTableRecord'),(2,name),(70,0),(62,7),(6,'CONTINUOUS')]:pair(k,v)
 for k,v in [(0,'ENDTAB'),(0,'ENDSEC'),(0,'SECTION'),(2,'ENTITIES')]:pair(k,v)
 for i,(kind,layer,data)in enumerate(entities):
  for k,v in [(0,kind),(5,format(max(256,32+len(layers))+i,'X')),(100,'AcDbEntity'),(8,layer)]+data:pair(k,v)
 for k,v in [(999,'SYNTHETIC_CODEC_STUDY_NO_AUTHORITY'),(999,'FIXTURE_SHA256 '+before),(0,'ENDSEC'),(0,'EOF')]:pair(k,v)
 data=('\r\n'.join(out)+'\r\n').encode('ascii')
 require(digest(s)==before and source_guard()==pin,'SOURCE_OR_FIXTURE_CHANGED')
 return data
def observe(data):
 import ezdxf
 from ezdxf.lldxf.encoding import decode_dxf_unicode
 require(ezdxf.__version__=='1.4.3','READER_VERSION')
 require(type(data)is bytes,'BYTES_REQUIRED')
 doc=ezdxf.read(io.StringIO(data.decode('ascii'),newline=None))
 require(doc.dxfversion=='AC1015' and doc.header.get('$INSUNITS')==6 and doc.header.get('$MEASUREMENT')==1,'DXF_UNITS_OR_VERSION')
 lines={};names={};declared=set(x.dxf.name for x in doc.layers)
 for e in doc.modelspace():
  layer=e.dxf.layer;require(layer in declared,'UNDECLARED_LAYER')
  if e.dxftype()=='LINE':
   require(layer=='LOT' or re.fullmatch(r'(?:W__[A-Za-z][A-Za-z0-9_]*__[0-9]+|[OR]__[A-Za-z][A-Za-z0-9_]*)',layer)is not None,'UNKNOWN_LAYER')
   a,b=e.dxf.start,e.dxf.end;require(a.z==b.z==0,'NONPLANAR')
   lines.setdefault(layer,[]).append(((F(str(a.x)),F(str(a.y))),(F(str(b.x)),F(str(b.y)))))
  elif e.dxftype()=='TEXT':
   require(layer.startswith('N__') and layer not in names,'TEXT_LAYER')
   p=e.dxf.insert;require(p.z==0,'NONPLANAR')
   try:text=decode_dxf_unicode(e.plain_text())
   except ValueError:raise ValueError('DXF_TEXT_ENCODING') from None
   names[layer]=(text,(F(str(p.x)),F(str(p.y))))
  else:raise ValueError('UNSUPPORTED_ENTITY')
 boxes={}
 for layer,segs in lines.items():
  require(len(segs)==4,'RECT_EDGE_COUNT')
  points={p for ab in segs for p in ab};require(len(points)==4,'RECT_CORNERS')
  xs=sorted({p[0]for p in points});ys=sorted({p[1]for p in points});require(len(xs)==len(ys)==2,'RECT_AXES')
  expected={frozenset((a,b))for a,b in [((xs[0],ys[0]),(xs[1],ys[0])),((xs[1],ys[0]),(xs[1],ys[1])),((xs[1],ys[1]),(xs[0],ys[1])),((xs[0],ys[1]),(xs[0],ys[0]))]}
  require({frozenset(ab)for ab in segs}==expected,'RECT_CLOSED')
  boxes[layer]=(xs[0],ys[0],xs[1],ys[1])
 return boxes,names
def covered(p,q):return q[0]<p[0]<q[2] and q[1]<p[1]<q[3]
def parity(s,data):
 validate(s);pin=source_guard();before=digest(s);boxes,names=observe(data)
 W,L=map(num,s['lot']);require(boxes.pop('LOT',None)==(F(0),F(0),W,L),'LOT_PARITY')
 for prefix,rows in [('O__',s['openings']),('R__',s['rooms'])]:
  for row in rows:require(boxes.pop(prefix+row['id'],None)==rect(row['rect']),'OBJECT_PARITY')
 expectednames={}
 for row in s['rooms']:
  q=rect(row['rect']);expectednames['N__'+row['id']]=(row['name'],((q[0]+q[2])/2,(q[1]+q[3])/2))
 require(names==expectednames,'NAME_OR_LOCATION_PARITY')
 # Independent exact cell occupancy oracle, not encoder's subtraction algorithm.
 for w in s['walls']:
  prefix='W__'+w['id']+'__';keys=[k for k in boxes if k.startswith(prefix)];pieces=[boxes.pop(k)for k in keys]
  wall=rect(w['rect']);holes=[rect(o['rect'])for o in s['openings']if o['host']==w['id']]
  allrects=[wall]+holes+pieces;xs=sorted({x for q in allrects for x in (q[0],q[2])});ys=sorted({y for q in allrects for y in(q[1],q[3])})
  for x,X in zip(xs,xs[1:]):
   for y,Y in zip(ys,ys[1:]):
    p=((x+X)/2,(y+Y)/2);want=covered(p,wall) and not any(covered(p,h)for h in holes)
    count=sum(covered(p,q)for q in pieces)
    require(count==int(want),'WALL_MINUS_OPENING_PARITY')
 require(not boxes,'EXTRA_OBJECT')
 require(before==digest(s) and pin==source_guard(),'SOURCE_OR_FIXTURE_CHANGED')
 return {'state':'EXACT_SYNTHETIC_CODEC_PARITY_ONLY','fixture_digest':before,'file_sha256':hashlib.sha256(data).hexdigest(),'historical_source_sha256':pin,'reader':'ezdxf1.4.3','precision_policy':'FLOAT_TO_12_SIGNIFICANT_DIGITS_EXACT_PARITY_OR_REJECT','parity_scope':'MODELSPACE_RECTANGLES_NAMES_LOCATIONS_UNITS','not_checked':['text_height_style_rotation','visibility_layer_flags','paperspace','visual_readability','complete_DXF_audit'],'product_snapshot_bound':False,'visual_reviewed':False,**AUTH}
def precision_observation(value):
 v=num(value);serialized=number(v);error=abs(v-F(serialized))
 return {'serialized':serialized,'absolute_error_rational':str(error),'exact':error==0,'tolerance_assumed':False,**AUTH}
