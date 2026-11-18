"""Fixed source lineage plus geometry-derived finite parameter selection."""
import json,hashlib,copy
from pathlib import Path
from fractions import Fraction as F
from family378 import enumerate_family
from contract114 import digest
P=Path(__file__).resolve().parents[1]/'staging362_core_notch/actual362.json'
SHA='d448292d87b2fbd351f150bbfba3c7b6bf8acb4c074d31d4192f6ccc64f229d8'
def core(W,L,selection):
 data=P.read_bytes()
 if hashlib.sha256(data).hexdigest()!=SHA:raise ValueError('FIXED_SOURCE362_CHANGED')
 r=json.loads(data)
 if list(map(F,r['candidate']['model']['inputs'][:2]))!=[W,L]:raise ValueError('FIXED_LINEAGE_REQUEST_MISMATCH')
 choices=enumerate_family(r)
 if selection not in choices:raise ValueError('UNREGISTERED_FINITE_SELECTION')
 p=copy.deepcopy(selection);c=copy.deepcopy(r['candidate']['packet']['core']);before=digest(c)
 for u,x in p['entry_x'].items():c['entry_centers'][u][0]=x
 c['balanced_portals365']={**p,'source_base_core_digest':before,'source_body_pose':'SOURCE_INSIDE_INSET_0.4_AT_ACTUAL_NEW_PORTAL_CENTER','metric_policy':'INDEPENDENT_CANDIDATE_EXPLICIT_TRADEOFF_NOT_PARETO_REPAIR','predictions_not_review':True}
 return c
