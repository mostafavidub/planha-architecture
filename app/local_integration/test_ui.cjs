// Synthetic DOM/network harness executing the actual ui.js, not browser evidence.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const {webcrypto}=require('node:crypto');
const {spawnSync}=require('node:child_process');
const path=require('node:path');
function setup(){
 const events={};const fields={W:'12',L:'14',n:'1',requested_count:'6'};
 const els={'#form':{addEventListener:(name,fn)=>events[name]=fn},'#submit':{disabled:false},'#status':{textContent:''},'#result':{textContent:'',hidden:true}};
 let requests=[];
 const ctx={document:{querySelector:k=>els[k]},window:{addEventListener:()=>{}},FormData:function(){return Object.entries(fields)},AbortController,TextEncoder,crypto:webcrypto,fetch:(url,opts)=>new Promise(resolve=>requests.push({opts,resolve}))};
 vm.runInNewContext(fs.readFileSync(path.join(__dirname,'ui.js'),'utf8'),ctx);
 function response(index=0,mutate=x=>x){const req=requests[index];const proc=spawnSync('python3',['-B',path.join(__dirname,'validate_request.py')],{input:req.opts.body,encoding:'utf8'});assert.equal(proc.status,0,proc.stderr);const data=JSON.parse(proc.stdout);req.resolve({status:data.http_status,json:async()=>mutate(data)});}
 return {events,fields,els,requests,response,submit:()=>events.submit({preventDefault(){}})};
}
(async()=>{
 let count=0;
 async function test(name,fn){await fn();count++;console.log('PASS '+name);}
 await test('valid response displays unsupported only',async()=>{let h=setup(),p=h.submit();h.response();await p;assert.equal(h.els['#result'].hidden,false);assert.match(h.els['#status'].textContent,/هیچ پلانی/);});
 await test('input invalidates completed response',async()=>{let h=setup(),p=h.submit();h.response();await p;h.fields.W='13';h.events.input();assert.equal(h.els['#result'].hidden,true);});
 await test('late response cannot overwrite changed input',async()=>{let h=setup(),p=h.submit();h.fields.W='13';h.events.input();h.response();await p;assert.equal(h.els['#result'].hidden,true);assert.match(h.els['#status'].textContent,/تغییر/);});
 await test('duplicate pending click makes one request',async()=>{let h=setup(),p=h.submit();await h.submit();assert.equal(h.requests.length,1);h.response();await p;});
 await test('wrong raw request is fail closed',async()=>{let h=setup(),p=h.submit();h.response(0,x=>{x.envelope.received_input.W='13';return x});await p;assert.equal(h.els['#result'].hidden,true);});
 await test('canonical dimension mutation is fail closed',async()=>{let h=setup(),p=h.submit();h.response(0,x=>{x.envelope.canonical_request.dimensions_m.W.numerator='13';return x});await p;assert.equal(h.els['#result'].hidden,true);});
 await test('false acceptance cannot be upgraded by response',async()=>{let h=setup(),p=h.submit();h.response(0,x=>{x.accepted=true;return x});await p;assert.equal(h.els['#result'].hidden,true);});
 await test('new request survives late old response',async()=>{let h=setup(),old=h.submit();h.fields.W='13';h.events.input();let next=h.submit();h.response(1);await next;h.response(0);await old;const result=JSON.parse(h.els['#result'].textContent);assert.equal(result.envelope.received_input.W,'13');});
 console.log(`PASS ${count} synthetic UI tests; not live-browser race evidence`);
})().catch(e=>{console.error(e);process.exitCode=1;});
