"""Explicit preflight of unchanged384 historical lexical reads; no proof promotion."""
import ast,json
from pathlib import Path
from frozen390 import bytes_for
ROOT=Path(__file__).resolve().parent.parent;W=ROOT.parent

def verify():
 source=ROOT/'staging382_cohort_binding_fix/cohort382.py'
 tree=ast.parse(bytes_for(source).decode())
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='evaluate')
 definitions=ast.literal_eval(next(n.value for n in fn.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='definitions'for t in n.targets)))
 paths={source,ROOT/'finite_comparison358/bound_comparison_actual358.json',ROOT/'staging384_rank2_semantics/historical_authority.json',ROOT/'staging365_balanced_portals/actual365.json',ROOT/'staging365_balanced_portals/assemble365.py',ROOT/'staging364_balanced_portals/actual364.json',ROOT/'review364_diagnostic/geometry_operations.json'}
 if len(definitions)!=8:raise ValueError('HISTORICAL_READSET_INVENTORY')
 for name,path,fresh,proof in definitions:
  paths.add(ROOT/path)
  if fresh:paths.add(ROOT/fresh)
  if proof:paths.add(ROOT/'semantic_rules357'/proof)
 authority=json.loads(bytes_for(ROOT/'staging384_rank2_semantics/historical_authority.json'))
 for spec in authority.values():paths.add(W/spec['path'])
 historical=json.loads(bytes_for(W/'review382_actual_v1/result.json'))
 paths.add(W/'review382_actual_v1/result.json')
 for path in historical['draft366_conditional_property']['source_proof']['source_readset']:paths.add(ROOT/path)
 import hashlib
 return {'scope':'EXPLICIT_UNCHANGED384_HISTORICAL_AUTHORITY_DEFINITIONS_RANK0_TERMINAL_READS','files':{str(p.relative_to(W)):hashlib.sha256(bytes_for(p)).hexdigest()for p in sorted(paths)},'all_frozen_bytes_verified':True}
