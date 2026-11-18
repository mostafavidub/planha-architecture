"""Trusted reducer for independently computed physics reports, not a validator.
Only the explicit non-Concept spatial-quality unknown is reclassified.
Lighting/ventilation checks are not run in MVP121, per latest owner scope. No door,
route, privacy, program-inventory or geometric failure is suppressed.
The source document/hash is attached and verified by the calling checker.
"""
from copy import deepcopy
SCOPE='CONCEPT117_SOURCE_COMPAT_V1'
EXCLUDED={
 'VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED':{
  'reason':'Overall program adequacy, spatial quality and global optimality remain for review. Required actual room/fixture inventory, use areas, circulation, privacy and independent functional witnesses are not excluded.',
  'label_fa':'تناسب کلی برنامه فضایی، کیفیت چیدمان و بهینه‌بودن تأیید نشده؛ موجودی فضا/اثاث و کارکردهای الزامی همچنان کنترل می‌شوند.'}}

def reduce_scope117(report):
 if not isinstance(report,dict) or not str(report.get('checker_version','')).startswith('GENERAL117_'):
  raise ValueError('CONCEPT117_REQUIRES_OWN_TRUSTED_CHECKER_REPORT')
 if not isinstance(report.get('errors'),list)or not isinstance(report.get('pending'),list)or any(not isinstance(p,str)for p in report['pending']):
  raise ValueError('CONCEPT117_REPORT_SCHEMA')
 out=deepcopy(report);original=list(report['pending']);moved=sorted(set(original)&set(EXCLUDED));remaining=sorted(set(original)-set(EXCLUDED))
 out['physics_status_before_scope']=report.get('status');out['original_pending']=original
 out['pending']=remaining;out['gate_scope']=SCOPE;out['pending_scope']='Mandatory limited-Concept controls only; other unknowns are retained separately, never marked PASS.'
 out['not_evaluated']=sorted(set(report.get('not_evaluated',[]))|set(moved))
 out['out_of_scope']=list(report.get('out_of_scope',[]))+[dict(code=k,status='NOT_EVALUATED',**EXCLUDED[k])for k in moved]
 ready=not out['errors']and not remaining
 out['status']='FAIL'if out['errors']else'NOT_EVALUATED'if remaining else'PASS_CONCEPT_SCOPED_REVIEW'
 out['eligible_for_draft_export']=ready;out['draft_review_allowed']=ready
 out.update(accepted=False,release=False,technical_accepted=False,public_release=False)
 out['limitations']=['پیش‌نویس برای بررسی کانسپت است، نه نقشه اجرایی، تأیید فنی یا پذیرش نهایی مالک.','هیچ تضمین پوشش همه ابعاد، شش گزینه، بهترین چیدمان یا کیفیت کلی از این نتیجه استنباط نمی‌شود.']+[EXCLUDED[k]['label_fa']for k in moved]
 return out
