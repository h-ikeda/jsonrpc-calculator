# coding: UTF-8

from unittest import TestCase
from multiprocessing import Process
from waitress import serve
import sys
sys.path.append('..')
from main import app
from time import sleep
from urllib2 import Request, urlopen, HTTPError
import json


class ResponseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__server_process = Process(target=serve, args=(app,))
        cls.__server_process.start()
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.__server_process.terminate()
        
    def test_invalid_HTTP_requests(self):
        # 不正なリクエストを送信すると、
        # HTTP status 400 (Bad Request) を返す。
        req = Request('http://127.0.0.1:8080')
        req.get_method = lambda: 'GEET'
        with self.assertRaises(HTTPError) as cm:
            urlopen(req)
        self.assertEqual(400, cm.exception.code)

    def test_not_allowed_HTTP_requests(self):
        # 許可されていないHTTPメソッドを使用すると、
        # HTTP status 405 (Method Not Allowed) を返す。
        req = Request('http://127.0.0.1:8080')
        req.get_method = lambda: method
        methods_not_allowed = (
            'GET',
            'PUT',
            'DELETE',
            'HEAD',
            'CONNECT',
            'TRACE',
            'LINK',
            'UNLINK',
            'PATCH'
        )
        for m in methods_not_allowed:
            method = m
            with self.assertRaises(HTTPError) as cm:
                urlopen(req)
            self.assertEqual(405, cm.exception.code)
    
    def test_OPTIONS_request(self):
        # OPTIONSメソッドでアクセス
        req = Request('http://127.0.0.1:8080')
        req.get_method = lambda: 'OPTIONS'
        handle = urlopen(req)
        headers = handle.info()
        testheaders = (
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST')
        )
        for n, v in testheaders:
            self.assertEqual(v, headers.getheader(n))

    @classmethod
    def postJson(cls, json_data):
        req = Request('http://127.0.0.1:8080', json.dumps(json_data))
        handle = urlopen(req)
        return json.loads(handle.read())

    def test_frame_calculate(self):
        result = self.postJson({
            'jsonrpc': '2.0',
            'id': '249teg25e',
            'method': 'frame_calculate',
            'params': {
                'frameModel': {
                    'nodes': [
                        {'recid': 0, 'x': 0, 'y': 0, 'z': 0},
                        {'recid': 1, 'x': 0, 'y': 0, 'z': 1}
                    ],
                    'lines': [
                        {'recid': 0, 'n1': 0, 'n2': 1, 'EA': 1}
                    ],
                    'boundaries': [
                        {'recid': 0, 'node': 0, 'x': True, 'y': True, 'z': True, 'rx': True, 'ry': True, 'rz': True},
                        {'recid': 1, 'node': 1, 'x': True, 'y': True, 'z': 0, 'rx': True, 'ry': True, 'rz': True}
                    ],
                    'nodeLoads': [
                        {'recid': 0, 'node': 1, 'x': 0, 'y': 1, 'z': 1, 'rx': 0, 'ry': 0, 'rz': -1}
                    ]
                }
            }
        })
        expected = {
            'jsonrpc': '2.0',
            'id': '249teg25e',
            'result': {
                'displacements': {
                    '1': {
                        'z': 1
                    }
                }
            }
        }
        self.assertEqual(result, expected)
