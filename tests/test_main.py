# coding: UTF-8

from unittest import TestCase
from multiprocessing import Process
from waitress import serve
import sys
sys.path.append('..')
from main import app
from time import sleep
import requests


class ResponseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__server_process = Process(target=serve, args=(app,))
        cls.__server_process.start()
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.__server_process.terminate()

    def test_invalid_http_requests(self):
        # 不正なリクエストを送信すると、
        # HTTP status 400 (Bad Request) を返す。
        r = requests.request('GEET', 'http://127.0.0.1:8080')
        self.assertEqual(400, r.status_code)

    def test_not_allowed_http_requests(self):
        # 許可されていないHTTPメソッドを使用すると、
        # HTTP status 405 (Method Not Allowed) を返す。
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
        for method in methods_not_allowed:
            r = requests.request(method, 'http://127.0.0.1:8080')
            self.assertEqual(405, r.status_code)

    def test_options_request(self):
        # OPTIONSメソッドでアクセス
        r = requests.options('http://127.0.0.1:8080')
        expected = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST'
        }
        for name, value in expected.items():
            self.assertTrue(name in r.headers)
            self.assertEqual(value, r.headers[name])

    def test_frame_calculate(self):
        result = requests.post('http://127.0.0.1:8080', json={
            'jsonrpc': '2.0',
            'id': '249teg25e',
            'method': 'frame.calculate',
            'params': {
                'model': {
                    'nodes': {
                        'a': {'x': 0, 'y': 0, 'z': 0},
                        'b': {'x': 0, 'y': 0, 'z': 1}
                    },
                    'lines': {
                        'c': {'n1': 'a', 'n2': 'b', 'section': 'g', 'material': 'h'}
                    },
                    'sections': {
                        'g': {'shape':'H', 'H': 1, 'B': 1.5, 'tw': 0.5, 'tf': 0.25}
                    },
                    'materials': {
                        'h': {'E': 1, 'G': 1}
                    },
                    'boundaries': {
                        'd': {'node': 'a', 'x': True, 'y': True, 'z': True, 'rx': True, 'ry': True, 'rz': True},
                        'e': {'node': 'b', 'x': True, 'y': True, 'z': 0, 'rx': True, 'ry': True, 'rz': True}
                    },
                    'nodeloads': {
                        'f': {'node': 'b', 'x': 0, 'y': 1, 'z': 1, 'rx': 0, 'ry': 0, 'rz': -1}
                    }
                }
            }
        }).json()
        expected = {
            'jsonrpc': '2.0',
            'id': '249teg25e',
            'result': {
                'displacements': {
                    'b': {
                        'z': 1
                    }
                }
            }
        }
        self.assertEqual(result, expected)
