'use strict';
const form=document.querySelector('#request'), result=document.querySelector('#result');
const fields=['W','L','n'].map(x=>document.getElementById(x));
const button=document.getElementById('submit');
let busy=false;
function show(state,text){result.dataset.state=state;result.textContent=text;}
function safe(v){return v && ['accepted','qualified','display_allowed','delivery_allowed'].every(k=>v[k]===false);}
form.addEventListener('submit',async event=>{
 event.preventDefault();if(busy)return;
 const raw={W:fields[0].value,L:fields[1].value,n:fields[2].value};
 busy=true;fields.forEach(x=>x.disabled=true);button.disabled=true;
 show('busy','درخواست در حال بررسی است؛ ارسال یا تلاش دوباره خودکار انجام نمی‌شود.');
 try{
  const response=await fetch('/api/public/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(raw)});
  const data=await response.json();
  if(response.status===422 || response.status===415){
   show('invalid','ورودی پذیرفته نشد؛ هیچ تولیدی برای این خطای ورودی آغاز نشده است.');return;
  }
  if(response.status===409 && data.code==='STUDY_BUSY_NO_QUEUE'){
   show('busy','مطالعه دیگری در حال اجرا است؛ این درخواست در صف قرار نگرفت. تلاش دوباره خودکار انجام نمی‌شود.');return;
  }
  if(response.status===409 && data.study_result?.state==='UNSUPPORTED_TRACE_STUDY_CONTRACT'){
   if(!safe(data)||!safe(data.study_result))throw new Error('AUTHORITY');
   show('unsupported','ورودی معتبر است ولی این مطالعه آن را پشتیبانی نمی‌کند؛ هیچ تولیدی آغاز نشد.');return;
  }
  if(!response.ok){
   show('error','نتیجه معتبر در دسترس نیست؛ اجرای سرور ممکن است شروع شده باشد. تلاش دوباره خودکار انجام نمی‌شود.');return;
  }
  const r=data.study_result;
  if(!safe(data)||!safe(r)||data.status!=='BLOCKED'||data.plan_payload!==null||data.download_available!==false)throw new Error('AUTHORITY');
  if(r.receipt_verified!==true||r.source_integrity_verified!==true||r.evidence_usable!==true){
   show('error','شواهد پاسخ تأیید نشده است؛ این پاسخ مجوز نمایش یا تحویل طرح نیست.');return;
  }
  const reasons={
   BLOCKED_NO_SUPPORTED_CAUSE:'علت قابل اصلاح در دامنه این عملگر یافت نشد.',
   BLOCKED_REPAIR_CONTROLLER_ADAPTER:'اتصال معتبر کنترل‌کننده اصلاح هنوز آماده نیست.',
   BLOCKED_NO_PARENT_PROPOSAL:'در این تلاش محدود، شاهد والد به دست نیامد؛ این به معنی ناممکن بودن طراحی نیست.'
  };
  if(!Object.hasOwn(reasons,r.state))throw new Error('STATE');
  show('blocked','بررسی پایان یافت، ولی تحویل مسدود است. '+reasons[r.state]+' معیارهای نامعلوم همچنان باز هستند؛ هیچ پلان یا دانلودی ارائه نمی‌شود.');
 }catch(error){
  show('error','پاسخ معتبر دریافت نشد؛ اجرای سرور ممکن است شروع شده باشد. تلاش دوباره خودکار انجام نمی‌شود.');
 }finally{busy=false;fields.forEach(x=>x.disabled=false);button.disabled=false;}
});
