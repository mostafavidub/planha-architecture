// Synthetic network/DOM using recorded real HTTP result, NOT a live new generation.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const {webcrypto,createHash}=require('node:crypto');
const local=fs.existsSync(path.join(__dirname,'.venv'))?__dirname:path.resolve(__dirname,'../..');
const recorded=JSON.parse(fs.readFileSync(process.argv[2]||path.join(local,'evidence/requests/a4216ee4-bc3e-4763-a9aa-f27ac810fd78/result.json')));
function setup(){
 const events={};const fields=Object.fromEntries(Object.entries(recorded.envelope.received_input).map(([k,v])=>[k,String(v)]));
 function el(){return {disabled:false,hidden:true,textContent:'',children:[],style:{},namespaceURI:'http://www.w3.org/2000/svg',addEventListener(n,f){(events[n]??=[]).push(f)},replaceChildren(...v){this.children=v},append(...v){this.children.push(...v)},setAttribute(){}}}
 const els=Object.fromEntries(['form','submit','status','result','generate','plans'].map(k=>['#'+k,el()]));let pending=[];const windowEvents={};els['#form'].elements={namedItem:k=>({set value(v){fields[k]=v}})};
 const ctx={document:{querySelector:k=>els[k],createElement:el,createElementNS:el},window:{addEventListener(n,f){windowEvents[n]=f}},FormData:function(){return Object.entries(fields)},AbortController,TextEncoder,crypto:webcrypto,fetch:(url,opts)=>new Promise(resolve=>pending.push({url,opts,resolve}))};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(__dirname,'ui.js'),'utf8'),ctx);vm.runInContext(fs.readFileSync(path.join(__dirname,'generation_ui.js'),'utf8'),ctx);
 return {els,fields,pending,click:()=>events.click[0](),repair:()=>windowEvents['planha-repair-request']({detail:{run_id:recorded.parent_run_id,candidate_id:recorded.candidates[0].repair_receipt.parent_candidate_id,request:recorded.envelope.received_input}}),input:()=>events.input.forEach(f=>f()),respond(mutate=x=>x){const replay=JSON.parse(JSON.stringify(recorded));replay.original_request_body=fs.readFileSync(path.join(local,'evidence/requests',recorded.parent_run_id,'request.json'),'utf8');const data=mutate(replay);pending[0].resolve({status:200,json:async()=>data})}};
}

(async()=>{let count=0;async function test(n,fn){await fn();count++;console.log('PASS '+n)}
const settle=()=>new Promise(resolve=>setTimeout(resolve,100));
await test('explicit history repair makes one bounded request and withholds unqualified natural child',async()=>{const h=setup();h.repair();assert.equal(h.pending[0].url,'/repair');assert.equal(h.pending.length,1);h.repair();assert.equal(h.pending.length,1);h.respond();await settle();assert.equal(h.els['#plans'].children.length,0);assert.match(h.els['#status'].textContent,/ادامه اصلاح یک عضو/)});
for(const [name,mutate] of [['parent',r=>{r.parent_run_id='wrong';return r}],['source body',r=>{r.original_request_body='{}';return r}],['controlled receipt',r=>{r.candidates[0].repair_receipt.test_only=true;return r}],['candidate',r=>{r.candidates[0].repair_receipt.parent_candidate_id='wrong';return r}]])await test(name+' tamper fails closed',async()=>{const h=setup();h.repair();h.respond(mutate);await settle();assert.equal(h.els['#plans'].children.length,0);assert.match(h.els['#status'].textContent,/کامل نشد/)});
await test('late repair after input hidden',async()=>{const h=setup();h.repair();h.fields.W='30';h.input();h.respond();await settle();assert.equal(h.els['#plans'].children.length,0)});
console.log('PASS '+count+' repair UI replay scenarios, not live geometry');
})().catch(e=>{console.error(e);process.exitCode=1});
