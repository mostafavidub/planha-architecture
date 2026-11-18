import sys,hashlib,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent
P='8f1df9e145080fe8a5f0787b8b8f528fbaa478ebc87478867c722370264e2431'
R='bc42326132a6186b3408995256d0fe1b15686bc05510ea8bfbcc7408ddb30c58'
if hashlib.sha256((H/"prereg.json").read_bytes()).hexdigest()!=P or hashlib.sha256((H/"run_once.py").read_bytes()).hexdigest()!=R:raise ValueError("EXTERNAL_ANCHOR")
sys.exit(subprocess.call([sys.executable,str(H/"run_once.py"),P]))
