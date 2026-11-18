"""Source-only freeze builder. No constructor/reviewer/semantic invocation."""
import json,hashlib,ast,os,difflib
from pathlib import Path
W=Path(__file__).resolve().parent.parent;O=W/'review387_preaudit';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=W/'review385_preaudit/source_freeze.json';files=json.loads(base.read_text())['files'];assert all((W/n).is_file()and sha(W/n)==h for n,h in files.items())
prior=dict(files);files[str(base.relative_to(W))]=sha(base)
# Discover actual lexical historical reads from unchanged original function.
root=W/'reconstruction357';tree=ast.parse((root/'staging382_cohort_binding_fix/cohort382.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='evaluate');defs=ast.literal_eval(next(n.value for n in fn.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='definitions'for t in n.targets)))
reads=[]
for name,p,fp,ep in defs:
 for path in [p]+([]if name=='baseline351'else[fp,'semantic_rules357/'+ep]):
  q=root/path;lex=Path(os.path.abspath(q));assert lex.is_relative_to(W)and lex.resolve().is_relative_to(W)
  rel=str(lex.relative_to(W));files[rel]=sha(q);reads.append({'member':name,'path':rel,'sha256':sha(q),'previously_registered':rel in prior})
for folder in ['reconstruction357/staging387_form','reconstruction357/staging387_current_semantics']:
 for p in(W/folder).rglob('*'):
  if p.is_file()and '__pycache__'not in p.parts and p.suffix not in('.pyc','.pyo'):files[str(p.relative_to(W))]=sha(p)
for name in ['prepare387.py','package387.py','test_portable387.py']:
 p=O/name
 if p.is_file():files[str(p.relative_to(W))]=sha(p)
# Explicit lexical entries: canonical resolution is an integrity check, not a substitute for a runtime location.
for n,h in list(files.items()):
 lexical=Path(os.path.abspath(W/n));assert lexical.is_relative_to(W)and lexical.resolve().is_relative_to(W)
 key=str(lexical.relative_to(W));assert key not in files or files[key]==h;files[key]=h
(O/'lexical_reads.json').write_text(json.dumps(reads,indent=2));files['review387_preaudit/lexical_reads.json']=sha(O/'lexical_reads.json')
(O/'source_freeze.json').write_text(json.dumps({'schema':'TWO_BUILDERS387_PIN_AND_RUNTIME_CLOSURE_FIX','files':files},sort_keys=True,indent=2))
(O/'prior385_unchanged.json').write_text(json.dumps({'verified':True,'pins':len(prior),'freeze_sha256':sha(base)},indent=2))
patch=[]
for folder in ['form','current_semantics']:
 for p in sorted((root/('staging387_'+folder)).glob('*')):
  if p.suffix not in('.py','.html'):continue
  q=root/('staging385_'+folder)/p.name.replace('387','385');old=q.read_text().replace('385','387')if q.exists()else''
  patch.extend(difflib.unified_diff(old.splitlines(True),p.read_text().splitlines(True),fromfile='VERSION_NORMALIZED/'+str(q.relative_to(W)),tofile=str(p.relative_to(W))))
(O/'non_version_changes.patch').write_text(''.join(patch));print(json.dumps({'pins':len(files),'freeze_sha256':sha(O/'source_freeze.json'),'new_actual_run':False}))
