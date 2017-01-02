import unittest
import json
import numpy as np
from jsonrpc import dispatcher as d
import frame
import funcs

class FrameTests(unittest.TestCase):
    def test_effectiveCoodinates(self):
        nodes = [{'recid':0,'x':-5.4,'y':3.2,'z':4.2},{'recid':1,'x':0,'y':-3.2,'z':1.5},{'recid':3,'x':-2.4,'y':-3.8,'z':9.9}]
        boundaries = [{'recid':0,'node':1,'x':100,'y':0,'z':False,'rx':-15,'ry':True,'rz':False},{'recid':2,'node':0,'x':0,'y':0,'z':True,'rx':False,'ry':False,'rz':1}]
        a = frame.effectiveCoodinates(nodes, boundaries)
        self.assertEqual(a, ((0,'x'),(0,'y'),(0,'rx'),(0,'ry'),(0,'rz'),(1,'x'),(1,'y'),(1,'z'),(1,'rx'),(1,'rz'),(3,'x'),(3,'y'),(3,'z'),(3,'rx'),(3,'ry'),(3,'rz')))

    def test_itemById(self):
        items = [{'recid':1,'data':True},{'recid':31,'data':24.8},{'recid':11,'data':12.8},{'recid':44,'data':'string'}]
        a = frame.itemById(items, 11)
        self.assertEqual(a, {'recid':11,'data':12.8})
        
    def test_transformMatrixLocalToGlobal(self):
        a = frame.transformMatrixLocalToGlobal([0,0,2.85])
        self.assertTrue(np.allclose(a, ((1,0,0)*2,(0,1,0)*2,(0,0,1)*2)*2))
        a = frame.transformMatrixLocalToGlobal([0,0,-1.2])
        self.assertTrue(np.allclose(a, ((1,0,0)*2,(0,-1,0)*2,(0,0,-1)*2)*2))
        a = frame.transformMatrixLocalToGlobal([4,0,3])
        self.assertTrue(np.allclose(a, ((0,-3./5,4./5)*2,(1,0,0)*2,(0,4./5,3./5)*2)*2))
        a = frame.transformMatrixLocalToGlobal([0,-4,-3])
        self.assertTrue(np.allclose(a, ((1,0,0)*2,(0,-3./5,-4./5)*2,(0,4./5,-3./5)*2)*2))
        
    def test_frame_calculate(self):
        model = {
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
        a = d['frame_calculate'](model)
        self.assertEqual(a, {'displacements':{1:{'z':1}}})

class FuncTests(unittest.TestCase):
    def test_dot_array(self):
        a = d['dot']([[1,2],[3,4]], [[1,3],[2,1]], [[2,1],[5,4]])
        self.assertEqual(a, [[35,25],[87,63]])
        #test json serializable
        self.assertEqual(json.dumps(a), json.dumps([[35,25],[87,63]]))
        
    def test_dot_dict(self):
        a = d['dot'](a=[[1,2],[3,4]], b=[[1,3],[2,1]], c=[[2,1],[5,4]])
        self.assertEqual(a, [[35,25],[87,63]])

    def test_solve_array(self):
        a = d['solve']([[1,2],[3,4]], [5,11])
        self.assertEqual(a, [1,2])
        #test json serializable
        self.assertEqual(json.loads(json.dumps(a)), json.loads(json.dumps([1,2])))
        
    def test_solve_dict(self):
        a = d['solve'](a=[[1,2],[3,4]], b=[5,11])
        self.assertEqual(a, [1,2])

if __name__ == '__main__':
    unittest.main()