"use strict";
(function(){
 const form=document.querySelector("#plan-form"),button=document.querySelector("#submit"),result=document.querySelector("#result");
 let busy=false;
 const stageNames=[["candidate","نامزد"],["constructed","ساخته‌شده"],["reviewed","بررسی‌شده"],["qualified","واجد شرایط"],["displayed","نمایش‌داده‌شده"],["downloaded","دانلودشده"]];
 function stageDisclosure(data){
  // This V1 response has no receipt-bound stage counters. Do not infer them.
  const known=data&&data.schema==="PUBLIC_WLN_STUDY_SUMMARY_V1";
  const attempts=known&&Number.isSafeInteger(data.actual_live_attempts)&&data.actual_live_attempts>=0?data.actual_live_attempts:"NOT_REPORTED";
  const available=known&&data.plan_count_available===0?0:"NOT_REPORTED";
  const target=document.querySelector("#stage-counts");
  target.textContent="تلاش‌های گزارش‌شده در این پاسخ: "+attempts+" (نه شمار گزینه متمایز)\n"+
   "پلان قابل ارائه در این پاسخ: "+available+" (نه شمار تاریخی دانلود)\n"+
   stageNames.map(([key,label])=>label+": NOT_REPORTED").join("\n");
  target.dataset.scope="RESPONSE_OBSERVATION_NOT_LIFECYCLE_VERIFIED";
 }
 stageDisclosure(null);
 function show(text,state){result.textContent=text;result.dataset.state=state;}
 form.addEventListener("submit",async function(event){
  event.preventDefault();if(busy)return;
  const body={W:form.elements.W.value,L:form.elements.L.value,n:form.elements.n.value};
  busy=true;button.disabled=true;Array.from(form.elements).forEach(x=>x.disabled=true);
  stageDisclosure(null);
  show("بررسی محدود در حال اجراست. هنوز هیچ طرحی تأیید نشده است.","running");
  try{
   const response=await fetch("/api/public/plan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
   const data=await response.json();
   if(data.schema==="PUBLIC_WLN_ERROR_SET_V1"){
    if(data.acceptance_contract!=="V25_PUBLIC_WLN_CONTRACT_V3"||data.generation_started!==false||!Array.isArray(data.errors)||!data.errors.length||!['accepted','qualified','display_allowed','delivery_allowed'].every(k=>data[k]===false))throw new Error("INVALID_ERROR_SET");
    if(!data.errors.every(e=>e&&typeof e.code==="string"&&(e.field===null||typeof e.field==="string")&&Number.isInteger(e.status)&&[409,422].includes(e.status)))throw new Error("INVALID_ERROR_ROW");
    if(![409,422].includes(response.status)||response.status!==data.primary_status||!data.errors.some(e=>e.code===data.code&&e.field===data.field&&e.status===data.primary_status))throw new Error("INCONSISTENT_ERROR_PRIMARY");
    show("درخواست اجرا نشد؛ خطاهای ورودی:\n"+data.errors.map(e=>(["W","L","n"].includes(e.field)?e.field:"JSON")+": "+e.code+" ["+e.status+"]").join("\n"),"error");return;
   }
   if(data.code==="STUDY_BUSY_NO_QUEUE"){show("یک بررسی دیگر در حال اجراست. درخواست شما در صف قرار نگرفت؛ تلاش دوباره خودکار نیست.","blocked");return;}
   if(data.schema==="PUBLIC_WLN_STUDY_SUMMARY_V1"){
    if(data.accepted!==false||data.qualified!==false||data.display_allowed!==false||data.delivery_allowed!==false||data.plan_count_available!==0||data.plan_payload!==null||data.download_available!==false)throw new Error("UNSAFE_SUMMARY");
    stageDisclosure(data);
    if(data.status.startsWith("UNSUPPORTED")){show("ورودی معتبر است، اما این حالت هنوز به مولد آماده متصل نیست. فعلاً فقط زمین ۱۸×۲۰ متر با ۲ واحد پشتیبانی آزمایشی دارد.","blocked");return;}
    if(data.source_integrity_verified!==true){show("نتیجهٔ کامل با منشأ تأییدشده در دسترس نیست. هیچ طرحی ارائه نشد.","error");return;}
    if(data.decision.state==="BLOCKED"){show("بررسی اجرا شد، اما طرح قابل تحویل نیست.\nرد هندسی، معیارهای نامعلوم یا خطای ارزیابی مانع تحویل است؛ هیچ طرح یا فایل خروجی ارائه نشده.\nاین نتیجه، تکمیل چرخه یا تأیید کیفیت نیست.","blocked");return;}
    show("بررسی کامل و تأییدشده در دسترس نیست. هیچ طرحی ارائه نشد.","blocked");return;
   }
   if(data.code==="STUDY_FAILED_CLOSED"||response.status>=500){show("نتیجهٔ معتبر در دسترس نیست؛ اجرای سرور ممکن است شروع شده باشد. تکرار خودکار انجام نمی‌شود.","error");return;}
   if(!response.ok){show("درخواست اجرا نشد: "+String(data.code||"خطای نامشخص")+". ورودی را بررسی کنید.","error");return;}
   throw new Error("UNEXPECTED_RESPONSE");
  }catch(error){show("نتیجهٔ قابل اتکا دریافت نشد. وضعیت اجرای سرور ممکن است نامعلوم باشد؛ تلاش دوباره خودکار انجام نمی‌شود.","error");}
  finally{busy=false;Array.from(form.elements).forEach(x=>x.disabled=false);}
 });
})();
