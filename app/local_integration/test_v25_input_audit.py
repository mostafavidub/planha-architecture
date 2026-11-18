"""V25 input-only audit. No geometric generation or architectural acceptance."""
import json
import unittest
from fractions import Fraction
from unittest.mock import patch
from dimension_contract import parse, InputError
from parametric_worker import prepare
import generation_gateway

MATRIX = [(str(w), str(l)) for w in (5,15,25) for l in (5,15,25)] + [('10','20'),('20','10'),('24.5','23.25')]

def body(w='25', l='25'):
    return json.dumps(dict(W=w,L=l,n=2,requested_count=1), ensure_ascii=False).encode()

class V25InputAudit(unittest.TestCase):
    def test_preregistered_matrix_exact_binding_no_acceptance(self):
        for w,l in MATRIX:
            with self.subTest(W=w,L=l):
                envelope, raw = prepare(body(w,l))
                self.assertEqual(Fraction(raw['W']), Fraction(w))
                self.assertEqual(Fraction(raw['L']), Fraction(l))
                self.assertFalse(envelope['accepted'])
                self.assertFalse(envelope['delivery_allowed'])
                for axis, value in (('W',w),('L',l)):
                    exact=envelope['canonical_request']['dimensions_m'][axis]
                    self.assertEqual(Fraction(int(exact['numerator']),int(exact['denominator'])),Fraction(value))
    def test_scripts_and_inclusive_edges(self):
        for value, expected in [('۵','5'),('۲۵','25'),('٥','5'),('٢٥','25'),('۲۴٫۵','24.5'),('٢٣٫٢٥','23.25')]:
            for axis in ('W','L'):
                pair={'w':'25','l':'25'};pair[axis.lower()]=value
                with self.subTest(axis=axis,value=value):
                    e=parse(body(**pair))
                    x=e['canonical_request']['dimensions_m'][axis]
                    self.assertEqual(Fraction(int(x['numerator']),int(x['denominator'])), Fraction(expected))
    def test_outside_has_no_process_or_evidence_creation(self):
        with patch.object(generation_gateway.subprocess,'Popen') as process, patch.object(generation_gateway.Path,'mkdir') as mkdir:
            for axis in ('w','l'):
                for value in ('4.9999','25.0001','۲۵٫۰۰۰۱','٢٥٫٠٠٠١','45','1000'):
                    pair={'w':'25','l':'25'};pair[axis]=value
                    with self.subTest(axis=axis,value=value):
                        status,result=generation_gateway.generate(body(**pair))
                        self.assertEqual(status,422)
                        self.assertEqual(result['code'],'DIMENSION_OUT_OF_OWNER_RANGE')
                        self.assertEqual(result['field'],axis.upper())
                        self.assertNotIn('run_id',result)
                        self.assertFalse(result['accepted'])
                        self.assertFalse(result['delivery_allowed'])
            process.assert_not_called()
            mkdir.assert_not_called()
    def test_valid_input_is_not_claim_of_feasibility(self):
        e=parse(body('5','5'))
        self.assertFalse(e['accepted'])
        self.assertFalse(e['delivery_allowed'])
        self.assertNotIn('model',e)
    def test_json_decimal_policy_is_explicit(self):
        with self.assertRaises(InputError) as error:
            parse(b'{"W":24.5,"L":"25","n":2,"requested_count":1}')
        self.assertEqual(error.exception.code,'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION')

if __name__ == '__main__':
    unittest.main()
