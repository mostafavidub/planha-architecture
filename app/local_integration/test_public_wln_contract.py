"""Task 1.1 only: public input validation is never design acceptance."""
import copy,json,unittest
from fractions import Fraction
from public_wln_contract import parse_public,verify_public,engine_raw
from dimension_contract import InputError
def body(**changes):
    x={'W':'12.5','L':'20','n':2};x.update(changes)
    return json.dumps(x,ensure_ascii=False).encode()
class PublicWLNTests(unittest.TestCase):
    def reject(self,b,code=None,status=None):
        with self.assertRaises(InputError) as e:parse_public(b)
        if code:self.assertEqual(e.exception.code,code)
        if status:self.assertEqual(e.exception.status,status)
    def test_four_boundaries(self):
        for w,l in ((5,5),(5,25),(25,5),(25,25)):
            e=parse_public(body(W=w,L=l));r=engine_raw(e)
            self.assertEqual((r['W'],r['L'],r['n']),(str(w),str(l),2))
    def test_outside_each_axis_exact(self):
        for a in ('W','L'):
            for v in ('4.999999999999999999','25.000000000000000001',45):
                self.reject(body(**{a:v}),'DIMENSION_OUT_OF_OWNER_RANGE',422)
    def test_exact_decimal_no_float(self):
        for v in ('5.000000000000000001','24.123456789012345678901234567890123456789','25.000000'):
            e=parse_public(body(W=v));r=engine_raw(e)
            self.assertEqual(Fraction(r['W']),Fraction(v))
            self.assertEqual(e['canonical_request']['dimensions_m']['W'],
                {'numerator':str(Fraction(v).numerator),'denominator':str(Fraction(v).denominator)})
    def test_localized_digits(self):
        for v,w in (('۵','5'),('٢٥','25'),('۱۲٫۵','12.5')):
            self.assertEqual(Fraction(engine_raw(parse_public(body(W=v)))['W']),Fraction(w))
    def test_three_fields_only(self):
        for k in ('bedrooms','requested_count','program','sleep_roles','capability','mode','accepted'):
            self.reject(body(**{k:2}),'UNEXPECTED_PUBLIC_FIELD',422)
    def test_missing(self):
        for k in ('W','L','n'):
            x=json.loads(body());del x[k];self.reject(json.dumps(x).encode(),'INPUT_REQUIRED' if k=='n' else 'FIELD_REQUIRED')
    def test_duplicates(self):
        for b in (b'{"W":5,"W":25,"L":20,"n":2}',b'{"W":5,"\\u0057":25,"L":20,"n":2}',
                  b'{"W":5,"L":20,"n":2,"program":{"x":1,"x":2}}'):
            self.reject(b,'DUPLICATE_FIELD')
    def test_invalid_types(self):
        for k in ('W','L','n'):
            for v in (True,False,None,[],{}):self.reject(body(**{k:v}),('INPUT_REQUIRED' if v is None else 'INVALID_BRIEF') if k=='n' else 'INVALID_FIELD_TYPE')
    def test_invalid_unit_count(self):
        for v in (0,-1,'0','-1','1.5','01',' 2'):
            self.reject(body(n=v),status=422)
    def test_valid_unsupported_unit_count(self):
        for n in (1,'1'):
            e=parse_public(body(n=n))
            self.assertEqual(e['canonical_request']['unit_count'],int(n))
            self.assertEqual(e['capability_status'],'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT')
            with self.assertRaises(InputError) as ex:engine_raw(e)
            self.assertEqual((ex.exception.status,ex.exception.code),(409,'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT'))
    def test_mvp_unit_domain(self):
        for n in (3,4,'3','4','۳','٤',100):
            self.reject(body(n=n),'INVALID_BRIEF',422)
        self.assertEqual(parse_public(body())['schema'],'V25_PUBLIC_WLN_CONTRACT_V3')
    def test_v1_envelope_not_silently_relabelled(self):
        e=parse_public(body());e['schema']='V25_PUBLIC_WLN_CONTRACT_V1'
        with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):engine_raw(e)
    def test_nonfinite_and_decimal_token_policy(self):
        for tok in ('NaN','Infinity','-Infinity'):
            self.reject(('{"W":'+tok+',"L":20,"n":2}').encode(),'NONFINITE_NUMBER',422)
        for tok in ('12.5','2.0','2e0','1e400','1e-4000'):
            self.reject(('{"W":'+tok+',"L":20,"n":2}').encode(),'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION',409)
    def test_body_depth_numeric_limits(self):
        self.reject(b' '*16385,'UNSUPPORTED_BODY_LIMIT',409)
        self.reject(b'['*25+b'0'+b']'*25,'UNSUPPORTED_NESTING_DEPTH',409)
        self.reject(body(W='5'*65),'UNSUPPORTED_NUMERIC_LENGTH',409)
        self.reject(body(n='9007199254740992'),'UNSUPPORTED_COUNT_TRANSPORT_PRECISION',409)
    def test_malformed(self):
        for b in (b'{',b'\xff',b'[]',b'null',b'{"W":"\\ud800","L":20,"n":2}'):
            self.reject(b,status=422)
        self.reject('notbytes','BODY_BYTES_REQUIRED')
    def test_original_bytes_binding(self):
        b=body();e=parse_public(b);self.assertEqual(verify_public(b,e),e)
        with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):verify_public(b+b' ',e)
    def test_envelope_mutations(self):
        e=parse_public(body())
        changes=[lambda x:x['canonical_request'].__setitem__('unit_count',True),
                 lambda x:x['canonical_request']['dimensions_m']['W'].__setitem__('denominator','3'),
                 lambda x:x.__setitem__('accepted',0),lambda x:x.__setitem__('qualified',True),
                 lambda x:x.__setitem__('unexpected',1)]
        for change in changes:
            x=copy.deepcopy(e);change(x)
            with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):engine_raw(x)
    def test_malformed_envelope_cycles_and_depth(self):
        e=parse_public(body());e['received_input']['W']=e
        with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):engine_raw(e)
        e=parse_public(body());deep=[]
        for _ in range(1200):deep=[deep]
        e['received_input']['W']=deep
        with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):engine_raw(e)
    def test_transport_hash_requires_original_bytes_verification(self):
        b=body();e=parse_public(b);e['transport_body_sha256']='0'*64
        # Conversion alone authenticates no transport. Future integration must verify bytes.
        self.assertEqual(engine_raw(e)['n'],2)
        with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):verify_public(b,e)
    def test_no_authority_or_hidden_program(self):
        e=parse_public(body());r=engine_raw(e)
        self.assertEqual(set(e['received_input']),{'W','L','n'})
        self.assertEqual(set(r),{'W','L','n','requested_count'})
        self.assertEqual(r['requested_count'],1)
        for k in ('accepted','qualified','display_allowed','delivery_allowed'):self.assertIs(e[k],False)
        self.assertNotIn('model',e);self.assertNotIn('program',r)
    def test_axis_independence(self):
        a=engine_raw(parse_public(body()));b=engine_raw(parse_public(body(W='13')))
        self.assertNotEqual(a['W'],b['W']);self.assertEqual(a['L'],b['L'])
    def test_input_unchanged(self):
        e=parse_public(body());before=copy.deepcopy(e);engine_raw(e);self.assertEqual(e,before)
if __name__=='__main__':unittest.main()
