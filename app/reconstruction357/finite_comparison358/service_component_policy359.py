"""Engineering operationalization: source-clearance vs dedicated circulation.
Bound B18 prerequisites required separately; result here is geometry and source
relation evidence, not live authority or a new universal service percentage.
"""
from service_roles_measurement import *
from circulation_role358 import components
from modules_spatial import intersection
from guest_closure import transformed_rect

def classify(m,measured):
 results=[]
 for r in measured:
  uid=r['unit'];u=next(u for u in m['units']if u['id']==uid);p=next(p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath')
  approach=[transformed_rect(q,p['transform'])for q in p['module']['unit']['rooms']['public_access']];actual=[rect(q)for q in m['module_aprons'][uid+'.bath']]
  if difference(approach,actual)or difference(actual,approach):raise ValueError('SOURCE_APPROACH_EXACT_TRANSFORM')
  opening=[o for o in m['openings']if o['id']==uid+'.bath'];assert len(opening)==1
  # Actual opening must bind mapped source opening, not arbitrary extra cover.
  old=next(o for o in p['module']['openings']if p['id_map'].get(o['id'])==uid+'.bath');assert transformed_rect(old['rect'],p['transform'])==rect(opening[0]['rect'])
  sole=[rect(q)for q in r['observed_service_only_regions']];unassigned=difference(sole,approach+[rect(opening[0]['rect'])])
  ss=set(r['service_target_ids']);routes={k:source_sweeps(path,F(m['profile']['body_m']))for k,path in u['routes'].items()};cr=[]
  for c in components([rect(q)for q in u['rooms']['entry_circulation']]):
   targetset=sorted(k for k,sweeps in routes.items()if any(intersection(a,b)for a in c for b in sweeps))
   service=set(targetset)&ss;other=set(targetset)-ss
   if not service:continue
   cr.append({'regions':[list(map(str,q))for q in c],'area_m2':str(union_area(c)),'served_service_targets':sorted(service),'served_nonservice_targets':sorted(other),'actual_sharing_witness':bool(other),'classification':'SHARED_ACTUAL_REQUIRED_ROUTE_COMPONENT'if other else 'SERVICE_ONLY_COMPONENT_REQUIRES_CLEARANCE_RECONCILIATION'})
  results.append({'unit':uid,'source_module_hash':p['module_hash'],'source_approach_exact_transform':True,'real_opening_source_binding':True,'observed_service_only_area_m2':r['observed_service_only_sweep_m2'],'unassigned_after_source_clearance_m2':str(union_area(unassigned)),'unassigned_regions':[list(map(str,q))for q in unassigned],'components':cr,'engineering_definition':'Dedicated exclusive service circulation is a connected assigned circulation component serving only source service targets, outside required source bundle use/operation/approach and real threshold footprints. Sharedness requires actual nonservice source-target traversal, not a room label.','dedicated_component_verdict':'NO_ADDITIONAL_OBSERVED_COMPONENT'if not unassigned and all(x['actual_sharing_witness']for x in cr) else 'UNKNOWN_COMPONENT_SCOPE','whole_floor_purpose_or_universal_minimum_proven':False})
 return results
if __name__=='__main__':
 from modules_spatial import intersection
 src=json.loads(Path(__file__).with_name('service_roles_actual359.json').read_text());out={'schema':'ENGINEERING_SERVICE_COMPONENT359_SOURCE_RELATIONS','parent_acceptance':False,'models':{}}
 for k,path in [('baseline351','actual_run/actual_response.json'),('translated357','staging357_comparative/attached_service_final357.json'),('row358','staging358_comparative/row_candidate358.json')]:
  x=json.loads((ROOT/path).read_text());m=x['selected'][0]['model']if k=='baseline351'else x['candidate']['model'];assert digest(m)==src['models'][k]['model_digest'];out['models'][k]={'model_digest':digest(m),'rows':classify(m,src['models'][k]['rows'])}
 Path(__file__).with_name('service_component_actual359.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print([(k,[(r['unit'],r['dedicated_component_verdict'],len(r['components']))for r in v['rows']])for k,v in out['models'].items()])
