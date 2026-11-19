"""Task3.5 extension: single-bed sufficient separator probes, never privacy closure."""
import copy,inspect,sys
from pathlib import Path
from front_rear_runtime_adapter import ROOT,ENGINE,transport,source_audit,ensure
from current_programme_evaluator import placed
from same_version_front_rear_contract import digest
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def target_key(target):return (target['unit'],target['fixture_id'])
def bind_targets(m):
 targets=[];wall_ids=[]
 for p in m['module_placements']:
  module=p['module'];ensure(digest(module)==p['module_hash'],'MODULE_HASH')
  u=next(u for u in m['units'] if u['id']==p['unit_id'])
  for key,q in module['walls'].items():
   wid=p['id_map'][key];ensure(placed(q,p['transform'])==placed(m['walls'][wid],{'matrix':[[1,0],[0,1]],'translation':[0,0]}),'WALL_BINDING')
   wall_ids.append(wid)
  if not p['room_id'].startswith('bed'):continue
  for key,q in module['unit']['fixtures'].items():
   meta=module['unit']['fixture_metadata'].get(key,{})
   if meta.get('kind')!='single_bed':continue
   wid=p['id_map'][key]
   ensure(placed(q,p['transform'])==placed(u['fixtures'][wid],{'matrix':[[1,0],[0,1]],'translation':[0,0]}),'SINGLE_BED_GEOMETRY')
   ensure(u['fixture_metadata'][wid]['kind']=='single_bed','SINGLE_BED_KIND')
   targets.append({'unit':u['id'],'room':p['room_id'],'fixture_id':wid,'rect':u['fixtures'][wid],'module_hash':p['module_hash'],'source_fixture_id':key})
 ensure(len(wall_ids)==len(set(wall_ids)),'WALL_ID_DUPLICATE')
 ensure(len(targets)==len({(x['unit'],x['fixture_id']) for x in targets}),'TARGET_ID_DUPLICATE')
 return targets,wall_ids
def assess(bundle):
 bundle,_=transport(bundle);pin=digest(bundle);m=bundle['packet']['world_model'];mh=digest(m)
 ensure(mh==bundle['model_digest'],'MODEL_DIGEST')
 ensure(bundle['reports']['physical']['model_hash']==mh,'PHYSICAL_MODEL_BINDING')
 for k,r in bundle['reports'].items():ensure(digest(r)==bundle['report_digests'][k],'REPORT_DIGEST')
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 from producer_provenance import snapshot,require_unchanged
 snap=snapshot(ROOT,['app/local_integration/'+p for p in ('single_bed_wall_separator_extension.py','current_programme_evaluator.py','source_wall_function_evaluator.py')])
 audit=source_audit()
 from geometry114 import cells
 from privacy115 import rect,boundary,crosses,separator
 import construction_replay127
 ensure(Path(inspect.getsourcefile(cells)).resolve()==ENGINE/'fast_cells120.py','CELLS_SOURCE')
 ensure(Path(inspect.getsourcefile(separator)).resolve()==ENGINE/'privacy115.py','SEPARATOR_SOURCE')
 ensure(Path(inspect.getsourcefile(construction_replay127.verify)).resolve()==ENGINE/'construction_replay127.py','REPLAY_SOURCE')
 out={'schema':'SINGLE_BED_WALL_SEPARATOR_EXTENSION_V1','criterion':'NONFUNCTIONAL_WALL_EXCLUSION','state':'UNKNOWN','model_digest':mh,
  'original_physical_report':copy.deepcopy(bundle['reports']['physical']),'original_physical_digest':bundle['report_digests']['physical'],
  'targets':[],'probes':[],'scope':'Single-bed targets only; sufficient single-wall separator before/after detached source removal. No ray proof, complete privacy, wall necessity or removal authorization.',
  **{k:False for k in AUTH}}
 try:
  replay=construction_replay127.verify(m,bundle['context']);out['replay']=replay
  ensure(replay['verified'] is True and replay['model_hash']==mh,'REPLAY')
  targets,ids=bind_targets(m);out['targets']=targets
  before=list(m['walls'].values());old=list(map(rect,cells(before,[])))
  apmap={}
  for t in targets:
   u=next(u for u in m['units'] if u['id']==t['unit']);role=t['unit']+'.'+t['room']
   edges=boundary(list(map(rect,u['rooms'][t['room']])))
   apmap[target_key(t)]=[o for o in m['openings'] if role in o.get('connects',[]) and any(crosses(rect(o['rect']),e) for e in edges)]
  for sid in sorted(ids):
   after=[q for k,q in m['walls'].items() if k!=sid];new=list(map(rect,cells(after,[])))
   checks=[]
   for t in targets:
    for ap in apmap[t['fixture_id']]:
     checks.append({'unit':t['unit'],'room':t['room'],'target_fixture_id':t['fixture_id'],'opening_id':ap['id'],
      'before_sufficient_separator':any(separator(rect(ap['rect']),rect(t['rect']),w) for w in old),
      'after_sufficient_separator':any(separator(rect(ap['rect']),rect(t['rect']),w) for w in new),
      'visibility_proven':False})
   out['probes'].append({'source_wall_id':sid,'physical_aliases':m['physical_wall_network']['source_aliases'].get(sid,[]),
    'material_union_unchanged':not cells(before,after),'checks':checks,'removal_authorized':False})
  out['counts']={'single_bed_targets':len(targets),'module_wall_probes':len(ids),'separator_pairs':sum(len(x['checks']) for x in out['probes']),
   'changed_certificates':sum(c['before_sufficient_separator']!=c['after_sufficient_separator'] for x in out['probes'] for c in x['checks'])}
 except Exception as ex:out['error']={'type':type(ex).__name__,'message':str(ex)}
 finally:
  try:
   ensure(digest(bundle)==pin,'INPUT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED');out['integrity_verified']=True
  except Exception as ex:out.update(integrity_verified=False,integrity_error=type(ex).__name__+':'+str(ex))
  out['source_snapshot']=snap
 return out
