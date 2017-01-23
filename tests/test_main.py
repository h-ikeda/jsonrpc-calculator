from unittest import TestCase
from os.path import dirname
from subprocess import Popen
import requests
import json

class ResponseTest(TestCase):
    
    def setUp(self):
        self.__proc = Popen(('gunicorn', 'main:app'))

    def tearDown(self):
        self.__proc.terminate()
        
    def test_frame_calculate(self):
        payload = {
            'jsonrpc':'2.0',
            'id':'249teg25e',
            'method':'frame_calculate',
            'params':{
                'model':{
                    'nodes':[
                        {'recid':0,'x':0,'y':0,'z':0},
                        {'recid':1,'x':0,'y':0,'z':1}
                    ],
                    'lines':[
                        {'recid':0,'n1':0,'n2':1,'EA':1}
                    ],
                    'boundaries':[
                        {'recid':0,'node':0,'x':True,'y':True,'z':True,'rx':True,'ry':True,'rz':True},
                        {'recid':1,'node':1,'x':True,'y':True,'z':0,'rx':True,'ry':True,'rz':True}
                    ],
                    'nodeLoads':[
                        {'recid':0,'node':1,'x':0,'y':1,'z':1,'rx':0,'ry':0,'rz':-1}
                    ]
                }
            }
        }
        response = requests.post('http://localhost:8000', data=json.dumps(payload))
        self.assertEqual(response.json(), {
            'jsonrpc':'2.0',
            'id':'249teg25e',
            'result':{
                'displacements':{'1':{'z':1}}
            }
        })