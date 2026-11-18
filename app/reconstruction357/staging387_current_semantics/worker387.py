"""Optional isolated entrypoint; orchestrator may call run_member directly."""
import json,sys,time,traceback
from pathlib import Path
P=Path(sys.argv[1]);start=time.monotonic()
try:
 from integration387 import run_member
 result=run_member(P,sys.argv[2])
 with(P/'semantic.json').open('x')as f:json.dump(result,f,indent=2)
except Exception as error:
 with(P/'semantic_error.json').open('x')as f:json.dump({'error':type(error).__name__+':'+str(error),'traceback':traceback.format_exc(),'seconds':time.monotonic()-start},f,indent=2)
 raise
