"""Pinned synthetic codec environment, not full OS or solver reproducibility."""
import hashlib,json,pathlib,sys,platform,sysconfig,importlib,inspect,importlib.metadata as md
ROOT=pathlib.Path(__file__).resolve().parents[2]
LOCK=pathlib.Path(__file__).with_name('codec_environment402.lock.json')
LOCK_BLOB='1cbc1f0a99310b52491cbb45363be49266076ce2'
MODULES={'ezdxf':'ezdxf','numpy':'numpy','fonttools':'fontTools','pyparsing':'pyparsing','typing_extensions':'typing_extensions'}
def require(ok,code):
 if not ok:raise ValueError(code)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_lock():
 b=LOCK.read_bytes();require(blob(b)==LOCK_BLOB,'ENVIRONMENT_LOCK_CHANGED');return json.loads(b)
def source_guard(lock):
 out={}
 for p,h in lock['source_blobs'].items():
  q=ROOT/p;b=q.read_bytes();require(blob(b)==h,'CODEC_SOURCE_CHANGED')
  out[p]=hashlib.sha256(b).hexdigest()
 return out
def verify_wheels(folder):
 lock=load_lock();paths={p.name:p for p in pathlib.Path(folder).glob('*.whl')}
 require(set(paths)=={p['filename']for p in lock['packages']},'WHEEL_SET')
 for p in lock['packages']:
  require(hashlib.sha256(paths[p['filename']].read_bytes()).hexdigest()==p['sha256'],'WHEEL_HASH')
 return {'state':'PINNED_WHEEL_BYTES_VERIFIED','count':len(paths),'lock_digest':digest(lock)}
def verify_environment():
 lock=load_lock();source=source_guard(lock)
 require(platform.python_version()==lock['python'],'PYTHON_PATCH')
 require(platform.python_implementation()==lock['implementation'],'PYTHON_IMPLEMENTATION')
 require(sys.platform==lock['platform'] and platform.machine()==lock['machine'],'PLATFORM_ARCH')
 require(sysconfig.get_config_var('SOABI')==lock['soabi'],'PYTHON_ABI')
 require(sys.prefix!=sys.base_prefix,'ISOLATED_VENV_REQUIRED')
 cfg=(pathlib.Path(sys.prefix)/'pyvenv.cfg').read_text().lower()
 require('include-system-site-packages = false'in cfg,'SYSTEM_SITE_PACKAGES')
 versions={};paths={}
 for row in lock['packages']:
  name=row['name'].lower().replace('-','_')
  require(md.version(row['name'])==row['version'],'PACKAGE_VERSION')
  mod=importlib.import_module(MODULES[name]);p=pathlib.Path(mod.__file__).resolve()
  require(p.is_relative_to(pathlib.Path(sys.prefix).resolve()),'PACKAGE_IMPORT_OUTSIDE_VENV')
  versions[name]=row['version'];paths[name]=str(p.relative_to(pathlib.Path(sys.prefix).resolve()))
 require(source_guard(lock)==source and load_lock()==lock,'ENVIRONMENT_CHANGED')
 return {'schema':'CODEC_ENVIRONMENT402_V1','state':'PINNED_RUNTIME_AND_SOURCES_ONLY',
  'python':platform.python_version(),'soabi':sysconfig.get_config_var('SOABI'),
  'machine':platform.machine(),'platform':sys.platform,'os_release':platform.freedesktop_os_release(),
  'versions':versions,'bootstrap_pip_version':md.version('pip'),'relative_import_paths':paths,'source_snapshot':source,
  'lock_digest':digest(lock),'os_image_immutable':False,'solver_reproducibility':False,
  'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
def gated(call):
 manifest=verify_environment()
 value=call()
 require(verify_environment()==manifest,'ENVIRONMENT_CHANGED_AFTER_CODEC')
 return value,manifest
def verify_baseline(value):
 expected=load_lock()['baseline_pair']['expected']
 observed={k:value.get(k)for k in expected}
 require(digest(observed)==digest(expected),'BASELINE_PAIR_NOT_REPRODUCED')
 return observed
def paired():
 # Resolve actual module AND callable paths before invoking codec or fixture.
 fixture_module=importlib.import_module('test_dxf_codec_study307')
 p=importlib.import_module('paired_codec308')
 for mod,name,functions in [(fixture_module,'test_dxf_codec_study307.py',['fixture']),(p,'paired_codec308.py',['assess','make_report']),(p.svg,'preview_codec_study306.py',['encode']),(p.dxf,'dxf_codec_study307.py',['encode'])]:
  expected=(ROOT/'studies/r4'/name).resolve()
  require(pathlib.Path(mod.__file__).resolve()==expected,'REPO_IMPORT_PATH')
  for fn in functions:
   source=inspect.getsourcefile(getattr(mod,fn))
   require(source is not None and pathlib.Path(source).resolve()==expected,'REPO_CALLABLE_PATH')
 s=fixture_module.fixture()
 value=p.assess(s,p.svg.encode(s),p.dxf.encode(s),p.make_report(s))
 verify_baseline(value)
 return value
def main():
 if len(sys.argv)==3 and sys.argv[1]=='--wheels':
  print(json.dumps(verify_wheels(sys.argv[2]),sort_keys=True));return
 require(len(sys.argv)==1,'CLI_ARGUMENTS')
 value,manifest=gated(paired)
 print(json.dumps({'environment':manifest,'paired':{k:value[k]for k in ('state','fixture_digest','svg_sha256','dxf_sha256','report_digest','mismatch_count')},'solver_calls':0,'artifact_uploads':0},sort_keys=True))
if __name__=='__main__':main()
