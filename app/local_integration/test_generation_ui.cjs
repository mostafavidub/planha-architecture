// Synthetic network/DOM using recorded real HTTP result, NOT a live new generation.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const {webcrypto,createHash}=require('node:crypto');
const local=fs.existsSync(path.join(__dirname,'.venv'))?__dirname:path.resolve(__dirname,'../..');
const recorded=JSON.parse(fs.readFileSync(process.argv[2]||path.join(local,'evidence/review_cycle/integrated_http_result.json')));
function setup(){
 const events={};const fields=Object.fromEntries(Object.entries(recorded.envelope.received_input).map(([k,v])=>[k,String(v)]));
 function el(){return {disabled:false,hidden:true,textContent:'',children:[],style:{},namespaceURI:'http://www.w3.org/2000/svg',addEventListener(n,f){(events[n]??=[]).push(f)},replaceChildren(...v){this.children=v},append(...v){this.children.push(...v)},setAttribute(){}}}
 const els=Object.fromEntries(['form','submit','status','result','generate','plans'].map(k=>['#'+k,el()]));let pending=[];
 const ctx={document:{querySelector:k=>els[k],createElement:el,createElementNS:el},window:{addEventListener(){}},FormData:function(){return Object.entries(fields)},AbortController,TextEncoder,crypto:webcrypto,fetch:(url,opts)=>new Promise(resolve=>pending.push({url,opts,resolve}))};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(__dirname,'ui.js'),'utf8'),ctx);vm.runInContext(fs.readFileSync(path.join(__dirname,'generation_ui.js'),'utf8'),ctx);
 return {els,fields,pending,click:()=>events.click[0](),input:()=>events.input.forEach(f=>f()),respond(mutate=x=>x){const replay=JSON.parse(JSON.stringify(recorded));replay.envelope.received_input={...fields};replay.envelope.transport_body_sha256=createHash('sha256').update(pending[0].opts.body).digest('hex');const data=mutate(replay);pending[0].resolve({status:200,json:async()=>data})}};
}
(async()=>{let count=0;async function test(n,fn){await fn();count++;console.log('PASS '+n)}
 await test('recorded bound review never renders missing required functional proof',async()=>{let h=setup(),p=h.click();h.respond();await p;assert.equal(h.els['#plans'].children.length,0);assert.match(h.els['#status'].textContent,/واجدشرایط صفر/)});
 for(const [name,mutate]of [
 ['review tamper',r=>{r.candidates[0].physical_review.status='FAKE_PASS';return r}],
 ['decision model tamper',r=>{r.candidates[0].review_decision.model_digest='other';return r}],
 ['false acceptance',r=>{r.candidates[0].review_decision.accepted=true;return r}],
 ['wrong decision state',r=>{r.candidates[0].review_decision.state='REJECTED_PHYSICAL';return r}],
 ['source mismatch',r=>{r.engine_source_revision='other';return r}],
 ['missing decision',r=>{delete r.candidates[0].review_decision;return r}]])
 await test(name+' fails closed',async()=>{let h=setup(),p=h.click();h.respond(mutate);await p;assert.equal(h.els['#plans'].children.length,0);assert.match(h.els['#status'].textContent,/کامل نشد/)});
 await test('late generation reply after input is hidden',async()=>{let h=setup(),p=h.click();h.fields.W='30';h.input();h.respond();await p;assert.equal(h.els['#plans'].children.length,0)});

 if(recorded.candidates[0].functional_review){
 for(const [name,mutate]of [['functional display promotion',r=>{r.candidates[0].functional_review.display_allowed=true;return r}],['functional model mismatch',r=>{r.candidates[0].functional_review.model_digest='wrong';return r}],['missing functional report',r=>{delete r.candidates[0].functional_review;return r}]])
 await test(name+' fails closed',async()=>{let h=setup(),p=h.click();h.respond(mutate);await p;assert.equal(h.els['#plans'].children.length,0);assert.match(h.els['#status'].textContent,/کامل نشد/)});
 }
 if(recorded.diversity_report){
 for(const [name,mutate]of [['diversity candidate mismatch',r=>{r.diversity_report.candidate_ids[0]='wrong';return r}],['missing diversity pair',r=>{r.diversity_report.pairs=[];return r}]])await test(name+' fails closed',async()=>{let h=setup(),p=h.click();h.respond(mutate);await p;assert.equal(h.els['#plans'].children.length,0);assert.match(h.els['#status'].textContent,/کامل نشد/)});
 }
 console.log('PASS '+count+' generation UI synthetic/replay cases; no live browser claim');
})().catch(e=>{console.error(e);process.exitCode=1});
