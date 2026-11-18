"""Audit sidecar: author mapping, never modifies evaluator verdict/admission."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from common import digest
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'recovered233_rendered/sections.json'
def evaluate(envelope,living,guest):
 data=SOURCE.read_bytes()
 if hashlib.sha256(data).hexdigest()!='98e39063ee7ba733335c450c7fb661b9939762873f19c788d1b0764cb2daf0e3':raise ValueError('PINNED_EXTRACT_DRIFT')
 d=json.loads(data);out={'schema':'RECONSTRUCTED357_AUTHOR233_SPATIAL_MAPPING','source_html_sha256':d['source_sha256'],'extracted_sections_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'model_hash':digest(envelope['packet']['world_model']),'parent_promotion_performed':False,'rules':{}}
 if d['source_sha256']!='046cb8490a0865b74a9f844fa7db513490c50393e21923d1aa458f846fa89108':raise ValueError('AUTHOR_SOURCE_DRIFT')
 for code in ('Q02','Q06'):
  sec=d['sections'][code];out['rules'][code]={'source_selector':sec['source_selector'],'html_character_range':sec['html_character_range'],'algorithm':sec['fields']['رابطه و الگوریتم دقیق'],'acceptance':sec['fields']['شرط پذیرش محدود']}
 raw=envelope['raw'];outside=(F(raw['W']),F(raw['L'])) not in ((F('12.5'),F('20')),(F('20'),F('12.5')))
 # A shape outside the exact trigger suffices for N_A. Inside/unknown requires
 # explicit six-option applicability and overlay evidence, never defaults away.
 gate={'status':'N_A'if outside else'UNKNOWN','reason':'BOUND_RAW_DIMENSIONS_OUTSIDE_EXACT_12_5x20_TRIGGER'if outside else'REQUIRES_SOURCE_SIX_OPTION_SCOPE_AND_OVERLAY','raw':raw}
 q=out['rules']['Q02'];q.update(r_liv=gate,comparative_scope='NO_COMPARATIVE_OR_AESTHETIC_CLAIM',descriptive_max_rect='NOT_COMPUTED_NOT_HARD_ACCEPTANCE',proof_conditions=['same-fresh source bundle inventory and capacity, all seating transfer operations verified','source288 full-body swept edges inside actual ownership and outside fixed conservative source scenario obstacles','all required standing targets connected to verified source entry root; no invented graph connectors','actual role excludes kitchen/dining; no entire residual declared useful'],whole_residual_claimed=False)
 network=living.get('evidence',{}).get('network',{});netrows=network.get('rows',[])
 connected=bool(netrows)and all(r.get('verdict')=='PASS_STORED_SOURCE_ROUTE_NETWORK_SCOPED'and not r.get('unconnected_stored_targets')and not r.get('blocked_body_poses')for r in netrows)
 q['audit_recommendation']='ELIGIBLE_CURRENT_PROFILE_PARENT_CLOSURE_PENDING_INDEPENDENT_AUDIT'if living.get('verdict')=='PASS_SCOPED_INTRINSIC_LIVING'and connected and outside else'UNKNOWN_REQUIRED_PROOF_OR_APPLICABILITY'
 q=out['rules']['Q06'];rels=guest.get('evidence',{}).get('relations',[]);units=[u['id']for u in envelope['packet']['world_model']['units']];wanted={(u,r)for u in units for r in('entry_living','entry_dining','entry_WC','living_dining')}
 q.update(proof_conditions=['same fresh source door/bath/kitchen/fixture/role prerequisite checks','independent actual source living, dining standing-body and WC targets','all four source-body swept relations per unit inside ownership','full bedroom/private vestibule union excluded','current source kitchen full leaf/actor/hand/object and drawer envelopes conservatively excluded','open-transit door state supported by separate same-fresh operation proof; no unsupported all-door simultaneous closure requirement'],separate_rule_not_claimed='H07_BATH_PRIVATE_DELETION',scenario_scope='CURRENT_REFERENCE113_SOURCE_PROFILE_NOT_ALL_POSSIBLE_PROFILES')
 q['audit_recommendation']='ELIGIBLE_CURRENT_PROFILE_PARENT_CLOSURE_PENDING_INDEPENDENT_AUDIT'if guest.get('verdict')=='PASS_SCOPED_FOUR_SOURCE_GUEST_RELATIONS'and len(rels)==len(wanted)and {(r['unit'],r['relation'])for r in rels}==wanted and all(r['verdict']=='PASS_SOURCE_CONSERVATIVE_PATH'and not r['collisions']for r in rels)else'UNKNOWN_REQUIRED_PROOF'
 return out
if __name__=='__main__':
 from living_closure import evaluate as lv
 from guest_closure import evaluate as gv
 root=Path(__file__).resolve().parents[1];r=json.loads((root/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0];args=[r[k]for k in('central_envelope','central_fresh_review','source_groups285')];o=evaluate(args[0],lv(*args),gv(*args));Path(__file__).with_name('author233_spatial_actual357.json').write_text(json.dumps(o,ensure_ascii=False,indent=2));print({k:v['audit_recommendation']for k,v in o['rules'].items()})
