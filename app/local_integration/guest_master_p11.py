"""P11: scoped FR guest master-panel source and exact same-model readback."""
import copy, hashlib, inspect
from fractions import Fraction as F
from pathlib import Path
import source_fit_profile207 as fit
from same_version_front_rear_contract import digest
from contract114 import S,WALL,BODY

PINS={'entry117.py':'56483ecd624dee7fddca5097ba284f8689bcfd9c',
 'assemble114.py':'6e19b12c62820e015055765e0fe56d6339cd4312',
 'public_program_audit118.py':'c5846f77b2678ec88a301d14bf8288e2171750dd',
 'core_wall_audit118.py':'e2873b155a777e40df866c353db62e47130eee90'}
GUESTS={'sofa1_use':'guest_living','dining_east':'guest_dining'}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')

def need(ok,code):
 if not ok:raise ValueError(code)
def one(rows,code):
 need(len(rows)==1,code)
 return rows[0]
def source_snapshot():
 expected=fit.ENGINE
 out={}
 for name,pin in PINS.items():
  p=expected/name;data=p.read_bytes()
  need(not p.is_symlink() and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==pin,'P11_FROZEN_SOURCE')
  out[name]=hashlib.sha256(data).hexdigest()
 return out
def pt(v):
 need(type(v) is list and len(v)==2 and all(type(x) in (str,int,float) for x in v),'P11_POINT')
 return tuple(F(str(x)) for x in v)
def reflect_rect(rect,L):
 x,y,X,Y=fit.q(rect)
 return x,L-Y,X,L-y
def entry_source(core):
 """Same two apertures that assemble114 supplies to actual entry117.install."""
 from entry117 import install
 pin=source_snapshot()
 need(Path(inspect.getsourcefile(install)).resolve()==fit.ENGINE/'entry117.py','P11_ENTRY_SOURCE_PATH')
 need(core['kind']=='COMPACT_CONNECTED_CENTRAL_CORE118' and set(core['entry_centers'])=={'A','B'},'P11_COMPACT_FR_PAIR')
 ax,_=pt(core['entry_centers']['A']);bx,_=pt(core['entry_centers']['B']);need(ax==bx,'P11_ENTRY_SYMMETRY')
 _,y,_,yt=fit.q(core['band']);L=y+yt
 source={'openings':[{'id':uid+'.entry','rect':[S(v)for v in (ax-F('.65'),lo,ax+F('.65'),hi)],
                      'host_wall_id':uid+'.unit_boundary'}
                      for uid,lo,hi in (('A',y-WALL,y),('B',yt,yt+WALL))],
         'operations':{}}
 a,b=[fit.q(core['units'][uid])for uid in ('A','B')]
 need(reflect_rect(core['units']['A'],L)==b,'P11_OWNER_FRAME')
 root=[S(ax),S(a[3]-F('.4'))]
 install(source)
 ops=source['operations']['doors'];panel=ops[0]['open_panel']
 need(reflect_rect(ops[1]['open_panel'],L)==fit.q(panel),'P11_ENTRY_PANEL_MIRROR')
 x,r=pt(root);h=BODY/2
 need(not fit.hit((x-h,r-h,x+h,r+h),fit.q(panel)),'P11_ROOT_BODY_ENTRY_PANEL')
 need(source_snapshot()==pin,'P11_FROZEN_SOURCE_CHANGED')
 return {'openings':source['openings'],'operations':ops,'local_panel':panel,'root':root,
         'length':S(L),'core_digest':digest(core),'frozen_source':pin}

def plan(proposal,core):
 """Exact residual of emitted guest tokens only, not physical room/route evaluation."""
 src=entry_source(core)
 need(proposal.get('p11_entry_source_digest')==digest(src),'P11_PRODUCER_ENTRY_SOURCE')
 x,y,_,_=fit.q(proposal['rectangles']['kitchen'])
 profile=fit.profiles(); motions=[fit.translated(r,x,y)for r in profile['kitchen_motions']]
 need(len(motions)==6,'P11_SOURCE_MOTION_INVENTORY')
 panel=fit.q(src['local_panel']);owner=[fit.q(r)for r in core['unit_ownership']['A']]
 rows=[]
 for terminal,role in sorted(GUESTS.items()):
  path=proposal['network_paths'][terminal];bands=fit.guest_bands(path);codes=[]
  if pt(path[0])!=pt(src['root']):codes.append('P11_SOURCE_ENTRY_ROOT_MISMATCH')
  if not all(fit.covered(band,owner)for band in bands):codes.append('P11_GUEST_BODY_OUTSIDE_OWNERSHIP')
  panel_hits=[i for i,band in enumerate(bands)if fit.hit(band,panel)]
  motion_hits=[[i,j]for i,band in enumerate(bands)for j,motion in enumerate(motions)if fit.hit(band,motion)]
  if panel_hits:codes.append('P11_GUEST_SOURCE_ENTRY_PANEL_COLLISION')
  if motion_hits:codes.append('P11_GUEST_SOURCE_KITCHEN_MOTION_COLLISION')
  rows.append({'role':role,'terminal':terminal,'codes':codes,'panel_segments':panel_hits,'motion_segment_pieces':motion_hits})
 return {'schema':'P11_GUEST_MASTER_RESIDUAL_V1','state':'GUEST_MASTER_SOURCE_RESERVATIONS_CLEAR_ONLY' if not any(r['codes']for r in rows) else 'REJECT_SELECTED_GUEST_MASTER_RESERVATIONS',
         'source_entry_digest':digest(src),'profile_digest':digest(profile),'proposal_digest':digest(proposal),
         'core_digest':digest(core),'routes':rows,**{k:False for k in AUTH}}

def installed(proposal,core,model,physical,pinned_plan):
 """Actual installed identity, typed floor and endpoint; no route generation."""
 from public_program_audit118 import bind_operation_destination
 from source_guest_route_evaluator import living_destination
 source=source_snapshot()
 need(Path(inspect.getsourcefile(bind_operation_destination)).resolve()==fit.ENGINE/'public_program_audit118.py','P11_DINING_BINDER_SOURCE')
 need(Path(inspect.getsourcefile(living_destination)).resolve()==fit.ROOT/'app/local_integration/source_guest_route_evaluator.py','P11_LIVING_BINDER_SOURCE')
 src=entry_source(core);mh=digest(model);ph=digest(physical);pp=digest(proposal);lp=digest(pinned_plan)
 need(physical['model_hash']==mh and pp==pinned_plan['proposal_digest'] and digest(src)==pinned_plan['source_entry_digest']
      and [u['id']for u in model['units']]==['A','B'] and F(model['inputs'][1])==F(src['length']),'P11_MODEL_BINDING')
 L=F(src['length']);profile=fit.profiles();x,y,_,_=fit.q(proposal['rectangles']['kitchen'])
 local_motions=[fit.translated(r,x,y) for r in profile['kitchen_motions']]
 rows=[]
 for i,u in enumerate(model['units']):
  uid=u['id'];entry=uid+'.entry';rs=[];source_codes=[]
  op=one([o for o in model['operations']['doors'] if o.get('opening_id')==entry],'P11_INSTALLED_ENTRY_INVENTORY')
  opening=one([o for o in model['openings'] if o.get('id')==entry],'P11_INSTALLED_APERTURE_INVENTORY')
  so=src['openings'][i]
  if digest(op)!=digest(src['operations'][i]) or any(digest(opening.get(k))!=digest(so[k])for k in so):
   source_codes.append('P11_INSTALLED_ENTRY_SOURCE_MISMATCH')
  ko=one([o for o in model['operations']['kitchen'] if o.get('unit')==uid],'P11_INSTALLED_KITCHEN_INVENTORY')
  motion=[fit.q(r) for r in ko.get('motion_envelopes',[])]
  expected=[r if uid=='A' else reflect_rect(r,L) for r in local_motions]
  # Original builder order is sink, prep. JSON sorted-key readback must
  # not reorder the meaning of the immutable six-piece motion list.
  need(set(ko['drawers'])=={'sink','prep'},'P11_INSTALLED_DRAWER_INVENTORY')
  canonical_op=copy.copy(ko);canonical_op['drawers']={k:ko['drawers'][k] for k in ('sink','prep')}
  rederived=[fit.q(r)for r in fit.motion_rectangles({'schema':'KITCHEN_MODULE117','operations':{'kitchen':[canonical_op]}})]
  if len(motion)!=6 or motion!=expected or motion!=rederived:source_codes.append('P11_INSTALLED_MOTION_SOURCE_MISMATCH')
  panel=fit.q(op['open_panel']);floor=[fit.q(r)for role in ('living','entry_circulation','dining') for r in u['rooms'].get(role,[])]
  owner=[fit.q(r) for r in u['ownership']]
  for terminal,role in sorted(GUESTS.items()):
   codes=list(source_codes);path=proposal['network_paths'][terminal];original=fit.guest_bands(path)
   pts=[pt(v)for v in path]
   if uid=='B':pts=[(a,L-b)for a,b in pts]
   bands=original if uid=='A' else [reflect_rect(r,L)for r in original]
   if pts[0]!=pt(u['entry_point']):codes.append('P11_INSTALLED_ROOT_MISMATCH')
   try:
    if role=='guest_living':
     end,binding=living_destination(u)
     need(binding['activity_id']=='sofa1_front' and binding['fixture_id']=='sofa1','P11_LIVING_DESTINATION_ROLE')
    else:
     dst=u['public_program']['destinations'][role]
     need(dst['activity_id']=='dining_east' and dst['fixture_id']=='dining_chair_east','P11_DINING_DESTINATION_ROLE')
     a,b,c,d=fit.q(u['activities'][dst['activity_id']]);end=[S((a+c)/2),S((b+d)/2)]
     bind_operation_destination(u,dst,pt(end))
    if pt(end)!=pts[-1]:codes.append('P11_INSTALLED_DESTINATION_MISMATCH')
   except (KeyError,IndexError,TypeError,ValueError):
    codes.append('P11_INSTALLED_DESTINATION_UNVERIFIED')
   if not floor or not all(fit.covered(r,floor) and fit.covered(r,owner)for r in bands):
    codes.append('P11_INSTALLED_TYPED_GUEST_FLOOR_NOT_VERIFIED')
   if any(fit.hit(r,panel)for r in bands):codes.append('P11_INSTALLED_GUEST_ENTRY_PANEL_COLLISION')
   if any(fit.hit(r,o)for r in bands for o in motion):codes.append('P11_INSTALLED_GUEST_KITCHEN_MOTION_COLLISION')
   rs.append({'role':role,'codes':sorted(codes),'state':'OBSERVED_ISSUES_NOT_WHOLE_ROUTE' if codes else 'ALIGNED_SOURCE_SUBSET_ONLY',
              'stored_guest_route_present':bool(u.get('scenario_routes',{}).get(role))})
  rows.append({'unit':uid,'orientation':'TRANSLATION' if uid=='A' else 'Y_REFLECTION','routes':rs,
               'entry_operation_digest':digest(op),'kitchen_operation_digest':digest(ko),'motion_pieces':len(motion)})
 need(digest(model)==mh and digest(physical)==ph and digest(proposal)==pp and digest(pinned_plan)==lp
      and source_snapshot()==source,'P11_EVIDENCE_MUTATION')
 return {'schema':'P11_INSTALLED_GUEST_MASTER_BINDING_V1','model_digest':mh,'physical_digest':ph,
         'proposal_digest':pp,'plan_digest':lp,'rows':rows,'serving_evaluated':False,
         'scope':'Source panel/motion, typed guest floor and actual destinations only; no serving, whole path or delivery decision.',
         **{k:False for k in AUTH}}

def observe(proposal,core,model,physical,pinned_plan):
 try:return installed(proposal,core,model,physical,pinned_plan)
 except (KeyError,IndexError,TypeError,ValueError,ArithmeticError):
  return {'schema':'P11_INSTALLED_GUEST_MASTER_BINDING_V1','model_digest':digest(model),'physical_digest':digest(physical),
          'proposal_digest':digest(proposal),'plan_digest':digest(pinned_plan),'state':'UNKNOWN_UNVERIFIED_SOURCE_OR_INPUT',
          'serving_evaluated':False,'rows':[],**{k:False for k in AUTH}}
