import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "staging368_final_pipeline"))
from request_contract368 import parse_json
from negative_cases397 import FORM_CASES, API_CASES, RAW_API_CASES, VALID_PREFLIGHT_ONLY


class MatrixTests(unittest.TestCase):
    def test_every_negative_is_preclassified(self):
        for name, value, reason in FORM_CASES + API_CASES:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "^" + reason.replace(".", "\\.") + "$"):
                parse_json(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
        for name, body, reason in RAW_API_CASES:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "^" + reason + "$"):
                parse_json(body)

    def test_decimal_dimension_strings_are_valid_but_not_network_cases(self):
        for name, value in VALID_PREFLIGHT_ONLY:
            with self.subTest(name=name):
                envelope = parse_json(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
                self.assertEqual(envelope["normalized_raw"], {"W": "26", "L": "28", "n": 2, "requested_count": 2})

    def test_no_valid_case_in_negative_network_matrix(self):
        self.assertEqual(len(FORM_CASES) + len(API_CASES) + len(RAW_API_CASES), 15)


if __name__ == "__main__":
    unittest.main()
