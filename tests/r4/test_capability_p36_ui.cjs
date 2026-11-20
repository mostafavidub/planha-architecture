"use strict";
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const {webcrypto,createHash}=require('node:crypto');
const source=fs.readFileSync('app/local_integration/public_wln.js','utf8');
const sh=s=>createHash('sha256').update(s).digest('hex');
const auth={accepted:false,qualified:false,display_allowed:false,delivery_allowed:false};
const e={W:{value:"18"},L:{value:"20"},n:{value:"2"}},fields=Object.assign(Object.values(e),e);
const text=()=>({textContent:"",dataset:{}});
const elements={"#submit":{},"#result":text(),"#stage-counts":text(),"#capability-status":text()};
let submit,make;
elements["#plan-form"]={elements:fields,addEventListener:(k,fn)=>{if(k==="submit")submit=fn;}};
const ctx={document:{querySelector:x=>elements[x]},fetch:async(_u,{body})=>make(body),TextEncoder,crypto:webcrypto,window:{addEventListener(){}}};
vm.runInNewContext(source,ctx);
const cap=(wire,kind,extra={})=>({schema:"PUBLIC_WLN_CAPABILITY_P36_V1",request_digest:sh(wire),capability_state:kind,product_available:false,...auth,...extra});
const value=(wire,extra={})=>({schema:"PUBLIC_WLN_STUDY_SUMMARY_V1",...auth,input_valid:true,source_integrity_verified:true,
 status:"LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED",actual_live_attempts:1,plan_count_available:0,plan_payload:null,download_available:false,
 http_lifecycle:{schema:"HTTP_WITHHOLDING_X04_V1",request_id:"a".repeat(32),summary_digest:"b".repeat(64),request_digest:sh(wire),response_state:"ON_TIME_OBSERVED",receipt_verified:false,evidence_usable:false},
 full_evidence_binding:{schema:"HTTP_FULL_EVIDENCE_X07_V1",state:"SAME_REQUEST_FULL_REPORT_CONSISTENCY_VERIFIED_SCOPED",request_digest:sh(wire),binding_verified:true,
 nonce_digest:"b".repeat(64),model_digest:"b".repeat(64),decision_digest:"b".repeat(64),source_digest:"b".repeat(64),file_hashes_digest:"b".repeat(64),file_count:9},
 decision:{state:"BLOCKED",blockers:["CURRENT_UNKNOWN"],...auth},
 capability:cap(wire,"STUDY_PERMITTED",{evidence_state:"SAME_REQUEST_STUDY_REPORTS_VERIFIED",evidence_contract:"HTTP_FULL_EVIDENCE_X07_V1",...extra})});
const response=(status,v)=>({status,ok:status===200,json:async()=>v});
async function go(fn){make=fn;await submit({preventDefault(){}});return elements["#capability-status"].dataset.capability;}
(async()=>{
 assert.equal(await go(w=>response(200,value(w))),"same_request_study_verified");
 assert.equal(await go(w=>response(200,value(w))),"study_permitted"); // stale lifetime id, no trust promotion
 assert.equal(await go(w=>response(200,value(w,{request_digest:"0".repeat(64)}))),"");
 assert.equal(await go(w=>response(409,{...auth,code:"STUDY_BUSY_NO_QUEUE",capability:cap(w,"STUDY_BUSY")})),"study_busy");
 assert.equal(elements["#result"].dataset.statusKind,"busy");
 assert.equal(await go(w=>response(504,{...auth,code:"DEADLINE_EXCEEDED_RESULT_WITHHELD",capability:cap(w,"STUDY_RESULT_WITHHELD")})),"study_result_withheld");
 assert.equal(elements["#result"].dataset.statusKind,"timeout");
 assert.equal(await go(w=>response(409,{...value(w),status:"UNSUPPORTED_SELECTED_SAME_VERSION_CASE",capability:cap(w,"VALID_UNSUPPORTED")})),"valid_unsupported");
 console.log("P36 renderer: exact-body hash, replay downgrade, 409/busy/504, no delivery");
})().catch(e=>{console.error(e);process.exitCode=1;});
