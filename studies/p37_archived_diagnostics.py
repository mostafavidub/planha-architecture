"""P37 private archived diagnosis renderer. No model, evaluator, API, publication or authority.

Caller independently checks archival/source/witness bytes and passes the expected
manifest digest from THAT trust channel. This module is a consistency+rendering
boundary; a hash supplied by an untrusted caller does not establish a location.
"""
import hashlib,json,re,html
from fractions import Fraction as F
from decimal import Decimal,localcontext

AUTH={k:False for k in ('accepted','qualified','display_allowed','delivery_allowed','production_supported')}
ACTUAL='ORIGINAL_ROUTE_REPORT'
PLANNED='SOURCE_PLANNED_WITNESS_NOT_STORED_ROUTE'
DETACHED='DETACHED_OPENING_REPRODUCTION_NOT_ORIGINAL'
RULES={'MISSING_REQUIRED_ACTIVITY_ROUTES':(ACTUAL,'NOT_LOCALIZABLE'),
 'PLANNED_ENTRY_PANEL_AND_KITCHEN_MOTION':(PLANNED,'LOCATED_PLANNED_WITNESS'),
 'NO_BODY_CROSSING_BETWEEN_DECLARED_REGIONS':(DETACHED,'LOCATED_DETACHED_CONTROL')}
LAYERS=('object','door','human','path')
LABELS={'object':'بدنه','door':'در','human':'بدن','path':'مسیر'}
TITLES={'MISSING_REQUIRED_ACTIVITY_ROUTES':'مسیر واقعی غذاخوری ثبت نشده است',
 'PLANNED_ENTRY_PANEL_AND_KITCHEN_MOTION':'مسیر پیشنهادی غذاخوری با پنل در و محدوده حرکت آشپزخانه برخورد دارد',
 'NO_BODY_CROSSING_BETWEEN_DECLARED_REGIONS':'در آزمون جداشده، دهانه برای عبور بدن کافی نیست'}
LAYER_LABELS={'NOT_OBSERVED':'شاهد مکانی موجود نیست','NOT_APPLICABLE':'در دامنه این یافته نیست',
 'INSTALLED_ENVELOPE':'بدنه یا پوش حرکتِ ثبت‌شده','ENTRY_PANEL':'پنل ثبت‌شده در ورودی',
 'WIDTH_BOUND':'حد عرض لازم برای بدن','PROPOSED_BODY_SWEEP':'پهنه حرکت بدن روی مسیر پیشنهادی',
 'PROPOSED_PATH':'مسیر پیشنهادی، نه مسیر واقعی ثبت‌شده','ACTUAL_PATH_MISSING':'مسیر واقعی ثبت نشده',
 'HOST_RETAINED':'میزبان و نقش بازشو ثابت نگه داشته شده',
 'NARROWED_APERTURE':'بازشو در نسخهٔ جداشده باریک شده','DIRECT_CROSSING_REJECTED':'گذر مستقیم در کنترل جداشده رد شده'}
LAYER_CODES={
 ACTUAL:{'object':{'NOT_OBSERVED'},'door':{'NOT_OBSERVED'},'human':{'NOT_OBSERVED'},'path':{'ACTUAL_PATH_MISSING'}},
 PLANNED:{'object':{'INSTALLED_ENVELOPE'},'door':{'ENTRY_PANEL'},'human':{'PROPOSED_BODY_SWEEP'},'path':{'PROPOSED_PATH'}},
 DETACHED:{'object':{'HOST_RETAINED'},'door':{'NARROWED_APERTURE'},'human':{'WIDTH_BOUND'},'path':{'DIRECT_CROSSING_REJECTED'}}}
CTX={'schema','model_digest','frame_digest','source_digest','original_report_digest','request_digest','original_ledger_digest'}
FACT={'schema','finding_id','code','unit','scope','evidence_digest','model_digest','frame_digest',
      'source_digest','original_report_digest','variant_digest','layers','geometry','detail'}
MANIFEST={'schema','context_digest','finding_digests'}
GEOM={'frame_digest','model_digest','variant_digest','boxes'}
KIND={PLANNED:{'entry_panel_overlap','kitchen_motion_overlap'},DETACHED:{'detached_aperture'}}
CAP=24

def need(ok,msg):
 if not ok:raise ValueError(msg)
def strict(o,depth=0):
 need(depth<=16,'P37_DEPTH')
 t=type(o);need(t in(dict,list,str,int,bool,type(None)),'P37_TYPE')
 if t is str:need(len(o)<=600,'P37_TEXT_CAP')
 if t is dict:
  need(len(o)<=80 and all(type(k)is str and len(k)<=128 for k in o),'P37_KEY_CAP')
  for v in o.values():strict(v,depth+1)
 if t is list:
  need(len(o)<=80,'P37_LIST_CAP')
  for v in o:strict(v,depth+1)
def digest(o):
 strict(o)
 return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def hexn(s):return type(s)is str and re.fullmatch('[a-f0-9]{64}',s)is not None
def idn(s):return type(s)is str and re.fullmatch('[a-z0-9][a-z0-9_-]{0,60}',s)is not None
def exact(v,fields):return type(v)is dict and set(v)==fields
def dimension(v):
 need(type(v)is str and re.fullmatch(r'-?(?:[0-9]{1,8})(?:/[0-9]{1,10}|\.[0-9]{1,10})?',v)is not None,'P37_RATIONAL_COORDINATE')
 need(not ('/'in v and int(v.split('/')[1])==0),'P37_RATIONAL_COORDINATE')
 x=F(v);need(-200<=x<=200,'P37_COORD_SCOPE')
 return x
def box(v):
 need(type(v)is list and len(v)==4,'P37_BOX')
 a,b,c,d=map(dimension,v)
 need(a<c and b<d,'P37_BOX_POSITIVE')
 return a,b,c,d
def base(ctx,manifest,expected):
 need(exact(ctx,CTX) and ctx['schema']=='P37_ARCHIVE_CONTEXT_V1'
   and all(hexn(ctx[k])for k in CTX-{'schema'}),'P37_CONTEXT')
 h=digest(ctx)
 need(exact(manifest,MANIFEST) and manifest['schema']=='P37_EXTERNAL_ARCHIVE_MANIFEST_V1'
   and manifest['context_digest']==h and hexn(expected) and digest(manifest)==expected,'P37_INDEPENDENT_MANIFEST')
 fp=manifest['finding_digests']
 need(type(fp)is dict and len(fp)<=CAP and all(idn(i)and hexn(v) for i,v in fp.items()),'P37_FINDING_MAP')
 return h,fp
PROFILE='public_all_seat_motion_occupied_and_kitchen_exclusion'
def detail_binding(f,scope):
 d=f['detail']
 if scope==ACTUAL:
  need(d=={'route':'guest_dining','reason':'NO_CONNECTED_BODY_ROUTE','profile':PROFILE},
   'P37_ORIGINAL_OCCURRENCE_DETAIL')
 if scope==PLANNED:
  need(exact(d,{'route','profile','body_m'}) and d['route']=='guest_dining' and d['profile']==PROFILE
   and dimension(d['body_m'])==F('0.7'),'P37_PLANNED_METHOD_DETAIL')
 if scope==DETACHED:
  need(exact(d,{'original_width_m','detached_width_m','body_m','width_deficit_m','opening_id','host_id','operation_mode'})
   and d['opening_id']==f['unit']+'.entry' and d['host_id']==f['unit']+'.unit_boundary'
   and d['operation_mode']=='SOURCE_LINEAR_SLIDE_NO_HINGE','P37_DETACHED_METHOD_DETAIL')
  original,new,body,lack=map(dimension,(d['original_width_m'],d['detached_width_m'],d['body_m'],d['width_deficit_m']))
  need((original,new,body,lack)==(F('1.3'),F('0.6'),F('0.7'),F('0.1'))
   and original>=body>new and body-new==lack,'P37_DETACHED_WIDTHS')
def bound_fact(ctx,fp,f):
 need(exact(f,FACT) and f['schema']=='P37_TYPED_FINDING_V1' and idn(f['finding_id'])
  and type(f['code'])is str and f['unit'] in ('A','B') and hexn(f['evidence_digest']),'P37_FINDING_TYPE')
 need(fp.get(f['finding_id'])==digest(f),'P37_FINDING_UNPINNED')
 need(all(f[k]==ctx[k]for k in ('model_digest','frame_digest','source_digest','original_report_digest')),'P37_FINDING_BASIS')
 if f['code'] not in RULES:
  need(f['scope']=='UNSUPPORTED' and f['variant_digest'] is None and f['geometry'] is None
    and f['detail'] is None and f['layers']==dict.fromkeys(LAYERS,'NOT_OBSERVED'),'P37_UNSUPPORTED_MUST_NOT_LOCALIZE')
  return 'UNSUPPORTED_CODE'
 scope,state=RULES[f['code']]
 detail_binding(f,scope)
 need(f['scope']==scope and exact(f['layers'],set(LAYERS)) and
  all(f['layers'][k] in LAYER_CODES[scope][k] for k in LAYERS),'P37_SCOPE_OR_LAYER')
 v=f['variant_digest']
 if scope==DETACHED:need(hexn(v) and v!=ctx['model_digest'],'P37_DETACHED_VARIANT')
 else:need(v is None,'P37_FALSE_VARIANT')
 g=f['geometry']
 if state=='NOT_LOCALIZABLE':
  need(g is None,'P37_MISSING_EVIDENCE_MUST_NOT_LOCALIZE')
  return state
 need(exact(g,GEOM) and g['model_digest']==ctx['model_digest'] and g['frame_digest']==ctx['frame_digest']
  and g['variant_digest']==v and type(g['boxes'])is list and 0<len(g['boxes'])<=CAP,'P37_GEOMETRY_BASIS')
 ks=set()
 for x in g['boxes']:
  need(exact(x,{'kind','rect'}) and type(x['kind'])is str and x['kind'] in KIND[scope],'P37_GEOMETRY_KIND')
  box(x['rect']);ks.add(x['kind'])
 need(ks==KIND[scope],'P37_GEOMETRY_INCOMPLETE')
 return state
NAMESPACES=('errors','pending','original_pending','not_evaluated','out_of_scope')
def check_ledger(ctx,ledger):
 need(exact(ledger,{'schema','original_report_digest','namespaces'}) and ledger['schema']=='P37_ORIGINAL_LEDGER_V1'
  and ledger['original_report_digest']==ctx['original_report_digest'] and digest(ledger)==ctx['original_ledger_digest'],'P37_ORIGINAL_LEDGER_BINDING')
 vals=ledger['namespaces']
 need(exact(vals,set(NAMESPACES)),'P37_LEDGER_NAMESPACES')
 for name in NAMESPACES:
  items=vals[name]
  need(type(items)is list and len(items)<=80,'P37_LEDGER_ENTRIES')
  for order,x in enumerate(items):
   need(exact(x,{'ordinal','code','rule_id','source_record_sha256'}) and type(x['ordinal'])is int and x['ordinal']==order
    and (x['code'] is None or type(x['code'])is str) and (x['rule_id'] is None or type(x['rule_id'])is str)
    and hexn(x['source_record_sha256']),'P37_LEDGER_ENTRY')
def report(ctx,facts,ledger,*,trusted_manifest,expected_manifest_digest):
 t,pins=base(ctx,trusted_manifest,expected_manifest_digest)
 check_ledger(ctx,ledger)
 need(type(facts)is list and len(facts)<=CAP,'P37_FINDING_LIST')
 before=digest([ctx,facts,ledger,trusted_manifest])
 rows=[];seen=set()
 for f in facts:
  state=bound_fact(ctx,pins,f)
  k=f['finding_id'];need(k not in seen,'P37_DUPLICATE_FINDING');seen.add(k)
  rows.append({'finding_id':k,'code':f['code'],'unit':f['unit'],'location_status':state,'scope':f['scope'],
   'evidence_digest':f['evidence_digest'],'layers':dict(f['layers']),
   'variant_digest':f['variant_digest'],'details':None if f['detail'] is None else dict(f['detail']),'geometry_digest':None if f['geometry'] is None else digest(f['geometry']),
   'reason':'MISSING_EVIDENCE' if state=='NOT_LOCALIZABLE'else 'UNSUPPORTED_CODE' if state=='UNSUPPORTED_CODE'else
     'PLANNED_NOT_ACTUAL_ROUTE' if f['scope']==PLANNED else'DETACHED_NOT_ORIGINAL'})
 need(seen==set(pins),'P37_FINDING_SET')
 need(digest([ctx,facts,ledger,trusted_manifest])==before,'P37_MUTATION')
 lines=['گزارش تشخیصی محدود، نه تأیید طرح یا مجوز تحویل.',
        'خطا، موارد معوق، موارد ارزیابی‌نشده و موارد خارج از دامنه جدا نگه داشته شده‌اند.']
 for r in rows:
  lines.append('واحد '+r['unit']+': '+TITLES.get(r['code'],'کد پشتیبانی‌نشده؛ محل اعلام نمی‌شود.'))
  if r['location_status']=='NOT_LOCALIZABLE':lines.append('شاهد کافی برای تعیین محل یا علتِ نبود مسیر نداریم.')
  if r['scope']==PLANNED:lines.append('نشان فقط روی مسیر پیشنهادی است؛ مسیر واقعی ثبت نشده و علت یکتا اثبات نشده است.')
  if r['scope']==DETACHED:lines.append('در نسخهٔ جداشده عرض بازشو از ۱٫۳ به ۰٫۶ متر رسید؛ برای بدن ۰٫۷ متری، ۰٫۱ متر کم است. این نقص به مدل اصلی نسبت داده نمی‌شود.')
  lines.extend(LABELS[k]+': '+LAYER_LABELS[r['layers'][k]] for k in LAYERS)
 return {'schema':'P37_ARCHIVED_PRIVATE_DIAGNOSTICS_V1','context_digest':t,'model_digest':ctx['model_digest'],
  'frame_digest':ctx['frame_digest'],'source_digest':ctx['source_digest'],'original_report_digest':ctx['original_report_digest'],
  'findings':rows,'original_report_namespaces':{k:[dict(x)for x in ledger['namespaces'][k]]for k in NAMESPACES},'persian_report':'\n'.join(lines)+'\n','private_overlay_contains_whole_model':False,**AUTH}
def decimal(v):
 with localcontext()as c:
  c.prec=23
  return format(Decimal(v.numerator)/Decimal(v.denominator),'.10f')
def overlay(ctx,fact,*,trusted_manifest,expected_manifest_digest):
 h,pins=base(ctx,trusted_manifest,expected_manifest_digest)
 state=bound_fact(ctx,pins,fact)
 need(state in ('LOCATED_PLANNED_WITNESS','LOCATED_DETACHED_CONTROL'),'P37_OVERLAY_NO_VERIFIED_LOCATION')
 xs=[(x['kind'],box(x['rect'])) for x in fact['geometry']['boxes']]
 x0=min(a for _,(a,b,c,d) in xs);x1=max(c for _,(a,b,c,d) in xs)
 y0=min(b for _,(a,b,c,d) in xs);y1=max(d for _,(a,b,c,d) in xs)
 # World +Y points up. Translate just the verified boxes to a local view, invert Y.
 attrs=html.escape(fact['finding_id'],quote=True)
 colors={'entry_panel_overlap':'#963445','kitchen_motion_overlap':'#165a8a','detached_aperture':'#79531e'}
 shapes=[]
 for k,(a,b,c,d) in xs:
  shapes.append(f'<rect data-kind="{k}" x="{decimal(a-x0)}" y="{decimal(y1-d)}" width="{decimal(c-a)}" height="{decimal(d-b)}" fill="{colors[k]}"/>')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {decimal(x1-x0)} {decimal(y1-y0)}" data-finding="{attrs}"><title>Private scoped diagnostic</title>'+''.join(shapes)+'</svg>'
 return {'schema':'P37_PRIVATE_FINDING_SVG_V1','context_digest':h,'finding_id':fact['finding_id'],'scope':fact['scope'],
  'geometry_digest':digest(fact['geometry']),'frame_digest':ctx['frame_digest'],'model_digest':ctx['model_digest'],
  'variant_digest':fact['variant_digest'],'svg':svg,'whole_model_embedded':False,**AUTH}
