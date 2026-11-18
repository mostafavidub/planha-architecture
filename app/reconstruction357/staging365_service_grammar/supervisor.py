"""Loaded only after pre-import freeze validation by run_audited.py."""
import os,sys,json,time
from pathlib import Path
from contract import HERE,check_pins
from containment import supervise

def main():
 check_pins()
 with (HERE/'attempt_started.json').open('x') as f:json.dump({'started':time.time(),'max_solver_calls':1,'outer_seconds':60},f)
 os.environ.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
 result=supervise([sys.executable,str(HERE/'run_audited.py'),'--worker'],60,evidence_directory=HERE)
 result.update(retry=0,accepted=False,delivery_allowed=False)
 (HERE/'supervision.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
