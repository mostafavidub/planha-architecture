import sys,json,hashlib,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;OUT=BASE/'review358_source_validation'
INPUT=BASE/'staging358_comparative/row_candidate358.json'

def frozen_check():
 f=json.loads((OUT/'frozen_sources.json').read_text())
 for name,h in f['sources'].items():
  if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=h:raise ValueError('FROZEN_SOURCE_MISMATCH:'+name)
 if hashlib.sha256(INPUT.read_bytes()).hexdigest()!=f['input_sha256']:raise ValueError('INPUT_FILE_MISMATCH')
 return f
if __name__=='__main__':
 frozen_check()
 if '--worker' in sys.argv:
  try:
   from evaluate358 import evaluate358
   result=evaluate358(json.loads(INPUT.read_text()),90)
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
  except Exception as e:
   (OUT/'error.json').write_text(json.dumps({'error':type(e).__name__+':'+str(e),'traceback':traceback.format_exc(),'accepted':False}));raise
 else:
  from supervisor import supervise
  result=supervise([sys.executable,str(Path(__file__).resolve()),'--worker'],110,evidence_directory=OUT)
  (OUT/'supervision.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
