"""Independent real archived records, not replacements for missing legacy fixtures."""
import hashlib,json,tarfile,tempfile
from pathlib import Path
from run_history import summary,list_history,output_gate
PIN={"run_id":44417514104,"path":"V25_run_44417514104.tar.gz","size":1134264,"sha256":"3c227801016f42c1d7dd0d7354ba64f2363c320fd56482c7acc245f6963fed90","members":[{"path":"evidence/requests/3ae91ee0-edc0-4077-a81c-b85c2f4d842a/lifecycle.json","size":74,"sha256":"f2d29a27a7a09bf4450ae8eab7a5e4e0d7893bb69e5d0c98816d57fe188b3e2d"},{"path":"evidence/requests/3ae91ee0-edc0-4077-a81c-b85c2f4d842a/request.json","size":89,"sha256":"a3d9087ee951678cec3d193121953f01b546a4ead84ee27f4c997fb99f201bb9"},{"path":"evidence/requests/3ae91ee0-edc0-4077-a81c-b85c2f4d842a/result.json","size":1734605,"sha256":"3655b7cefda402b23eade7d19fe37a5328ae153eb11db8fc566e062e765a2079"},{"path":"evidence/requests/3ae91ee0-edc0-4077-a81c-b85c2f4d842a/stderr.txt","size":0,"sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},{"path":"evidence/requests/4ac2d52f-e014-4c02-80d7-89f033ab93aa/exploratory_evidence.json","size":2400249,"sha256":"4db29049bf9d88fad455245da8d42c269c8f5f305c0b4a63f4fe42e699ee7b77"},{"path":"evidence/requests/4ac2d52f-e014-4c02-80d7-89f033ab93aa/lifecycle.json","size":74,"sha256":"cf6816d6b6f875c092526a526b5e81ff448d3e7f41161f35c87f80257c9da628"},{"path":"evidence/requests/4ac2d52f-e014-4c02-80d7-89f033ab93aa/request.json","size":89,"sha256":"a3d9087ee951678cec3d193121953f01b546a4ead84ee27f4c997fb99f201bb9"},{"path":"evidence/requests/4ac2d52f-e014-4c02-80d7-89f033ab93aa/result.json","size":1735295,"sha256":"e8f145ff7ee1b2ab8687353c90e745809cf08f7891824d693bdbddeeba7cfe08"},{"path":"evidence/requests/4ac2d52f-e014-4c02-80d7-89f033ab93aa/stderr.txt","size":0,"sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},{"path":"evidence/requests/74157a4c-fa28-441c-a56b-38c716fd2a6c/lifecycle.json","size":74,"sha256":"bc78ecfafb5097112a5eadaa617ec6cc494e8a07063e67583d6b89c7b8e31fe1"},{"path":"evidence/requests/74157a4c-fa28-441c-a56b-38c716fd2a6c/request.json","size":45,"sha256":"dc7bec45a5812ad0b6e16328829c8b903722d5befaddd915561b2e21581bf5cb"},{"path":"evidence/requests/74157a4c-fa28-441c-a56b-38c716fd2a6c/result.json","size":4300167,"sha256":"cbd6d1bee274bcbf18e6c24fd7df477af910241a268e3a8943799dd6a3af110d"},{"path":"pair-http.json","size":1736198,"sha256":"9d9b6fae6f3b9037c9528b0f73f319a1b5c2028d4ae9b01d87c967b9d7986e75"}]}

def run(root):
    archive=root/'evidence/archive'/PIN['path']
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==PIN['sha256']
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp)/'evidence/requests'
        with tarfile.open(archive,'r:gz') as tar:
            members={m.name:m for m in tar.getmembers()}
            for expected in PIN['members']:
                name=expected['path'];member=members[name]
                assert member.isfile()
                data=tar.extractfile(member).read()
                assert len(data)==expected['size'] and hashlib.sha256(data).hexdigest()==expected['sha256']
                if name.startswith('evidence/requests/'):
                    dest=Path(tmp)/name
                    assert dest.resolve().is_relative_to(Path(tmp).resolve())
                    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        before={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in base.rglob('*') if p.is_file()}
        rows=[]
        for folder in sorted(base.iterdir()):
            result=json.loads((folder/'result.json').read_text());record=summary(folder.name,base)
            assert record['outcome']==result['outcome']
            assert record['generated_count']==result['generated_count']
            assert record['reviewed_candidate_count']==len(result['candidates'])
            assert record['qualified_count']==0 and record['accepted'] is False and record['delivery_allowed'] is False
            assert record['live_model_restored'] is False
            assert record['status_taxonomy']['global_infeasibility_proven'] is False
            assert record['status_taxonomy']['primary'] in ('UNKNOWN','REJECTED','MULTIPLE')
            if result.get('scope')=='EXPLORATORY_ONLY_NOT_PRODUCTION_REPAIR':
                created=result['candidates'][0]['exploratory_redirection_receipt']['child_created']
                assert record['generated_count']==int(created) and result['reused_parent'] is (not created)
            status,denied=output_gate(folder.name,base)
            assert status==403 and denied['artifact_bytes_sent']==0 and denied['delivery_allowed'] is False
            rows.append({'run_id':folder.name,'generated_count':record['generated_count'],'reviewed_candidate_count':record['reviewed_candidate_count'],'taxonomy':record['status_taxonomy'],'states':[c['state'] for c in record['candidates']]})
        listed=list_history(base)
        assert len(rows)==3 and len(listed['records'])==3 and listed['omitted_unverifiable_or_legacy']==0
        after={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in base.rglob('*') if p.is_file()}
        assert before==after
    return {'passed':True,'archive_run':44417514104,'archive_sha256':PIN['sha256'],'records':rows,'immutable':True,'scope':'Previously generated real archived records through current history consistency gates; no fresh geometry or qualification. Separate from unavailable legacy fixtures.'}
