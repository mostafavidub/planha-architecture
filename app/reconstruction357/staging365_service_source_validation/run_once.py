import sys,json,hashlib,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;OUT=BASE/'review365_service_source_validation'
INPUT=BASE/'staging365_service_grammar/candidate365.json'

def frozen_check():
 data=(OUT/'frozen_sources.json').read_bytes()
 expected=sys.argv[sys.argv.index('--expected-freeze-sha')+1] if '--expected-freeze-sha'in sys.argv else None
 if expected is None or hashlib.sha256(data).hexdigest()!=expected:raise ValueError('FROZEN_MANIFEST_EXTERNAL_ANCHOR_MISMATCH')
 f=json.loads(data)
 for name,h in f['sources'].items():
  if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=h:raise ValueError('FROZEN_SOURCE_MISMATCH:'+name)
 if hashlib.sha256(INPUT.read_bytes()).hexdigest()!=f['input_sha256']:raise ValueError('INPUT_FILE_MISMATCH')
 return f
if __name__=='__main__':
 frozen_check()
 if '--worker' in sys.argv:
  try:
   from evaluate365 import evaluate365
   result=evaluate365(json.loads(INPUT.read_text()),90)
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
  except Exception as e:
   (OUT/'error.json').write_text(json.dumps({'error':type(e).__name__+':'+str(e),'traceback':traceback.format_exc(),'accepted':False}));raise
 else:
  if any((OUT/n).exists() for n in ('result.json','error.json','supervision.json')):raise SystemExit('PRESERVE_ONE_ATTEMPT')
  from supervisor import supervise
  result=supervise([sys.executable,str(Path(__file__).resolve()),'--worker','--expected-freeze-sha',sys.argv[sys.argv.index('--expected-freeze-sha')+1]],110,evidence_directory=OUT)
  (OUT/'supervision.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
