import json,time
from pathlib import Path
from engine114 import run
P=Path(__file__).resolve().parent
for case in (1,2):
 raw=json.loads((P.parent/f'planha_hybrid_independent/baseline117/random_{case}/request.json').read_text());raw={k:v for k,v in raw.items()if k!='operation_id'}
 p=run(raw);(P/f'evidence/general118_changed_case{case}.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
 print(case,p['status'],p['search_evidence']['attempts'][0]['status'],p['total_seconds'],flush=True)
 if p.get('internal_proposals'):print(p['internal_proposals'][0]['gate']['status'],p['internal_proposals'][0]['gate']['errors'],flush=True)
