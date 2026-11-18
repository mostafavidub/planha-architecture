'use strict';
const form = document.querySelector('#form');
const button = document.querySelector('#submit');
const status = document.querySelector('#status');
const result = document.querySelector('#result');
let revision = 0;
let controller = null;
function snapshot() { return Object.fromEntries(new FormData(form)); }
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
  return {dimensions_m:{W:exact(raw.W),L:exact(raw.L)},unit_count:Number(latin(raw.n)),requested_count:Number(latin(raw.requested_count)),program_present:false};
}
function sameRaw(a,b) {
  return a && Object.keys(a).length===4 && ['W','L','n','requested_count'].every(k=>a[k]===b[k]);
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
