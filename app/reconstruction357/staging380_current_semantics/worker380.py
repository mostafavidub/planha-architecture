import json,sys,time
from pathlib import Path
from gate380 import load_inputs
P=Path(sys.argv[1]);start=time.monotonic()
try:
 from semantic380 import run
 i=load_inputs();result=run(i['record'],i['fresh']);(P/'result.json').write_text(json.dumps(result,indent=2))
except Exception as e:
 (P/'error.json').write_text(json.dumps({'error':type(e).__name__+':'+str(e),'seconds':time.monotonic()-start}));raise
