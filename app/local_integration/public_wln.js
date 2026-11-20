"use strict";
(function(){
 const form=document.querySelector("#plan-form"),button=document.querySelector("#submit"),result=document.querySelector("#result");
 let busy=false,requestSequence=0;
 const capabilityLabel=document.querySelector("#capability-status");
 const capabilityText={
  INVALID_INPUT:"پشتیبانی: ورودی نامعتبر است.",
  WIRE_UNSUPPORTED:"پشتیبانی: قالب ارسال این ورودی پشتیبانی نمی‌شود.",
  VALID_UNSUPPORTED:"پشتیبانی: ورودی معتبر است؛ اجرای آزمایشی برای این ترکیب آماده نیست.",
  STUDY_PERMITTED:"پشتیبانی: فقط بررسی آزمایشی؛ نه مجوز ارائهٔ طرح.",
  STUDY_BUSY:"پشتیبانی: مسیر آزمایشی مشغول است.",
  STUDY_RESULT_WITHHELD:"پشتیبانی: نتیجه در مهلت پاسخ ارائه نشد.",
  SERVER_RESULT_UNAVAILABLE:"پشتیبانی: نتیجهٔ معتبر در دسترس نیست."
 };
 function renderCapability(value,verified=false){
  if(!capabilityLabel)return;
  capabilityLabel.textContent=value?(verified?"پشتیبانی: گزارش‌های همین بررسی آزمایشی تطبیق داده شدند؛ تحویل طرح مجاز نیست.":capabilityText[value.capability_state]):"";
  capabilityLabel.dataset.capability=value?(verified?"same_request_study_verified":value.capability_state.toLowerCase()):"";
 }
 async function capabilityFor(data,response,wire){
  const c=data&&data.capability;if(!c||c.schema!=="PUBLIC_WLN_CAPABILITY_P36_V1"||
   !Object.hasOwn(capabilityText,c.capability_state)||c.product_available!==false||c.production_supported!==false||
   !['accepted','qualified','display_allowed','delivery_allowed'].every(k=>c[k]===false))return null;
  const status=c.capability_state;
  const s=response.status,summary=data.schema==="PUBLIC_WLN_STUDY_SUMMARY_V1",errors=data.schema==="PUBLIC_WLN_ERROR_SET_V1";
  const matches={
   INVALID_INPUT:s===422&&errors&&data.primary_status===422,
   WIRE_UNSUPPORTED:s===409&&errors&&data.primary_status===409,
   VALID_UNSUPPORTED:s===409&&summary&&data.input_valid===true&&typeof data.status==="string"&&data.status.startsWith("UNSUPPORTED"),
   STUDY_BUSY:s===409&&data.code==="STUDY_BUSY_NO_QUEUE",
   STUDY_RESULT_WITHHELD:s===504&&["DEADLINE_EXCEEDED_BEFORE_DISPATCH","DEADLINE_EXCEEDED_RESULT_WITHHELD"].includes(data.code),
   STUDY_PERMITTED:s===200&&summary&&data.input_valid===true&&["BLOCKED","LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED"].includes(data.status),
   SERVER_RESULT_UNAVAILABLE:s===500&&["INPUT_VALIDATION_FAILED_CLOSED","STUDY_FAILED_CLOSED","HTTP_WORKER_START_FAILED"].includes(data.code)
  };
  if(!matches[status]||!denied(data))return null;
  try{
   const h=Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(wire))),x=>x.toString(16).padStart(2,"0")).join("");
   return c.request_digest===h?c:null;
  }catch(_){return null;}
 }
 const seenResponses=new Set(),seenNonces=new Set();
 const auth=['accepted','qualified','display_allowed','delivery_allowed'];
 const hex=(v,n=64)=>typeof v==='string'&&new RegExp('^[0-9a-f]{'+n+'}$').test(v);
 const denied=v=>v&&auth.every(k=>v[k]===false);
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
 function show(text,state,kind=state){result.textContent=text;result.dataset.state=state;result.dataset.statusKind=kind;}

 // P32-A: consistency of a scoped observation, never authenticity/admission.
 async function boundObservation(data,response,wire){
  const binding=data.full_evidence_binding,life=data.http_lifecycle,decision=data.decision;
  if(response.status!==200||!["BLOCKED","LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED"].includes(data.status)||data.input_valid!==true||data.source_integrity_verified!==true||
     !binding||binding.binding_verified!==true||!decision||decision.state!=="BLOCKED"||!denied(decision)||
     !Array.isArray(decision.blockers)||!decision.blockers.every(x=>typeof x==="string")||
     !life||life.schema!=="HTTP_WITHHOLDING_X04_V1"||life.response_state!=="ON_TIME_OBSERVED"||
     life.evidence_usable!==false||life.receipt_verified!==false||!hex(life.request_id,32)||!hex(life.summary_digest))return false;
  const bytes=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(wire));
  const requestHash=Array.from(new Uint8Array(bytes),x=>x.toString(16).padStart(2,"0")).join("");
  if(life.request_digest!==requestHash||seenResponses.has(life.request_id))return false;
  if(binding.schema==="SINGLE_READBACK_P17_V1"){
   if(data.status!=="BLOCKED")return false;
   const rows=data.single_unit_evidence;
   if(!Array.isArray(rows)||rows.length!==1||data.actual_live_attempts!==1)return false;
   const row=rows[0],states=row.current_states,hashes=row.observed_file_hashes;
   if(row.receipt_verified!==true||row.state!=="FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED"||
      row.timed_out!==false||row.wait_completed!==true||row.returncode!==0||
      !hex(row.nonce,32)||seenNonces.has(row.nonce)||!hex(row.model_digest)||!hex(row.runtime_digest)||
      row.observed_model_digest!==row.model_digest||!hashes||hashes.model!==row.model_digest||
      hashes.summary!==row.runtime_digest||!hex(hashes.decision)||
      !Number.isSafeInteger(row.physical_errors)||row.physical_errors<0||
      !Number.isSafeInteger(row.physical_pending)||row.physical_pending<0||
      !["FAIL","PASS_CONCEPT_SCOPED_REVIEW"].includes(row.physical_status)||
      !states||Object.keys(states).sort().join("|")!==["CONTINUOUS_USEFUL_LIVING","CURRENT_PROGRAM_SUITABILITY","KITCHEN_GUEST_PATH_SEPARATION","NONFUNCTIONAL_WALL_EXCLUSION"].sort().join("|")||
      !Object.values(states).every(x=>["PASS","FAIL","UNKNOWN","NOT_EVALUATED","EVALUATOR_ERROR"].includes(x)))return false;
   if((row.physical_errors>0&&row.physical_status!=="FAIL")||
      (row.physical_status==="FAIL")!==decision.blockers.includes("PHYSICAL_FAIL")||
      Object.values(states).includes("UNKNOWN")!==decision.blockers.includes("CURRENT_UNKNOWN")||
      Object.values(states).includes("FAIL")!==decision.blockers.includes("CURRENT_NECESSARY_FAIL")||
      Object.values(states).includes("NOT_EVALUATED")!==decision.blockers.includes("CURRENT_NOT_EVALUATED")||
      (Object.values(states).includes("EVALUATOR_ERROR")&&!decision.blockers.includes("EVALUATOR_ERROR"))||
      (row.physical_pending>0)!==decision.blockers.includes("PHYSICAL_PENDING"))return false;
  }else if(binding.schema==="HTTP_FULL_EVIDENCE_X07_V1"){
   if(data.status!=="LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED"||binding.request_digest!==requestHash||binding.state!=="SAME_REQUEST_FULL_REPORT_CONSISTENCY_VERIFIED_SCOPED"||
      !["nonce_digest","model_digest","decision_digest","source_digest","file_hashes_digest"].every(k=>hex(binding[k]))||
      binding.file_count!==9||data.actual_live_attempts!==1)return false;
  }else return false;
  seenResponses.add(life.request_id);
  if(binding.schema==="SINGLE_READBACK_P17_V1")seenNonces.add(data.single_unit_evidence[0].nonce);
  return true;
 }
 function observationText(blockers){
  const physical=blockers.includes("PHYSICAL_FAIL"),unknown=blockers.includes("CURRENT_UNKNOWN");
  const evaluator=blockers.some(x=>x==="EVALUATOR_ERROR"||x==="CURRENT_EVALUATOR_ERROR");
  const necessary=blockers.includes("CURRENT_NECESSARY_FAIL"),notEvaluated=blockers.includes("CURRENT_NOT_EVALUATED"),pending=blockers.includes("PHYSICAL_PENDING")||blockers.includes("PHYSICAL_NOT_VERIFIED");
  const parts=[];
  if(physical)parts.push("بررسی فیزیکی این مدل رد شده است؛ جزئیات علت در این پاسخ گزارش نشده.");
  if(necessary)parts.push("حداقل یک شرط ضروری در بررسی فعلی رد شده است.");
  if(notEvaluated)parts.push("حداقل یک معیار هنوز ارزیابی نشده است.");
  if(pending)parts.push("بررسی فیزیکی هنوز موارد تعیین‌تکلیف‌نشده دارد.");
  if(unknown)parts.push("نتیجهٔ معیارهای کیفیت هنوز نامشخص است.");
  if(evaluator)parts.push("ارزیابی با خطا مواجه شده است؛ این خطا به‌معنای ناممکن بودن طرح نیست.");
  if(!parts.length)parts.push("بررسی ثبت شد، اما مجوز ارائهٔ طرح وجود ندارد.");
  parts.push("رسید داخلی با شواهد همان درخواست تطبیق شده؛ این تأیید مستقل چرخهٔ HTTP یا مجوز تحویل نیست. هیچ طرح یا فایلی ارائه نمی‌شود.");
  return {text:parts.join("\n"),kind:evaluator?"evaluation_error":physical?(unknown?"physical_rejected_quality_unknown":"physical_rejected"):(necessary?"current_rejected":notEvaluated?"not_evaluated":unknown?"quality_unknown":pending?"physical_unresolved":"delivery_blocked")};
 }
 function resetForm(){busy=false;Array.from(form.elements).forEach(x=>x.disabled=false);}
 // Navigation invalidates a pending response, not the server job. No cancellation claim.
 if(typeof window!=="undefined"){
  window.addEventListener("pagehide",()=>{requestSequence++;});
  window.addEventListener("pageshow",event=>{if(event.persisted){requestSequence++;resetForm();stageDisclosure(null);renderCapability(null);show("وضعیت اجرای قبلی نامعلوم است؛ درخواست تازه‌ای خودکار ارسال نشد.","error","outcome_unknown");}});
 }

 form.addEventListener("submit",async function(event){
  event.preventDefault();if(busy)return;
  const body={W:form.elements.W.value,L:form.elements.L.value,n:form.elements.n.value};
  const sequence=++requestSequence,wire=JSON.stringify(body);
  busy=true;button.disabled=true;Array.from(form.elements).forEach(x=>x.disabled=true);
  stageDisclosure(null);renderCapability(null);
  show("بررسی محدود در حال اجراست. هنوز هیچ طرحی تأیید نشده است.","running");
  try{
   const response=await fetch("/api/public/plan",{method:"POST",headers:{"Content-Type":"application/json"},body:wire});
   const data=await response.json();
   if(sequence!==requestSequence)return;
   const capability=await capabilityFor(data,response,wire);
   if(sequence!==requestSequence)return;
   renderCapability(capability);
   if(data.schema==="PUBLIC_WLN_ERROR_SET_V1"){
    if(data.acceptance_contract!=="V25_PUBLIC_WLN_CONTRACT_V3"||data.generation_started!==false||!Array.isArray(data.errors)||!data.errors.length||!['accepted','qualified','display_allowed','delivery_allowed'].every(k=>data[k]===false))throw new Error("INVALID_ERROR_SET");
    if(!data.errors.every(e=>e&&typeof e.code==="string"&&(e.field===null||typeof e.field==="string")&&Number.isInteger(e.status)&&[409,422].includes(e.status)))throw new Error("INVALID_ERROR_ROW");
    if(![409,422].includes(response.status)||response.status!==data.primary_status||!data.errors.some(e=>e.code===data.code&&e.field===data.field&&e.status===data.primary_status))throw new Error("INCONSISTENT_ERROR_PRIMARY");
    show("درخواست اجرا نشد؛ خطاهای ورودی:\n"+data.errors.map(e=>(["W","L","n"].includes(e.field)?e.field:"JSON")+": "+e.code+" ["+e.status+"]").join("\n"),"error",data.primary_status===409?"unsupported_wire":"invalid_input");return;
   }
   if(data.code==="STUDY_BUSY_NO_QUEUE"){if(response.status!==409||!denied(data))throw new Error("BUSY_RESPONSE");show("یک بررسی دیگر در حال اجراست. درخواست شما در صف قرار نگرفت؛ تلاش دوباره خودکار نیست.","blocked","busy");return;}
   if(data.schema==="PUBLIC_WLN_STUDY_SUMMARY_V1"){
    if(data.accepted!==false||data.qualified!==false||data.display_allowed!==false||data.delivery_allowed!==false||data.plan_count_available!==0||data.plan_payload!==null||data.download_available!==false)throw new Error("UNSAFE_SUMMARY");
    stageDisclosure(data);
    if(typeof data.status==="string"&&data.status.startsWith("UNSUPPORTED")){if(response.status!==409||data.input_valid!==true)throw new Error("UNSUPPORTED_RESPONSE");show("ورودی معتبر است، اما این حالت هنوز به مولد آماده متصل نیست. اجرای آزمایشی فقط برای ترکیب‌های اعلام‌شده در فرم فعال است.","blocked","unsupported_case");return;}
    const bound=await boundObservation(data,response,wire);
    if(sequence!==requestSequence)return;
    if(!bound){show("نتیجه‌ای مشاهده شد، اما اتصال معتبر آن به شواهد همین درخواست تأیید نشد. رد یا تأیید معماری اعلام نمی‌شود؛ هیچ طرحی ارائه نشد.","blocked","observed_unverified");return;}
    if(capability&&capability.evidence_state==="SAME_REQUEST_STUDY_REPORTS_VERIFIED"&&capability.evidence_contract===data.full_evidence_binding.schema)renderCapability(capability,true);
    const status=observationText(data.decision.blockers);show(status.text,"blocked",status.kind);return;
   }
   if(response.status===504&&["DEADLINE_EXCEEDED_BEFORE_DISPATCH","DEADLINE_EXCEEDED_RESULT_WITHHELD"].includes(data.code)&&denied(data)){show("مهلت پاسخ پایان یافت؛ نتیجهٔ دیررس ارائه نمی‌شود. توقف اجرای سرور یا رد معماری احراز نشده است.","error","timeout");return;}
   if(data.code==="STUDY_FAILED_CLOSED"||response.status>=500){show("نتیجهٔ معتبر در دسترس نیست؛ اجرای سرور ممکن است شروع شده باشد. تکرار خودکار انجام نمی‌شود.","error","server_error");return;}
   if(!response.ok){show("درخواست اجرا نشد: "+String(data.code||"خطای نامشخص")+". ورودی را بررسی کنید.","error");return;}
   throw new Error("UNEXPECTED_RESPONSE");
  }catch(error){if(sequence!==requestSequence)return;renderCapability(null);show("نتیجهٔ قابل اتکا دریافت نشد. وضعیت اجرای سرور ممکن است نامعلوم باشد؛ تلاش دوباره خودکار انجام نمی‌شود.","error","outcome_unknown");}
  finally{if(sequence===requestSequence)resetForm();}
 });
})();