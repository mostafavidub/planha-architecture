"""19.8m2 source-fixed group plus unchanged whole-group route exclusion."""
from nonseating144 import POLICY,check_packet
from shared_gate140 import require_runtime_group_proposal,GROUP_MARKER

def require(p):
 if p.get('nonseating_protection144')!=POLICY:raise ValueError('BRANCH146_NO_THROUGH_POLICY')
 if (p.get('ordered_macro')or{}).get('kind')!='PARALLEL_TWINS_BRANCH146':raise ValueError('BRANCH146_KIND')
 require_runtime_group_proposal(p,expected_marker=GROUP_MARKER)
