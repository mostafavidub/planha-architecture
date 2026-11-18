"""Measurements while B18 safety gate remains UNKNOWN. No substitute gate."""
from build_ledger import *
from comparison_metrics import route_metrics
from fractions import Fraction as F

def run():
 old=json.loads(Path(__file__).with_name('bound_comparison_actual358.json').read_text()); models={}
 for member in old['members']:
  p=ROOT/member['artifact'];assert hashlib.sha256(p.read_bytes()).hexdigest()==member['artifact_sha256'];x=json.loads(p.read_text());models[member['id']]=x['selected'][0]['model']if member['id']=='baseline351'else x['candidate']['model']
 record=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text());c=record['candidate'];models['clamped359']=c['model'];assert digest(c)==record['trace']['candidate_digest'];assert digest(c['model'])==record['trace']['model_digest']
 raw=json.loads((ROOT/'review359_source_validation/result.json').read_text());assert raw['input_record_digest']==digest(record) and raw['model_digest']==digest(c['model'])
 eligibility=json.loads((ROOT/'semantic_rules357/eligibility_intrinsic_actual359.json').read_text())
 out={'schema':'Q04_SOURCE359_MEASUREMENT_PENDING_UNMODIFIED_B18_SAFETY_GATE','model_digest':digest(c['model']),'fresh_result_digest':digest(raw),'eligibility_evidence_digest':digest(eligibility),'eligibility_verdict':eligibility['verdict'],'eligibility_missing':eligibility.get('missing'),'comparison_authorized_as_complete':False,'rule_acceptance':False,'protected_measurements':{},'candidate_metrics':{},'pair_measurements':[],'required_source233_subclaims':['all exclusive circulation components and target purposes','actual per-target lengths/turns/bottlenecks/area','closed source-supported finite alternatives with eligibility','componentwise protected-function comparison'],'still_pending':['B18 safety gate remains unmodified; no alternate eligibility substitute','source-profile bottleneck measurement coverage','independent finite branch closure audit']}
 for k,m in models.items():out['candidate_metrics'][k]={'model_digest':digest(m),'metrics':measure_model(m)}
 for name,m in models.items():
  if name=='clamped359':continue
  now=models['clamped359'];pres={'program_equal':m['program']==now['program'],'profile_equal':m['profile']==now['profile'],'units':[]};pairs=[]
  for u in m['units']:
   v=next(v for v in now['units']if v['id']==u['id']);pres['units'].append({'unit':u['id'],'ownership_equal':u['ownership']==v['ownership'],'fixture_ID_inventory_equal':set(u['fixtures'])==set(v['fixtures']),'activity_ID_inventory_equal':set(u['activities'])==set(v['activities']),'fixture_geometry_equal':u['fixtures']==v['fixtures'],'activity_geometry_equal':u['activities']==v['activities'],'bedroom_geometry_equal':{k:r for k,r in u['rooms'].items()if k.startswith('bed')}=={k:r for k,r in v['rooms'].items()if k.startswith('bed')}})
   am=out['candidate_metrics'][name]['metrics']['units'][u['id']];bm=out['candidate_metrics']['clamped359']['metrics']['units'][u['id']]
   pairs.append({'unit':u['id'],'metric':'declared_circulation_union_m2','old':am['declared_circulation_union_m2'],'current':bm['declared_circulation_union_m2'],'delta':str(F(bm['declared_circulation_union_m2'])-F(am['declared_circulation_union_m2']))})
   for target in sorted(set(u['routes'])&set(v['routes'])):
    if target not in u['route_targets']or target not in v['route_targets']:continue
    a,b=route_metrics(u['routes'][target]),route_metrics(v['routes'][target])
    for metric in ['length','direction_changes']:pairs.append({'unit':u['id'],'target':target,'metric':metric,'old':a[metric],'current':b[metric],'delta':str(F(b[metric])-F(a[metric]))})
  out['protected_measurements'][name]=pres;out['pair_measurements'].append({'baseline':name,'current':'clamped359','dimensions':pairs,'improved_count':sum(F(p['delta'])<0 for p in pairs),'worsened_count':sum(F(p['delta'])>0 for p in pairs),'equal_count':sum(F(p['delta'])==0 for p in pairs),'dominance_status':'NOT_ADJUDICATED_B18_PENDING_NO_GATE_BYPASS'})
 purposepath=ROOT/'semantic_rules357/circulation_role_actual359.json';purpose=json.loads(purposepath.read_text());assert purpose['model_hash']==digest(c['model']) and purpose['record_digest']==digest(record);out['component_purpose_artifact']={'path':str(purposepath.relative_to(ROOT)),'sha256':hashlib.sha256(purposepath.read_bytes()).hexdigest(),'data':purpose,'scope':'INDEPENDENT_INTRINSIC_PURPOSE_NOT_B18_SUBSTITUTE'}
 Path(__file__).with_name('q04_measurement_actual359.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print([(p['baseline'],p['improved_count'],p['worsened_count'],p['equal_count'])for p in out['pair_measurements']]);return out
if __name__=='__main__':run()
