"""Independent exact final-route analytical floor classification.
This does not make the residual living label evidence of useful capacity.
"""
from fractions import Fraction as F
from space_accounting118 import rect,merge,subtract,overlap,route_rectangles

def evaluate(m):
 errors=[];rows=[]
 try:
  body=F(str(m['profile']['body_m']))
  if body!=F('.7'):raise ValueError('BODY_PROFILE_CHANGED')
  walls=list(map(rect,m['walls'].values()))
  for u in m['units']:
   groups={'owner':list(map(rect,u['ownership'])),'wall':walls,'fixed':[rect(r)for k,rs in u['rooms'].items()if k not in('entry_circulation','living')for r in rs], 'route':[], 'entry':list(map(rect,u['rooms']['entry_circulation'])),'living':list(map(rect,u['rooms']['living']))}
   paths={**u['routes'],**{'scenario:'+k:v for k,v in u.get('scenario_routes',{}).items()}}
   for p in paths.values():groups['route']+=route_rectangles(p,body)
   ys=sorted({v for rs in groups.values()for r in rs for v in(r[1],r[3])});wrong_entry=F(0);wrong_living=F(0);actual_entry=F(0);expected_entry=F(0)
   for y,Y in zip(ys,ys[1:]):
    mid=(y+Y)/2;iv={k:merge((r[0],r[2])for r in rs if r[1]<mid<r[3])for k,rs in groups.items()}
    available=subtract(iv['owner'],merge(iv['fixed']+iv['wall']));want_entry=overlap(available,iv['route']);want_living=subtract(available,want_entry)
    def length(rs):return sum((b-a for a,b in rs),F(0))
    wrong_entry+=(length(subtract(iv['entry'],want_entry))+length(subtract(want_entry,iv['entry'])))*(Y-y)
    wrong_living+=(length(subtract(iv['living'],want_living))+length(subtract(want_living,iv['living'])))*(Y-y)
    actual_entry+=length(iv['entry'])*(Y-y);expected_entry+=length(want_entry)*(Y-y)
   if wrong_entry:errors.append({'unit':u['id'],'code':'ENTRY_CLASSIFICATION_NOT_FINAL_ROUTE_UNION','symmetric_difference_m2':str(wrong_entry)})
   if wrong_living:errors.append({'unit':u['id'],'code':'PUBLIC_REMAINDER_NOT_FINAL_ROUTE_COMPLEMENT','symmetric_difference_m2':str(wrong_living)})
   rows.append({'unit':u['id'],'actual_entry_area_m2':str(actual_entry),'final_route_entry_area_m2':str(expected_entry),'entry_difference_m2':str(wrong_entry),'living_difference_m2':str(wrong_living),'final_paths':len(paths)})
 except (KeyError,TypeError,ValueError,IndexError)as ex:errors.append({'code':'FINAL_ROUTE_LEDGER_SCHEMA','detail':str(ex)})
 return {'status':'FAIL'if errors else'PASS_LIMITED','witness':{'errors':errors,'pending':[],'units':rows,'residual_useful_capacity_proven':False},'scope':'Exact union of final .7 body routes including scenarios, intersected with actual ownership and excluding fixed functional rooms/physical walls. Remaining public floor is not automatically useful living, necessary circulation or physical dead corridor.'}
