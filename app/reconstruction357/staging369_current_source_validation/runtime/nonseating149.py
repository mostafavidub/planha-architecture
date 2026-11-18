"""Rooted branch variant: source contact and all branch/group/no-through contracts."""
from nonseating144 import POLICY,check_packet
from shared_gate140 import require_runtime_group_proposal,ROOT_MARKER

def require(p,core):
 if p.get('nonseating_protection144')!=POLICY:raise ValueError('BRANCH149_NO_THROUGH_POLICY')
 if (p.get('ordered_macro')or{}).get('kind')!='PARALLEL_TWINS_BRANCH146':raise ValueError('BRANCH149_KIND')
 require_runtime_group_proposal(p,expected_marker=ROOT_MARKER,core=core)
