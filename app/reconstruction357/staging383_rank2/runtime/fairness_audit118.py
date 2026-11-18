"""Q12: per-unit measured vector, no average or fabricated quality score."""
from fractions import Fraction as F
from checker114 import digest
from space_accounting118 import ledger

def worst_unit_function(m):
 from program_capacity_audit118 import examine
 p=examine(m);errors=list(p['errors']);pending=list(p['pending']);cap={u['unit']:u for u in p['evidence']['units']}
 l=ledger(m);account={u['unit']:u for u in l['witness']['units']};rows=[]
 if l['errors']:errors.extend(l['errors'])
 if set(cap)!={u['id']for u in m['units']}:pending.append('PER_UNIT_CAPACITY_VECTOR_INCOMPLETE')
 for u in m['units']:
  uid=u['id'];lengths={k:sum(abs(F(a[0])-F(b[0]))+abs(F(a[1])-F(b[1]))for a,b in zip(path,path[1:]))for k,path in u['routes'].items()}
  windows=[w for w in m['concept_windows']if w['unit']==uid]
  rows.append({'unit':uid,'capacity':cap.get(uid),'measured_floor_areas_m2':account.get(uid,{}).get('areas_m2'),'bedroom_count':sum(k.startswith('bed')for k in u['rooms']),'declared_activity_route_lengths_m':{k:str(v)for k,v in lengths.items()},'longest_declared_route_m':str(max(lengths.values(),default=F(0))),'window_contacts':[{k:w[k]for k in('id','room','destination','plan_rect')}for w in windows],'front_orientation_is_assumed_not_actual_north':True,'overall_spatial_quality':'NOT_VERIFIED','daylight_ventilation':'NOT_VERIFIED','independent_other_mandatory_checks':'Separately required for every unit by named whole-model gate; no average substitutes for failure'})
 measured={}
 if rows:
  margins={r['unit']:r['capacity']['worst_capacity_margin']for r in rows if r['capacity']}
  lengths={r['unit']:F(r['longest_declared_route_m'])for r in rows}
  unknown={r['unit']:F(r['measured_floor_areas_m2']['unaccounted_declared_floor'])for r in rows if r['measured_floor_areas_m2']}
  for name,vals,mode in [('capacity_margin',margins,'min'),('longest_declared_route_m',lengths,'max'),('unaccounted_declared_floor_m2',unknown,'max')]:
   if vals:
    v=(min if mode=='min'else max)(vals.values());measured[name]={'worst_observed_value':str(v),'units_at_value':[k for k,x in vals.items()if x==v],'spread':str(max(vals.values())-min(vals.values())),'not_a_quality_or_necessity_threshold':True}
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','witness':{'model_hash':digest(m),'units':rows,'worst_measured_vectors':measured,'errors':errors,'pending':pending,'averaging_used':False},'scope':'Q12 reporting: every actual unit and worst measured capacity/route/unaccounted-floor value; differences in hypothetical frontage retained. No overall fairness or architectural-quality approval. All other named functional conditions remain separately mandatory, failures cannot be averaged away.'}
