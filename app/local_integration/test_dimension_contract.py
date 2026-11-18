import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from dimension_contract import InputError, evaluate, parse, verify


def body(**changes):
    value = {'W': '12', 'L': '14', 'n': 1, 'requested_count': 6}
    value.update(changes)
    return json.dumps(value, ensure_ascii=False).encode()


class ContractTests(unittest.TestCase):
    def test_four_corners_and_center(self):
        for w, l in [(5,5),(5,25),(25,5),(25,25),(25,25)]:
            with self.subTest(w=w,l=l):
                request = parse(body(W=w,L=l))['canonical_request']
                self.assertEqual(request['dimensions_m'], {'W': {'numerator':str(w),'denominator':'1'}, 'L': {'numerator':str(l),'denominator':'1'}})
                self.assertEqual((request['unit_count'], request['requested_count']), (1,6))

    def test_exact_boundaries_no_rounding(self):
        for value in ['4.999999999999999999999', '25.000000000000000001']:
            self.assertEqual(evaluate(body(W=value))[0], 422)
        exact = parse(body(W='5.000000000000000001'))['canonical_request']['dimensions_m']['W']
        self.assertEqual(exact, {'numerator':'5000000000000000001','denominator':'1000000000000000000'})

    def test_both_digit_systems(self):
        for w,l in [('۵','۲۵'),('١٢٫٥','١٤')]:
            parsed = parse(body(W=w,L=l))
            self.assertEqual(parsed['received_input']['W'], w)
            self.assertEqual(evaluate(body(W=w,L=l))[0],409)

    def test_axis_independence(self):
        a = parse(body())['canonical_request']; b = parse(body(W='13'))['canonical_request']
        self.assertNotEqual(a['dimensions_m']['W'],b['dimensions_m']['W'])
        self.assertEqual(a['dimensions_m']['L'],b['dimensions_m']['L'])
        self.assertEqual(a['unit_count'],b['unit_count']);self.assertEqual(a['requested_count'],b['requested_count'])

    def test_program_preserved_not_defaulted(self):
        program = {'bedrooms': 2, 'notes': ['خواسته مالک']}
        value = parse(body(program=program))
        self.assertEqual(value['canonical_request']['program'],program)
        self.assertNotIn('program',parse(body())['canonical_request'])
        value['canonical_request']['program']['notes'].append('changed')
        self.assertEqual(value['received_input']['program'],program)

    def test_roundtrip_and_binding(self):
        raw=body(); envelope=json.loads(json.dumps(parse(raw)))
        self.assertEqual(verify(raw,copy.deepcopy(envelope)),envelope)
        envelope['canonical_request']['unit_count']=2
        with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):verify(raw,envelope)

    def test_other_request_and_transport_mutation(self):
        raw=body(); envelope=parse(raw)
        for other in [body(L='15'),raw+b' ']:
            with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):verify(other,envelope)

    def test_false_booleans_cannot_equal_zero(self):
        raw=body();env=parse(raw);env['accepted']=0
        with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):verify(raw,env)

    def test_invalid_fields(self):
        for change in [{'W':True},{'L':None},{'W':[]},{'W':''},{'W':'NaN'},{'W':'Infinity'},{'W':'-5'},{'n':0},{'n':'1.0'},{'requested_count':False},{'W':46},{'L':4},{'unexpected':'value'}]:
            with self.subTest(change=change):self.assertEqual(evaluate(body(**change))[0],422)

    def test_missing_fields(self):
        for key in ['W','L','n','requested_count']:
            obj=json.loads(body());obj.pop(key)
            self.assertEqual(evaluate(json.dumps(obj).encode())[1]['code'],'FIELD_REQUIRED')

    def test_duplicate_fields_nested_or_top_level(self):
        for raw in [b'{"W":5,"W":6}',b'{"program":{"x":1,"x":2}}']:
            self.assertEqual(evaluate(raw)[1]['code'],'DUPLICATE_FIELD')

    def test_bad_json_and_unicode(self):
        for raw in [b'{',b'\xff',b'null',b'[]',b'{"W":"\\ud800"}']:
            self.assertEqual(evaluate(raw)[0],422)

    def test_decimal_tokens_not_overflowed(self):
        for token in [b'1e400',b'12.5']:
            raw=b'{"W":'+token+b',"L":14,"n":1,"requested_count":6}'
            self.assertEqual(evaluate(raw)[1]['code'],'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION')
        for token in [b'NaN',b'Infinity',b'-Infinity']:
            self.assertEqual(evaluate(b'{"W":'+token+b'}')[0],422)

    def test_technical_limits_not_invalid_geometry(self):
        for raw in [b' '*16385,body(W='0'*65),b'['*25+b'0'+b']'*25]:
            self.assertEqual(evaluate(raw)[0],409)

    def test_valid_does_not_admit_or_fallback(self):
        for w,l,n,count in [(24,25,2,2),(12,14,1,6),(25,5,2,6),(13,15,3,8)]:
            status,result=evaluate(body(W=w,L=l,n=n,requested_count=count))
            self.assertEqual(status,409);self.assertFalse(result['accepted']);self.assertFalse(result['delivery_allowed'])
            self.assertEqual(result['envelope']['canonical_request']['requested_count'],count)
            self.assertNotIn('model',result)

    def test_count_transport_precision(self):
        self.assertEqual(evaluate(body(requested_count='9007199254740992'))[1]['code'], 'UNSUPPORTED_COUNT_TRANSPORT_PRECISION')

    def test_integer_token_limit_before_python_conversion(self):
        raw=b'{"W":'+b'9'*5000+b',"L":14,"n":1,"requested_count":6}'
        self.assertEqual(evaluate(raw)[1]['code'],'UNSUPPORTED_NUMERIC_LENGTH')
        self.assertEqual(evaluate(raw)[0],409)

    def test_actual_cli(self):
        script=Path(__file__).with_name('validate_request.py')
        for raw,expected in [(body(),409),(b'{',422)]:
            run=subprocess.run([sys.executable,'-B',str(script)],input=raw,capture_output=True,timeout=5)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(json.loads(run.stdout)['http_status'],expected)


if __name__ == '__main__': unittest.main()
