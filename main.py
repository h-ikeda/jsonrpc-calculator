from jsonrpc import JSONRPCResponseManager
from frame import d

def app(environ, start_response):
    if 'POST'!=environ.get('REQUEST_METHOD'):
        if 'OPTIONS'==environ.get('REQUEST_METHOD'):
            start_response('200 OK',[
                ('Access-Control-Allow-Origin','*'),
                ('Access-Control-Allow-Methods', 'POST'),
                ('Access-Control-Allow-Headers', 'Content-Type')])
            yield b''
        else:
            start_response('405 Method Not Allowed',[('Content-Type','text/plain')])
            yield b'405 Method Not Allowed'
    else:
        j=JSONRPCResponseManager.handle(environ['wsgi.input'].read().decode(), d)
        if j:
            start_response('200 OK',[('Content-Type','application/json'), ('Access-Control-Allow-Origin','*')])
            yield j.json.encode()
        else:
            start_response('204 No Content',[('Access-Control-Allow-Origin','*')])
            yield b''
