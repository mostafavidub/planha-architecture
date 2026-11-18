"""Delegates to new explicit source369 replay; never patches a final model."""
import sys
from pathlib import Path
from operator369 import digest,bind_reconstructed

def reconstruct(parent,plan,run_id,root):
    root=Path(root).resolve()
    if plan.get('kind')!='balanced' or plan.get('status')!='RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED':
        raise ValueError('UNSUPPORTED_PROPOSAL')
    if plan['parent_record_digest']!=digest(parent) or plan['proposal_digest']!=digest(plan['proposal']):
        raise ValueError('PLAN_BINDING')
    sys.path.insert(0,str(root/'staging369_current_source_validation'))
    from source369 import construct
    op=plan['operator']
    child=construct(parent,op['source_key'],op['dx'],op['dy'],purpose='CURRENT_REPAIR_PROPOSAL')
    if child['trace']['proposal_digest']!=plan['proposal_digest']:raise ValueError('SOURCE_PROPOSAL_CHANGED')
    return {'record':child,'lineage':bind_reconstructed(parent,plan,child,run_id),
            'status':'SOURCE_RECONSTRUCTED_PENDING_FRESH_REPLAY_AND_REVIEW','live_authority':False,
            'accepted':False,'delivery_allowed':False}
