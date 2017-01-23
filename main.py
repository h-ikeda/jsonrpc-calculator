from jsonrpc import JSONRPCResponseManager
from jsonrpc import dispatcher as d
from frame import frame_calculate as c

d['frame_calculate'] = c

def app(environ, start_response):
    if 'POST'!=environ.get('REQUEST_METHOD'):
        if 'OPTIONS'==environ.get('REQUEST_METHOD'):
            start_response('200 OK',[
                ('Access-Control-Allow-Origin','*'),
                ('Access-Control-Allow-Methods', 'POST')])
            yield b''
        else:
            start_response('405 Method Not Allowed',[])
            yield b''
    else:
        j=JSONRPCResponseManager.handle(environ['wsgi.input'].read().decode(), d)
        if j:
            start_response('200 OK',[('Access-Control-Allow-Origin','*')])
            yield j.json.encode()
        else:
            start_response('204 No Content',[('Access-Control-Allow-Origin','*')])
            yield b''
