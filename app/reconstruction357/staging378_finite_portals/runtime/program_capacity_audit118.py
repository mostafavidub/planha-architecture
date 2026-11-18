"""Independent actual-instance capacity study; never infer places from area/length."""
from pathlib import Path
import json
from public_program_audit118 import F,q,hit,covered,sweeps,digest
from dining_motion_audit118 import examine_whole,motion
CAT=Path(__file__).with_name('fixture_catalog114.json')
def examine(model):
 errors=[];pending=[];rows=[];catalog=json.loads(CAT.read_text())
 try:
  if model['fixture_catalog_hash']!=digest(catalog):raise ValueError('CATALOG_HASH')
  walls=list(map(q,model['walls'].values()));dining=examine_whole(model);errors.extend(dining['errors']);pending.extend(dining['pending'])
  for u in model['units']:
   cap=u['public_program']['capacity'];fs={k:q(v)for k,v in u['fixtures'].items()};owner=list(map(q,u['ownership']));res=F(str(cap['residents']));counts={};records={}
   if res.denominator!=1 or res<1:raise ValueError('RESIDENT_COUNT')
   actual_sleep=sum(2 if md.get('kind')=='bed'else 1 if md.get('kind')=='single_bed'else 0 for md in u['fixture_metadata'].values())
   if res!=actual_sleep or res!=F(str(model['program']['design_occupants_per_unit'])):raise ValueError('RESIDENT_ACTUAL_SLEEP_PROGRAM_BINDING')
   expected_sleep_ids={k for k,md in u['fixture_metadata'].items()if md.get('kind')in('bed','single_bed')}
   if {e['fixture_id']for e in cap['sleeping_places']}!=expected_sleep_ids:raise ValueError('SLEEP_CAPACITY_INSTANCE_INVENTORY')
   for group in ('sleeping_places','dining_seats','living_seats'):
    entries=cap[group];keys=[x['fixture_id']for x in entries]
    if len(set(keys))!=len(keys):raise ValueError('REUSED_CAPACITY_FIXTURE')
    records[group]=entries;counts[group]=0
    for e in entries:
     fid=e['fixture_id'];r=fs[fid];kind=u['fixture_metadata'][fid]['kind'];dims=sorted((r[2]-r[0],r[3]-r[1]))
     if group=='sleeping_places'and kind not in('bed','single_bed'):raise ValueError('SLEEP_ROLE_TYPE')
     if group=='dining_seats'and not kind.startswith('dining_chair'):raise ValueError('DINING_ROLE_TYPE')
     if group=='living_seats'and kind not in('sofa1','sofa2','armchair1','armchair2'):raise ValueError('LIVING_ROLE_TYPE')
     source=catalog['types'].get(kind)
     if source is not None:expected=sorted((F(source['width_m']),F(source['depth_m'])))
     elif kind=='single_bed':expected=[F('.9'),F('1.9')]
     else:raise ValueError('UNKNOWN_FIXTURE_SOURCE:'+kind)
     if dims!=expected:raise ValueError('ACTUAL_SOURCE_SIZE:'+fid)
     places=F(str(e['places']));allowed=2 if kind=='bed'and group=='sleeping_places'else 1
     if places!=allowed:raise ValueError('PLACE_COUNT_NOT_INSTANCE_PROFILE:'+fid)
     counts[group]+=int(places)
    if counts[group]<res:errors.append({'code':'ACTUAL_CAPACITY_SHORTFALL','unit':u['id'],'group':group})
   # Sleep capacity exists only with each actual source bed and both access routes.
   for e in records['sleeping_places']:
    fid=e['fixture_id']
    for side in ('front','back'):
     name=fid+'_'+side;path=u['routes'].get(name)
     if not path:pending.append('SLEEP_ACCESS_MISSING:'+u['id']+'.'+name);continue
     for s in sweeps(path):
      if not covered(s,owner)or any(hit(s,x)for x in walls+list(fs.values())):errors.append({'code':'SLEEP_ACCESS_COLLISION','unit':u['id'],'route':name})
   occupied={e['fixture_id']:q(e['occupied_body'])for e in records['living_seats']}
   otherdining=[q(o['occupied_body'])for o in model['operations']['dining_chairs']if o['unit']==u['id']]
   for e in records['living_seats']:
    fid=e['fixture_id'];body=occupied[fid];r=fs[fid];act=q(u['activities'][e['access_activity_id']]);path=u['routes'][e['access_activity_id']]
    if (body[2]-body[0],body[3]-body[1])!=(F('.7'),F('.7'))or not covered(body,[r]):raise ValueError('LIVING_OCCUPIED_BODY_NOT_ON_OWN_SEAT')
    end=tuple(map(F,path[-1]));start=(end[0]-F('.35'),end[1]-F('.35'),end[0]+F('.35'),end[1]+F('.35'))
    if not covered(start,[act])or hit(start,r):raise ValueError('LIVING_STANDING_STATION')
    target=((body[0]+body[2])/2,(body[1]+body[3])/2)
    if end[0]!=target[0]and end[1]!=target[1]:raise ValueError('LIVING_TRANSFER_NOT_NORMAL')
    approach=sweeps(path);transfer=motion(start,body)
    obs=walls+[v for k,v in fs.items()if k!=fid]+[v for k,v in occupied.items()if k!=fid]+otherdining
    for s in approach:
     if not covered(s,owner)or any(hit(s,x)for x in obs+[r]):errors.append({'code':'LIVING_ACCESS_COLLISION','unit':u['id'],'seat':fid})
    if not covered(transfer,owner)or any(hit(transfer,x)for x in obs):errors.append({'code':'LIVING_SEAT_TRANSFER_COLLISION','unit':u['id'],'seat':fid})
   rows.append({'unit':u['id'],'residents_study':int(res),'actual_places':counts,'living_occupied_instances':len(occupied),'actual_closet_instances':sum(md.get('kind')=='closet'for md in u['fixture_metadata'].values()),'clothing_storage_volume_sufficiency':'NOT_VERIFIED; source closet operation and access are separate mandatory gates, no per-person volume standard inferred','worst_capacity_margin':min(counts.values())-int(res)})
 except(KeyError,ValueError,TypeError,IndexError)as e:errors.append({'code':'CAPACITY_AUDIT_MALFORMED','detail':str(e)})
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':{'status':'FAIL_SCOPED'if errors else'NOT_EVALUATED'if pending else'PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY','model_hash':digest(model),'units':rows,'worst_unit_margin':min((r['worst_capacity_margin']for r in rows),default=None),'scope':'Actual double2/single1 sleeping places, one per real dining chair and conservative one .7-body place per real sofa/armchair. Living access and normal seat-transfer tested with other living and dining seats occupied. Own support contact only during seat task, not walking. Height/ergonomics NOT_VERIFIED. Not full fixture operations, kitchen/bath/privacy or whole-plan admission.','accepted':False}}
