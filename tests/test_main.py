from unittest import TestCase
from subprocess import Popen
from time import sleep

import requests
import json


class ResponseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__proc = Popen(('gunicorn', 'main:app'))
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.__proc.terminate()

    def test_invalid_HTTP_requests(self):
        # GET method not allowed.
        result = requests.get('http://localhost:8000')
        self.assertEqual(result.status_code, 405)
        # PUT method not allowed.
        result = requests.put('http://localhost:8000')
        self.assertEqual(result.status_code, 405)
        # DELETE method not allowed.
        result = requests.delete('http://localhost:8000')
        self.assertEqual(result.status_code, 405)

    def postJson(self, json_data):
        return requests.post('http://localhost:8000', data=json.dumps(json_data)).json()

    def test_frame_calculate(self):
        result = self.postJson({
            'jsonrpc': '2.0',
            'id': '249teg25e',
            'method': 'frame_calculate',
            'params': {
                'model': {
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
