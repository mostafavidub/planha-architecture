"""Read only files explicitly in the current385 frozen dependency closure."""
import json,hashlib,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent

def bytes_for(path):
 path=Path(path).resolve()
 if not path.is_relative_to(W):raise ValueError('FROZEN_PATH_OUTSIDE_WORKSPACE')
 files=json.loads((W/'review385_preaudit/source_freeze.json').read_text())['files']
 matches={h for n,h in files.items()if(W/n).resolve()==path}
 if len(matches)!=1:raise ValueError('UNREGISTERED_FROZEN_DEPENDENCY:'+str(path.relative_to(W)))
 data=path.read_bytes()
 if hashlib.sha256(data).hexdigest()!=next(iter(matches)):raise ValueError('FROZEN_DEPENDENCY_CHANGED:'+str(path.relative_to(W)))
 return data

def read(path):return json.loads(bytes_for(path))
def module(path,name):
 path=Path(path);data=bytes_for(path);spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
 exec(compile(data,str(path),'exec'),m.__dict__);return m
