"""Explicit n1 family dispatch beside unchanged n2 scheduler and X07 consumer."""
import time
from public_wln_contract import parse_public,verify_public
from live_program_scheduler import preflight as pair_preflight
from http_evidence_x07 import run_bound as pair_bound
import single_model_p15 as single
def is_single(body):
 envelope=parse_public(body);verify_public(body,envelope)
 return envelope['canonical_request']['unit_count']==1
def preflight(body):
 if not is_single(body):return pair_preflight(body)
 result=single.preflight(body)
 result['case_scope']='18x20/n1/P2/SINGLE_FRONT_TOP_CORE_P15_V1 only'
 return result
def run_bound(body,runtime,*,deadline=None):
 if not is_single(body):return pair_bound(body,runtime)
 from single_runtime_p17 import run_bound as single_bound
 single.require(deadline is not None,'SINGLE_SERVER_DEADLINE_REQUIRED')
 return single_bound(body,deadline)
