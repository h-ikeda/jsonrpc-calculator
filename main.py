from jsonrpc import JSONRPCResponseManager, dispatcher
from frame import frame_calculate

dispatcher['frame_calculate'] = frame_calculate


def app(environ, start_response):
    if 'POST' != environ.get('REQUEST_METHOD'):
        if 'OPTIONS' == environ.get('REQUEST_METHOD'):
            start_response('200 OK', [
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'POST')])
            yield b''
        elif environ.get('REQUEST_METHOD') in {'GET', 'PUT', 'DELETE', 'HEAD', 'CONNECT', 'TRACE', 'LINK', 'UNLINK', 'PATCH'}:
            start_response('405 Method Not Allowed', [])
            yield b''
        else:
            start_response('400 Bad Request', [])
            yield b''
    else:
        j = JSONRPCResponseManager.handle(environ['wsgi.input'].read().decode(), dispatcher)
        if j:
            start_response('200 OK', [('Access-Control-Allow-Origin', '*')])
            yield j.json.encode()
        else:
            start_response('204 No Content', [('Access-Control-Allow-Origin', '*')])
            yield b''
