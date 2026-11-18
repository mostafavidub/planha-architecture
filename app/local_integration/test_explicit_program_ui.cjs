// Synthetic replay checks using real HTTP evidence; not new geometry or live browser.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const {webcrypto,createHash}=require('node:crypto');
const parentText=fs.readFileSync(process.argv[2],'utf8'),childText=fs.readFileSync(process.argv[3],'utf8');
const parent=JSON.parse(parentText),child=JSON.parse(childText);
const hash=x=>createHash('sha256').update(x).digest('hex');
function setup(){
 const events={},windowEvents={};
 const raw=parent.envelope.received_input,fields={W:raw.W,L:raw.L,n:raw.n,requested_count:raw.requested_count,bedrooms_per_unit:'2'};
 function el(){return {disabled:false,hidden:true,textContent:'',children:[],addEventListener(n,f){(events[n]??=[]).push(f)},replaceChildren(...v){this.children=v},append(...v){this.children.push(...v)}}}
 const els=Object.fromEntries(['form','submit','status','result','generate','plans'].map(k=>['#'+k,el()]));
 els['#form'].elements={namedItem:k=>({get value(){return fields[k]},set value(v){fields[k]=v}})};
 const pending=[],ctx={document:{querySelector:k=>els[k]},window:{addEventListener(n,f){(windowEvents[n]??=[]).push(f)},dispatchEvent(){}},CustomEvent:function(n,d){this.type=n;this.detail=d.detail},FormData:function(){return Object.entries(fields)},AbortController,TextEncoder,crypto:webcrypto,fetch:(url,opts)=>new Promise(resolve=>pending.push({url,opts,resolve}))};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(__dirname,'ui.js'),'utf8'),ctx);vm.runInContext(fs.readFileSync(path.join(__dirname,'generation_ui.js'),'utf8'),ctx);
 return {els,fields,pending,wire:ctx.readExactWire,canonical:ctx.exactWireCanonical,click:()=>events.click[0](),input:()=>events.input.forEach(f=>f()),repair(mode='explicit-pair'){const source={run_id:parent.run_id,candidate_id:parent.candidates[0].candidate_id,model_digest:parent.candidates[0].model_digest,pending:parent.candidates[0].physical_review.pending,request:raw,mode};for(const f of windowEvents['planha-repair-request'])f({detail:source})},respond(kind,mutate=x=>x,wireTransform=x=>x){const r=JSON.parse(JSON.stringify(kind==='parent'?parent:child));if(kind==='parent'){r.envelope.received_input=JSON.parse(pending[0].opts.body);r.envelope.transport_body_sha256=hash(pending[0].opts.body);}const changed=mutate(r),wire=ctx.readExactWire(kind==='parent'?parentText:childText);pending[0].resolve({status:200,text:async()=>wireTransform(ctx.exactWireCanonical(changed,wire.numbers),ctx,wire),json:async()=>changed});}};
}
const settle=()=>new Promise(r=>setTimeout(r,200));
(async()=>{
 let count=0;async function test(name,fn){await fn();console.log('PASS '+name);count++}

 await test('numeric lexical identity differs for equal 7.0 and 7',async()=>{const h=setup(),a=h.wire('{"x":7.0}'),b=h.wire('{"x":7}');assert.equal(a.data.x,b.data.x);assert.notEqual(hash(h.canonical(a.data,a.numbers)),hash(h.canonical(b.data,b.numbers)));assert.equal(h.canonical(a.data,a.numbers),'{"x":7.0}')});
 await test('scientific notation and negative zero retain wire spelling',async()=>{const h=setup(),w=h.wire('{"x":[1e-05,-0.0,9007199254740993]}');assert.equal(h.canonical(w.data,w.numbers),'{"x":[1e-05,-0.0,9007199254740993]}');assert(Object.is(w.data.x[1],-0))});
 await test('number strings and escaped text are not numeric tokens',async()=>{const h=setup(),raw=JSON.stringify({text:'7.0 1e-05 "quote" \\ slash',number:'-0.0'}),w=h.wire(raw);assert.equal(w.numbers.size,0);assert.deepEqual(JSON.parse(h.canonical(w.data,w.numbers)),JSON.parse(raw))});
 await test('escaped Unicode canonicalizes as a string value',async()=>{const h=setup(),w=h.wire('{"x":"\\u06f7"}');assert.equal(h.canonical(w.data,w.numbers),'{"x":"۷"}')});
 await test('duplicate keys and malformed syntax fail closed',async()=>{const h=setup();for(const raw of ['{"x":1,"x":2}','{"a":{"x":1,"x":1}}','{"x":01}','[1,]','{"x":1} trailing'])assert.throws(()=>h.wire(raw))});
 await test('structural changes produce a different canonical digest',async()=>{const h=setup(),w=h.wire('{"x":[7.0,8.0]}'),before=hash(h.canonical(w.data,w.numbers));w.data.x.reverse();assert.notEqual(hash(h.canonical(w.data,w.numbers)),before)});
 await test('semantically equivalent numeric transport tamper is rejected by receipt',async()=>{const h=setup(),p=h.click();h.respond('parent',x=>x,(text,ctx,wire)=>{const original=ctx.exactWireCanonical(parent.candidates[0].generation_context,wire.numbers,['candidates',0,'generation_context']),changed=original.replace(/([:\[,])(-?[0-9]+)\.0(?=[,\]}])/,'$1$2');assert.notEqual(original,changed,'fixture needs at least one integral float');assert.deepEqual(JSON.parse(original),JSON.parse(changed));assert(text.includes(original));return text.replace(original,changed)});await p;assert.match(h.els['#status'].textContent,/PAIR_PRODUCER_RECEIPT/);assert.equal(h.els['#plans'].children.length,0)});
 await test('explicit programme in request and constructor127 response remains nondisplay',async()=>{const h=setup(),p=h.click();assert.deepEqual(JSON.parse(h.pending[0].opts.body).program,{bedrooms_per_unit:2});h.respond('parent');await p;assert.match(h.els['#status'].textContent,/واجدشرایط صفر/);assert.equal(h.els['#plans'].children.length,0)});
 for(const [name,mutate] of [
 ['wrong requested programme',r=>{r.envelope.canonical_request.program.bedrooms_per_unit=3;return r}],
 ['missing initial producer receipt',r=>{delete r.candidates[0].initial_producer_receipt;return r}],
 ['ambiguous source provenance',r=>{r.candidates[0].physical_review.hierarchical_provenance129={verified:true};return r}],
 ['wrong source programme',r=>{r.candidates[0].generation_context.construction_trace.proposals.A.bedrooms=3;return r}],
 ['functional display escalation',r=>{r.candidates[0].functional_review.display_allowed=true;return r}]
 ])await test(name+' rejected',async()=>{const h=setup(),p=h.click();h.respond('parent',mutate);await p;assert.match(h.els['#status'].textContent,/کامل نشد/);assert.equal(h.els['#plans'].children.length,0)});
 await test('pair cannot reach legacy repair handler',async()=>{const h=setup();h.repair('legacy');assert.equal(h.pending.length,0)});
 await test('bound pair continuation one request and no preview',async()=>{const h=setup();h.repair();h.repair();assert.equal(h.pending.length,1);assert.equal(h.pending[0].url,'/redesign-explicit-two');h.respond('child');await settle();assert.match(h.els['#status'].textContent,/بازطراحی اکتشافی دوخواب/);assert.equal(h.els['#plans'].children.length,0)});
 for(const [name,mutate]of[
 ['wrong parent model',r=>{r.candidates[0].exploratory_redirection_receipt.parent_model_digest='0'.repeat(64);return r}],
 ['wrong parent pending',r=>{r.candidates[0].exploratory_redirection_receipt.parent_pending_preserved=[];return r}],
 ['forged child count',r=>{r.generated_count=r.generated_count?0:1;return r}],
 ['missing exploratory receipt',r=>{delete r.candidates[0].exploratory_redirection_receipt;return r}],
 ['production escalation',r=>{r.candidates[0].exploratory_redirection_receipt.production_repair_registered=true;return r}]
 ])await test(name+' rejected',async()=>{const h=setup();h.repair();h.respond('child',mutate);await settle();assert.match(h.els['#status'].textContent,/کامل نشد/);assert.equal(h.els['#plans'].children.length,0)});
 await test('programme change suppresses late reply',async()=>{const h=setup();h.repair();h.fields.bedrooms_per_unit='3';h.input();h.respond('child');await settle();assert.equal(h.els['#result'].hidden,true);assert.equal(h.els['#plans'].children.length,0)});
 console.log('EXPLICIT_UI_REPLAY '+count+' passed; synthetic responses only');
})().catch(e=>{console.error(e);process.exitCode=1});
