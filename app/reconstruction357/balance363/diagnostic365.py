"""One independent artifact-only diagnostic. Never invokes SOURCE362 authority."""
import json,hashlib,time
from pathlib import Path
from assessor import ROOT,model_route,digest

def run():
 p=ROOT/'staging365_balanced_portals/actual365.json';r=json.loads(p.read_text());c=r['candidate'];t=r['trace'];m=c['model']
 if digest(m)!=t['model_digest']or digest(m)!=c['model_digest']or digest(c)!=t['candidate_digest']or digest(c['packet']['world_model'])!=digest(m):raise ValueError('CURRENT365_BINDING')
 for name,h in t['source_inventory'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('PRODUCER_SOURCE_DRIFT:'+name)
 g=ROOT/'review365_balanced_diagnostic/geometry_operations_privacy.json';diagnostic=json.loads(g.read_text());rows=[]
 for route in sorted(m['common_routes']):
  try:rows.append(model_route(m,route))
  except (ValueError,KeyError,TypeError)as e:rows.append({'route_id':route,'verdict':'UNKNOWN','reason':str(e)})
 return {'schema':'BALANCED365_FIXED_PATH_SQUARE_CAPACITY_DIAGNOSTIC_ONLY','model_digest':digest(m),'record_digest':digest(r),'record_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'profile':m['profile'],'rows':rows,'prior_primitive_diagnostic':{'path':str(g.relative_to(ROOT)),'sha256':hashlib.sha256(g.read_bytes()).hexdigest(),'result':diagnostic},'fresh_executed':False,'source362_review_borrowed':False,'eligibility':'NOT_ESTABLISHED; primitive operation/privacy evidence retained, no full fresh or eligibility','accepted':False,'balance_accepted':False,'scope':'Exact current model365 fixed-path square-body capacity under static plus fully-open entry passage only; primitive operation/privacy checks do not establish full eligibility; no all-state clearance claim.'}
if __name__=='__main__':
 x=run();p=Path(__file__).with_name('fixed_path_square_capacity_diagnostic365.json');assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2));print([(a['route_id'],a.get('fully_open_entry_passage_square_capacity',{}).get('max_axis_aligned_square_width_m'),a.get('reason'))for a in x['rows']])
