"""Versioned obligation admission study. No product authorization or report authentication.
The caller supplies independent request/evidence pins, never policy authority.
The coverage inventory is server-owned and pinned to an immutable source map.
This function verifies consistency/classification, not truth of report contents.
No production API import, solver, network, artifact reader or inferred applicability.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP_PATH = 'specs/V25_TASK_2_2_FRONT_REAR_RULE_EVIDENCE_MAP.json'
MAP_BLOB = '0b8bb876cc675ed27f88b340b3c6ed4e41608eb4'
UNRESOLVED_APPLICABILITY = frozenset(('llm_budget', 'geometric_diversity',
    'window_opportunities', 'export_parity', 'immutable_history', 'owner_access',
    'per_option_rule_report', 'claim_boundary_display'))
CURRENT_IDS = ('CURRENT_PROGRAM_SUITABILITY', 'KITCHEN_GUEST_PATH_SEPARATION',
               'CONTINUOUS_USEFUL_LIVING', 'NONFUNCTIONAL_WALL_EXCLUSION')

AUTH = ('accepted', 'qualified', 'display_allowed', 'delivery_allowed')
STATES = ('PASS', 'FAIL', 'UNKNOWN', 'NOT_EVALUATED', 'ERROR')
BINDINGS = ('request_digest', 'model_digest', 'source_digest', 'rule_digest',
            'profile_digest', 'coverage_digest')
CODES = ('MISSING_RULE', 'MISSING_PROFILE', 'MISSING_EVIDENCE', 'NOT_RUN',
         'EVALUATOR_ERROR', 'SOURCE_CONFLICT')
def require(ok, code):
    if not ok:
        raise ValueError(code)
def strict(value):
    if value is None or type(value) in (str, bool, int):
        if type(value) is str:
            value.encode('utf-8')
        return
    if type(value) is list:
        for x in value:
            strict(x)
        return
    if type(value) is dict:
        require(all(type(k) is str for k in value), 'JSON_KEYS')
        for k, x in value.items():
            strict(k); strict(x)
        return
    raise ValueError('EXACT_JSON_TYPE')
def digest(value):
    strict(value)
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False).encode('utf-8')).hexdigest()
def hash_ok(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None
def key(row):
    return (row['obligation'], row['subject'])

def coverage_contract():
    """Server-owned fixed subset; caller cannot remove obligations or change scope.
    Historical named obligations are GLOBAL report obligations, NOT proof that
    every named subcondition has per-unit evidence. Four criteria and quality
    require separate A/B rows; adapters for actual aggregate reports are not built.
    Conditional LLM/diversity and product-stage obligations remain unresolved;
    no absent activity is silently treated as an exclusion.
    """
    data = (ROOT / MAP_PATH).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + bytes([0]) + data).hexdigest()
    require(blob == MAP_BLOB, 'PINNED_SOURCE_MAP_CHANGED')
    source = json.loads(data)
    named = source['layers']['named']
    require(len(named) == 38 and len({r['id'] for r in named}) == 38, 'NAMED_INVENTORY')
    require({r['id'] for r in source['layers']['current']} == set(CURRENT_IDS), 'CURRENT_INVENTORY')
    rows = []
    def add(oid, subject, applicability='REQUIRED'):
        rows.append({'obligation': oid, 'subject': subject, 'applicability': applicability,
                     'rule_ref': 'SOURCE_MAP_V1:' + oid, 'profile_ref': 'UNQUALIFIED_STUDY_PROFILE',
                     'report_schema': 'OBLIGATION_EVIDENCE111_V1', 'exclusion_evidence_digest': None})
    for oid in ('CURRENT_PUBLIC_WLN', 'PAIR127_ORIGIN', 'PHYSICAL_GEOMETRY_AND_OPERATIONS'):
        add(oid, 'GLOBAL')
    for row in named:
        add(row['id'], 'GLOBAL', 'UNRESOLVED' if row['id'] in UNRESOLVED_APPLICABILITY else 'REQUIRED')
    for unit in ('A', 'B'):
        for cid in CURRENT_IDS:
            add(cid, unit)
        add('CALIBRATED_UNIT_QUALITY', unit)
    return {'schema': 'OBLIGATION_COVERAGE111_V1', 'version': 'PINNED_N2_SCOPE_V1',
            'units': ['A', 'B'], 'obligations': rows,
            'source_map_digest': hashlib.sha256(data).hexdigest(),
            'whole_product_coverage_verified': False}

def validate_contract(contract, expected):
    require(digest(contract) == digest(coverage_contract()), 'SERVER_COVERAGE_CONTRACT')
    require(hash_ok(expected) and digest(contract) == expected, 'COVERAGE_PIN')
    require(set(contract) == {'schema', 'version', 'units', 'obligations', 'source_map_digest',
                              'whole_product_coverage_verified'}, 'CONTRACT_FIELDS')
    require(contract['schema'] == 'OBLIGATION_COVERAGE111_V1', 'CONTRACT_SCHEMA')
    require(type(contract['version']) is str and bool(contract['version']), 'CONTRACT_VERSION')
    require(contract['whole_product_coverage_verified'] is False, 'PRODUCT_COVERAGE_UNESTABLISHED')
    require(hash_ok(contract['source_map_digest']), 'SOURCE_MAP_DIGEST')
    units = contract['units']
    require(type(units) is list and units and all(type(u) is str and u and u != 'GLOBAL' for u in units)
            and len(units) == len(set(units)), 'UNIT_SET')
    rows = contract['obligations']
    require(type(rows) is list and rows, 'EMPTY_COVERAGE')
    seen = set()
    for row in rows:
        require(type(row) is dict and set(row) == {'obligation', 'subject', 'applicability',
                'rule_ref', 'profile_ref', 'report_schema', 'exclusion_evidence_digest'}, 'OBLIGATION_FIELDS')
        require(all(type(row[k]) is str and row[k] for k in
                    ('obligation', 'rule_ref', 'profile_ref', 'report_schema')), 'OBLIGATION_REFERENCE')
        require(row['subject'] in units + ['GLOBAL'], 'SUBJECT')
        require(key(row) not in seen, 'DUPLICATE_OBLIGATION')
        seen.add(key(row))
        require(row['applicability'] in ('REQUIRED', 'EXCLUDED', 'UNRESOLVED'), 'APPLICABILITY')
        if row['applicability'] == 'EXCLUDED':
            require(hash_ok(row['exclusion_evidence_digest']), 'EXCLUSION_EVIDENCE_REQUIRED')
        else:
            require(row['exclusion_evidence_digest'] is None, 'UNEXPECTED_EXCLUSION')
    # The declared contract is a scoped inventory, not proof that all PRD obligations
    # or all unit/subcondition combinations have been enumerated.
    return rows
def result_base():
    return {'schema': 'OBLIGATION_ADMISSION111_V1', 'state': 'BLOCKED',
            'consistency_verified': False, 'declared_conditions_complete': False,
            'product_coverage_verified': False, 'execution_authenticity_verified': False,
            **{k: False for k in AUTH}, 'rows': [], 'blockers': [],
            'scope': 'Declared coverage only; no whole-PRD inference, calibration, execution authentication or product admission.'}
def admission(contract, expected_contract_digest, binding, expected_binding_digest,
              reports, expected_report_digests):
    out = result_base()
    # Preserve valid JSON source evidence even on mismatch; non-JSON evidence has
    # a non-content forensic marker only, never repr/raw secret leakage.
    out['observed_report_preservation'] = 'NOT_ESTABLISHED'
    out['observed_report_container_type'] = type(reports).__name__
    try:
        strict([contract, binding, reports, expected_report_digests])
        out['observed_reports'] = copy.deepcopy(reports)
        out['observed_report_preservation'] = 'EXACT_VALID_JSON_COPY'
        out['observed_reports_digest'] = digest(reports)
        pin = digest([contract, binding, reports, expected_report_digests])
        obligations = validate_contract(contract, expected_contract_digest)
        require(hash_ok(expected_binding_digest) and digest(binding) == expected_binding_digest, 'BINDING_PIN')
        require(type(binding) is dict and set(binding) == set(BINDINGS), 'BINDING_FIELDS')
        require(all(hash_ok(binding[k]) for k in BINDINGS), 'BINDING_DIGEST')
        require(binding['coverage_digest'] == expected_contract_digest, 'COVERAGE_BINDING')
        require(type(reports) is dict and type(expected_report_digests) is dict
                and set(reports) == set(expected_report_digests), 'REPORT_PIN_SET')
        report_rows = {}
        for rid, report in reports.items():
            require(type(rid) is str and rid and type(report) is dict, 'REPORT_TYPE')
            require(hash_ok(expected_report_digests[rid]) and digest(report) == expected_report_digests[rid], 'REPORT_DIGEST')
            require(set(report) == {'schema', 'binding', 'rows', 'errors', 'pending',
                                    'accepted', 'qualified', 'display_allowed', 'delivery_allowed'}, 'REPORT_FIELDS')
            require(type(report['schema']) is str and bool(report['schema']), 'REPORT_SCHEMA')
            require(digest(report['binding']) == digest(binding), 'REPORT_BINDING')
            require(all(report[k] is False for k in AUTH), 'FORGED_AUTHORITY')
            require(type(report['errors']) is list and type(report['pending']) is list, 'REPORT_DIAGNOSTICS')
            if report['errors']:
                out['blockers'].append({'code': 'EVALUATOR_ERROR', 'report': rid})
            if report['pending']:
                out['blockers'].append({'code': 'REPORT_PENDING', 'report': rid})
            require(type(report['rows']) is list, 'REPORT_ROWS')
            for row in report['rows']:
                require(type(row) is dict and set(row) == {'obligation', 'subject', 'state',
                        'errors', 'pending', 'missing'}, 'RESULT_FIELDS')
                require(type(row['obligation']) is str and type(row['subject']) is str, 'RESULT_KEY')
                require(key(row) not in report_rows, 'DUPLICATE_RESULT')
                require(row['state'] in STATES, 'RESULT_STATE')
                require(all(type(row[k]) is list for k in ('errors', 'pending', 'missing')), 'RESULT_DIAGNOSTICS')
                require(all(type(x) is str and x in CODES for x in row['missing']), 'MISSING_KIND')
                report_rows[key(row)] = (rid, report['schema'], row)
        required_keys = {key(row) for row in obligations}
        require(set(report_rows) <= required_keys, 'UNDECLARED_RESULT')
        for spec in obligations:
            k = key(spec); found = report_rows.get(k)
            entry = {'obligation': k[0], 'subject': k[1], 'applicability': spec['applicability'],
                     'reported_state': None, 'blocking_reasons': [], 'report_digest': None}
            reasons = entry['blocking_reasons']
            if found:
                rid, schema, row = found
                require(schema == spec['report_schema'], 'RESULT_SCHEMA')
                entry.update(reported_state=row['state'], report_digest=expected_report_digests[rid],
                             errors=copy.deepcopy(row['errors']), pending=copy.deepcopy(row['pending']),
                             missing=copy.deepcopy(row['missing']))
                # A definite violation never disappears merely because another check errors.
                if row['state'] == 'FAIL':
                    reasons.append('NECESSARY_FAIL' if spec['applicability'] == 'REQUIRED'
                                   else 'REPORTED_FAIL_APPLICABILITY_UNRESOLVED')
                if row['state'] == 'ERROR' or row['errors']: reasons.append('EVALUATOR_ERROR')
                if row['pending']: reasons.append('NECESSARY_PENDING')
                reasons.extend(row['missing'])
            if spec['applicability'] == 'EXCLUDED':
                # Exclusion is justified by the separately pinned policy, never converted to PASS.
                if found and row['state'] != 'NOT_EVALUATED':
                    reasons.append('EXCLUDED_STATE_CONFLICT')
                entry['excluded_not_pass'] = True
                # A retained FAIL/error still remains visible and conservatively blocks this
                # study until the scope conflict is explicitly reconciled.
            else:
                if spec['applicability'] == 'UNRESOLVED':
                    reasons.append('UNRESOLVED_APPLICABILITY')
                if not found:
                    reasons.append('MISSING_EVIDENCE')
                elif row['state'] in ('UNKNOWN', 'NOT_EVALUATED'):
                    reasons.append(('NECESSARY_' if spec['applicability'] == 'REQUIRED' else 'REPORTED_') + row['state'])
            for reason in dict.fromkeys(reasons):
                out['blockers'].append({'code': reason, 'obligation': k[0], 'subject': k[1]})
            out['rows'].append(entry)
        require(digest([contract, binding, reports, expected_report_digests]) == pin, 'INPUT_MUTATION')
        require(digest(coverage_contract()) == expected_contract_digest, 'COVERAGE_SOURCE_CHANGED')
        out['consistency_verified'] = True
        out['declared_conditions_complete'] = not out['blockers']
        if not out['blockers']:
            out['state'] = 'DECLARED_CONDITIONS_COMPLETE_NOT_PRODUCT_ADMITTED'
        out['blockers'].append({'code': 'PRODUCT_COVERAGE_AND_AUTHENTIC_EXECUTION_UNESTABLISHED'})
        out['contract_digest'] = expected_contract_digest
        out['binding_digest'] = expected_binding_digest
        out['report_digests'] = copy.deepcopy(expected_report_digests)
        return out
    except (ValueError, KeyError, TypeError, UnicodeError, OverflowError, OSError) as exc:
        out['state'] = 'EVIDENCE_ERROR'
        out['consistency_verified'] = False
        out['declared_conditions_complete'] = False
        # Error messages are internal enum-like markers, never arbitrary report text.
        out['blockers'].append({'code': 'BINDING_OR_SCHEMA_ERROR', 'error_type': type(exc).__name__})
        return out
