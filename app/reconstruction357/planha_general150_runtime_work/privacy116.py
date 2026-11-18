"""Privacy-only bedroom module audit. No bath waiver for whole-model audits.
Actual plan wall opacity is hypothetical; no real sight-height/material claim.
"""
import hashlib
from pathlib import Path
from privacy115 import rect,digest,contained,hit,boundary,interval_covered,separator,clear_witness,F

def examine_module(m):
 errors=[];pending=[];rows=[];gid=digest(m)
 try:
  if m.get('schema')not in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118'):errors.append({'code':'MODULE_SCHEMA'})
  units=m.get('units',[m.get('unit')])
  if len(units)!=1:raise ValueError('one bedroom module required')
  u=units[0];rooms={k:list(map(rect,v))for k,v in u['rooms'].items()};walls={k:rect(v)for k,v in m['walls'].items()}
  if set(rooms)!={'bed1','public_access'}:errors.append({'code':'MODULE_ROOM_INVENTORY'})
  fixtures={k:rect(v)for k,v in u['fixtures'].items()};acts=u['activities'];rs=rooms['bed1']
  # Only physical source-sized cabinet skins, never the gross fixture envelope.
  from q11_boundary118 import bound_closet_shells
  local=dict(m);local['unit']=u
  skins=bound_closet_shells(local);errors.extend(skins['errors'])
  walls.update({k:rect(v)for k,v in skins['opaque_materials'].items()})
  targets={}
  metadata=u.get('fixture_metadata',{})
  bed_ids=[k for k,v in metadata.items()if v.get('kind')in('bed','single_bed')]
  if not bed_ids and 'bed1.bed'in fixtures:bed_ids=['bed1.bed']
  expected=2 if m.get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'else 1
  if len(bed_ids)!=expected:errors.append({'code':'PRIVATE_BED_TARGET_INVENTORY','expected':expected,'actual':len(bed_ids)})
  for name in bed_ids:
   if name not in fixtures:pending.append('TARGET_MISSING:'+name)
   else:targets[name]=rect(fixtures[name])
  if 'bed1.changing'not in acts:pending.append('TARGET_MISSING:bed1.changing')
  else:targets['changing']=rect(acts['bed1.changing'])
  if any(hit(a,b)for a in rs for b in rooms['public_access']):errors.append({'code':'PUBLIC_PRIVATE_OVERLAP'})
  for key,t in targets.items():
   if not contained(t,rs):errors.append({'code':'TARGET_OUTSIDE_ROOM','target':key})
  ops={v['opening_id']:v for v in m.get('operations',{}).get('doors',[])}
  apertures=[o for o in m['openings']if u['id']+'.bed1'in o.get('connects',[])]
  if not apertures:pending.append('EXTERNAL_APERTURE_MISSING')
  # A solid abutting either side of a room edge closes it. Floors are unions;
  # the exposed screen edges are actual walls, never bbox-filled room area.
  for ax,high,p,lo,hi in boundary(rs):
   other=1-ax;intervals=[]
   for q in list(walls.values())+[rect(o['rect'])for o in apertures]:
    if q[ax]<=p<=q[ax+2]:intervals.append((max(lo,q[other]),min(hi,q[other+2])))
   if not interval_covered(lo,hi,[(a,b)for a,b in intervals if a<b]):errors.append({'code':'ROOM_CLOSURE_GAP','edge':list(map(str,(ax,high,p,lo,hi)))})
  for o in apertures:
   oid=o['id'];ap=rect(o['rect']);op=ops.get(oid);opened=None
   if op:
    c=rect(op['closed_panel']);opened=rect(op['open_panel']);d=list(map(F,op['translation']))
    if len(d)!=2 or tuple(c[i]+d[i%2]for i in range(4))!=opened or hit(ap,opened):errors.append({'code':'INVALID_OPEN_STATE','opening':oid});opened=None
   if opened is None:pending.append('OPEN_STATE_MISSING:'+oid)
   for name,t in targets.items():
    proof=next(({'wall':k,**p}for k,w in walls.items()if(p:=separator(ap,t,w))),None)
    witness=None
    if proof is None:
     if opened is not None:witness=clear_witness(ap,t,list(walls.values())+[opened]+[v for v in fixtures.values()if not hit(v,t)])
     if witness:errors.append({'code':'PRIVATE_TARGET_VISIBLE','target':name,'opening':oid,'witness':witness})
     else:pending.append('ALL_RAYS_NOT_PROVEN:'+oid+':'+name)
    rows.append({'target':name,'opening':oid,'strict_certificate':proof,'counterexample':witness})
 except (KeyError,TypeError,ValueError,IndexError)as e:errors.append({'code':'MALFORMED_MODULE','detail':str(e)})
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':{'status':'FAIL_SCOPED'if errors else'NOT_EVALUATED'if pending else'PASS_SCOPED_MODULE_PRIVACY','model_hash':gid,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'targets':rows,'accepted':False,'release_allowed':False,'scope':'Only full-aperture to full bed/changing targets in one bedroom module. No whole-model, operation, real-height or professional approval. Closet envelopes never prove opacity.'}}
