"""Current finite cohort; current rank2 comparison plus exact-readset history.
Rank2 intrinsic384 is an explicitly stored proof for immutable actual383, not
new385 semantic execution of rank2. Current rank1 intrinsic is freshly computed.
"""
import copy,sys
from gate385 import validate,D,ROOT,W
from frozen385 import read,module

def evaluate(record,fresh,intrinsic):
 binding=validate(record,fresh)
 path=ROOT/'staging384_rank2_semantics';spec=read(path/'inputs.json')
 alternative={k:read(W/spec[k]['path'])for k in('record','fresh')}
 proof=read(W/'review384_actual_v1/result.json')
 ar,af=alternative['record'],alternative['fresh']
 rank2_gate=module(path/'gate384.py','_current385_rank2_gate384');rank2_binding=rank2_gate.validate(ar,af)
 if proof['binding']!=rank2_binding:raise ValueError('AUTHENTIC_RANK2_SOURCE_GATE')
 supervision=read(W/'review384_actual_v1/supervision.json');pre=read(W/'review384_actual_v1/preregistration.json');unchanged=read(W/'review384_actual_v1/source_unchanged.json');state=read(W/'review384_actual_v1/state.json')
 if not(supervision.get('reason')=='COMPLETED'and supervision.get('worker_returncode')==0 and supervision.get('worker_reaped')is True and supervision.get('cleanup_verified')is True and supervision.get('unresolved')==[] and unchanged.get('verified')is True and state.get('state')=='COMPLETED'):raise ValueError('RANK2_INTRINSIC_EXECUTION_NOT_VERIFIED')
 if pre['binding']!=rank2_binding:raise ValueError('RANK2_INTRINSIC_PREREGISTRATION_BINDING')
 from frozen385 import bytes_for
 import hashlib
 if hashlib.sha256(bytes_for(W/'review384_preaudit/source_freeze.json')).hexdigest()!=pre['freeze_sha256']:raise ValueError('RANK2_INTRINSIC_SOURCE_FREEZE')
 if proof.get('schema')!='ACTUAL383_RANK2_INTRINSIC_AND_CURRENT379_FINITE_JOIN384'or proof.get('rank2_intrinsic_recomputed')is not True:raise ValueError('AUTHENTIC_RANK2_INTRINSIC_REQUIRED')
 if any(proof['binding'].get(k)!=v for k,v in {'record_digest':D(ar),'fresh_digest':D(af),'model_digest':D(ar['candidate']['model'])}.items()):raise ValueError('RANK2_PROOF_BINDING')
 if ar['trace']['schema']!='FINITE_PORTALS383_SOURCE_TRACE_V1'or ar['trace']['selection_rank']!=2:raise ValueError('ACTUAL_RANK2_SOURCE_REQUIRED')
 ai=proof['evidence']['rank2_intrinsic']
 compare=module(path/'cohort384.py','_current385_cohort384')
 # This call verifies the actual383 own record/fresh/intrinsic correspondence.
 compare.bind_intrinsic(ar,af,ai)
 historical=read(W/'review382_actual_v1/result.json');old_digest=D(historical)
 if historical['binding']['model_digest']!=D(record['candidate']['model']):raise ValueError('HISTORICAL_TEMPLATE_MODEL_NOT_CURRENT')
 # Recheck original history against the same full model before updating any
 # current envelope. Old run identity never serves as current execution proof.
 compare.verify_historical(historical,record)
 out=compare.compare_registered(record,fresh,intrinsic,ar,af,ai,historical)
 out.update(historical_comparisons_recomputed=False,historical_template_digest=old_digest,historical_comparison_reuse_scope='EXACT_PINNED382_OBJECT_IDENTICAL_FULL_CURRENT_MODEL_AND_BRIEF_WITH_EIGHT_OWN_RECEIPTS_RECHECKED',
            rank2_intrinsic_proof_digest=D(proof),rank2_intrinsic_recomputed_in385=False,rank2_proof_reuse_scope='IMMUTABLE_ACTUAL383_OWN_RECORD_FRESH_INTRINSIC_ONLY',
            current_intrinsic_recomputed_in385=True,old_rank1_parent_pass_reused=False)
 validate(record,fresh)
 return out
