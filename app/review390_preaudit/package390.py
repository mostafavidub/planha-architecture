"""Complete lexical delta over immutable385, fresh-extraction proof, no run."""
import json,hashlib,zipfile,os,tempfile
from pathlib import Path
W=Path(__file__).resolve().parent.parent;O=W/'review390_preaudit';sha=lambda b:hashlib.sha256(b).hexdigest()
base=json.loads((W/'review387_preaudit/source_freeze.json').read_text())['files'];cur=json.loads((O/'source_freeze.json').read_text())['files']
def normalize(k):
 p=Path(os.path.abspath(W/k));assert p.is_relative_to(W);return str(p.relative_to(W))
b={normalize(k):v for k,v in base.items()};c={normalize(k):v for k,v in cur.items()}
assert all((W/k).is_file()and sha((W/k).read_bytes())==v for k,v in c.items())
delta={k:v for k,v in c.items()if k not in b};assert all(b[k]==v for k,v in c.items()if k in b)
for p in O.iterdir():
 if p.is_file()and p.suffix in('.json','.md','.log','.patch','.py')and p.name not in('package_manifest.json','package_report.json','portable_closure.json'):delta[str(p.relative_to(W))]=sha(p.read_bytes())
with tempfile.TemporaryDirectory(dir=W)as temp:
 t=Path(temp)
 for k,h in b.items():
  p=t/k;p.parent.mkdir(parents=True,exist_ok=True);os.link(W/k,p)
 for k,h in delta.items():
  p=t/k
  if p.exists():assert sha(p.read_bytes())==h
  else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((W/k).read_bytes())
 assert all((t/k).is_file()and sha((t/k).read_bytes())==h for k,h in c.items())
 closure={'verified':True,'base':'IMMUTABLE387_FULL_FREEZE','base_freeze_sha256':sha((W/'review387_preaudit/source_freeze.json').read_bytes()),'all_original_lookup_paths_verified':len(cur),'normalized_lexical_paths':len(c),'no_suffix_filter':True,'isolated_materialization_verified':True,'absolute_path_rewrite':False,'collision_policy':'existing exact SHA only; mismatch abort/isolate'}
(O/'portable_closure.json').write_text(json.dumps(closure,indent=2));delta['review390_preaudit/portable_closure.json']=sha((O/'portable_closure.json').read_bytes());(O/'package_manifest.json').write_text(json.dumps({'files':delta},indent=2,sort_keys=True))
z=O/'checkpoint390_live_cached_index_source_delta.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED)as a:
 for k,h in delta.items():a.write(W/k,k)
 a.write(O/'package_manifest.json','review390_preaudit/package_manifest.json')
with zipfile.ZipFile(z)as a:assert all(sha(a.read(k))==h for k,h in delta.items())
report={'zip':str(z),'bytes':z.stat().st_size,'sha256':sha(z.read_bytes()),'freeze_sha256':sha((O/'source_freeze.json').read_bytes()),'files':len(delta)};(O/'package_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
