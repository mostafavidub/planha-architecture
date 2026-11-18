"""Only run after pre-audit. One distinct fixed-proposal rebuild, no solver."""
import json,time
from pathlib import Path
from adapter359 import construct,digest,lineage
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
 target=HERE/'actual359.json'
 if target.exists():raise SystemExit('PRESERVE_EXISTING_ACTUAL359_NO_REPEAT')
 t=time.monotonic();old=lineage();x=construct();target.write_text(json.dumps(x,ensure_ascii=False,indent=2))
 m=x['candidate']['model'];before=old['candidate']['model'];rows=[]
 for a in before['units']:
  b=next(u for u in m['units']if u['id']==a['id'])
  rows.append({'unit':a['id'],'ownership_equal':a['ownership']==b['ownership'],'fixtures_equal':a['fixtures']==b['fixtures'],'activities_equal':a['activities']==b['activities'],'bedroom_rooms_equal':all(a['rooms'][k]==b['rooms'][k]for k in a['rooms']if k.startswith('bed'))})
 r={'model_digest':digest(m),'before_model_digest':digest(before),'request_equal':x['candidate']['request']==old['candidate']['request'],'program_equal':m['program']==before['program'],'profile_equal':m['profile']==before['profile'],'core_equal':x['candidate']['packet']['core']==old['candidate']['packet']['core'],'unit_preservation':rows,'route_failures':m['route_failures'],'hall_clamps':m.get('source_hall_clamp359'),'elapsed_seconds':time.monotonic()-t,'fresh_executed':False,'accepted':False,'released_floor_function':'NOT_ESTABLISHED'}
 (HERE/'precheck359.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps({'model_digest':digest(m),'route_failures':m['route_failures'],'elapsed_seconds':r['elapsed_seconds']}))
