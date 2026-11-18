import json
from pathlib import Path
from engine114 import run
p=run({'W':'18','L':'24','n':2,'requested_count':6,'program':{'bedrooms_per_unit':2}})
Path('evidence/capacity118_whole18x24_explicit2.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
print(p['status'],p['search_evidence']['attempts'][0]['status'],p.get('rejections'),flush=True)
