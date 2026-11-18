const fs=require('fs'),vm=require('vm'),assert=require('assert');
const script=fs.readFileSync(__dirname+'/index.html','utf8').split('<script>')[1].split('</script>')[0];
const nodes={};function node(){return {textContent:'',children:[],addEventListener(){},replaceChildren(){this.children=[]},append(...xs){this.children.push(...xs)}};}
const context=vm.createContext({document:{querySelector(k){return nodes[k]??=(node())},createElement:node},setTimeout,URL,Blob,console});
vm.runInContext(script,context);
(async()=>{
 const expected={generation_run_id:'run',canonical_request_digest:'canonical',raw_digest:'raw'};
 for(const key of Object.keys(expected)){
  context.fetch=async()=>({ok:true,json:async()=>({...expected,[key]:'stale',state:'UNKNOWN'})});
  context.expected=expected;
  await assert.rejects(vm.runInContext("poll('/api/runs/run',0,0,expected)",context),/همین ورودی/);
  assert.equal(nodes['#result'].textContent,'');
 }
 context.fetch=async()=>({ok:true,json:async()=>({...expected,state:'UNKNOWN',reason:'test only'})});
 await vm.runInContext("poll('/api/runs/run',0,0,expected)",context);
 assert.match(nodes['#status'].textContent,/نامشخص/);
 vm.runInContext("renderMembers({members:[{kind:'joint',binding:{candidate_id:'CURRENT',fresh_digest:'ownfresh'},quality:[]}]})",context);
 assert.match(nodes['#summary'].children[0].children[1].textContent,/CURRENT/);
 console.log('5 UI poll/render checks PASS; no browser/server/generation');
})().catch(e=>{console.error(e);process.exit(1)});
