"""Public three-field contract only. Diagnostic program/count API stays separate."""
import copy, hashlib, json
from decimal import Decimal, localcontext
from dimension_contract import (InputError, MAX_BODY, JsonDecimal, _pairs,
    _nonfinite, _integer, _bounded_tree, _number, digest)

SCHEMA = 'V25_PUBLIC_WLN_CONTRACT_V1'
def parse_public(body):
    if type(body) is not bytes: raise InputError('BODY_BYTES_REQUIRED')
    if len(body)>MAX_BODY: raise InputError('UNSUPPORTED_BODY_LIMIT',status=409)
    try:
        raw=json.loads(body.decode('utf-8'),object_pairs_hook=_pairs,
            parse_float=JsonDecimal,parse_int=_integer,parse_constant=_nonfinite)
    except InputError: raise
    except RecursionError: raise InputError('UNSUPPORTED_NESTING_DEPTH',status=409)
    except (UnicodeError,ValueError): raise InputError('JSON_SYNTAX_INVALID')
    _bounded_tree(raw)
    if type(raw) is not dict: raise InputError('OBJECT_REQUIRED')
    if set(raw)-{'W','L','n'}: raise InputError('UNEXPECTED_PUBLIC_FIELD',sorted(set(raw)-{'W','L','n'})[0])
    if {'W','L','n'}-set(raw): raise InputError('FIELD_REQUIRED',sorted({'W','L','n'}-set(raw))[0])
    dimensions={a:_number(raw[a],a) for a in ('W','L')}
    n=_number(raw['n'],'n',count=True)
    canonical={'dimensions_m':dimensions,'unit_count':n}
    return {'schema':SCHEMA,'received_input':copy.deepcopy(raw),
        'transport_body_sha256':hashlib.sha256(body).hexdigest(),
        'canonical_request':canonical,'canonical_request_digest':digest(canonical),
        'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
        'capability_status':'SUPPORTED_INPUT_ONLY' if n==2 else 'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT'}

def engine_raw(envelope):
    # Rebuild the envelope from its preserved input and check all semantic fields.
    # Original transport hash cannot be reconstructed without the original bytes.
    if type(envelope) is not dict: raise InputError('ENVELOPE_BINDING_CHANGED')
    try:
        expected=parse_public(json.dumps(envelope['received_input'],ensure_ascii=False,allow_nan=False).encode())
        if set(envelope)!=set(expected): raise ValueError('FIELDS')
        for key in expected:
            if key!='transport_body_sha256' and digest(envelope[key])!=digest(expected[key]): raise ValueError(key)
        h=envelope['transport_body_sha256']
        if type(h) is not str or len(h)!=64 or any(c not in '0123456789abcdef' for c in h): raise ValueError('HASH')
    except (KeyError,TypeError,ValueError,UnicodeError,RecursionError):
        raise InputError('ENVELOPE_BINDING_CHANGED')
    c=envelope['canonical_request'];out={}
    if c['unit_count']!=2: raise InputError('UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT','n',409)
    for a in ('W','L'):
        q=c['dimensions_m'][a]
        with localcontext() as ctx:
            ctx.prec=140
            out[a]=format(Decimal(q['numerator'])/Decimal(q['denominator']),'f')
    out.update(n=c['unit_count'],requested_count=1)
    return out

def verify_public(body,envelope):
    expected=parse_public(body)
    try: same=digest(expected)==digest(envelope)
    except (TypeError,ValueError,RecursionError,UnicodeError): same=False
    if not same: raise InputError('ENVELOPE_BINDING_CHANGED')
    return expected
