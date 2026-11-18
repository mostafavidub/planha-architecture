'use strict';
// This separate view never changes the historical 400 form or its one-shot guard.
(() => {
 const generateButton=document.querySelector('#generate'),plans=document.querySelector('#plans');
 let active=null,sequence=0;
 function cancel(){sequence++;if(active)active.abort();active=null;generateButton.disabled=false;plans.replaceChildren();}
 form.addEventListener('input',cancel);
 form.addEventListener('submit',cancel);
 window.addEventListener('popstate',cancel);
 window.addEventListener('pageshow',event=>{if(event.persisted)cancel();});
 async function run(repairSource=null){
  if(generateButton.disabled)return;
  invalidate();cancel();const current=sequence,raw=snapshot(),body=JSON.stringify(raw);active=new AbortController();const signal=active.signal;
  generateButton.disabled=true;button.disabled=true;clear();status.textContent=repairSource?'ادامه اصلاح عضو ردشده با بازسازی و بررسی تازه در حال اجراست…':'ساخت و بررسی واقعی در حال اجراست…';
  const fresh=()=>current===sequence&&JSON.stringify(snapshot())===body;
  try{
   const response=await fetch(repairSource?'/repair':'/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:repairSource?JSON.stringify({run_id:repairSource.run_id,candidate_id:repairSource.candidate_id}):body,signal});const data=await response.json();if(!fresh())return;
   if(data.schema!=='PLANHA_MAC_PARAMETRIC_EXPERIMENT_V1'||data.accepted!==false||data.delivery_allowed!==false)throw Error('RESPONSE_AUTHORITY');
   if(response.status!==200){status.textContent=data.code==='DIMENSION_OUT_OF_OWNER_RANGE'?'عرض و طول باید هرکدام از ۵ تا ۲۵ متر باشند؛ بزرگ‌تر از ۲۵ متر پذیرفته نمی‌شود.':data.outcome==='UNSUPPORTED'?'این تعداد واحد یا برنامه فعلاً پشتیبانی نمی‌شود؛ ورودی به درخواست دیگری تبدیل نشد.':'ساخت کامل نشد؛ نتیجه پذیرفته نشد.';result.textContent=JSON.stringify(data,null,2);result.hidden=false;return;}
   const e=data.envelope,expected=canonical(raw);
   if(stable(e.canonical_request)!==stable(expected)||e.canonical_request_digest!==await sha256(stable(expected)))throw Error('REQUEST_BINDING');
   if(repairSource){const original=data.original_request_body;if(typeof original!=='string'||stable(JSON.parse(original))!==stable(e.received_input)||stable(e.received_input)!==stable(repairSource.request)||e.transport_body_sha256!==await sha256(original)||data.parent_run_id!==repairSource.run_id||data.candidates.length!==1)throw Error('REPAIR_REQUEST_BINDING');const receipt=data.candidates[0].repair_receipt;if(!receipt||receipt.parent_run_id!==repairSource.run_id||receipt.parent_candidate_id!==repairSource.candidate_id||receipt.test_only!==false||receipt.natural_failure!==true)throw Error('REPAIR_SOURCE_BINDING');}
   else if(!sameRaw(e.received_input,raw)||e.transport_body_sha256!==await sha256(body))throw Error('REQUEST_BINDING');
   if(data.qualified_count!==0||data.request_fulfilled!==false||data.requested_count!==expected.requested_count||!Array.isArray(data.candidates)||data.candidates.length>Math.min(2,expected.requested_count)||data.generated_count!==data.candidates.length)throw Error('COUNT_OR_AUTHORITY');
   const diversity=data.diversity_report;
   if(diversity){if(data.diversity_report_digest!==await sha256(stable(diversity))||diversity.request_digest!==e.canonical_request_digest||diversity.source_revision!==data.engine_source_revision||stable(diversity.candidate_ids)!==stable(data.candidates.map(c=>c.candidate_id))||stable(diversity.model_digests)!==stable(data.candidates.map(c=>c.model_digest))||diversity.required_pairs!==data.candidates.length*(data.candidates.length-1)/2||diversity.pairs.length!==diversity.required_pairs||diversity.qualified_count!==0||diversity.accepted!==false||diversity.delivery_allowed!==false)throw Error('DIVERSITY_BINDING');}
   const views=[];
   for(const c of data.candidates){if(c.accepted!==false||c.delivery_allowed!==false||c.qualified!==false||await sha256(c.model_json)!==c.model_digest)throw Error('MODEL_BINDING');const model=JSON.parse(c.model_json);if(stable(exact(model.inputs[0]))!==stable(expected.dimensions_m.W)||stable(exact(model.inputs[1]))!==stable(expected.dimensions_m.L)||model.inputs[2]!==expected.unit_count)throw Error('MODEL_INPUT_BINDING');const d=c.review_decision,r=c.physical_review,origin=r.hierarchical_provenance129;
    if(!d||d.schema!=='MAC_FRESH_REVIEW_DECISION_V1'||d.candidate_id!==c.candidate_id||d.request_digest!==e.canonical_request_digest||d.model_digest!==c.model_digest||r.model_hash!==c.model_digest||d.review_digest!==await sha256(stable(r))||d.source_revision!==data.engine_source_revision||origin.verified!==true||origin.model_hash!==c.model_digest||origin.source_revision!==d.source_revision||d.accepted!==false||d.delivery_allowed!==false||d.qualified!==false||typeof d.repair_attempted!=='boolean'||d.operator_invoked!==d.repair_attempted)throw Error('REVIEW_DECISION_BINDING');
    if(c.repair_receipt){if(d.repair_receipt_digest!==await sha256(stable(c.repair_receipt))||c.repair_receipt.repair_attempted!==d.repair_attempted||c.repair_receipt.accepted!==false||c.repair_receipt.delivery_allowed!==false)throw Error('REPAIR_RECEIPT_BINDING');}else if(d.repair_attempted!==false||d.operator_invoked!==false)throw Error('UNBOUND_REPAIR_CLAIM');
    const unsigned={...d};delete unsigned.decision_id;
    if(d.decision_id!==await sha256(stable(unsigned))||stable(d.errors)!==stable(r.errors)||stable(d.pending)!==stable(r.pending))throw Error('DECISION_DIGEST');
    const state=r.errors.length?'REJECTED_PHYSICAL':r.pending.length?'UNKNOWN_REVIEW':r.status==='PASS_CONCEPT_SCOPED_REVIEW'?'PHYSICAL_PASS_SEMANTIC_UNKNOWN':'UNKNOWN_REVIEW';
    if(d.state!==state||(r.errors.length&&r.status!=='FAIL'))throw Error('DECISION_STATE');
    const functional=c.functional_review;if(functional){if(d.functional_review_digest!==await sha256(stable(functional))||functional.model_digest!==c.model_digest||functional.physical_review_digest!==d.review_digest||functional.source_revision!==d.source_revision||functional.display_allowed!==false||functional.accepted!==false||functional.delivery_allowed!==false||functional.qualified!==false||d.design_display_allowed!==false)throw Error('FUNCTIONAL_BINDING');}else if(d.functional_review_digest)throw Error('MISSING_FUNCTIONAL_REVIEW');
    // Current required functional closure remains unknown. No design preview is authorized, even with a draft label.
    }
   if(!fresh())return;plans.replaceChildren(...views);status.textContent=(repairSource?'ادامه اصلاح یک عضو ذخیره‌شده، نه بازتولید همه گزینه‌ها. ':'')+`${data.generated_count} مدل آزمایشی ساخته شد؛ تعداد واجدشرایط صفر از هدف ${data.requested_count} است. نمایش گزینه طراحی تا تکمیل شواهد عملکردی ضروری مسدود است.`;
   result.textContent=JSON.stringify({run_id:data.run_id,outcome:data.outcome,program_policy:data.program_policy,review_decisions:data.candidates.map(c=>c.review_decision),diversity_report:data.diversity_report,functional_reviews:data.candidates.map(c=>c.functional_review||{state:'MISSING_REQUIRED_FUNCTIONAL_PROOF',display_allowed:false}),attempts:data.attempts.map(a=>({family:a.family,state:a.state,reason:a.reason})),accepted:false,delivery_allowed:false},null,2);result.hidden=false;
  }catch(error){if(!fresh()||error.name==='AbortError')return;clear();plans.replaceChildren();status.textContent='اجرا یا کنترل هویت پاسخ کامل نشد؛ نتیجه‌ای پذیرفته نشد.';}
  finally{if(fresh()){generateButton.disabled=false;button.disabled=false;active=null;}}
 }
 generateButton.addEventListener('click',()=>run());
 window.addEventListener('planha-repair-request',event=>{if(active||generateButton.disabled)return;const source=event.detail;if(!source||!source.request||Object.keys(source.request).sort().join(',')!=='L,W,n,requested_count')return;for(const key of ['W','L','n','requested_count'])form.elements.namedItem(key).value=String(source.request[key]);run(source);});
})();
