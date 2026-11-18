"""Independent rational ledger reproduction from saved before/after geometry."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).parent

def area(rs):
 rs=[tuple(map(F,r))for r in rs];xs=sorted({v for r in rs for v in(r[0],r[2])});ys=sorted({v for r in rs for v in(r[1],r[3])})
 return sum((x1-x0)*(y1-y0)for x0,x1 in zip(xs,xs[1:])for y0,y1 in zip(ys,ys[1:])if any(r[0]<=x0<x1<=r[2]and r[1]<=y0<y1<=r[3]for r in rs))
rows=json.loads((ROOT/'evidence/q11_module118_impact_ledger.json').read_text());out=[]
sourcehash=hashlib.sha256((ROOT/'evidence/bedroom_before_q11.py.txt').read_bytes()).hexdigest()
for row in rows:
 suffix=row['width']+'x'+row['depth'];observed={}
 assert row['old_source_sha256']==sourcehash
 for stage,prefix in [('before','q11_before_module118_'),('after','q11_module118_')]:
  m=json.loads((ROOT/f'evidence/{prefix}{suffix}.json').read_text());u=m['unit'];a=area(u['rooms']['bed1']);fa=area(u['fixtures'].values());lengths={k:sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1]))for a,b in zip(path,path[1:]))for k,path in u['routes'].items()}
  assert a==F(row[stage]['actual_room_floor_area']);assert fa==F(row[stage]['fixture_area']);assert a-fa==F(row[stage]['free_room_floor_area'])
  assert lengths=={k:F(v)for k,v in row[stage]['route_lengths'].items()};assert u['activities']==row[stage]['activity_rects'];assert sorted(u['route_targets'])==row[stage]['all_targets_preserved']
  observed[stage]={'floor_area':str(a),'fixture_area':str(fa),'free_floor_not_automatically_useful':str(a-fa),'route_lengths':{k:str(v)for k,v in lengths.items()}}
 out.append({'parameters':suffix,'status':'EXACT_LEDGER_MATCH','geometry':observed,'limitations':['Route length may increase; no claim all paths improved','Body width .7 is demonstrated by separate actual module gate, not inferred from length','No module window inserted; whole actual host/contact still mandatory','No spatial-quality or all-residual-usefulness claim']})
(ROOT/'evidence/independent118/q11_impact_independent.json').write_text(json.dumps(out,indent=2));print('Four independent before/after exact ledger matches')
