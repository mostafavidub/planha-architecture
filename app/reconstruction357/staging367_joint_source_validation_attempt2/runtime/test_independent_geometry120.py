"""Adversarial exact comparison only; no whole assembly or solver."""
import types,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from fast_cells120 import cells
from fast_route120 import route
ROOT=Path(__file__).parent
p=ROOT/'references/geometry_reference119.py.txt';old=types.ModuleType('old');exec(compile(p.read_text(),str(p),'exec'),old.__dict__)
def run():
 rows=[]
 cases=[('empty',[],[['0','0','1','1']]),('hole',[['-1','-1','3','3']],[['0','0','2','2']]),('L',[['0','0','2','1'],['0','1','1','2']],[]),('fraction',[['0','0','1/3','2/7'],['1/3','0','2/3','2/7']],[['1/7','1/9','2/7','1/5']]),('duplicate',[['0','0','2','2']]*2,[['.5','.5','1.5','1.5']]*2),('outsidecut',[['0','0','1','1']],[['-2','-2','-1','-1']]),('thin',[['0','0','1','1']],[['0','0','0.999999999999999999999999999999999999999999999999999999999999999','1']])]
 for name,g,s in cases:
  a,b=old.cells(g,s),cells(g,s);assert a==b,name;rows.append({'case':name,'kind':'cells','exact_equal':True})
 routes=[('zero_distance',['.5','.5'],['.5','.5'],[],18000),('blockedwall',['.5','.5'],['3.5','3.5'],[['1.9','0','2.1','4']],18000),('exactclearance',['.35','2'],['3.65','2'],[['1','0','3','1.65'],['1','2.35','3','4']],18000),('belowclearance',['.35','2'],['3.65','2'],[['1','0','3','1.65000000000000000001'],['1','2.35','3','4']],18000),('reversed_obstacle',['.5','.5'],['3.5','3.5'],[['2','1','1','2']],18000),('zero_obstacle',['.5','.5'],['3.5','3.5'],[['1','1','1','3']],18000),('tie_symmetric',['.5','2'],['3.5','2'],[['1.5','1.5','2.5','2.5']],18000),('budget',['.5','.5'],['3.5','3.5'],[['1','1','2','2']],3)]
 for name,start,end,obs,budget in routes:
  args=(start,end,['0','0','4','4'],obs);a,b=old.route(*args,max_nodes=budget),route(*args,max_nodes=budget);assert a==b,(name,a,b);rows.append({'case':name,'kind':'route','exact_equal':True,'result':b})
 return {'scope':'Exact legacy equivalence on adversarial geometry; not plan admission or proof for arbitrary malformed inputs','rows':rows,'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()for f in ['fast_cells120.py','fast_route120.py','references/geometry_reference119.py.txt']},'findings':['Integer lifting uses all rational denominators without rounding.','Positive-area collision is symmetric; undirected edge memoization preserves predicate.','Tie-breaking neighbor order, cost scaling, heap keys and node budget preserved.','Both legacy and optimized endpoint inflation can reject degenerate obstacle interiors even while edge ignores their zero area; legacy behavior retained, not fixed.']}
if __name__=='__main__':
 r=run();(ROOT/'evidence/performance120/independent_equivalence.json').write_text(json.dumps(r,indent=2));print(len(r['rows']),'exact equality checks passed')
