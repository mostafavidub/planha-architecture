"""Runs in its own Python process: no solver or application imported."""
import json,sys,tempfile
from pathlib import Path
from containment361 import supervise
with tempfile.TemporaryDirectory() as d:
 marker=Path(d)/'pid'
 # Immediate worker exits; detached grandchild outlives it and is adopted.
 code="import os,time; p=os.fork();\nif p==0:\n os.setsid(); open("+repr(str(marker))+",'w').write(str(os.getpid())); time.sleep(30)\nelse:\n os._exit(0)"
 result=supervise([sys.executable,'-c',code],2)
 assert marker.exists(),result
 pid=int(marker.read_text())
 assert pid in [x['pid'] for x in result['tracked_processes']],result
 assert result['cleanup_verified'] and result['worker_reaped'] and not result['unresolved'],result
 assert not Path('/proc',str(pid)).exists(),result
 print(json.dumps({'test':'DETACHED_CHILD_EARLY_PARENT_EXIT','passed':True,'supervision':result}))
