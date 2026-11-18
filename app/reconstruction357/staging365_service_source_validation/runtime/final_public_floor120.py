"""Final route-bound public floor classification; never a new physical wall."""
from fractions import Fraction as F
from contract114 import S,digest
from geometry114 import Q,cells

def rebuild(m):
 L=F(m['inputs'][1]);seq=lambda q:list(map(S,q))
 m['concept_windows']=[w for w in m.get('concept_windows',[])if w.get('id')not in('A.living.window','B.living.window')]
 for u in m['units']:
  uid=u['id'];reserved=[]
  paths={**u.get('routes',{}),**{'scenario:'+k:v for k,v in u.get('scenario_routes',{}).items()}}
  for path in paths.values():
   for p0,p1 in zip(path,path[1:]):
    a,b=Q(p0),Q(p1);reserved.append([min(a[0],b[0])-F('.35'),min(a[1],b[1])-F('.35'),max(a[0],b[0])+F('.35'),max(a[1],b[1])+F('.35')])
  reserved=[[max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3])]for a in map(Q,reserved)for b in map(Q,u['ownership'])if max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])]
  other=[q for role,rr in u['rooms'].items()if role not in('entry_circulation','living')for q in rr]
  physicalwalls=list(m['walls'].values())
  u['rooms']['entry_circulation']=cells(reserved,other+physicalwalls)
  u['rooms']['living']=cells(u['ownership'],other+physicalwalls+u['rooms']['entry_circulation'])
  u['public_floor_classification']={'source':'Final actual route/scenario body sweeps after all occupied-seat rerouting','route_geometry_hash':digest(paths),'not_a_new_physical_partition':True,'residual_not_claimed_useful_living':True}
  # Optional opening on first fitting physical host interval; no room ranking or admission requirement.
  edge=F('.25')if uid=='A'else L-F('.25');ivs=[(Q(r)[0],Q(r)[2])for r in u['rooms']['living']if (Q(r)[1]if uid=='A'else Q(r)[3])==edge];ivs.sort();merged=[]
  for a,b in ivs:
   if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
   else:merged.append((a,b))
  # Subtract actual fixture intervals touching the assumed open face; a
  # window is never placed behind one just because the room envelope is open.
  blockers=[Q(q)for q in u['fixtures'].values()if(Q(q)[1]if uid=='A'else Q(q)[3])==edge]
  for fx in blockers:
   free=[]
   for a,b in merged:
    if fx[2]<=a or fx[0]>=b:free.append((a,b))
    else:
     if a<fx[0]:free.append((a,fx[0]))
     if fx[2]<b:free.append((fx[2],b))
   merged=free
  if merged:
   a,b=next(((x,y)for x,y in merged if y-x>=F('.9')),merged[0]);avail=b-a-F('.2')
   if avail>=F('.7'):
    ww=min(F(2),avail);xx=(a+b-ww)/2;wr=[xx,0,xx+ww,F('.25')]if uid=='A'else[xx,L-F('.25'),xx+ww,L]
    m['concept_windows'].append({'id':uid+'.living.window','unit':uid,'room':uid+'.living','plan_rect':seq(wr),'host_wall_id':'front'if uid=='A'else'back','destination':{'edge':'bottom'if uid=='A'else'top'},'sill_m':'1.1','head_m':'2.1','floor_portal':False,'assumed_open_edge':True,'available_width_m':S(avail),'geometry_only_optional_opening':True})
 return m
