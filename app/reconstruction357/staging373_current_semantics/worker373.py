import json,sys,traceback
from pathlib import Path
from gate373 import validate
P=Path(sys.argv[1])
try:
 payload=json.loads((P/'input_payload.json').read_text());validate(payload['record'],payload['fresh'],payload['lineage'])
 from semantic373 import run
 result=run(payload['record'],payload['fresh'],payload['lineage'])
 with(P/'result.json').open('x')as f:json.dump(result,f,indent=2)
except BaseException:
 (P/'error.txt').write_text(traceback.format_exc());raise
