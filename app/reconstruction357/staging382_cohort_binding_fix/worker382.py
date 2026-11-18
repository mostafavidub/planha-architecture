import json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;P=Path(sys.argv[1]);start=time.monotonic()
sys.path[:0]=[str(HERE),str(ROOT/'staging381_role_semantics'),str(ROOT/'semantic_rules357'),str(ROOT/'staging378_finite_portals'),str(ROOT/'finite_comparison358')]
try:
 from gate381 import load_inputs
 from cohort382 import evaluate
 i=load_inputs();result=evaluate(i['record'],i['fresh']);(P/'result.json').write_text(json.dumps(result,indent=2))
except Exception as e:
 (P/'error.json').write_text(json.dumps({'error':type(e).__name__+':'+str(e),'seconds':time.monotonic()-start}));raise
