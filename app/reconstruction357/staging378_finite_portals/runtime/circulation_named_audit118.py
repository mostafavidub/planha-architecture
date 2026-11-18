"""IR-P13 / Q04 exact facts without invented compactness/length thresholds.
No producer pass, grouped-name or short/long flag is accepted as evidence.
"""
from fractions import Fraction as F
from core_wall_audit118 import q,sweep,hit,covered,output,safe

def measures(path):
 p=[tuple(map(F,x))for x in path];length=sum(abs(a[0]-b[0])+abs(a[1]-b[1])for a,b in zip(p,p[1:]));straight=abs(p[0][0]-p[-1][0])+abs(p[0][1]-p[-1][1]);directions=[]
 for a,b in zip(p,p[1:]):
  dx,dy=b[0]-a[0],b[1]-a[1]
  if dx and dy:raise ValueError('NONORTHOGONAL_ROUTE')
  if dx or dy:directions.append((0 if dx==0 else 1 if dx>0 else-1,0 if dy==0 else 1 if dy>0 else-1))
 return {'length_m':str(length),'unobstructed_manhattan_lower_bound_m':str(straight),'excess_over_lower_bound_m':str(length-straight),'direction_changes':sum(a!=b for a,b in zip(directions,directions[1:])),'lower_bound_is_not_feasible_alternative':True}
def area(rs):
 ys=sorted({v for r in rs for v in(r[1],r[3])});total=F(0)
 for y,Y in zip(ys,ys[1:]):
  intervals=sorted((r[0],r[2])for r in rs if r[1]<Y and y<r[3]);merged=[]
  for x,X in intervals:
   if merged and x<=merged[-1][1]:merged[-1]=(merged[-1][0],max(merged[-1][1],X))
   else:merged.append((x,X))
  total+=(Y-y)*sum(X-x for x,X in merged)
 return total

def intersection(a,b):return(max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3]))
@safe
def private_grouping(m):
 from paired_private_zone118 import examine as examine_pairs
 pairs=examine_pairs(m)
 findings=[];pending=[];errors=[]
 for u in m['units']:
  uid=u['id'];beds={uid+'.'+k for k in u['rooms']if k.startswith('bed')}
  if len(beds)<2:findings.append({'unit':uid,'applicability':'single bedroom'});continue
  if len(beds)>=3:
   from private_binding121 import examine as bind_private
   b=bind_private(m);errors.extend(b['errors']);pending.extend(b['pending'])
   if uid+'.private_access' not in b['regions']:pending.append(uid+':ACTUAL_MULTI_BED_DOMAIN_MISSING')
   findings.append({'unit':uid,'actual_typed_private_domain':b,'compactness_metric_claim':False});continue
  # A common REAL private hall can demonstrate grouping topology. It does not
  # prove minimum route length or globally optimal compactness.
  halls={uid+'.'+k for k in u['rooms']if k=='private_corridor'}
  graph={k:set()for k in beds|halls};outside=[]
  for o in m['openings']:
   links=o['connects']
   if len(links)!=2:continue
   a,b=links
   if a in graph and b in graph:graph[a].add(b);graph[b].add(a)
   elif a in graph or b in graph:outside.append({'opening':o['id'],'inside':a if a in graph else b,'outside':b if a in graph else a})
  seen=set();groups=[]
  for node in graph:
   if node in seen:continue
   todo=[node];group=[];seen.add(node)
   while todo:
    k=todo.pop();group.append(k)
    for v in graph[k]-seen:seen.add(v);todo.append(v)
   groups.append(sorted(group))
  groups.sort() # Canonical unordered connected components; route/path ordering untouched.
  grouped=len(groups)==1 and halls and len(outside)==1 and outside[0]['inside']in halls
  physical_pairs=[p for p in pairs['zones']if p['unit']==uid and p['status']=='PASS_TWO_BEDROOM_PRIVATE_APPROACH_TOPOLOGY'and set(p['bedrooms'])==beds]
  paired=bool(physical_pairs)
  grouped=bool(grouped or paired)
  # Same-model opening-host audit separately proves graph edges geometrically.
  if not grouped:pending.append(uid+':PRIVATE_GROUPING_NEEDS_REAL_COMMON_PRIVATE_ZONE_OR_BOUND_ALTERNATIVE_COMPARISON')
  findings.append({'unit':uid,'bedroom_nodes':sorted(beds),'actual_private_hall_nodes':sorted(halls),'physical_opening_components':groups,'public_interfaces':outside,'single_entry_private_group_topology':bool(grouped),'actual_paired_approach_proof':physical_pairs,'compactness_metric_claim':False})
 return output('IR-P13',errors,pending,{'units':findings,'source_line':4008,'required_comparison_if_scattered':['Same site/unit-count/bed and furniture program alternative actual model','Each bedroom-to-bath, entry and public route, lengths/bends/free body passage','Explicit functional reason for selection and retained trade-offs; no producer PASS flag accepted'],'scope_limit':'Grouped topology alone does not approve long corridors, closet orientation, room proportions or all IR-P13 subconditions.'})
@safe
def long_corridor_facts(m):
 rows=[];body=F(str(m['profile']['body_m']))
 for u in m['units']:
  paths={**u['routes'],**{'scenario:'+k:v for k,v in u.get('scenario_routes',{}).items()}}
  footprints=[r for p in paths.values()for r in sweep(p,body)];dedicated=[q(r)for r in u['rooms'].get('entry_circulation',[])];public=[q(r)for k in('living','dining')for r in u['rooms'].get(k,[])]
  overlap=[intersection(a,b)for a in footprints for b in dedicated if hit(a,b)];inpublic=[intersection(a,b)for a in footprints for b in public if hit(a,b)]
  rows.append({'unit':u['id'],'routes':{k:measures(v)for k,v in paths.items()},'all_route_body_union_m2':str(area(footprints)),'route_inside_designated_circulation_m2':str(area(overlap)),'route_inside_living_or_dining_m2':str(area(inpublic)),'regions_may_overlap_and_are_not_added':True})
 return output('Q04',[],['LONG_CORRIDOR_APPLICABILITY_AND_COMPARATIVE_NECESSITY_NOT_YET_BOUND'],{'units':rows,'source_line':7,'no_numeric_length_threshold_invented':True,'required_next_evidence':['Actual same-program alternative with fresh routes, not Manhattan lower bound','Record functional differences and why current route is necessary; retain comparison outcomes','Corridor applicability cannot be supplied as an unsupported long=false flag']})

@safe
def circulation_domains(m):
 """Distinguish physical common corridor from swept analytical circulation.
 Neither a room label nor a numerical ratio classifies a corridor as 'long'.
 """
 domains=[];hosts=[q(r)for r in m['wall_hosts'].values()];common=m['common_spaces'];lobby=[q(r)for r in common['lobby']];paths=m['common_routes']
 for i,r in enumerate(lobby):
  x,y,X,Y=r;boundaries=[]
  for side,axis,value,span in [('bottom',1,y,(x,X)),('top',1,Y,(x,X)),('left',0,x,(y,Y)),('right',0,X,(y,Y))]:
   intervals=[]
   for h in hosts:
    if h[axis]<=value<=h[axis+2]:
     a=max(span[0],h[1-axis]);b=min(span[1],h[3-axis])
     if a<b:intervals.append((a,b))
   intervals.sort();merged=[]
   for a,b in intervals:
    if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
    else:merged.append((a,b))
   boundaries.append({'side':side,'full_source_host_boundary':len(merged)==1 and merged[0]==span})
  bounded={z['side']for z in boundaries if z['full_source_host_boundary']}
  domains.append({'domain':'common_lobby_component_'+str(i),'actual_floor_rect':list(map(str,r)),'width_x_m':str(X-x),'height_y_m':str(Y-y),'opposed_horizontal_boundaries':{'bottom','top'}<=bounded,'opposed_vertical_boundaries':{'left','right'}<=bounded,'boundaries':boundaries,'common_routes_using_rect':[k for k,p in paths.items()if any(hit(r,s)for s in sweep(p,F(str(m['profile']['body_m']))))],'long_by_arbitrary_threshold':False})
 private=[]
 for u in m['units']:
  private.append({'unit':u['id'],'entry_circulation_representation':'Analytical floor pieces; name alone is NOT evidence of constructed/enclosed corridor','entry_circulation_union_m2':str(area([q(r)for r in u['rooms'].get('entry_circulation',[])]))})
 route_rows={k:measures(p)for k,p in paths.items()};differences={}
 for src in('stair','lift'):
  values=[F(route_rows[src+'_'+u['id']]['length_m'])for u in m['units']]
  differences[src+'_unit_access_length_difference_m']=str(max(values)-min(values))
 return output('Q04',[],['NO_SOURCE_NUMERIC_LONG_THRESHOLD; ACTUAL_CORE_ALTERNATIVE_COMPARISON_NEEDED_FOR_CURRENT_FULL_SPAN_BAND'],{'common_domains':domains,'unit_analytical_domains':private,'common_route_metrics':route_rows,'unit_access_differences':differences,'minimal_relevant_alternative':'Same raw W/L/n and stair/lift sizes and unit program; move lift adjacent to existing stair/entries, reconstruct its real walls/openings/common paths, fresh whole gates. This isolates needless endpoint separation; do not claim band-area reduction unless actual ownership/walls also changed.','stronger_alternative':'Compact shared core/lobby and reallocated actual unit floor with all functional/ownership/wall gates; not a decorative line or empty-floor relabel.','comparison_outside_scope':'Two furniture variants with unchanged opposite-end stair/lift do not test this common corridor cause.'})
