"""Current362 exact route/circulation comparative ledger, not a verdict shortcut."""
from q04_closure359 import dimensions,ROOT,digest,json,Path,F,rectangle_union_area
from branch_registry362 import build as registry

def objective(m):
 d=dimensions(m);d['COMMON/lobby_floor_m2']=rectangle_union_area(m['common_spaces']['lobby']);return d

def compare(a,b):
 x,y=objective(a),objective(b)
 worse=[{'metric':k,'current':str(x[k]),'alternative':str(y[k]),'increase':str(y[k]-x[k])}for k in sorted(x.keys()&y.keys())if y[k]>x[k]]
 return {'dominance':'FALSE'if worse else'UNKNOWN','negative_witnesses':worse,'same_metric_inventory':set(x)==set(y),'missing_dimensions':sorted(x.keys()^y.keys()),'known_strictly_better_alternative_dimensions':[k for k in sorted(x.keys()&y.keys())if y[k]<x[k]],'unknown_other_metrics_not_passed':True}

def build():
 record=json.loads((ROOT/'staging362_core_notch/actual362.json').read_text());m=record['candidate']['model'];rows=[]
 for name,path,selected in [('baseline351','actual_run/actual_response.json',True),('translated357','staging357_comparative/attached_service_final357.json',False),('row358','staging358_comparative/row_candidate358.json',False),('clamped359','staging359_hall_clamp/actual359.json',False)]:
  r=json.loads((ROOT/path).read_text());c=r['selected'][0]if selected else r['candidate'];a=c['model'];assert c['request']==record['candidate']['request']and a['program']==m['program']and a['profile']==m['profile']
  rows.append({'alternative':name,'model_digest':digest(a),'comparison':compare(m,a)})
 return {'schema':'Q04_CURRENT362_MEASURED_NEGATIVE_OBJECTIVES','model_digest':digest(m),'record_digest':digest(record),'objective_source_map':{'per_unit_circulation':'actual unit circulation rectangles, exact union; Q04 circulation necessity cost','route_length_and_turns':'actual source entry-to-required-target bound paths; engineering componentwise nondeterioration','common_lobby_floor':'actual common_spaces.lobby exact floor union; source Q04 common circulation/core-cost scope, not a proof of its useful function'},'branches':registry(),'comparisons':rows,'current_objectives':{k:str(v)for k,v in objective(m).items()},'accepted':False,'remaining':['CURRENT362_INTRINSIC_GATE','CURRENT362_PURPOSE_CLOSURE','INDEPENDENT_FINITE_DOMAIN_AUDIT'],'negative_witness_scope':'A known strictly worse contractual cost refutes componentwise dominance; unmeasured metrics stay unknown; no global optimum.'}
if __name__=='__main__':
 out=build();Path(__file__).with_name('q04_measurement_actual362.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print([(r['alternative'],r['comparison']['dominance'],r['comparison']['negative_witnesses'][:1])for r in out['comparisons']])
