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
    except (UnicodeError,ValueError,RecursionError): raise InputError('JSON_SYNTAX_INVALID')
    _bounded_tree(raw)
    if type(raw) is not dict: raise InputError('OBJECT_REQUIRED')
    if set(raw)-{'W','L','n'}: raise InputError('UNEXPECTED_PUBLIC_FIELD',sorted(set(raw)-{'W','L','n'})[0])
    if {'W','L','n'}-set(raw): raise InputError('FIELD_REQUIRED',sorted({'W','L','n'}-set(raw))[0])
    dimensions={a:_number(raw[a],a) for a in ('W','L')}
    n=_number(raw['n'],'n',count=True)
    if n!=2: raise InputError('UNSUPPORTED_CURRENT_MVP_UNIT_COUNT','n',409)
    canonical={'dimensions_m':dimensions,'unit_count':n}
    return {'schema':SCHEMA,'received_input':copy.deepcopy(raw),
        'transport_body_sha256':hashlib.sha256(body).hexdigest(),
        'canonical_request':canonical,'canonical_request_digest':digest(canonical),
        'accepted':False,'delivery_allowed':False}

def engine_raw(envelope):
    c=envelope['canonical_request'];out={}
    for a in ('W','L'):
        q=c['dimensions_m'][a]
        with localcontext() as ctx:
            ctx.prec=140
            out[a]=format(Decimal(q['numerator'])/Decimal(q['denominator']),'f')
    out.update(n=c['unit_count'],requested_count=1)
    return out
