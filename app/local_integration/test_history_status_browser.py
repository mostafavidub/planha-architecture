"""Actual Chromium history UI with controlled saved records; no geometry."""
import json,tempfile,threading
from pathlib import Path
from unittest.mock import patch
from http.server import HTTPServer
from playwright.sync_api import sync_playwright,expect
from validation_server import Handler
import run_history as history
from test_history_status_taxonomy import completed,write_record

def run():
    with tempfile.TemporaryDirectory()as tmp:
        base=Path(tmp);fixtures={}
        for label,states in [('NO_PROPOSAL',['NO_PROPOSAL_IN_THIS_TOPOLOGY']),('TIMEOUT',['TIMEOUT_NO_WITNESS']),
            ('UNSUPPORTED',['UNSUPPORTED_BUNDLE_FIT']),('MULTIPLE',['EXECUTION_ERROR','TIMEOUT_NO_WITNESS'])]:
            rid=write_record(base,completed(states));fixtures[label]=(rid,states)
        original_summary=history.summary;original_list=history.list_history
        def summary(rid,base=None):return original_summary(rid,Path(tmp)if base is None else base)
        with patch.object(history,'summary',summary),patch.object(history,'list_history',lambda:original_list(Path(tmp))):
            server=HTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,kwargs={'poll_interval':.05},daemon=True);thread.start()
            try:
                with sync_playwright()as p:
                    browser=p.chromium.launch();context=browser.new_context();page=context.new_page();errors=[]
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    try:
                        page.goto('http://127.0.0.1:'+str(server.server_port))
                        expect(page.locator('#history-list button')).to_have_count(4)
                        initial=[page.locator('input[name="'+n+'"]').input_value()for n in ['W','L','n','requested_count']]
                        for label,(rid,states)in fixtures.items():
                            button=page.locator('#history-list button').filter(has_text=rid).first
                            expect(button).to_be_visible()
                            for state in states:expect(button.locator('..')).to_contain_text(state)
                            button.click()
                            expect(page.locator('#history-detail')).to_contain_text('سابقه ذخیره‌شده')
                            for state in states:expect(page.locator('#history-detail')).to_contain_text(state)
                            expect(page.locator('#history-detail')).to_contain_text(label)
                            expect(page.locator('#plans')).to_be_empty()
                            assert initial==[page.locator('input[name="'+n+'"]').input_value()for n in ['W','L','n','requested_count']]
                        page.locator('#history-refresh').click();expect(page.locator('#history-list button')).to_have_count(4)
                        assert not errors,errors
                        page.screenshot(path='history-status-browser.png',full_page=True)
                        return {'schema':'V25_CONTROLLED_HISTORY_BROWSER_V1','passed':True,'browser_version':browser.version,
                            'cases':list(fixtures),'no_live_model_restore':True,'form_unchanged':True,'browser_errors':errors,
                            'scope':'Actual Chromium and unchanged HTTP Handler reading synthetic saved zero-candidate records through current summary. No geometry execution or positive qualification proof.'}
                    finally:context.close();browser.close()
            finally:server.shutdown();server.server_close();thread.join(5);assert not thread.is_alive()
if __name__=='__main__':
    report=run();Path('history-status-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('HISTORY_BROWSER '+json.dumps(report,ensure_ascii=False))
