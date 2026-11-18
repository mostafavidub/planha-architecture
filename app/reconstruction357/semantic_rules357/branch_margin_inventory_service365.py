"""Source-port reservation inventory; does not equate reserved margin to whole-hall necessity."""
import json
from pathlib import Path
from common import digest
from modules_spatial import rect,difference,intersection,union_area
from guest_closure import transformed_rect
from circulation_role_service365 import evaluate as circulation
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record,review):
 prior=circulation(record,review);m=record['candidate']['model'];out=[]
 for ur in prior['units']:
  uid=ur['unit'];u=next(u for u in m['units']if u['id']==uid);private=list(map(rect,u['rooms']['private_circulation']));ports=[]
  for p in m['module_placements']:
   if p['unit_id']!=uid or not p['room_id'].startswith('bed'):continue
   if digest(p['module'])!=p['module_hash']:raise ValueError('MODULE_HASH')
   for src in p['module']['external_ports']:
    oid=p['id_map'][src['opening_id']];actual=[x for x in m['module_ports']if x['opening_id']==oid]
    if len(actual)!=1 or transformed_rect(src['rect'],p['transform'])!=rect(actual[0]['rect']):raise ValueError('SOURCE_PORT_GEOMETRY')
    q=rect(actual[0]['rect']);clips=[z for v in private if(z:=intersection(q,v))]
    ports.append({'opening_id':oid,'source_module_hash':p['module_hash'],'source_port_digest':digest(src),'actual_port_digest':digest(actual[0]),'source_port_region':list(map(str,q)),'private_intersection':[list(map(str,z))for z in clips],'scope':'Source reserved approach attached to an actually checked bedroom opening. Candidate valid supporting margin, not blanket whole-hall purpose.'})
  residual=[rect(x)for c in ur['private_circulation_components']for x in c['unsupported_margin_regions']];allow=[rect(x)for p in ports for x in p['private_intersection']];remaining=difference(residual,allow)
  out.append({'unit':uid,'source_ports':ports,'before_source_port_intersection_m2':str(union_area(residual)),'outside_source_port_and_measured_use_m2':str(union_area(remaining)),'outside_regions':[list(map(str,x))for x in remaining],'whole_role_complete':False})
 return {'schema':'SERVICE365_EXACT_BRANCH_SOURCE_PORT_MARGIN_INVENTORY','model_digest':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'circulation_digest':digest(prior),'units':out,'scope':'Current fresh prerequisite and exact module-port joins. Outside regions remain UNKNOWN, not proven useless; no global necessity or parent PASS.','fresh_execution':False,'admission_allowed':False}
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());v=json.loads((ROOT/'review365_service_source_validation/result.json').read_text());print(json.dumps(evaluate(r,v),indent=2))
