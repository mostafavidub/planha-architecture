"""Independent H09/H10/H15 named geometry audits. No producer or checker imports.
Source: Blueprint full text lines 572/573/579, modified 2026-11-12.
H15 is conceptual only, never execution/regulatory or street-entry approval.
"""
from fractions import Fraction as F
import hashlib,json

SOURCE={'H09': {'source_line': 572, 'source_text': 'H09 WALL_NETWORK — شبکه دیوار یکتا، ضخامت\u200cدار و متصل با faces معلوم باشد. QA: اتصال T معتبر مثبت؛ دیوار با ضخامت صفر، دیوار مشترک دوبله یا شکاف ناخواسته منفی. نازک\u200cکاری ثبت\u200cنشده در مدل → INDETERMINATE با علت MISSING_EVIDENCE؛ سامانه/پروفایل لازمِ جداره و نازک\u200cکاریِ آماده\u200cنشده → INDETERMINATE با علت PROFILE_NOT_READY. مرجع:B2.', 'source_modified': '2026-11-12T19:13:23.746Z'}, 'H10': {'source_line': 573, 'source_text': 'H10 OPENING_HOST — میزبان، بازه روی دیوار، عرض و دو فضای مرتبط هر بازشو معلوم باشند. QA: در روی مرز صحیح مثبت؛ در در فضای خالی یا پنجره بی\u200cمیزبان منفی. میزبان نامعلوم → INDETERMINATE با علت MISSING_EVIDENCE؛ بی\u200cمیزبان\u200cبودنِ اثبات\u200cشده با میزبانِ هنوز ثبت\u200cنشده فرق دارد. مرجع:B2؛ ترمیم مستلزم کنترل دوباره روابط است.', 'source_modified': '2026-11-12T19:13:23.746Z'}, 'H15': {'source_line': 579, 'source_text': 'H15 CORE_2D — در MVP فقط جانمایی مفهومی یک هسته پله مشترک، آسانسور، لابی مستقل بیرون محفظه پله و دسترسی مستقل و پیوسته هر واحد در قاب طراحی کنترل می\u200cشود. حذف اجزای الزامی، تداخل قطعی یا عبور اجباری از محفظه پله ایراد مفهومی است. ظرفیت و مدل اجرایی، مقطع و سرگیر پله، نصب آسانسور، چاهک و بالاسری و تأیید ابعاد اجرایی POST_MVP / NOT_EVALUATED هستند و فقدان آنها به\u200cتنهایی گام دوم MVP را متوقف نمی\u200cکند. حضور شماتیک هیچ تأیید قانونی یا اجرایی ایجاد نمی\u200cکند.', 'source_modified': '2026-11-12T19:13:23.746Z'}, 'source_sha256': 'd9cf1ac027529a0c340d6ce4c8a3c8dee595202832dcddc6484480caf9584d9a'}

def q(r):
 r=tuple(F(str(v))for v in r)
 if len(r)!=4 or r[0]>=r[2]or r[1]>=r[3]:raise ValueError('NONPOSITIVE_RECTANGLE')
 return r

def hit(a,b):return max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])
def inside(a,b):return b[0]<=a[0]<=a[2]<=b[2]and b[1]<=a[1]<=a[3]<=b[3]
def covered(a,rs):
 xs=sorted({a[0],a[2]}|{v for b in rs for v in(b[0],b[2])if a[0]<v<a[2]});ys=sorted({a[1],a[3]}|{v for b in rs for v in(b[1],b[3])if a[1]<v<a[3]})
 return all(any(inside((x,y,X,Y),b)for b in rs)for x,X in zip(xs,xs[1:])for y,Y in zip(ys,ys[1:]))
def sweep(path,body):
 half=body/2
 if len(path)<2:raise ValueError('ROUTE_TOO_SHORT')
 for a,b in zip(path,path[1:]):
  x,y=map(F,a);X,Y=map(F,b)
  if x!=X and y!=Y:raise ValueError('NONORTHOGONAL_ROUTE')
  yield(min(x,X)-half,min(y,Y)-half,max(x,X)+half,max(y,Y)+half)
def output(rule,errors,pending,witness):
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','witness':{'rule':rule,'source':SOURCE.get(rule,{}),'source_document_sha256':SOURCE['source_sha256'],'errors':errors,'pending':pending,**witness},'scope':'Actual same-model exact 2D geometry for '+rule+'; no hardware, legal, daylight or architectural-quality approval.'}
def safe(fn):
 def run(m):
  try:return fn(m)
  except(KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as e:
   return output(fn.__name__,['NONPOSITIVE_RECTANGLE']if str(e)=='NONPOSITIVE_RECTANGLE'else[],[]if str(e)=='NONPOSITIVE_RECTANGLE'else['SCHEMA_OR_PROFILE_NOT_EVALUATED:'+str(e)],{})
 return run

@safe
def core_concept(m):
 errors=[];pending=[];common=m['common_spaces'];units=m['units'];body=F(str(m['profile']['body_m']));W,L=map(F,m['inputs'][:2]);frame=(F(0),F(0),W,L)
 if set(common)!={'stair','lift','lobby'}:return output('H15',['CORE_COMPONENT_INVENTORY'],[],{})
 stair=q(common['stair']);lift=q(common['lift']);lobby=[q(x)for x in common['lobby']];walls=[q(x)for x in m['walls'].values()];fx=[q(r)for u in units for r in u['fixtures'].values()]
 if hit(stair,lift)or any(hit(r,stair)or hit(r,lift)for r in lobby):errors.append('LOBBY_NOT_INDEPENDENT_FROM_CORE_ENCLOSURES')
 if not all(inside(r,frame)for r in [stair,lift]+lobby):errors.append('CORE_OUTSIDE_FRAME')
 required={a+'_'+u['id']for a in('stair','lift')for u in units}
 if set(m['common_routes'])!=required:errors.append('CORE_ROUTE_INVENTORY')
 rows=[]
 for u in units:
  entry=[q(r)for r in u['rooms'].get('entry_circulation',[])];public=entry+[q(r)for r in u['rooms'].get('living',[])];own=[q(r)for r in u['ownership']];others=[q(r)for v in units if v['id']!=u['id']for r in v['ownership']]
  openings=[q(o['rect'])for o in m['openings']if'lobby'in o['connects']and any(s.startswith(u['id']+'.')for s in o['connects'])]
  for src,region,forbidden in [('stair',stair,lift),('lift',lift,stair)]:
   name=src+'_'+u['id'];path=m['common_routes'].get(name,[])
   if not path:continue
   a=tuple(map(F,path[0]));b=tuple(map(F,path[-1]));h=body/2
   if not inside((a[0]-h,a[1]-h,a[0]+h,a[1]+h),region):errors.append(name+':START_NOT_IN_CORE')
   if not covered((b[0]-h,b[1]-h,b[0]+h,b[1]+h),entry):errors.append(name+':END_NOT_IN_ENTRY')
   used_lobby=False
   for rect in sweep(path,body):
    if not inside(rect,frame)or any(hit(rect,o)for o in walls+fx+others+[forbidden]):errors.append(name+':BODY_COLLISION_OR_OTHER_UNIT')
    if not covered(rect,[region]+lobby+public+openings+[q(o['rect'])for o in m['openings']if src in o['connects']and'lobby'in o['connects']]):errors.append(name+':OUTSIDE_DECLARED_COMMON_AND_ENTRY_FLOOR')
    used_lobby=used_lobby or any(hit(rect,r)for r in lobby)
   if not used_lobby:errors.append(name+':NO_LOBBY_TRAVERSAL')
   rows.append({'route':name,'segments':len(path)-1,'source':src,'destination':u['id']})
 return output('H15',sorted(set(errors)),pending,{'routes':rows,'body_m':str(body),'hardware_and_external_entry':'NOT_EVALUATED_OUTSIDE_CONCEPT'})

@safe
def opening_hosts(m):
 errors=[];pending=[];walls={k:q(v)for k,v in m['walls'].items()};hosts={k:q(v)for k,v in m['wall_hosts'].items()};body=F(str(m['profile']['body_m']));h=body/2;regions={}
 for key,value in m['common_spaces'].items():regions[key]=[q(r)for r in value]if isinstance(value[0],list)else[q(value)]
 for u in m['units']:
  for name,parts in u['rooms'].items():regions[u['id']+'.'+name]=[q(r)for r in parts]
 for key,role in m.get('logical_regions',{}).items():
  if 'source_roles'in role:regions[key]=[r for name in role['source_roles']for r in regions.get(role['unit']+'.'+name,[])]
  elif 'parts'in role:
   if role.get('kind')=='BOUND_PRIVATE_DOMAIN121':
    from private_binding121 import examine as bind_private
    binding=bind_private(m);errors.extend(binding['errors']);pending.extend(binding['pending'])
    if key not in binding['regions']:errors.append(key+':UNBOUND_PRIVATE_DOMAIN')
    else:regions[key]=[q(r)for r in binding['regions'][key]]
    continue
   rs=[q(r)for r in role['parts']];parent=regions.get(role['unit']+'.bath',[])
   if not all(covered(r,parent)for r in rs):errors.append(key+':LOGICAL_REGION_OUTSIDE_ACTUAL_BATH')
   regions[key]=rs
 rows=[];obstacles=list(walls.values())+[q(r)for u in m['units']for k,r in u['fixtures'].items()if not u['fixture_metadata'][k].get('walkable')]
 for o in m['openings']:
  oid=o['id'];r=q(o['rect']);host=hosts.get(o.get('host_wall_id'));roles=o.get('connects',[])
  if host is None:pending.append(oid+':HOST_MISSING');continue
  if not inside(r,host):
   # Source113 pocket names a real adjoining jamb rather than uncut host.
   # Establish actual collinear edge contact, never assume containment.
   vertical=r[3]-r[1]>r[2]-r[0]
   adjacent=(r[0]==host[0]and r[2]==host[2]and(r[1]==host[3]or r[3]==host[1]))if vertical else(r[1]==host[1]and r[3]==host[3]and(r[0]==host[2]or r[2]==host[0]))
   if o.get('kind')!='pocket_source113'or not adjacent:errors.append(oid+':OUTSIDE_HOST_WITHOUT_ACTUAL_JAMB')
   elif not any(inside(w,host)for w in walls.values()):errors.append(oid+':POCKET_JAMB_WITHOUT_PHYSICAL_SOLID')
  if len(roles)!=2 or roles[0]==roles[1]or any(not regions.get(k)for k in roles):pending.append(oid+':TWO_ACTUAL_REGIONS_UNRESOLVED');continue
  if any(hit(r,w)for w in walls.values()):errors.append(oid+':APERTURE_BLOCKED_BY_SOLID')
  vertical=r[3]-r[1]>r[2]-r[0];axis=1 if vertical else 0;low=r[axis]+h;high=r[axis+2]-h;values={low,high}
  for rect in obstacles+regions[roles[0]]+regions[roles[1]]:
   values|={v for v in(rect[axis]-h,rect[axis]+h,rect[axis+2]-h,rect[axis+2]+h)if low<=v<=high}
  sv=sorted(values);values|={(a+b)/2 for a,b in zip(sv,sv[1:])};found=False
  for t in values:
   if not low<=t<=high:continue
   if vertical:
    cross=(r[0]-h,t-h,r[2]+h,t+h);sides=[(r[0]-h,t-h,r[0],t+h),(r[2],t-h,r[2]+h,t+h)]
   else:
    cross=(t-h,r[1]-h,t+h,r[3]+h);sides=[(t-h,r[1]-h,t+h,r[1]),(t-h,r[3],t+h,r[3]+h)]
   if any(hit(cross,v)for v in obstacles):continue
   if any(covered(sides[0],regions[a])and covered(sides[1],regions[b])for a,b in(roles,roles[::-1])):found=True;break
  if not found:errors.append(oid+':NO_BODY_CROSSING_BETWEEN_DECLARED_REGIONS')
  rows.append({'opening':oid,'host':o['host_wall_id'],'regions':roles,'crossing_found':found})
 # Owner121 excludes light/ventilation; only already modeled object geometry.
 for w in m.get('concept_windows',[]):
  wid=w['id'];r=q(w['plan_rect']);host=walls.get(w.get('host_wall_id'))
  if host is None:pending.append(wid+':WINDOW_HOST_MISSING');continue
  if not inside(r,host):errors.append(wid+':WINDOW_OUTSIDE_PHYSICAL_HOST')
  if w.get('floor_portal')is not False:errors.append(wid+':WINDOW_FLOOR_PORTAL_AMBIGUOUS')
  if not 0<=F(str(w['sill_m']))<F(str(w['head_m'])):errors.append(wid+':WINDOW_HEIGHT_INTERVAL_INVALID')
  rows.append({'window':wid,'host':w['host_wall_id'],'scope':'Actual object geometry only; light/ventilation excluded, not evaluated.'})
 return output('H10',sorted(set(errors)),sorted(set(pending)),{'openings':rows,'body_m':str(body),'logical_bath_regions_scope':'Actual explicit partition regions must also have source-placement binding in separate mandatory gate.'})

@safe
def wall_network(m):
 errors=[];pending=[];walls={k:q(v)for k,v in m['walls'].items()};hosts={k:q(v)for k,v in m['wall_hosts'].items()};seen={}
 net=m.get('physical_wall_network');union_verified=False;duplicate_sources=[]
 if net is not None:
  expected_hash=hashlib.sha256(json.dumps(m['walls'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
  if net.get('source_wall_hash')!=expected_hash:errors.append('PHYSICAL_UNION_SOURCE_HASH_MISMATCH')
  solids={k:q(v)for k,v in net['solids'].items()};aliases=net['source_aliases']
  if set(aliases)!=set(walls):errors.append('PHYSICAL_UNION_ALIAS_INVENTORY')
  if any(hit(a,b)for i,a in enumerate(solids.values())for b in list(solids.values())[i+1:]):errors.append('PHYSICAL_SOLIDS_OVERLAP')
  if not all(covered(r,list(solids.values()))for r in walls.values())or not all(covered(r,list(walls.values()))for r in solids.values()):errors.append('PHYSICAL_UNION_CHANGED_MATERIAL')
  for k,r in walls.items():
   ids=aliases.get(k,[]);actual={j for j,v in solids.items()if hit(r,v)}
   if set(ids)!=actual or len(ids)!=len(set(ids)):errors.append('PHYSICAL_UNION_ALIAS_MISMATCH:'+k)
   intersections=[(max(r[0],solids[j][0]),max(r[1],solids[j][1]),min(r[2],solids[j][2]),min(r[3],solids[j][3]))for j in actual]
   if not covered(r,intersections):errors.append('SOURCE_WALL_NOT_RECONSTRUCTED:'+k)
  union_verified=not errors
 for k,r in walls.items():
  if r in seen:
   duplicate_sources.append([seen[r],k])
   if not union_verified:errors.append('DUPLICATE_SOLID:'+seen[r]+':'+k)
  seen[r]=k
 # Door apertures interrupt solids; uncut host graph is the intended partition
 # network. Corner-only contact is not positive-length T/end connectivity.
 todo=set(hosts);groups=[]
 def contact(a,b):
  dx=min(a[2],b[2])-max(a[0],b[0]);dy=min(a[3],b[3])-max(a[1],b[1]);return dx>=0 and dy>=0 and(dx>0 or dy>0)
 while todo:
  first=todo.pop();group=[first];queue=[first]
  while queue:
   a=hosts[queue.pop()]
   for k in list(todo):
    if contact(a,hosts[k]):todo.remove(k);group.append(k);queue.append(k)
  groups.append(sorted(group))
 if len(groups)!=1:errors.append('DISCONNECTED_PARTITION_HOST_NETWORK')
 from finish_profile_audit118 import examine as examine_finish
 finish=examine_finish(m);errors.extend(finish['errors']);pending.extend(finish['pending'])
 return output('H09',errors,pending,{'face_layer_profile':finish,'physical_union_verified':union_verified,'duplicate_source_aliases':duplicate_sources,'solid_count':len(walls),'host_count':len(hosts),'host_components':groups,'thicknesses_m':sorted({str(min(r[2]-r[0],r[3]-r[1]))for r in hosts.values()})})

ADAPTERS={'core_concept':core_concept,'opening_hosts':opening_hosts,'wall_network':wall_network}
