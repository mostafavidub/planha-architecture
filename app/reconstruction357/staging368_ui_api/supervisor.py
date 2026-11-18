"""Private subprocess containment; no caller-supplied processes accepted."""
import os,time,signal,subprocess,ctypes,psutil,threading,json,math
from pathlib import Path

def attempt_status(folder, now):
 if folder is None:return None
 for i in range(1,5):
  begin=folder/('attempt_%02d_begin.json'%i);end=folder/('attempt_%02d_end.json'%i)
  if not begin.exists():
   if end.exists():return 'ATTEMPT_PROTOCOL_ERROR'
   continue
  try:
   if begin.is_symlink()or begin.stat().st_size>1024:raise ValueError()
   b=json.loads(begin.read_bytes())
   if set(b)!={'started','deadline','limit_seconds'}:raise ValueError()
   if any(type(b[k])not in(int,float)or not math.isfinite(b[k])for k in b):raise ValueError()
   if not 0<b['limit_seconds']<=120 or abs(b['deadline']-b['started']-b['limit_seconds'])>1e-6 or b['started']>now:raise ValueError()
   if end.exists():
    if end.is_symlink()or end.stat().st_size>1024:raise ValueError()
    e=json.loads(end.read_bytes())
    if set(e)!={'ended'}or type(e['ended'])not in(int,float)or not math.isfinite(e['ended'])or e['ended']<b['started']:raise ValueError()
    if e['ended']>b['deadline']:return 'ATTEMPT_TIMEOUT'
   elif now>=b['deadline']:return 'ATTEMPT_TIMEOUT'
  except Exception:return 'ATTEMPT_PROTOCOL_ERROR'
 return None

def supervise(command,seconds,cancel=None,*,evidence_directory=None):
 # Linux subreaper lets this dedicated supervisor reap orphaned grandchildren.
 if ctypes.CDLL(None).prctl(36,1,0,0,0)!=0:raise RuntimeError('SUBREAPER_UNAVAILABLE')
 start=time.monotonic();deadline=start+seconds
 proc=subprocess.Popen(command,start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 known={};reason='COMPLETED'
 def discover():
  for p in psutil.Process().children(recursive=True):
   try:known[(p.pid,p.create_time())]=p
   except psutil.NoSuchProcess:pass
 def alive(p,stamp):
  try:return p.create_time()==stamp and p.status()!=psutil.STATUS_ZOMBIE
  except psutil.NoSuchProcess:return False
 def reap():
  # Popen owns its immediate child; do not consume its wait status here.
  proc.poll()
  for (pid,stamp),p in list(known.items()):
   if pid==proc.pid:continue
   try:
    if p.create_time()!=stamp:continue
    os.waitpid(pid,os.WNOHANG)
   except (ChildProcessError,ProcessLookupError,psutil.NoSuchProcess):pass
 while True:
  discover()
  if evidence_directory is not None and sum(p.stat().st_size for p in evidence_directory.rglob('*')if p.is_file())>96000000:
   reason='EVIDENCE_DISK_LIMIT';break
  attempt_reason=attempt_status(evidence_directory,time.monotonic())
  if attempt_reason is not None:reason=attempt_reason;break
  if cancel is not None and cancel.is_set():reason='CANCELLED';break
  if time.monotonic()>=deadline:reason='TIMEOUT';break
  if proc.poll() is not None:break
  time.sleep(.02)
 # Cleanup is bounded even for a child that exits leaving a separate session.
 cleanup_deadline=time.monotonic()+2
 discover()
 for (pid,stamp),p in list(known.items()):
  if alive(p,stamp):
   try:p.send_signal(signal.SIGTERM)
   except psutil.NoSuchProcess:pass
 while time.monotonic()<cleanup_deadline:
  discover()
  for (pid,stamp),p in list(known.items()):
   if alive(p,stamp):
    try:p.kill()
    except psutil.NoSuchProcess:pass
  reap()
  if proc.poll() is not None and not any(alive(p,s) for (pid,s),p in known.items()):break
  time.sleep(.02)
 reap()
 unresolved=[]
 for (pid,stamp),p in known.items():
  try:
   if p.create_time()==stamp:unresolved.append({'pid':pid,'create_time':stamp,'status':p.status()})
  except psutil.NoSuchProcess:pass
 return {'worker_returncode':proc.returncode,'reason':reason,'worker_reaped':proc.poll() is not None,'tracked_processes':[{'pid':pid,'create_time':s} for pid,s in known], 'unresolved':unresolved,'cleanup_verified':not unresolved and proc.poll() is not None,'elapsed_seconds':time.monotonic()-start,'delivery_allowed':False}
