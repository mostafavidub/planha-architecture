"use strict";
(function(){
 const form=document.querySelector("#plan-form"),button=document.querySelector("#submit"),result=document.querySelector("#result");
 let busy=false;
 function show(text,state){result.textContent=text;result.dataset.state=state;}
 form.addEventListener("submit",async function(event){
  event.preventDefault();if(busy)return;
  const n=Number(form.elements.n.value);
  if(!Number.isSafeInteger(n)||n<1){show("تعداد واحد باید عدد صحیح مثبت باشد.","error");return;}
  const body={W:form.elements.W.value,L:form.elements.L.value,n:n};
  busy=true;button.disabled=true;Array.from(form.elements).forEach(x=>x.disabled=true);
  show("بررسی محدود در حال اجراست. هنوز هیچ طرحی تأیید نشده است.","running");
  try{
   const response=await fetch("/api/public/plan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
   const data=await response.json();
   if(data.code==="STUDY_BUSY_NO_QUEUE"){show("یک بررسی دیگر در حال اجراست. درخواست شما در صف قرار نگرفت؛ تلاش دوباره خودکار نیست.","blocked");return;}
   if(data.schema==="PUBLIC_WLN_STUDY_SUMMARY_V1"){
    if(data.accepted!==false||data.qualified!==false||data.display_allowed!==false||data.delivery_allowed!==false||data.plan_count_available!==0||data.plan_payload!==null||data.download_available!==false)throw new Error("UNSAFE_SUMMARY");
    if(data.status.startsWith("UNSUPPORTED")){show("ورودی معتبر است، اما این حالت هنوز به مولد آماده متصل نیست. فعلاً فقط زمین ۱۸×۲۰ متر با ۲ واحد پشتیبانی آزمایشی دارد.","blocked");return;}
    if(data.decision.state==="BLOCKED"){show("بررسی اجرا شد، اما طرح قابل تحویل نیست.\nرد هندسی یا معیارهای نامعلوم هنوز باقی است؛ هیچ طرح یا فایل خروجی ارائه نشده.\nاین نتیجه، تکمیل چرخه یا تأیید کیفیت نیست.","blocked");return;}
    show("بررسی کامل و تأییدشده در دسترس نیست. هیچ طرحی ارائه نشد.","blocked");return;
   }
   if(!response.ok){show("درخواست اجرا نشد: "+String(data.code||"خطای نامشخص")+". ورودی را بررسی کنید.","error");return;}
   throw new Error("UNEXPECTED_RESPONSE");
  }catch(error){show("نتیجهٔ قابل اتکا دریافت نشد. وضعیت اجرای سرور ممکن است نامعلوم باشد؛ تلاش دوباره خودکار انجام نمی‌شود.","error");}
  finally{busy=false;Array.from(form.elements).forEach(x=>x.disabled=false);}
 });
})();
