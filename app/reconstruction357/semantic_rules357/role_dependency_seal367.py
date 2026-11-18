"""Finalize typed semantic dependencies before hashing; no verdict changes."""
import copy
from common import digest
def order(dag):
 out=[]
 while len(out)<len(dag):
  ready=sorted(k for k in dag if k not in out and all(d in out for d in dag[k]))
  if not ready:raise ValueError('DEPENDENCY_CYCLE_OR_UNKNOWN')
  out+=ready
 return out
def seal(nodes,dag):
 n=copy.deepcopy(nodes)
 if set(n)!=set(dag):raise ValueError('NODE_INVENTORY')
 for k in dag:
  n[k]['depends_on']=list(dag[k]);n[k]['blocking_dependencies']=[d for d in dag[k]if not n[d]['status'].startswith('PASS_')]
 for k in order(dag):
  if k=='WALL_PURPOSE':
   for row in n[k]['evidence']['closed_hall_dependency_rows']:
    row['intrinsic_private_role_digest']=digest(n['PRIVATE_CIRCULATION'])
    row['finite_q04_digest']=digest(n['Q04_COMPARISON']['evidence'])
  if k=='Q11_WHOLE_ROLE':n[k]['evidence']['dependency_digests']={d:digest(n[d])for d in dag[k]}
  if k=='Q05_PRIVACY':
   n[k]['evidence']['wall_role_digest']=digest(n['WALL_PURPOSE']);n[k]['evidence']['whole_role_digest']=digest(n['Q11_WHOLE_ROLE'])
  if k=='Q12_PER_UNIT':
   for u in n[k]['evidence']:
    u['resolved_dependency_digests']={d:digest(n[d])for d in ('COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON')}
    u['balanced_access_digest']=digest(n[k]['balanced_common_access'])
  n[k]['sealed_dependency_digests']={d:digest(n[d])for d in dag[k]}
 return n
def verify(nodes,dag):
 if digest(nodes)!=digest(seal(nodes,dag)):raise ValueError('STALE_OR_MUTATED_DEPENDENCY_SEAL')
 return True
