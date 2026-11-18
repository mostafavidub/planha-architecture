"""Independent GENERAL115 privacy: finite certificates, never a prior PASS.
Transferred contract: reference privacy102 / audit_lr_target_privacy.preliminary
used actual opaque wall skins, every bedroom bed+changing target, bath WC-use,
shower-use and shower-floor targets; all points of the open aperture, rather than
assuming a shut door. Boundary-only certificates retain an explicit conditional
label. Closet gross envelopes are NOT opaque; no new closet-shell assumption.

This checker certifies a sufficient single-wall interval separator. Failure to
find one is NOT proof of visibility; a separately checked clear ray can refute
privacy under the stated open-aperture observation assumption. No ray sampling
is ever used to certify privacy. Whole building operation/route gates remain
separate. Inputs are never modified; no producer/checker imports.
"""
from fractions import Fraction as Fraction
from itertools import product
import hashlib,json
from pathlib import Path
RULE_SOURCE = {'reference_versions':[103,109,113], 'privacy102_sha256':'9b5011652f9109458b70fb7cd6d0cacdb0295a3d1095c5126357c9444bb82bfc', 'concept_scope_sha256':'8804bca0ecb774c5186969f85c0d03b73766e23e20d30304b84f580c41a1d05e', 'transfer':'Target inventory, actual solid closure, open-aperture all-ray certificate, conditional closed-boundary labeling; no receipt transferred.'}
F=lambda x:Fraction(str(x))
def digest(m):return hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def rect(q):
 q=tuple(F(v)for v in q)
 if len(q)!=4 or q[0]>=q[2]or q[1]>=q[3]:raise ValueError('INVALID_RECT')
 return q
def hit(a,b):return max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])
def inside(p,rs):return any(r[0]<=p[0]<=r[2]and r[1]<=p[1]<=r[3]for r in rs)
def contained(q,rs):
 xs=sorted({q[0],q[2]}|{r[i]for r in rs for i in(0,2)if q[0]<r[i]<q[2]});ys=sorted({q[1],q[3]}|{r[i]for r in rs for i in(1,3)if q[1]<r[i]<q[3]})
 return all(inside(((a+b)/2,(c+d)/2),rs)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:]))
def interval_covered(lo,hi,intervals):
 end=lo
 for a,b in sorted(intervals):
  if a>end:return False
  end=max(end,b)
  if end>=hi:return True
 return False

def boundary(rs):
 xs=sorted({r[i]for r in rs for i in(0,2)});ys=sorted({r[i]for r in rs for i in(1,3)});cells={(i,j)for i in range(len(xs)-1)for j in range(len(ys)-1)if inside(((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2),rs)};edges=[]
 for i,j in cells:
  for axis,high,other in[(0,False,(i-1,j)),(0,True,(i+1,j)),(1,False,(i,j-1)),(1,True,(i,j+1))]:
   if other not in cells:edges.append((axis,high,(xs[i+int(high)]if axis==0 else ys[j+int(high)]),(ys[j]if axis==0 else xs[i]),(ys[j+1]if axis==0 else xs[i+1])))
 return edges

def crosses(q,edge):
 ax,high,p,lo,hi=edge;other=1-ax
 return (q[ax]<=p<q[ax+2]if high else q[ax]<p<=q[ax+2])and max(lo,q[other])<min(hi,q[other+2])
def closure_gaps(rs,walls,apertures):
 gaps=[]
 for edge in boundary(rs):
  ax,high,p,lo,hi=edge;k=1-ax;intervals=[(max(lo,q[k]),min(hi,q[k+2]))for q in list(walls)+list(apertures)if crosses(q,edge)]
  if not interval_covered(lo,hi,intervals):gaps.append(list(map(str,edge)))
 return gaps

def separator(source,target,wall,closed=False):
 """Exact rectangle-to-rectangle all-rays interval certificate at wall interior.
The rational projection extrema occur at endpoint vertices when the separating
axis ordering is strict. Unsupported geometry returns None, never a fake PASS.
"""
 for ax in(0,1):
  k=1-ax;p=(wall[ax]+wall[ax+2])/2
  if not(source[ax+2]<p<target[ax]or target[ax+2]<p<source[ax]):continue
  projections=[b+(d-b)*(p-a)/(c-a)for a,b,c,d in product((source[ax],source[ax+2]),(source[k],source[k+2]),(target[ax],target[ax+2]),(target[k],target[k+2]))]
  lo,hi=min(projections),max(projections)
  if (wall[k]<=lo<=hi<=wall[k+2])if closed else(wall[k]<lo<=hi<wall[k+2]):return {'axis':ax,'plane':str(p),'projected_interval':[str(lo),str(hi)],'conditional_closed_boundary':closed}
 return None

def segment_hits(a,b,q):
 """Conservative CLOSED rectangle hit; no tangent ray counted visibly clear."""
 lo,hi=Fraction(0),Fraction(1)
 for ax in (0,1):
  d=b[ax]-a[ax]
  if not d:
   if not q[ax]<=a[ax]<=q[ax+2]:return False
  else:
   u,v=(q[ax]-a[ax])/d,(q[ax+2]-a[ax])/d;lo=max(lo,min(u,v));hi=min(hi,max(u,v))
   if lo>hi:return False
 return hi>=0 and lo<=1

def clear_witness(aperture,target,obstacles):
 # A finite clear ray can DISPROVE all-ray privacy, never prove it.
 for u,v in product((Fraction(1,4),Fraction(1,2),Fraction(3,4)),repeat=2):
  s=(aperture[0]+u*(aperture[2]-aperture[0]),aperture[1]+v*(aperture[3]-aperture[1]))
  for a,b in product((Fraction(1,4),Fraction(1,2),Fraction(3,4)),repeat=2):
   t=(target[0]+a*(target[2]-target[0]),target[1]+b*(target[3]-target[1]))
   if not any(segment_hits(s,t,q)for q in obstacles):return {'source':list(map(str,s)),'target':list(map(str,t)),'state':'fully_open','scope':'Clear ray from an interior point of the open aperture; no claim about real observer height.'}
 return None

def examine(model):
 errors=[];pending=[];rows=[];before=digest(model)
 def err(code,**kw):errors.append({'code':code,**kw})
 def pend(code,**kw):pending.append(code+(':'+json.dumps(kw,sort_keys=True)if kw else''))
 try:
  walls={k:rect(q)for k,q in model['walls'].items()};openings=model.get('openings',[]);byid={o['id']:o for o in openings}
  if len(byid)!=len(openings):err('PRIVACY_DUPLICATE_OPENING')
  ops={o['opening_id']:o for o in model.get('operations',{}).get('doors',[])}
  if len(ops)!=len(model.get('operations',{}).get('doors',[])):err('PRIVACY_DUPLICATE_DOOR_STATE')
  opened={}
  for oid,op in ops.items():
   if oid not in byid:err('PRIVACY_UNKNOWN_DOOR',opening=oid);continue
   closed,opn=rect(op['closed_panel']),rect(op['open_panel']);delta=tuple(F(v)for v in op['translation']);ap=rect(byid[oid]['rect'])
   if len(delta)!=2 or tuple(closed[i]+delta[i%2]for i in range(4))!=opn or hit(opn,ap):err('PRIVACY_INVALID_OPEN_DOOR_STATE',opening=oid);continue
   opened[oid]=opn
  for unit in model['units']:
   uid=unit['id'];rooms={k:[rect(q)for q in rs]for k,rs in unit['rooms'].items()};fixtures={k:rect(q)for k,q in unit['fixtures'].items()};acts={k:rect(q)for k,q in unit.get('activities',{}).items()};md=unit.get('fixture_metadata',{})
   beds=[k for k in rooms if k.split('.')[-1].startswith('bed')or model.get('room_metadata',{}).get(uid+'.'+k,{}).get('role')=='bedroom']
   if not beds:err('PRIVACY_BEDROOM_INVENTORY_EMPTY',unit=uid)
   declared=model.get('program',{}).get('bedrooms_per_unit')
   if declared is not None and F(declared)!=len(beds):err('PRIVACY_DECLARED_BEDROOM_COUNT',unit=uid)
   if sum(v.get('kind')=='bed'for v in md.values())!=len(beds):err('PRIVACY_BED_TARGET_ROOM_COUNT',unit=uid)
   if 'bath'not in rooms:err('PRIVACY_BATH_MISSING',unit=uid)
   private=set(beds)|{'bath'}
   public=[r for u in model['units']for k,rs in u['rooms'].items()if not k.split('.')[-1].startswith('bed')and k!='bath'for r in map(rect,rs)]
   for value in model.get('common_spaces',{}).values():public += [rect(q)for q in value]if isinstance(value[0],list)else[rect(value)]
   for role in beds+(['bath']if 'bath'in rooms else[]):
    rs=rooms[role];qualified=uid+'.'+role;targets={}
    if role in beds:
     found=[(k,q)for k,q in fixtures.items()if md.get(k,{}).get('kind')=='bed'and contained(q,rs)]
     if len(found)!=1:err('PRIVACY_BED_TARGET_INVENTORY',room=qualified)
     else:targets['bed']=found[0][1]
     change=acts.get(role+'.changing')
     if change is None:pend('PRIVACY_CHANGING_TARGET_MISSING',room=qualified)
     else:targets['changing']=change
    else:
     for name,key,source in [('WC_use','WC_front',acts),('shower_use','shower_use',acts),('shower_floor','shower_floor',fixtures)]:
      if key not in source:pend('PRIVACY_TARGET_MISSING',room=qualified,target=name)
      else:targets[name]=source[key]
    for name,t in targets.items():
     if not contained(t,rs):err('PRIVACY_TARGET_OUTSIDE_ROOM',room=qualified,target=name)
    if any(hit(r,s)for r in rs for s in public):err('PRIVACY_PUBLIC_PRIVATE_OVERLAP',room=qualified)
    edges=boundary(rs);apertures=[o for o in openings if qualified in o.get('connects',[])and any(crosses(rect(o['rect']),edge)for edge in edges)]
    if not apertures:pend('PRIVACY_EXTERNAL_APERTURE_MISSING',room=qualified)
    gap=closure_gaps(rs,walls.values(),[rect(o['rect'])for o in apertures])
    if gap:err('PRIVACY_ROOM_NOT_CLOSED_EXCEPT_PORTALS',room=qualified,gaps=gap)
    for op in apertures:
     oid=op['id'];ap=rect(op['rect']);state_known=oid in opened
     if not state_known:pend('PRIVACY_ACTUAL_OPEN_DOOR_STATE_MISSING',opening=oid)
     for name,t in targets.items():
      strict=next(({'wall':wid,**proof}for wid,q in walls.items()if(proof:=separator(ap,t,q))),None)
      conditional=None if strict else next(({'wall':wid,**proof}for wid,q in walls.items()if(proof:=separator(ap,t,q,True))),None)
      witness=None
      if not(strict or conditional):
       if state_known:
        # Unknown-height furniture is not an opacity certificate, but may occlude:
        # do not claim definite clear sight through another fixture envelope.
        possible_occluders=[rect(q)for other in model['units']for q in other['fixtures'].values()if not hit(rect(q),t)]
        witness=clear_witness(ap,t,list(walls.values())+list(opened.values())+possible_occluders)
       if witness:err('PRIVATE_TARGET_VISIBLE_FROM_OPEN_APERTURE',room=qualified,target=name,opening=oid,witness=witness)
       else:pend('PRIVACY_ALL_RAYS_NOT_PROVEN',room=qualified,target=name,opening=oid)
      rows.append({'room':qualified,'target':name,'opening':oid,'open_state_bound':state_known,'strict_certificate':strict,'conditional_closed_boundary_certificate':conditional,'clear_visibility_counterexample':witness})
  if digest(model)!=before:err('PRIVACY_MODEL_MUTATED')
 except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError)as ex:err('PRIVACY_MALFORMED',detail=type(ex).__name__+':'+str(ex))
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':{'model_hash':before,'rule_sources':RULE_SOURCE,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'targets':rows,'strict_count':sum(bool(r['strict_certificate'])for r in rows),'conditional_count':sum(bool(r['conditional_closed_boundary_certificate'])for r in rows),'status':'FAIL_SCOPED'if errors else'NOT_EVALUATED'if pending else'PASS_SCOPED_PRIVACY','accepted':False,'release_allowed':False,'assumptions':['Opaque actual model wall solids in plan, same hypothetical opacity scope as reference privacy102.','Every open aperture point considered; closed panels are never used to hide a target.','Closet fixture envelopes and pre-cut wall_hosts are never opaque barriers.','Sufficient single-wall interval proof; missing multi-wall/U-shell certificate remains pending, not impossible.','No real sight heights/material transparency/legal compliance claim.']}}
