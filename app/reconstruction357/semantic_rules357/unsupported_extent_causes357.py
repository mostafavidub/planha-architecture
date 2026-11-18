"""Exact generic diagnostics on measured unsupported floor, not blanket FAIL."""
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,union_area,intersection
from wall_purpose import touches

def uncovered(interval,covered):
 segs=[interval]
 for a,b in covered:
  nxt=[]
  for x,y in segs:
   if b<=x or a>=y:nxt.append((x,y));continue
   if x<a:nxt.append((x,a))
   if b<y:nxt.append((b,y))
  segs=nxt
 return segs

def boundary_openings(component,solids):
 out=[]
 for i,q in enumerate(component):
  for axis in(0,1):
   other=1-axis
   for side in(0,2):
    coordinate=q[axis+side];span=(q[other],q[other+2]);covered=[]
    for j,b in enumerate(component):
     if i!=j and b[axis+(2 if side==0 else 0)]==coordinate:covered.append((b[other],b[other+2]))
    for b in solids:
     if b[axis]<=coordinate<=b[axis+2]:covered.append((b[other],b[other+2]))
    for a,b in uncovered(span,covered):out.append({'axis':axis,'coordinate':str(coordinate),'span':[str(a),str(b)],'width_m':str(b-a)})
 return out

def evaluate(model,support):
 if support['model_hash']!=digest(model):raise ValueError('SUPPORT_MODEL_BINDING')
 out={'schema':'UNSUPPORTED_EXTENT_CAUSES357','model_hash':digest(model),'support_digest':digest(support),'units':[],'parent_complete':False,'geometry_mutated':False}
 for row in support['rows']:
  u=next(u for u in model['units']if u['id']==row['unit']);qs=list(map(rect,row['unresolved_regions']));left=set(range(len(qs)));components=[];body=F(model['profile']['body_m'])
  while left:
   first=min(left);left.remove(first);seen=[first];todo=[first]
   while todo:
    i=todo.pop()
    for j in list(left):
     if touches(qs[i],qs[j])or intersection(qs[i],qs[j]):left.remove(j);seen.append(j);todo.append(j)
   c=[qs[i]for i in seen];openings=boundary_openings(c,list(map(rect,model['walls'].values())));box=(min(q[0]for q in c),min(q[1]for q in c),max(q[2]for q in c),max(q[3]for q in c));thin=min(box[2]-box[0],box[3]-box[1])<body
   kind='SOLID_ENCLOSED_FLOOR_ISLAND'if not openings else'BLIND_STRIP_BELOW_SOURCE_BODY'if thin else'UNRESOLVED_ROLE_OR_CONFIGURATION_SPACE_GAP'
   adjacent_walls=[k for k,v in model['walls'].items()if any(touches(q,rect(v))for q in c)];adjacent_fixtures=[k for k,v in u['fixtures'].items()if any(touches(q,rect(v))for q in c)]
   components.append({'fragment_indices':sorted(seen),'regions':[list(map(str,q))for q in c],'area_m2':str(union_area(c)),'classification':kind,'source_body_m':str(body),'bounding_width_depth_m':[str(box[2]-box[0]),str(box[3]-box[1])],'wall_boundary_openings':openings,'actual_adjacent_wall_ids':adjacent_walls,'actual_adjacent_fixture_ids':adjacent_fixtures,'evidence_scope':'Exact unsupported component geometry and actual solid enclosure/width. Does not prove absence of every conceivable other activity.'})
  out['units'].append({'unit':u['id'],'fragment_count':len(qs),'unsupported_area_m2':str(union_area(qs)),'components':components})
 out['producer_constraints']=[{'id':'SOURCE_BUNDLE_NO_SEALED_PUBLIC_RESIDUAL','constraint':'After constructing immutable private modules and hallway, compute owned residual floor components with actual walls; reject proposals containing solid-enclosed residual counted as public useful floor unless an independently verified source function serves it.','scope':'No re-labeling or arbitrary wall removal; change eligible source topology/placement then full functional recheck.'},{'id':'SOURCE_SEATING_REACHABLE_GAP_OR_FLUSH','constraint':'Between actual source seating compounds and enclosing walls/fixtures, require a source-function witness, or a full source-body configuration-space connection; otherwise revise compound placement with its activity intact. Flush only when permitted by source operation profile.','scope':'0.7m applies only to current pinned body profile; no new universal rule, fixture shrinking or deleted activity.'}]
 return out
if __name__=='__main__':
 import json
 from pathlib import Path
 p=Path(__file__).resolve().parent;r=json.loads((p.parent/'staging357_comparative/attached_service_final357.json').read_text());s=json.loads((p/'support_identity_actual357.json').read_text());o=evaluate(r['candidate']['model'],s);(p/'unsupported_extent_causes_actual357.json').write_text(json.dumps(o,indent=2));print([(r['unit'],[(c['classification'],c['area_m2'])for c in r['components']])for r in o['units']])
