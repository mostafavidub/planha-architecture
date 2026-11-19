// Current JS handler tests with fake DOM/fetch, not browser or solver.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
(async()=>{
 const W={value:'18'},L={value:'20'},n={value:'3'},elements=[W,L,n];Object.assign(elements,{W,L,n});
 let handler,calls=[];const result={dataset:{}},button={};
 const form={elements,addEventListener:(event,fn)=>{assert.equal(event,'submit');handler=fn;}};
 const context={document:{querySelector:s=>({'#plan-form':form,'#submit':button,'#result':result}[s])},fetch:async(url,options)=>{
  calls.push({url,body:JSON.parse(options.body)});
  return {ok:false,status:409,json:async()=>({schema:'PUBLIC_WLN_STUDY_SUMMARY_V1',status:'UNSUPPORTED_SYNTHETIC_HANDLER_TEST',accepted:false,qualified:false,display_allowed:false,delivery_allowed:false,plan_count_available:0,plan_payload:null,download_available:false})};
 }};
 vm.runInNewContext(fs.readFileSync('app/local_integration/public_wln.js','utf8'),context);
 for(const value of ['3','4']){n.value=value;await handler({preventDefault(){}});assert.equal(calls.length,0);assert.equal(result.dataset.state,'error');}
 for(const value of ['1','2']){n.value=value;await handler({preventDefault(){}});}
 assert.equal(calls.length,2);assert.deepEqual(calls.map(x=>x.body.n),[1,2]);
 assert(calls.every(x=>Object.keys(x.body).sort().join(',')==='L,W,n'));
 console.log(JSON.stringify({scope:'FAKE_DOM_HANDLER_ONLY',invalid_n3_n4_fetch_calls:0,valid_n1_n2_mock_fetch_calls:2,fresh_geometry:false,real_browser:false}));
})().catch(e=>{console.error(e);process.exitCode=1;});
