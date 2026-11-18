"""Diagnostic-only deletion experiment, never an admitted candidate."""
import json,time
from pathlib import Path
from fractions import Fraction as F
from scipy.optimize import milp,LinearConstraint
import numpy as np
from search114 import propose
from contract114 import core_first,program
P=Path(__file__).resolve().parent
results=[]
for case in (1,2):
 d=P.parent/f'planha_hybrid_independent/baseline117/random_{case}'
 raw=json.loads((d/'request.json').read_text());raw=raw.get('raw',raw)
 print(raw,flush=True)
 W,L=F(str(raw['W'])),F(str(raw['L']));core=core_first(W,L);b=program(W,L,core,raw)['bedroom_choices'][0]
 a=propose(core,b,diagnostic_capture=lambda x:x)
 keep=np.ones(len(a['row_metadata']),dtype=bool)
 if case==1: keep=np.array([r['group']!='rooted_body_network'for r in a['row_metadata']])
 else:
  i=next(i for i,z in enumerate(a['specs'])if z[0]=='sofa1_use');a['bounds'].lb[4*i+1]=50;a['bounds'].ub[4*i+1]=int((F(core['units']['A'][3])-F('1.6'))/F('.005'))
 t=time.monotonic()
 r=milp(a['objective'],integrality=a['integrality'],bounds=a['bounds'],constraints=LinearConstraint(a['matrix'][keep],a['lower'][keep],a['upper'][keep]),options={'time_limit':3,'mip_rel_gap':.02,'presolve':True})
 out={'case':case,'raw':raw,'bedrooms':b,'removed_group':'rooted_body_network'if case==1 else'sofa1_fixed_front_y_bound','removed_rows':int(sum(~keep)),'status':int(r.status),'message':r.message,'has_incumbent':r.x is not None,'seconds':time.monotonic()-t,'diagnostic_only':True,'physical_plan_or_admission':False}
 results.append(out);print(out,flush=True)
(P/'evidence/constraint_group_ablation118_second.json').write_text(json.dumps(results,indent=2))
