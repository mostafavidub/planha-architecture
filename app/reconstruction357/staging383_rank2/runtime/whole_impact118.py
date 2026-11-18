"""Read-only exact before/after whole-model impact accounting."""
import json
from pathlib import Path
from fractions import Fraction as F
from contract114 import digest
P=Path(__file__).resolve().parent
out=[]
for case in (1,2):
 before=json.loads((P/f'evidence/general118_changed_case{case}.json').read_text())['internal_proposals'][0]['model']
 after=json.loads((P/f'evidence/q11_whole118_case{case}.json').read_text())['model']
 def measure(m):
  return {'model_hash':digest(m),'program':m['program'],'room_areas':{u['id']:{k:str(sum((F(q[2])-F(q[0]))*(F(q[3])-F(q[1]))for q in rs))for k,rs in u['rooms'].items()}for u in m['units']},'routes':{u['id']:{k:{'length':str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1]))for a,b in zip(path,path[1:]))),'body_m':'.7'}for k,path in u['routes'].items()}for u in m['units']},'actual_windows':m['concept_windows'],'fixtures':{u['id']:u['fixtures']for u in m['units']},'activities':{u['id']:u['activities']for u in m['units']},'route_failures':m['route_failures']}
 out.append({'case':case,'input_unchanged':before['inputs']==after['inputs'],'program_unchanged':before['program']==after['program'],'before':measure(before),'after':measure(after),'limitations':['Route length may increase; no shortest-path global optimality claim.','Exact window geometry/host must be freshly gate checked; actual daylight and ventilation are not established.','Freed area is measured, not automatically useful living area.','Unresolved spatial program and other named rules are not passed by Q11.']})
(P/'evidence/q11_whole118_impact_ledger.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print([(x['case'],x['input_unchanged'],x['program_unchanged'])for x in out])
