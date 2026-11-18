"""Measured before/after geometric ledger. No functional/privacy approval."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from bedroom_module116 import build
from geometry114 import cells
P=Path(__file__).resolve().parent
oldsource=(P/'evidence/bedroom_before_q11.py.txt').read_text()
ns={'__name__':'old_producer_for_measurement','__file__':str(P/'bedroom_module116.py')}
exec(compile(oldsource,'preserved_before_q11','exec'),ns)
def area(rs):return str(sum((F(q[2])-F(q[0]))*(F(q[3])-F(q[1]))for q in cells(rs,[])))
def metrics(m):
 u=m['unit'];floor=u['rooms']['bed1'];obs=list(u['fixtures'].values())+list(m['walls'].values())
 return {'actual_room_floor_area':area(floor),'fixture_area':area(list(u['fixtures'].values())),'free_room_floor_area':area(cells(floor,obs)), 'route_lengths':{k:str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1]))for a,b in zip(v,v[1:])))for k,v in u['routes'].items()},'route_body_width_m':'.7','all_targets_preserved':sorted(u['route_targets']),'activity_rects':u['activities'],'closet':u['fixtures']['bed1.closet'],'bed':u['fixtures']['bed1.bed'],'front_boundary_walls_intruding_room':[{'id':k,'rect':q}for k,q in m['walls'].items()if F(q[1])<=0<F(q[3]) and F(q[0])>=0 and F(q[2])<=F(m['input_program']['width'])], 'window_scope':'Module has no inserted window; whole front-host/fixture-height opportunity must be freshly checked after placement. This ledger does not prove daylight.'}
out=[]
for w,h in [('5.45','3.6'),('6','4.2'),('6.015','4.205'),('7','5')]:
 old=ns['build'](w,h);new=build(w,h)
 old['source_binding']['producer_sha256']=hashlib.sha256(oldsource.encode()).hexdigest()
 (P/f'evidence/q11_before_module118_{w}x{h}.json').write_text(json.dumps(old,indent=2))
 out.append({'width':w,'depth':h,'old_source_sha256':hashlib.sha256(oldsource.encode()).hexdigest(),'before':metrics(old),'after':metrics(new),'no_acceptance_claim':True})
(P/'evidence/q11_module118_impact_ledger.json').write_text(json.dumps(out,indent=2))
print([(r['width'],r['before']['free_room_floor_area'],r['after']['free_room_floor_area'])for r in out])
