"""Loopback-only validation and bounded parametric experiment. No release or delivery.

Run manually with: python3 -B validation_server.py --port 0
Prints its bound address; Ctrl-C stops it. No import-time side effects.
"""
import argparse
import json
import socket
import select
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from dimension_contract import MAX_BODY, SCHEMA, evaluate


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def setup(self):
        super().setup()
        self.connection.settimeout(3)

    def log_message(self, *args):
        pass

    def respond(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            # Input changed or browser closed: do not re-run the worker.
            self.close_connection = True

    def do_GET(self):
        assets = {'/': ('index.html', 'text/html; charset=utf-8'),
                  '/ui.js': ('ui.js', 'text/javascript; charset=utf-8'),
                  '/generation_ui.js': ('generation_ui.js', 'text/javascript; charset=utf-8'),
                  '/history_ui.js': ('history_ui.js', 'text/javascript; charset=utf-8')}
        if self.path in assets:
            filename, content_type = assets[self.path]
            data = Path(__file__).with_name(filename).read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(data)
            return
        if self.path == '/history':
            from run_history import list_history
            self.respond(200,list_history());return
        if self.path.startswith(('/history/','/export/','/download/')):
            from run_history import summary,output_gate
            kind,run_id=self.path[1:].split('/',1)
            try:
                status,payload=(200,summary(run_id)) if kind=='history' else output_gate(run_id)
            except (ValueError,KeyError,TypeError,OSError):
                status,payload=404,{'code':'VERIFIED_RECORD_NOT_FOUND','delivery_allowed':False}
            self.respond(status,payload);return
        if self.path != '/health':
            self.respond(404, {'code':'NOT_FOUND'})
            return
        self.respond(200, {'schema':SCHEMA, 'mode':'EXPERIMENTAL_PARAMETRIC',
                           'generation_enabled':True, 'accepted':False,
                           'delivery_allowed':False})

    def request_disconnected(self):
        try:
            if not select.select([self.connection],[],[],0)[0]:return False
            return self.connection.recv(1,socket.MSG_PEEK)==b''
        except OSError:return True

    def do_POST(self):
        if self.path not in ('/validate','/generate','/repair','/redesign-explicit-two'):
            self.respond(404, {'code':'NOT_FOUND'})
            return
        lengths = self.headers.get_all('Content-Length', [])
        if self.headers.get('Transfer-Encoding') is not None or len(lengths) != 1 or not lengths[0].isascii() or not lengths[0].isdigit():
            self.respond(422, {'code':'BODY_LENGTH_REQUIRED'})
            return
        if self.headers.get_content_type() != 'application/json':
            self.respond(415, {'code':'JSON_CONTENT_TYPE_REQUIRED'})
            return
        if len(lengths[0]) > 8 or int(lengths[0]) > MAX_BODY:
            self.respond(409, {'outcome':'UNSUPPORTED','code':'UNSUPPORTED_BODY_LIMIT'})
            return
        length = int(lengths[0])
        try:
            body = self.rfile.read(length)
        except TimeoutError:
            self.respond(408, {'code':'BODY_READ_TIMEOUT'})
            return
        if len(body) != length:
            self.respond(422, {'code':'BODY_LENGTH_MISMATCH'})
            return
        try:
            if self.path == '/redesign-explicit-two':
                from explicit_pair_saved_run import redirect_saved
                status, response = redirect_saved(body,cancelled=self.request_disconnected)
            elif self.path == '/repair':
                from repair_saved_run import repair
                status, response = repair(body,cancelled=self.request_disconnected)
            elif self.path == '/generate':
                from generation_gateway import generate
                status, response = generate(body,cancelled=self.request_disconnected)
            else:
                status, response = evaluate(body)
        except Exception:
            self.respond(500, {'outcome':'EXECUTION_ERROR','code':'INTERNAL_VALIDATION_ERROR',
                               'accepted':False,'delivery_allowed':False})
            return
        self.respond(status, response)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=0)
    args=parser.parse_args()
    with HTTPServer(('127.0.0.1',args.port),Handler) as server:
        print(json.dumps({'host':'127.0.0.1','port':server.server_port,'mode':'EXPERIMENTAL_PARAMETRIC'}),flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    print(json.dumps({'listener_closed':True}),flush=True)


if __name__=='__main__':main()
