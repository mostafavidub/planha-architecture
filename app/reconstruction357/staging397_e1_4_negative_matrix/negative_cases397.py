"""Preregistered negative matrix plus valid decimal-text preflight; no valid network POST."""
BASE = {"W": "۲۶", "L": "۲۸", "n": "۲", "requested_count": "۲"}

FORM_CASES = [
    ("empty_width", {**BASE, "W": ""}, "EXACT_DECIMAL_REQUIRED:W"),
    ("space_only_length", {**BASE, "L": "   "}, "EXACT_DECIMAL_REQUIRED:L"),
    ("outside_width", {**BASE, "W": "۲۵"}, "UNSUPPORTED_EXACT_FIXED_DIMENSION:W"),
    ("zero_units", {**BASE, "n": "۰"}, "COUNT_CANONICAL_DIGITS_REQUIRED:n"),
    ("negative_requested_count", {**BASE, "requested_count": "-۲"}, "EXACT_DECIMAL_REQUIRED:requested_count"),
    ("decimal_requested_count", {**BASE, "requested_count": "۲٫۵"}, "COUNT_CANONICAL_DIGITS_REQUIRED:requested_count"),
    ("exponent_units", {**BASE, "n": "2e0"}, "EXACT_DECIMAL_REQUIRED:n"),
    ("overprecision_width", {**BASE, "W": "26.0001"}, "UNSUPPORTED_EXACT_FIXED_DIMENSION:W"),
]

API_CASES = [
    ("wrong_type_boolean_width", {**BASE, "W": True}, "INVALID_FIELD_TYPE:W"),
    ("wrong_type_array_units", {**BASE, "n": [2]}, "INVALID_FIELD_TYPE:n"),
    ("missing_requested_count", {"W": "۲۶", "L": "۲۸", "n": "۲"}, "EXACT_FIELD_INVENTORY_REQUIRED"),
    ("extra_custom_program", {**BASE, "program": {"bedrooms": 4}}, "EXACT_FIELD_INVENTORY_REQUIRED"),
    ("extra_program_name", {**BASE, "program_name": "owner_custom"}, "EXACT_FIELD_INVENTORY_REQUIRED"),
]

RAW_API_CASES = [
    ("json_float_width", '{"W":26.0,"L":"۲۸","n":"۲","requested_count":"۲"}', "JSON_FLOAT_NOT_SUPPORTED_USE_DECIMAL_TEXT"),
    ("duplicate_width", '{"W":"۲۶","W":"۲۵","L":"۲۸","n":"۲","requested_count":"۲"}', "DUPLICATE_FIELD:W"),
]

VALID_PREFLIGHT_ONLY = [
    ("ascii_decimal_dimension_text", {"W": "26.0", "L": "28.00", "n": "2", "requested_count": "2"}),
    ("persian_decimal_dimension_text", {"W": "۲۶٫۰", "L": "۲۸٫۰۰", "n": "۲", "requested_count": "۲"}),
]
