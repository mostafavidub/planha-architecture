"""Own source367 finite Q04 evidence; no saved PASS is used as eligibility."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'semantic_rules357'),str(ROOT/'finite_comparison365'),str(ROOT/'finite_comparison358')]
from common import digest
from cohort367 import inventory
from group_readsets367 import build
from eligibility_intrinsic367 import evaluate as eligible
from entry_role_joint367 import evaluate as entry_role
from private_role_joint367 import evaluate as private_role
from common_role_joint367 import evaluate as common_role
from q04_closure362_v2 import full_band_current
from branch_registry362 import build as old_domain

def evaluate(record,review):
 before=digest([record,review]);g=build(record,review,source_profile='SOURCE_JOINT367');e=eligible(record,review,source_profile='SOURCE_JOINT367');entry=entry_role(record,review);private=private_role(record,review);common=common_role(record,review);cohort=inventory(record,'joint367');core=full_band_current(record);pending=[]
 if e.get('verdict')!='PASS'or not e.get('eligible'):pending.append('CURRENT_INTRINSIC_NOT_PASS')
 if entry['verdict']!='PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE':pending.append('CURRENT_ENTRY_ROLE_NOT_PASS')
 if private['status']!='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE':pending.append('CURRENT_PRIVATE_ROLE_NOT_PASS')
 if not common['verdict'].startswith('PASS_'):pending.append('CURRENT_COMMON_ROLE_NOT_PASS')
 for k,v in [('record_digest',digest(record)),('fresh_result_digest',digest(review)),('model_digest',digest(record['candidate']['model']))]:
  if entry[k]!=v:raise ValueError('CURRENT_ENTRY_BINDING')
 for row in cohort['members']:
  if row['role']=='ALTERNATIVE'and row['comparison']['dominance']!='FALSE':pending.append('UNRESOLVED_ALTERNATIVE:'+row['id'])
 # Explicitly retained until source-supported selector/attempt lineage is independently closed.
 pending.append('EXPANDED_SOURCE367_BRANCH_DOMAIN_AUDIT_PENDING')
 domain={'previous_active_dispatch':old_domain(),'current_joint_source_trace_digest':digest(record['trace']),'selector_source':'staging367_service_joint_attempt2/selector367.py','selector_sha256':hashlib.sha256((ROOT/'staging367_service_joint_attempt2/selector367.py').read_bytes()).hexdigest(),'scope':'Deterministic interior point of exact source-feasible portal/entry cells; no continuous optimum claim','historical_attempts':['staging364_balanced_portals/actual364.json','review367_joint_diagnostic','review367_joint_attempt2/source_delta.json'],'domain_closed':False}
 if digest([record,review])!=before:raise ValueError('INPUT_MUTATION')
 return {'schema':'Q04_367_OWN_FINITE_EVIDENCE','source_profile':'SOURCE_JOINT367','record_digest':digest(record),'fresh_result_digest':digest(review),'model_digest':digest(record['candidate']['model']),'group_digest':digest(g),'intrinsic':e,'entry_role':entry,'private_role':private,'common_role':common,'full_band_protection':core,'cohort':cohort,'domain':domain,'remaining':pending,'verdict':'UNKNOWN'if pending else'PASS_SCOPED_FINITE_Q04','accepted':False,'new_fresh_execution':False,'all_parent_acceptance':False}
