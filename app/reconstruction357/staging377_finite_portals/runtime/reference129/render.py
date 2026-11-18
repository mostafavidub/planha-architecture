"""Model-driven SVG. No furniture rendering, no generated decorative openings."""
from fractions import Fraction as F
import json,html
from checker114 import digest

def admitted(c):
 g=c['gate']
 if g.get('model_hash')!=digest(c['model'])or g.get('status')!='PASS_CONCEPT_SCOPED_REVIEW'or g.get('gate_scope')!='CONCEPT117_SOURCE_COMPAT_V1'or not g.get('eligible_for_draft_export')or g.get('errors')or g.get('pending'):
  raise ValueError('EXPORT_REQUIRES_COMPLETE_NAMED_GATE')
 return c['model'],g

def encode(c,source_revision):
 m,g=admitted(c)
 if not isinstance(source_revision,str)or not source_revision:raise ValueError('SOURCE_REVISION_REQUIRED')
 W,L,_=map(lambda z:float(F(str(z))),m['inputs']);S=55;X=40;CW=W*S+80;FS=17*CW/1000;Y=max(90,FS*3.8);footer=max(170,FS*7.2);H=Y+L*S+footer;out=[]
 def r(q):return list(map(lambda z:float(F(str(z))),q))
 def rectangle(q,fill='white',stroke='#999',width=1):
  x,y,a,b=r(q);out.append(f'<rect x="{X+x*S}" y="{Y+(L-b)*S}" width="{(a-x)*S}" height="{(b-y)*S}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
 def line(q,width=1):
  x,y,a,b=r(q);out.append(f'<line x1="{X+x*S}" y1="{Y+(L-y)*S}" x2="{X+a*S}" y2="{Y+(L-b)*S}" stroke="#222" stroke-width="{width}"/>')
 def text(s,x,y,size):out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="DejaVu Sans" font-size="{size}" direction="rtl">{html.escape(s)}</text>')
 def label(name,parts):
  qs=[tuple(F(str(v))for v in q)for q in parts]
  if not qs:return
  # Exact first-maximum tie rule matches model semantics; float only for pixels.
  chosen=max(qs,key=lambda z:(z[2]-z[0])*(z[3]-z[1]))
  q=list(map(float,chosen));size=min(FS,(q[2]-q[0])*S*.85/max(1,len(name))/.6,(q[3]-q[1])*S*.6)
  text(name,X+(q[0]+q[2])/2*S,Y+(L-(q[1]+q[3])/2)*S,max(6,size))
 out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{H}" viewBox="0 0 {CW} {H}" data-scale="{S}" data-offset-x="{X}" data-offset-y="{Y}" data-length="{L}"><rect width="100%" height="100%" fill="white"/>')
 out.append('<metadata>'+html.escape(json.dumps({'model':m,'gate':g,'source_revision':source_revision,'scope':'GENERAL129_CONCEPT_DRAFT_NOT_EXECUTABLE_OR_TECHNICALLY_ACCEPTED'},ensure_ascii=False))+'</metadata>')
 beds=[sum(1 for key in u['rooms'] if key.split('.')[-1].startswith('bed'))for u in m['units']]
 text(f'{W:g} × {L:g} | پیش‌نویس کانسپت | خواب هر واحد: '+ '/'.join(map(str,beds)),CW/2,max(32,FS*1.65),FS*1.4);text('فقط کنترل‌های کانسپت؛ نه نقشه اجرایی یا تأیید فنی و مقررات',CW/2,max(64,FS*3.05),FS)
 rectangle([0,0,W,L],stroke='#222')
 for q in m['walls'].values():rectangle(q,'#333','#333')
 for o in m.get('openings',[]):
  rectangle(o['rect'],'white','white')
 for op in m.get('operations',{}).get('doors',[]):
  rectangle(op['closed_panel'],'white','#222',1.5)
 for w in m.get('concept_windows',[]):
  x,y,a,b=r(w['plan_rect']);rectangle(w['plan_rect'],'white','#333')
  for t in(1/3,2/3):line([x,y+(b-y)*t,a,y+(b-y)*t])
 names={'living':'پذیرایی','dining':'غذاخوری','kitchen':'آشپزخانه','bath':'حمام و سرویس','bathroom':'حمام و سرویس','entry_circulation':'گردش داخلی','private_corridor':'راهروی خصوصی','private_circulation':'راهروی خصوصی'}
 for u in m['units']:
  metadata=u.get('room_metadata',{})
  for key,parts in u['rooms'].items():
   if not parts:continue
   short=key.split('.')[-1];global_meta=m.get('room_metadata',{}).get(u['id']+'.'+key,{})
   name=metadata.get(key,{}).get('name_fa')or global_meta.get('display_name_fa')or global_meta.get('name_fa')or('خواب '+short[3:]if short.startswith('bed')else names.get(short,short))
   if short=='living':name+=' '+u['id']
   label(name,parts)
 for key,value in m['common_spaces'].items():
  parts=value if value and isinstance(value[0],list)else[value]
  label({'stair':'راه‌پله','lift':'آسانسور','lobby':'لابی مشترک'}.get(key,key),parts)
 yy=Y+L*S
 text('دهانه‌ها و پنجره‌ها از مدل‌اند؛ اثاث فقط در تصویر پنهان شده است.',CW/2,yy+FS*2,FS)
 text('نور و تهویه خارج از بررسی MVP هستند؛ این پیش‌نویس تأیید فنی نیست.',CW/2,yy+FS*3.6,FS)
 text('نام‌های فضاهای کوچک ممکن است نیاز به بزرگ‌نمایی داشته باشند.',CW/2,yy+FS*5.2,FS*.85)
 text('مقایسه گردش، ترجیح طراحی است؛ شاهد بهینگی یا پذیرش نهایی نیست.',CW/2,yy+FS*6.6,FS*.85)
 out.append('</svg>');return '\n'.join(out).encode()
