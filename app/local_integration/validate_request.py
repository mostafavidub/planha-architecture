"""Local validation-only command; stdin JSON -> typed response. No generation."""
import json
import sys
from dimension_contract import MAX_BODY, evaluate


def main():
    status, result = evaluate(sys.stdin.buffer.read(MAX_BODY + 1))
    print(json.dumps({'http_status': status, **result}, ensure_ascii=False,
                     sort_keys=True, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
