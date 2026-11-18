"""Stdlib-only preimport freezecheck, dedicated process group and Linux subreaper."""
import sys,os,time,signal,subprocess,json,hashlib,ctypes
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def snapshot():
 out={}
 for f in Path('/proc').glob('[0-9]*/stat'):
  try:
   v=f.read_text();tail=v[v.rindex(')')+2:].split();out[int(f.parent.name)]={'state':tail[0],'ppid':int(tail[1]),'pgrp':int(tail[2]),'start':tail[19]}
  except (OSError,ValueError,IndexError):pass
 return out

def main():
 prereg=HERE/'dispatch361_preregistration.json'
 if len(sys.argv)!=2 or hashlib.sha256(prereg.read_bytes()).hexdigest()!=sys.argv[1]:raise ValueError('EXTERNAL_PREREG_PIN')
 pins=json.loads(prereg.read_text())
 for path,h in pins['code_pins'].items():
  if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=h:raise ValueError('PREIMPORT_FREEZE_CHANGED:'+path)
 target=HERE/'dispatch361_supervision.json'
 if target.exists():raise ValueError('SUPERVISOR_WRITE_ONCE')
 if ctypes.CDLL(None).prctl(36,1,0,0,0)!=0:raise RuntimeError('SUBREAPER_REQUIRED')
 out=open(HERE/'dispatch361_stdout.log','w');err=open(HERE/'dispatch361_stderr.log','w');p=subprocess.Popen([sys.executable,str(HERE/'complete_active_dispatch361.py')],stdout=out,stderr=err,start_new_session=True);started=time.monotonic();tracked={p.pid};births={p.pid:snapshot()[p.pid]['start']};timed_out=False
 def update():
  snap=snapshot();changed=True
  while changed:
   before=len(tracked)
   for pid,v in snap.items():
    if v['pgrp']==p.pid or (v['ppid']in tracked and snap.get(v['ppid'],{}).get('start')==births.get(v['ppid'])):
     if pid not in tracked:births[pid]=v['start'];tracked.add(pid)
   changed=before!=len(tracked)
  return snap
 while p.poll()is None:
  update()
  if time.monotonic()-started>=90:timed_out=True;break
  time.sleep(.1)
 snap=update();live=[pid for pid in tracked if pid in snap and snap[pid]['state']!='Z']
 if timed_out or live:
  try:os.killpg(p.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  for pid in live:
   try:
    if snapshot().get(pid,{}).get('start')==births.get(pid):os.kill(pid,signal.SIGTERM)
   except ProcessLookupError:pass
  end=time.monotonic()+5
  while time.monotonic()<end:
   snap=update()
   if not any(pid in snap and snap[pid]['state']!='Z'for pid in tracked):break
   time.sleep(.1)
  try:os.killpg(p.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  for pid in tracked:
   try:
    if snapshot().get(pid,{}).get('start')==births.get(pid):os.kill(pid,signal.SIGKILL)
   except ProcessLookupError:pass
 code=p.wait();reaped=[]
 while True:
  try:pid,status=os.waitpid(-1,os.WNOHANG)
  except ChildProcessError:break
  if pid==0:break
  reaped.append(pid)
 out.close();err.close();snap=update();survivors=[pid for pid in tracked if pid in snap and snap[pid]['state']!='Z'];changed=[path for path,h in pins['code_pins'].items()if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=h]
 result={'schema':'DISPATCH361_SUPERVISION','prereg_sha256':sys.argv[1],'worker_pid':p.pid,'tracked_pids':sorted(tracked),'reaped_descendant_pids':reaped,'returncode':code,'timed_out':timed_out,'survivors':survivors,'source_changed':changed,'elapsed_seconds':time.monotonic()-started,'fresh_executed':False,'accepted':False};target.write_text(json.dumps(result,indent=2));print(json.dumps(result))
 if survivors or changed or code:raise SystemExit(1)
if __name__=='__main__':main()
