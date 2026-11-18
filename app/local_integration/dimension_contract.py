"""Mac-native DIM-B2/B3 reimplementation, not recovered 541/588 source.

Exact input validation is separate from geometric feasibility and permission
for generation. Current owner range is inclusive 5..25 on each axis; no clamping.
"""
import copy
import hashlib
import json
import re
from decimal import Decimal
from fractions import Fraction

SCHEMA = 'PLANHA_MAC_DIMENSION_VALIDATION_V1'
TRANSLATE = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩٫', '01234567890123456789.')
MAX_BODY = 16384


class InputError(ValueError):
    def __init__(self, code, field=None, status=422):
        super().__init__(code)
        self.code, self.field, self.status = code, field, status


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise InputError('DUPLICATE_FIELD', key)
        result[key] = value
    return result


def _nonfinite(token):
    raise InputError('NONFINITE_NUMBER')


def _integer(token):
    if len(token.lstrip('-')) > 64:
        raise InputError('UNSUPPORTED_NUMERIC_LENGTH', status=409)
    return int(token)


class JsonDecimal(str):
    """Retain lexical decimal token; do not overflow/coerce it to float."""


def _bounded_tree(value, depth=0):
    if depth > 20:
        raise InputError('UNSUPPORTED_NESTING_DEPTH', status=409)
    if isinstance(value, JsonDecimal):
        raise InputError('UNSUPPORTED_JSON_DECIMAL_REPRESENTATION', status=409)
    if isinstance(value, str):
        try:
            value.encode('utf-8')
        except UnicodeError:
            raise InputError('INVALID_UNICODE')
    elif isinstance(value, dict):
        for key, item in value.items():
            _bounded_tree(key, depth + 1)
            _bounded_tree(item, depth + 1)
    elif isinstance(value, list):
        for item in value:
            _bounded_tree(item, depth + 1)


def _number(value, field, count=False):
    if type(value) not in (str, int):
        raise InputError('INVALID_FIELD_TYPE', field)
    text = str(value).strip().translate(TRANSLATE)
    if len(text) > 64:
        raise InputError('UNSUPPORTED_NUMERIC_LENGTH', field, 409)
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?', text):
        raise InputError('EXACT_DECIMAL_REQUIRED', field)
    number = Decimal(text)
    if count:
        if not re.fullmatch(r'[1-9][0-9]*', text) or str(value) != str(value).strip():
            raise InputError('POSITIVE_INTEGER_REQUIRED', field)
        if number > 9007199254740991:
            raise InputError('UNSUPPORTED_COUNT_TRANSPORT_PRECISION', field, 409)
        return int(number)
    if not Decimal(5) <= number <= Decimal(25):
        raise InputError('DIMENSION_OUT_OF_OWNER_RANGE', field)
    exact = Fraction(number)
    return {'numerator': str(exact.numerator), 'denominator': str(exact.denominator)}


def parse(body):
    if type(body) is not bytes:
        raise InputError('BODY_BYTES_REQUIRED')
    if len(body) > MAX_BODY:
        raise InputError('UNSUPPORTED_BODY_LIMIT', status=409)
    try:
        text = body.decode('utf-8')
        raw = json.loads(text, object_pairs_hook=_pairs,
                         parse_float=JsonDecimal, parse_int=_integer, parse_constant=_nonfinite)
    except InputError:
        raise
    except RecursionError:
        raise InputError('UNSUPPORTED_NESTING_DEPTH', status=409)
    except (UnicodeError, ValueError):
        raise InputError('JSON_SYNTAX_INVALID')
    _bounded_tree(raw)
    if type(raw) is not dict:
        raise InputError('OBJECT_REQUIRED')
    required = {'W', 'L', 'n', 'requested_count'}
    if required - raw.keys():
        raise InputError('FIELD_REQUIRED', sorted(required - raw.keys())[0])
    if raw.keys() - required - {'program'}:
        raise InputError('UNEXPECTED_FIELD', sorted(raw.keys() - required - {'program'})[0])
    canonical = {
        'dimensions_m': {axis: _number(raw[axis], axis) for axis in ('W', 'L')},
        'unit_count': _number(raw['n'], 'n', count=True),
        'requested_count': _number(raw['requested_count'], 'requested_count', count=True),
        'program_present': 'program' in raw,
    }
    if 'program' in raw:
        canonical['program'] = copy.deepcopy(raw['program'])
    return {
        'schema': SCHEMA,
        'received_input': copy.deepcopy(raw),
        'transport_body_sha256': hashlib.sha256(body).hexdigest(),
        'received_digest': digest(raw),
        'canonical_request': canonical,
        'canonical_request_digest': digest(canonical),
        'accepted': False,
        'delivery_allowed': False,
    }


def verify(body, envelope):
    """Rebuild from actual bytes, not caller-provided canonical claims."""
    expected = parse(body)
    try:
        matches = digest(expected) == digest(envelope)
    except (TypeError, ValueError, RecursionError, UnicodeError):
        matches = False
    if not matches:
        raise InputError('ENVELOPE_BINDING_CHANGED')
    return expected


def evaluate(body):
    """Explicitly unsupported until a verified generator/program capability exists.

    Intentionally takes no dispatcher/caller capability: valid input cannot
    invoke the historical fixed 26 x 28 generator as an implicit fallback.
    """
    try:
        envelope = parse(body)
    except InputError as error:
        return error.status, {
            'schema': SCHEMA,
            'outcome': 'INVALID_INPUT' if error.status == 422 else 'UNSUPPORTED',
            'code': error.code, 'field': error.field,
            'accepted': False, 'delivery_allowed': False,
        }
    return 409, {'schema': SCHEMA, 'outcome': 'UNSUPPORTED',
                 'code': 'UNSUPPORTED_CURRENT_IMPLEMENTATION',
                 'accepted': False, 'delivery_allowed': False,
                 'envelope': envelope}
