"""Reconstructed357 restricted FRONT_REAR translated sidecar validator.
Only call after trusted source-registry trace resolution/replay. Self-asserted
trace digests do not authorize a candidate. Scope excludes functional admission.
"""
from fractions import Fraction as F
import sys,json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'planha_general150_runtime_work';sys.path.insert(0,str(ROOT))
from contract114 import digest
from frame_audit125 import equal,rectangle
from frame_circulation125 import same_union
from geometry114 import cells
PINS={'bed1':'c876cb026c2f227a10ed6a36ba6e49f0dc9c92fcf2c7ab300d42236ed2bf3fc1','bed2':'82e66b18d79b2b5ad3eb8aebff1ac3625ee4ac11279d44cec8950b712df901f8','bed3':'82e66b18d79b2b5ad3eb8aebff1ac3625ee4ac11279d44cec8950b712df901f8'}
BEDS={'bed1':['12.8','.15','16.4','5.6'],'bed2':['.15','.15','5.6','4.65'],'bed3':['6.9','.15','12.35','4.65']}
HALL={'bottom':['5.6','0','6.9','.15'],'stem_left':['5.6','4.65','5.75','6.9'],'stem_right':['6.75','4.65','6.9','5.75'],'cap_lower':['6.75','5.6','12.8','5.75'],'cap_upper_left':['5.6','6.75','7.85','6.9'],'cap_upper_right':['8.85','6.75','16.7','6.9'],'cap_end':['16.55','5.6','16.7','6.9']}
def translated(rect,origin,uid,length):
 a,b,c,d=map(F,rect);x,y=map(F,origin);r=[x+a,y+b,x+c,y+d]
 if uid=='B':r=[r[0],F(length)-r[3],r[2],F(length)-r[1]]
 elif uid!='A':raise ValueError('UNIT_ID')
 return r

def verify(model,trace):
 errors=[]
 try:
  if trace['schema']!='TRANSLATED_PRIVATE357_SOURCE_TRACE_V1':raise ValueError('TRACE_SCHEMA')
  if digest(model)!=trace['model_digest']:raise ValueError('MODEL_TRACE_BINDING')
  manifest=json.loads(Path(__file__).with_name('source_manifest.json').read_text())
  for name,sha in manifest.items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_DRIFT:'+name)
  if trace['source_manifest_digest']!=digest(manifest):raise ValueError('SOURCE_MANIFEST_BINDING')
  from packing_validator import verify as verify_packing
  if verify_packing(trace['raw'],trace['proposal'])['errors']:raise ValueError('PACKING_SOURCE_CLOSURE')
  from constructor129 import frame
  core,_=frame(trace['raw'],'FRONT_REAR');p=trace['proposal'];origin=p['ordered_macro']['origin'];L=F(model['inputs'][1])
  if p['sleep_roles']!=['double','twin','twin']or p['bedrooms']!=3:raise ValueError('PROGRAM')
  if not equal(model['inputs'],[trace['raw']['W'],trace['raw']['L'],trace['raw']['n']]):raise ValueError('INPUTS')
  if model['ordered_macro']!=p['ordered_macro']:raise ValueError('MACRO')
  if p['ordered_macro']['kind']!='SIDECAR_T136':raise ValueError('PRIMITIVE_KIND')
  if F(p['ordered_macro']['private_interface_center_x'])!=F(origin[0])+F('8.35'):raise ValueError('ROOT_TRANSLATION')
  for bed,r in BEDS.items():
   expected=translated(r,origin,'A',L)
   if not equal(expected,p['rectangles'][bed])or not equal(expected,p['ordered_macro']['rectangles'][bed]):raise ValueError('RIGID_SOURCE_PRIMITIVE')
  units={u['id']:u for u in model['units']}
  if len(model['units'])!=2 or set(units)!={'A','B'}:raise ValueError('UNIT_INVENTORY')
  for uid,u in units.items():
   if not equal(u['ownership'],core.get('unit_ownership',{}).get(uid,[core['units'][uid]])):raise ValueError('OWNERSHIP')
   for bed,pin in PINS.items():
    ps=[v for v in model['module_placements']if v['unit_id']==uid and v['room_id']==bed]
    if len(ps)!=1:raise ValueError('MODULE_INVENTORY')
    v=ps[0];source=v['module']
    if digest(source)!=pin or v['module_hash']!=pin:raise ValueError('SOURCE_ASSET')
    a,b,c,d=translated(BEDS[bed],origin,'A',L);A={'bed1':[[0,1],[-1,0]],'bed2':[[-1,0],[0,1]],'bed3':[[1,0],[0,1]]}[bed];shift={'bed1':[a,d],'bed2':[c,b],'bed3':[a,b]}[bed]
    if uid=='B':A=[A[0],[-x for x in A[1]]];shift=[shift[0],L-shift[1]]
    T={'matrix':A,'translation':shift}
    if not equal(T,v['transform']):raise ValueError('EXACT_RIGID_PLACEMENT')
    if not same_union(u['rooms'][bed],[rectangle(r,T)for r in source['unit']['rooms']['bed1']]):raise ValueError('SOURCE_ROOM')
    for k,r in source['walls'].items():
     if not equal(model['walls'].get(v['id_map'][k]),rectangle(r,T)):raise ValueError('MODULE_WALL')
   for k,r in HALL.items():
    for fld in('walls','wall_hosts','source_wall_hosts'):
     if not equal(model[fld].get(uid+'.private_sidecar.'+k),translated(r,origin,uid,L)):raise ValueError('HALL_WALL')
   ds=[d for d in model['private_domains']if d['unit']==uid]
   if len(ds)!=1:raise ValueError('DOMAIN_INVENTORY')
   d=ds[0];gross=[translated(r,origin,uid,L)for r in(['5.75','.15','6.75','6.75'],['5.75','5.75','16.55','6.75'])]
   if not same_union(cells(gross,list(model['walls'].values())),d['parts'])or not same_union(u['rooms']['private_circulation'],d['parts']):raise ValueError('HALL_FLOOR')
   if not equal(d['public_interface']['rect'],translated(['7.85','6.4','8.85','7.1'],origin,uid,L))or d['public_interface']['open_side']!=('top'if uid=='A'else'bottom'):raise ValueError('ACTUAL_INTERFACE')
 except(KeyError,TypeError,ValueError,IndexError)as e:errors.append(str(e))
 return {'status':'FAIL_BINDING'if errors else'PASS_TRANSLATED_SOURCE_SCOPE_ONLY','errors':errors,'accepted':False,'scope':'SOURCE_PRIMITIVE_TRANSLATION_REFLECTION_HALL_ONLY_NOT_NETWORK_OR_FUNCTIONAL_ELIGIBILITY','reconstruction':'NEW357_NOT_RECOVERED354_BYTES'}
