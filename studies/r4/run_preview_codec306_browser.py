"""Real Chromium geometry measurement of synthetic SVG; no screenshot or network."""
import copy,hashlib,importlib.metadata,json
from playwright.sync_api import sync_playwright
from preview_codec_study306 import encode,inspect,guard,MEASURE_JS
from test_dxf_codec_study307 import fixture
def main():
 before=guard();s=fixture();data=encode(s);xml=inspect(s,data);counts={'viewport':0,'overflow':0,'overlap':0,'zero_font_heuristic_acceptance':0}
 with sync_playwright()as p:
  browser=p.chromium.launch();page=browser.new_page();requests=[]
  page.route('**/*',lambda route:(requests.append(route.request.url),route.abort()))
  results=[]
  def load(svg):
   page.set_content(svg.decode('utf-8'));page.evaluate('document.fonts.ready')
  for w,h in ((390,844),(768,1024),(1280,900)):
   page.set_viewport_size({'width':w,'height':h});load(data)
   result=page.evaluate(MEASURE_JS)
   assert result['state']=='NO_MEASURED_LABEL_DEFECT_IN_THIS_RENDER'and result['labelCount']==2
   results.append({'viewport':[w,h],**result});counts['viewport']+=1
  tiny=fixture();tiny['rooms'][0]['rect']=['1','2','1.1','2.1'];tiny['rooms'][0]['name']='نام بسیار طولانی برای فضای کوچک'
  b=encode(tiny);inspect(tiny,b);load(b)
  r=page.evaluate(MEASURE_JS);assert r['state']=='LAYOUT_DEFECT_OBSERVED' and 'label_room1'in r['overflow'];counts['overflow']+=1
  # Same semantic input, deliberately corrupt rendered placement. Not a new plan.
  load(data);page.evaluate("() => { const a=document.getElementById('label_room1'),b=document.getElementById('label_room2');b.setAttribute('x',a.getAttribute('x'));b.setAttribute('y',a.getAttribute('y')); }")
  r=page.evaluate(MEASURE_JS);assert ['label_room1','label_room2']in r['overlap'];counts['overlap']+=1
  # Enlarged real glyph bounds, not accepting based on source character count.
  load(data);page.locator('#label_room1').evaluate("(e)=>e.setAttribute('font-size','200')")
  r=page.evaluate(MEASURE_JS);assert 'label_room1'in r['overflow'];counts['zero_font_heuristic_acceptance']+=1
  assert requests==[];version=browser.version;browser.close()
 assert guard()==before
 print(json.dumps({'schema':'SYNTHETIC_PREVIEW306_BROWSER','counts':counts,'viewports':results,
  'xml_receipt':xml,'chromium_version':version,'playwright_version':importlib.metadata.version('playwright'),
  'network_requests':len(requests),'solver_calls':0,'screenshots_created':False,'visual_reviewed':False,
  'product_snapshot_bound':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False},sort_keys=True))
if __name__=='__main__':main()
