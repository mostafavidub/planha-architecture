"""Exact negative witnesses for a newly defined finite Q04 partial order.
No positive dominance/necessity/parent acceptance is produced.
"""
from build_ledger import *
from comparison_metrics import route_metrics
from operationalization import partial_dominance
from fractions import Fraction as F

def run():
 ledger=json.loads(Path(__file__).with_name('bound_comparison_actual358.json').read_text()); models={}
 for row in ledger['members']:
  p=ROOT/row['artifact'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['artifact_sha256'];x=json.loads(p.read_text());c=x['selected'][0] if row['id']=='baseline351'else x['candidate'];m=c['model'];assert digest(m)==row['model_digest'];models[row['id']]=m
 out={'schema':'ENGINEERING358_EXACT_NEGATIVE_DOMINANCE_WITNESSES','canonical_PARETO_CIRC':False,'whole_Q04_acceptance':False,'finite_branch_coverage_proven':False,'component_purpose_proven':False,'pairs':[],'source_authority':{'section':'Q04','selector':'details > summary[text=Q04]','html_character_range':[447999,464629],'sha256':'046cb8490a0865b74a9f844fa7db513490c50393e21923d1aa458f846fa89108','derived_metric':'actual entry-to-required-function path length and turns','engineering_assumption':'componentwise nondeterioration for each same source target/scenario, no averaging; at least one strict objective improvement'}}
 for aid,a in models.items():
  for bid,b in models.items():
   if aid==bid:continue
   found=None
   for au in a['units']:
    bu=next(u for u in b['units']if u['id']==au['id'])
    for target in sorted(au['route_targets']):
     if target not in bu['route_targets'] or target not in au['routes']or target not in bu['routes']:continue
     ap,bp=au['routes'][target],bu['routes'][target]
     if ap[0]!=au['entry_point']or bp[0]!=bu['entry_point']or ap[-1]!=au['route_targets'][target]or bp[-1]!=bu['route_targets'][target]:continue
     am,bm=route_metrics(ap),route_metrics(bp)
     for metric,key in [('path_length_m','length'),('turn_count','direction_changes')]:
      if F(bm[key])<=F(am[key]):continue
      definition={'metric':metric,'role':'objective','unit':au['id'],'scenario':'DECLARED_SOURCE_ENTRY_TO_FUNCTION:'+target,'source_pointer':'rendered233/Q04/actual-per-target-lengths-turns'}
      defs={'witness':definition,'unmeasured_protected_function':{'metric':'functional_capacity','role':'protected','unit':au['id'],'scenario':'ALL_APPLICABLE_SOURCE_STATES','source_pointer':'rendered233/Q04/preserved-functions'}}
      ar={'value':am[key],'definition':definition,'readset_digest':digest(a)};br={'value':bm[key],'definition':definition,'readset_digest':digest(b)}
      found={'unit':au['id'],'target':target,'metric':metric,'baseline_value':am[key],'alternative_value':bm[key],'increase':str(F(bm[key])-F(am[key])),'baseline_path':ap,'alternative_path':bp,'baseline_model_digest':digest(a),'alternative_model_digest':digest(b),'baseline_target':au['route_targets'][target],'alternative_target':bu['route_targets'][target],'target_identity_scope':'same source role ID under matched program/profile; geometric locations may differ','logic':partial_dominance({'witness':ar},{'witness':br},defs)};break
     if found:break
    if found:break
   out['pairs'].append({'baseline':aid,'alternative':bid,'state':'DOMINANCE_REFUTED_BY_EXACT_OBJECTIVE' if found else 'UNKNOWN','witness':found})
 Path(__file__).with_name('negative_dominance_actual358.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print([(p['baseline'],p['alternative'],p['witness']['target'],p['witness']['baseline_value'],p['witness']['alternative_value'])for p in out['pairs']])
 return out
if __name__=='__main__':run()
