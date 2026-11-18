"""Independent file/model semantic audit; never authorizes a model or produces it.
Uses stdlib only. SVG/DXF bytes must be actual exported artifacts, not receipts.
"""
import json,hashlib,re,math
from fractions import Fraction
from collections import Counter
from xml.etree import ElementTree as ET

def audit_exports(model,svg_bytes,dxf_bytes,source_revision):
 errors=[];witness={};ns='{http://www.w3.org/2000/svg}'
 def fail(code):errors.append(code)
 def f(x):return float(Fraction(str(x)))
 def point(x):return tuple(round(f(v),9)for v in x)
 def rectangle_lines(q):
  x,y,X,Y=map(f,q);return [(point(a),point(b))for a,b in [((x,y),(X,y)),((X,y),(X,Y)),((X,Y),(x,Y)),((x,Y),(x,y))]]
 def key(a,b):return tuple(sorted((a,b)))
 try:
  root=ET.fromstring(svg_bytes);md=json.loads(root.find(ns+'metadata').text)
  if md['model']!=model:fail('SVG_MODEL_MISMATCH')
  if md['source_revision']!=source_revision:fail('SVG_REVISION_MISMATCH')
  S=f(root.attrib['data-scale']);X=f(root.attrib['data-offset-x']);Y=f(root.attrib['data-offset-y']);L=f(root.attrib['data-length'])
  if not math.isclose(L,f(model['inputs'][1]),abs_tol=1e-9):fail('SVG_LENGTH_TRANSFORM')
  lines=dxf_bytes.decode('ascii').splitlines()
  if len(lines)%2:raise ValueError('DXF_ODD_CODE_LINES')
  pairs=[(int(lines[i]),lines[i+1])for i in range(0,len(lines),2)]
  comments=[v for k,v in pairs if k==999]
  if 'SOURCE_REVISION '+source_revision not in comments:fail('DXF_REVISION_MISMATCH')
  # Parse only ENTITIES, never accept layer-table entries as physical entities.
  entities=[];active=False;current=None
  for idx,(code,value)in enumerate(pairs):
   if code==2 and value=='ENTITIES' and idx and pairs[idx-1]==(0,'SECTION'):active=True;continue
   if not active:continue
   if code==0:
    if current is not None:entities.append(current)
    current=None
    if value=='ENDSEC':break
    current=[(code,value)]
   elif current is not None:current.append((code,value))
  def one(e,k,default=None):return next((v for c,v in e if c==k),default)
  def decode(s):return re.sub(r'\\U\+([0-9A-Fa-f]{4})',lambda m:chr(int(m[1],16)),s)
  actual_names=Counter((decode(one(e,1,'')),point([one(e,10),one(e,20)]))for e in entities if one(e,0)=='TEXT'and one(e,8)=='SPACE_NAMES')
  wanted_names=Counter()
  for t in root.iter(ns+'text'):
   px,py=f(t.attrib['x']),f(t.attrib['y'])
   if Y<=py<=Y+S*L:wanted_names[(t.text or '',point([(px-X)/S,L-(py-Y)/S]))]+=1
  if not wanted_names or actual_names!=wanted_names:fail('SPACE_NAMES_TEXT_OR_COORDINATE_MISMATCH')
  witness['matching_space_names']=sum(actual_names.values())
  # Names and anchors must also be derived from the source model independently.
  # Equal corruption of both files must not pass by mutual agreement.
  role_names={'living':'پذیرایی','dining':'غذاخوری','kitchen':'آشپزخانه','bath':'حمام و سرویس','bathroom':'حمام و سرویس','entry_circulation':'گردش داخلی','private_corridor':'راهروی خصوصی','private_circulation':'راهروی خصوصی'}
  model_names=Counter()
  def model_label(name,parts):
   if not parts:return
   qs=[tuple(Fraction(str(v))for v in q)for q in parts]
   q=max(qs,key=lambda q:(q[2]-q[0])*(q[3]-q[1]))
   model_names[(name,point([(q[0]+q[2])/2,(q[1]+q[3])/2]))]+=1
  for u in model['units']:
   for room,parts in u['rooms'].items():
    short=room.split('.')[-1]
    global_meta=model.get('room_metadata',{}).get(u['id']+'.'+room,{})
    name=u.get('room_metadata',{}).get(room,{}).get('name_fa')or global_meta.get('display_name_fa')or global_meta.get('name_fa')
    if not name:name=('خواب '+short[3:])if short.startswith('bed')else role_names.get(short,short)
    if short=='living':name+=' '+u['id']
    model_label(name,parts)
  for role,parts in model['common_spaces'].items():
   model_label({'stair':'راه‌پله','lift':'آسانسور','lobby':'لابی مشترک'}.get(role,role),parts if parts and isinstance(parts[0],list)else[parts])
  if wanted_names!=model_names:fail('SVG_SPACE_NAMES_OR_ANCHORS_NOT_MODEL_DERIVED')
  if actual_names!=model_names:fail('DXF_SPACE_NAMES_OR_ANCHORS_NOT_MODEL_DERIVED')
  witness['matching_model_derived_space_names']=sum(model_names.values())

  expected_doors=Counter(key(a,b)for o in model.get('operations',{}).get('doors',[])for a,b in rectangle_lines(o['closed_panel']))
  got_doors=Counter(key(point([one(e,10),one(e,20)]),point([one(e,11),one(e,21)]))for e in entities if one(e,0)=='LINE'and one(e,8)=='DOORS')
  if got_doors!=expected_doors:fail('REAL_DOOR_PANEL_MISMATCH')
  witness['matching_door_panels']=len(expected_doors)//4
  expected_windows=Counter()
  for w in model['concept_windows']:
   x,y,a,b=map(f,w['plan_rect']);expected_windows[(tuple(point(p)for p in[(x,y),(a,y),(a,b),(x,b)]),round(f(w['sill_m']),9))]+=1
  actual_windows=Counter()
  for e in entities:
   if one(e,0)!='LWPOLYLINE'or one(e,8)!='WINDOWS_ELEVATED':continue
   xs=[v for k,v in e if k==10];ys=[v for k,v in e if k==20]
   actual_windows[(tuple(point(p)for p in zip(xs,ys)),round(f(one(e,38)),9))]+=1
  if actual_windows!=expected_windows:fail('WINDOW_RECTANGLE_OR_HEIGHT_MISMATCH')
  witness['matching_windows']=sum(actual_windows.values())
  # SVG wall solids are uncut source rectangles; white aperture/window masks are separate.
  svg_walls=[]
  for r in root.iter(ns+'rect'):
   if r.attrib.get('fill')!='#333':continue
   x=(f(r.attrib['x'])-X)/S;y=L-(f(r.attrib['y'])-Y)/S;w=f(r.attrib['width'])/S;h=f(r.attrib['height'])/S
   svg_walls.append(point([x,y-h,x+w,y]))
  if Counter(svg_walls)!=Counter(point(q)for q in model['walls'].values()):fail('SVG_SOURCE_WALLS_MISMATCH')
  witness['matching_svg_source_walls']=len(svg_walls)
  # Reconstruct DXF wall-face rectangles from actual line entities, then compare
  # horizontal sweep intervals with union(source walls) minus real display masks.
  dl=[e for e in entities if one(e,0)=='LINE'and one(e,8)=='WALLS'];dr=[]
  if len(dl)%4:fail('DXF_WALL_LINE_GROUP_INCOMPLETE')
  for i in range(0,len(dl)-3,4):
   es=dl[i:i+4];pts=[point([one(e,10),one(e,20)])for e in es]+[point([one(e,11),one(e,21)])for e in es]
   a=min(p[0]for p in pts);b=min(p[1]for p in pts);A=max(p[0]for p in pts);B=max(p[1]for p in pts)
   want=Counter(key(x,y)for x,y in rectangle_lines([a,b,A,B]));got=Counter(key(point([one(e,10),one(e,20)]),point([one(e,11),one(e,21)]))for e in es)
   if a>=A or b>=B or want!=got:fail('DXF_NONRECTANGULAR_WALL_FACE')
   dr.append((a,b,A,B))
  masks=[point(o['rect'])for o in model['openings']]+[point(w['plan_rect'])for w in model['concept_windows']]
  sr=[point(q)for q in model['walls'].values()]
  def union_intervals(qs,y):
   pieces=sorted((a,A)for a,b,A,B in qs if b<y<B);merged=[]
   for a,A in pieces:
    if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(A,merged[-1][1]))
    else:merged.append((a,A))
   return merged
  ys=sorted({v for q in sr+masks+dr for v in(q[1],q[3])})
  for lo,hi in zip(ys,ys[1:]):
   y=(lo+hi)/2;expected=union_intervals(sr,y)
   for ma,mA in union_intervals(masks,y):
    updated=[]
    for a,A in expected:
     if mA<=a or ma>=A:updated.append((a,A))
     else:
      if a<ma:updated.append((a,ma))
      if mA<A:updated.append((mA,A))
    expected=updated
   if expected!=union_intervals(dr,y):fail('DXF_WALL_FACE_UNION_MISMATCH');break
  witness['wall_face_sweep_slabs']=max(0,len(ys)-1)

  if any(f(t.attrib['y'])-f(t.attrib['font-size'])<0 or f(t.attrib['y'])>f(root.attrib['height'])for t in root.iter(ns+'text')):fail('SVG_VERTICAL_TEXT_CLIPPING')
  witness['svg_sha256']=hashlib.sha256(svg_bytes).hexdigest();witness['dxf_sha256']=hashlib.sha256(dxf_bytes).hexdigest()
 except Exception as ex:fail('EXPORT_PARSE_OR_SCHEMA:'+type(ex).__name__+':'+str(ex))
 return {'status':'FAIL'if errors else'PASS_LIMITED','errors':errors,'witness':witness,'scope':'Actual serialized SVG model binding, source walls, Persian space names/coordinates, DXF real door panels and elevated windows; DXF display-wall face union; not architectural validity or browser download. Light/ventilation assessment is excluded from MVP by owner instruction.','accepted':False,'eligible_for_draft_export':False}
