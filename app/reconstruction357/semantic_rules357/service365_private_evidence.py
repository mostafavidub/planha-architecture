"""Own service branch sections/task paths, not row equivalence or parent approval."""
import json,hashlib,time
from pathlib import Path
P=Path(__file__).resolve().parent
from common import digest
from group_readsets_service365 import build
from bedroom_sections358 import measure
from bedroom_route_witness358 import validate_model

def evaluate(record,result):
 pins=json.loads((P/'service365_private_evidence_pins.json').read_text())
 def check():
  for n,h in pins['files'].items():
   if hashlib.sha256((P/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED:'+n)
 check();view=build(record,result);m=view['envelope']['packet']['world_model'];before=digest(m);start=time.monotonic();rows=[];cache={}
 for rec in m['module_placements']:
  if not rec['room_id'].startswith('bed'):continue
  h=digest(rec['module'])
  if rec['module_hash']!=h:raise ValueError('MODULE_HASH')
  if h not in cache:cache[h]=measure(rec['module'])
  rows.append({'unit':rec['unit_id'],'room':rec['room_id'],'module_digest':h,'sections':cache[h]})
 if len(rows)!=6 or len({(x['unit'],x['room'])for x in rows})!=6:raise ValueError('SIX_SOURCE_ROOMS_REQUIRED')
 routes=validate_model(m,time.monotonic()+10)
 check()
 if digest(m)!=before:raise ValueError('MODEL_MUTATION')
 return {'schema':'SERVICE365_PRIVATE_SOURCE_EVIDENCE','model_digest':before,'rows':rows,'unique_source_modules':len(cache),'task_routes':routes,'elapsed':time.monotonic()-start,'parent_complete':False,'accepted':False,'delivery_allowed':False,'missing':['OWN_BRANCH_ELONGATION_CLOSET_SELECTION_RATIONALE','FINITE_NONCOMPENSATORY_ROOM_AREA_AND_ROUTE_TRADEOFF_REVIEW'],'scope':'EXACT_OWN_SOURCE_ROOM_RESERVATIONS_AND_OPEN_TRANSIT_TASK_PATHS; NOT_ROW_SECTION_EQUIVALENCE_OR_GLOBAL_OPTIMUM'}
