"""Read-only current-report adapter. Source-shaped tests are not live evidence.
No model, evaluator or solver is executed. No aggregate PASS/FAIL is assigned to a unit.
Expected pins are a caller's independently established evidence anchor, not authentication.
"""
import copy
import hashlib
from obligation_admission111 import (AUTH, ROOT, digest, strict, require, hash_ok,
                                    coverage_contract, admission)
ENGINE_REVISION = 'faada6a8a1106adfe8a24a5f18dfdf6b550f20a6ecc93d81ce07d47a20d6a279'
SCHEMAS = {
 'CURRENT_PROGRAM_SUITABILITY': 'CURRENT_PROGRAMME_SOURCE_EVALUATION_V1',
 'KITCHEN_GUEST_PATH_SEPARATION': 'SOURCE_BOUND_FOUR_GUEST_ROUTES_V1',
 'CONTINUOUS_USEFUL_LIVING': 'CURRENT_LIVING_SOURCE_EVIDENCE_V1',
 'NONFUNCTIONAL_WALL_EXCLUSION': 'SOURCE_WALL_FUNCTION_EVIDENCE_V1'}
SOURCES = {
 'CURRENT_PROGRAM_SUITABILITY': ('current_programme_evaluator.py', 'program_profile_registry.py',
                                 'specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json'),
 'KITCHEN_GUEST_PATH_SEPARATION': ('source_guest_route_evaluator.py', 'current_programme_evaluator.py',
                                 'kitchen_guest_review.py', 'guest_four_route_diagnostic.py'),
 'CONTINUOUS_USEFUL_LIVING': ('source_living_evaluator.py', 'source_guest_route_evaluator.py',
                            'living_connectivity_diagnostic.py', 'fixed_route_clearance_diagnostic.py',
                            'kitchen_guest_review.py'),
 'NONFUNCTIONAL_WALL_EXCLUSION': ('source_wall_function_evaluator.py', 'source_wall_counterfactual.py',
                                 'current_programme_evaluator.py')}
def source_snapshot(cid):
    paths = [x if '/' in x else 'app/local_integration/' + x for x in SOURCES[cid]]
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
def markers(value):
    found = []
    def walk(x):
        if type(x) is dict:
            if x.get('state') in ('EVALUATOR_ERROR', 'UNKNOWN_EVALUATOR_OR_BINDING_ERROR'):
                found.append('EVALUATOR_ERROR')
            if x.get('kind') in ('EVALUATOR_OR_SOURCE_BINDING_ERROR', 'INTEGRITY_ERROR'):
                found.append('SOURCE_OR_EVALUATOR_ERROR')
            for k, v in x.items():
                if k not in ('original_physical_report', 'historical_physical_report', 'reports', 'replay'):
                    walk(v)
        elif type(x) is list:
            for v in x: walk(v)
    walk(value)
    if value.get('missing'): found.append('MISSING_EVIDENCE')
    if value.get('integrity_verified') is not True: found.append('SOURCE_OR_EVALUATOR_ERROR')
    return found
def adapt(raw, expected_raw_digest, binding, expected_binding_digest):
    out = {'schema': 'CURRENT_RAW_ADAPTER111_V1', 'state': 'EVIDENCE_ERROR',
           'consistency_verified': False, 'live_execution_verified': False,
           'per_unit_criterion_mapping_verified': False,
           'whole_obligation_mapping_verified': False,
           'unverified_anchor_associations': ['request_digest', 'source_digest', 'rule_digest', 'profile_digest'],
           **{k: False for k in AUTH}, 'aggregate_findings': [], 'unit_observations': [],
           'errors': [], 'raw_preservation': 'NOT_ESTABLISHED'}
    try:
        strict(raw)
        out['raw_reports'] = copy.deepcopy(raw)
        out['raw_preservation'] = 'EXACT_VALID_JSON_COPY'
        out['raw_digest'] = digest(raw)
        require(hash_ok(expected_raw_digest) and digest(raw) == expected_raw_digest, 'RAW_PIN')
        require(type(raw) is dict and set(raw) == {'physical', 'replay', 'current'}, 'RAW_FIELDS')
        require(digest(binding) == expected_binding_digest, 'ANCHOR_BINDING')
        require(set(raw['current']) == set(SCHEMAS), 'CURRENT_SET')
        physical, replay = raw['physical'], raw['replay']
        mh = binding['model_digest']
        require(physical['model_hash'] == mh and replay['model_hash'] == mh, 'ORIGINAL_MODEL')
        require(replay['verified'] is True and replay['source_revision'] == ENGINE_REVISION, 'REPLAY_REVISION_OR_VERIFICATION')
        require(type(physical['errors']) is list and type(physical['pending']) is list, 'PHYSICAL_LISTS')
        require(physical['status'] in ('FAIL', 'PASS_CONCEPT_SCOPED_REVIEW'), 'PHYSICAL_STATUS')
        source_pins = {}
        for cid, r in raw['current'].items():
            require(r['schema'] == SCHEMAS[cid] and r['criterion'] == cid, 'CURRENT_SCHEMA')
            require(r['model_digest'] == mh, 'CURRENT_MODEL')
            require(all(r[k] is False for k in AUTH), 'CURRENT_AUTHORITY')
            require(r['state'] in ('PASS', 'FAIL', 'UNKNOWN', 'NOT_EVALUATED'), 'CURRENT_STATE')
            require(type(r['source_snapshot']) is dict and r['source_snapshot'] == source_snapshot(cid), 'CURRENT_SOURCE')
            source_pins[cid] = copy.deepcopy(r['source_snapshot'])
            if cid == 'CURRENT_PROGRAM_SUITABILITY':
                pr, rr = r['historical_physical_report'], r['reports']['replay']
                ph = r['historical_physical_digest']
                cap = r['reports'].get('capacity')
                if cap is not None:
                    require(cap['evidence']['model_hash'] == mh, 'CAPACITY_MODEL')
                unit_rows = r.get('inventory', [])
                # inventory shape belongs to producer; it is retained, not treated as a unit verdict.
                out['unit_observations'].append({'criterion': cid,
                    'scope': 'INVENTORY_RETAINED_NOT_UNIT_VERDICT', 'inventory_digest': digest(unit_rows)})
            else:
                pr, rr, ph = r['original_physical_report'], r['replay'], r['original_physical_digest']
                if cid in ('KITCHEN_GUEST_PATH_SEPARATION', 'CONTINUOUS_USEFUL_LIVING'):
                    rows = r['units']; require(type(rows) is list, 'UNIT_ROWS')
                    ids = [x['unit'] for x in rows]
                    require(all(type(x) is str and x in ('A','B') for x in ids)
                            and len(ids) == len(set(ids)), 'UNIT_IDENTITY')
                    for row in rows:
                        out['unit_observations'].append({'criterion': cid, 'unit': row['unit'],
                            'raw_unit_digest': digest(row), 'scope': 'SUBSTUDY_NOT_CRITERION_PASS'})
                else:
                    require(type(r['walls']) is list, 'WALL_ROWS')
                    ids = [x['source_id'] for x in r['walls']]
                    require(all(type(x) is str for x in ids) and len(ids) == len(set(ids)), 'WALL_IDENTITY')
            require(ph == digest(physical) and digest(pr) == digest(physical), 'PHYSICAL_COPY')
            require(digest(rr) == digest(replay), 'REPLAY_COPY')
            out['aggregate_findings'].append({'criterion': cid, 'reported_state': r['state'],
                'diagnostic_markers': markers(r), 'raw_report_digest': digest(r),
                'scope': 'AGGREGATE_ONLY_NO_UNIT_PROPAGATION'})
        # Binding source/profile/request provenance is not inferred from model-only reports.
        # Their externally established anchor is retained; unproved associations remain missing.
        contract = coverage_contract()
        normalized = []
        for spec in contract['obligations']:
            normalized.append({'obligation': spec['obligation'], 'subject': spec['subject'],
                'state': 'UNKNOWN', 'errors': [], 'pending': [],
                'missing': ['MISSING_EVIDENCE']})
        report = {'schema': 'OBLIGATION_EVIDENCE111_V1', 'binding': copy.deepcopy(binding),
                  'rows': normalized, 'errors': [], 'pending': [],
                  **{k: False for k in AUTH}}
        decision = admission(contract, digest(contract), binding, expected_binding_digest,
                             {'unmapped_raw': report}, {'unmapped_raw': digest(report)})
        require(decision['consistency_verified'] is True, 'NORMALIZED_CONSISTENCY')
        # Do not classify an architectural violation as evaluator error or erase either.
        if physical.get('status') == 'FAIL' or physical['errors']:
            decision['blockers'].append({'code': 'RETAINED_PHYSICAL_FAIL'})
        if physical['pending']:
            decision['blockers'].append({'code': 'RETAINED_PHYSICAL_PENDING'})
        for row in out['aggregate_findings']:
            if row['reported_state'] == 'FAIL':
                decision['blockers'].append({'code': 'RETAINED_AGGREGATE_CURRENT_FAIL',
                                             'criterion': row['criterion']})
            for reason in row['diagnostic_markers']:
                decision['blockers'].append({'code': reason, 'criterion': row['criterion']})
        require(digest(raw) == expected_raw_digest, 'RAW_MUTATION')
        require(all(source_snapshot(cid) == snap for cid, snap in source_pins.items()), 'SOURCE_CHANGED')
        out.update(state='BLOCKED_UNMAPPED_NECESSARY_SUBCONDITIONS',
                   consistency_verified=True, decision=decision,
                   source_snapshot=source_pins, anchor_binding=copy.deepcopy(binding))
        return out
    except (KeyError, ValueError, TypeError, UnicodeError, OSError) as exc:
        out['errors'].append({'code':'RAW_BINDING_OR_SCHEMA_ERROR','type':type(exc).__name__})
        return out
