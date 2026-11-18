'use strict';
const form = document.querySelector('#form');
const button = document.querySelector('#submit');
const status = document.querySelector('#status');
const result = document.querySelector('#result');
let revision = 0;
let controller = null;
function snapshot() { const raw=Object.fromEntries(new FormData(form)); if(Object.hasOwn(raw,'bedrooms_per_unit')) { raw.program={bedrooms_per_unit:Number(raw.bedrooms_per_unit)}; delete raw.bedrooms_per_unit; } return raw; }
function clear() { result.textContent = ''; result.hidden = true; }
function invalidate() {
  revision += 1;
  if (controller) controller.abort();
  controller = null;
  button.disabled = false;
  clear();
  status.textContent = 'ورودی تغییر کرد؛ نتیجه قبلی کنار گذاشته شد.';
}
form.addEventListener('input', invalidate);
window.addEventListener('popstate', invalidate);
window.addEventListener('pageshow', event => { if (event.persisted) invalidate(); });
async function sha256(text) {
  return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text))), b=>b.toString(16).padStart(2,'0')).join('');
}
function latin(value) {
  return value.trim().replace(/[۰-۹٠-٩٫]/g,c=>c==='٫'?'.':String('۰۱۲۳۴۵۶۷۸۹'.includes(c)?'۰۱۲۳۴۵۶۷۸۹'.indexOf(c):'٠١٢٣٤٥٦٧٨٩'.indexOf(c)));
}
function exact(value) {
  const normalized=latin(value);
  if(!/^[0-9]+(?:\.[0-9]+)?$/.test(normalized) || normalized.length>64) throw Error('INVALID_CANONICAL_SOURCE');
  const parts=normalized.split('.');let n=BigInt(parts.join('')),d=10n**BigInt((parts[1]||'').length);
  let a=n,b=d;while(b){const t=a%b;a=b;b=t;}
  return {numerator:String(n/a),denominator:String(d/a)};
}
function stable(value) {
  if(Array.isArray(value)) return '['+value.map(stable).join(',')+']';
  if(value && typeof value==='object' && !Array.isArray(value)) return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+stable(value[k])).join(',')+'}';
  return JSON.stringify(value);
}
function canonical(raw) {
  const value={dimensions_m:{W:exact(String(raw.W)),L:exact(String(raw.L))},unit_count:Number(latin(String(raw.n))),requested_count:Number(latin(String(raw.requested_count))),program_present:Object.hasOwn(raw,'program')};
  if(!Number.isSafeInteger(value.unit_count)||!Number.isSafeInteger(value.requested_count)||value.unit_count<1||value.requested_count<1)throw Error('UNSAFE_UI_COUNT');
  if(value.program_present)value.program=raw.program;
  return value;
}
function validUiRequest(raw) {
  if(!raw||!['L,W,n,requested_count','L,W,n,program,requested_count'].includes(Object.keys(raw).sort().join(',')))return false;
  return !Object.hasOwn(raw,'program') || (raw.program && Object.keys(raw.program).join(',')==='bedrooms_per_unit' && [2,3].includes(raw.program.bedrooms_per_unit));
}
function sameRaw(a,b) {
  return validUiRequest(a) && stable(a)===stable(b);
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (button.disabled) return;
  const current = ++revision;
  const raw = snapshot();
  const body = JSON.stringify(raw);
  const active = new AbortController();
  controller = active;
  button.disabled = true;
  clear();
  status.textContent = 'در حال بررسی ورودی…';
  const fresh = () => current===revision && JSON.stringify(snapshot())===body;
  try {
    const response = await fetch('/validate',{method:'POST',headers:{'Content-Type':'application/json'},body,signal:active.signal});
    const data = await response.json();
    if (!fresh()) return;
    if (data.schema!=='PLANHA_MAC_DIMENSION_VALIDATION_V1' || data.accepted!==false || data.delivery_allowed!==false) throw Error('INVALID_RESPONSE_CONTRACT');
    if (data.envelope) {
      const envelope = data.envelope;
      if (response.status!==409 || data.code!=='UNSUPPORTED_CURRENT_IMPLEMENTATION' || !sameRaw(envelope.received_input,raw) || envelope.transport_body_sha256!==await sha256(body) || envelope.accepted!==false || envelope.delivery_allowed!==false) throw Error('REQUEST_IDENTITY_MISMATCH');
      const expected=canonical(raw);
      if(stable(envelope.canonical_request)!==stable(expected) || envelope.canonical_request_digest!==await sha256(stable(expected)) || envelope.received_digest!==await sha256(stable(raw))) throw Error('CANONICAL_IDENTITY_MISMATCH');
      if (!fresh()) return;
    }
    if (response.status===422 && data.outcome==='INVALID_INPUT') status.textContent=data.code==='DIMENSION_OUT_OF_OWNER_RANGE'?'عرض و طول باید هرکدام از ۵ تا ۲۵ متر باشند؛ بزرگ‌تر از ۲۵ متر پذیرفته نمی‌شود.':'ورودی نامعتبر است؛ مقدارها و فیلد اعلام‌شده را اصلاح کنید.';
    else if (response.status===409 && data.outcome==='UNSUPPORTED') status.textContent=data.envelope?'ورودی معتبر است، اما تولید برای این درخواست هنوز پشتیبانی نمی‌شود. هیچ پلانی تولید نشده است.':'این شکل ورودی فعلاً پشتیبانی نمی‌شود؛ این پیام به معنی ناممکن بودن زمین نیست.';
    else throw Error('UNEXPECTED_RESPONSE');
    result.textContent=JSON.stringify(data,null,2);result.hidden=false;
  } catch(error) {
    if (!fresh() || error.name==='AbortError') return;
    clear();status.textContent='بررسی کامل نشد یا هویت پاسخ نامعتبر بود؛ نتیجه‌ای پذیرفته نشد.';
  } finally {
    if (fresh()) { button.disabled=false;controller=null; }
  }
});

/* Preserve JSON numeric lexemes for Python source receipts (e.g. 7.0 vs 7).
   This is server-receipt consistency, not an authenticity signature or acceptance.
   Lexemes preserve transport; parsed JS numbers can still round large integers.
   Meaningful unit/count fields are independently restricted to safe integers. */
function readExactWire(text) {
  let i=0; const numbers=new Map();
  const ws=()=>{while(/\s/.test(text[i]||'')&&i<text.length)i++;};
  function stringToken(){const start=i++;while(i<text.length){const c=text[i++];if(c==='\\'){i++;continue;}if(c==='"')return JSON.parse(text.slice(start,i));}throw Error('INVALID_JSON_WIRE');}
  function visit(path){ws();const c=text[i];
    if(c==='{'){i++;ws();const seen=new Set();if(text[i]==='}'){i++;return;}while(true){ws();if(text[i]!=='"')throw Error('INVALID_JSON_WIRE');const key=stringToken();if(seen.has(key))throw Error('DUPLICATE_JSON_WIRE_KEY');seen.add(key);ws();if(text[i++]!==':')throw Error('INVALID_JSON_WIRE');visit([...path,key]);ws();const end=text[i++];if(end==='}')return;if(end!==',')throw Error('INVALID_JSON_WIRE');}}
    if(c==='['){i++;ws();if(text[i]===']'){i++;return;}let index=0;while(true){visit([...path,index++]);ws();const end=text[i++];if(end===']')return;if(end!==',')throw Error('INVALID_JSON_WIRE');}}
    if(c==='"'){stringToken();return;}
    for(const token of ['true','false','null'])if(text.startsWith(token,i)){i+=token.length;return;}
    const match=/^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/.exec(text.slice(i));
    if(!match)throw Error('INVALID_JSON_WIRE');numbers.set(JSON.stringify(path),match[0]);i+=match[0].length;
  }
  visit([]);ws();if(i!==text.length)throw Error('INVALID_JSON_WIRE');
  return {data:JSON.parse(text),numbers};
}
function exactWireCanonical(value,numbers,path=[]) {
  if(typeof value==='number'){if(numbers===null||numbers===undefined)return JSON.stringify(value);const raw=numbers.get(JSON.stringify(path));if(raw===undefined||!Object.is(Number(raw),value))throw Error('NUMBER_WIRE_BINDING');return raw;}
  if(Array.isArray(value))return '['+value.map((v,i)=>exactWireCanonical(v,numbers,[...path,i])).join(',')+']';
  if(value&&typeof value==='object')return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+exactWireCanonical(value[k],numbers,[...path,k])).join(',')+'}';
  return JSON.stringify(value);
}
