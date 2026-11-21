"""One controlled, non-admitting LR generation and evaluation."""
import argparse
import json

from p19_archived_lr_loopback import AUTH, CASE_SCOPE, digest, need, private_directory, write
from study_frame125_two_nonsquare import (
    SETTINGS, build, context, evaluate_pair, frame, propose, source_binding,
    transport_boundary, verify,
)


def run(output):
    import current_four_decision as four
    from current_programme_evaluator import assess as programme
    from source_guest_route_evaluator import assess as guest
    from source_living_evaluator import assess as living
    from source_wall_function_evaluator import assess as wall

    output = private_directory(output)
    width, length, units = CASE_SCOPE
    raw = {'W': width, 'L': length, 'n': units, 'requested_count': 1}
    core, _ = frame(raw, 'LEFT_RIGHT')
    proposal = propose(core, topology='FRAME125_SERVICE_SIDE', **SETTINGS)
    write(output, 'proposal.json', proposal)
    if proposal.get('status') != 'PROPOSAL_ONLY':
        return {'state': 'NO_FRESH_MODEL', 'proposal_status': proposal.get('status')}

    packet = build(raw, 'LEFT_RIGHT', proposal, proposal)
    ctx = context(raw, packet, {'A': proposal, 'B': proposal})
    packet, ctx, _ = transport_boundary(packet, ctx)
    model = packet['world_model']
    model_digest = digest(model)
    need(model['inputs'] == CASE_SCOPE, 'FRESH_LR_WORLD_AXES')
    binding = source_binding(packet, ctx)
    replay = verify(model, ctx)
    need(binding['scoped_verified'] and replay['verified'], 'FRESH_LR_SOURCE_BINDING')
    physical = evaluate_pair(packet, ctx)
    need(physical['model_hash'] == model_digest, 'FRESH_LR_PHYSICAL_BINDING')
    reports = {'replay': replay, 'physical': physical}
    bundle = {
        'schema': 'P19_FRESH_LR_PRIVATE_EVALUATION_INPUT_V1',
        'packet': packet, 'context': ctx, 'model_digest': model_digest,
        'engine_revision': replay['source_revision'], 'reports': reports,
        'report_digests': {key: digest(value) for key, value in reports.items()},
        **dict.fromkeys(AUTH, False),
    }
    pin = digest(bundle)
    write(output, 'bound-input.json', bundle)
    results = {}
    for criterion, assessor in zip(four.SCHEMAS, (programme, guest, living, wall), strict=True):
        result = assessor(bundle)
        need(result['integrity_verified'] and result['model_digest'] == model_digest
             and digest(bundle) == pin, 'FRESH_LR_ASSESSMENT_BINDING')
        results[criterion] = result
        write(output, criterion + '.json', result)
    decision = four.assemble(bundle, results, {key: digest(value) for key, value in results.items()})
    need(decision['integrity_verified'] and decision['model_digest'] == model_digest
         and all(decision[key] is False for key in AUTH), 'FRESH_LR_DECISION_BINDING')
    write(output, 'decision.json', decision)
    return {'state': 'FRESH_LR_EVALUATED', 'model_digest': model_digest,
            'physical': physical['status'], 'criteria': {k: v['state'] for k, v in results.items()},
            'decision': decision['decision']['state']}


if __name__ == '__main__':
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    print(json.dumps(run(parser.parse_args().output)))
