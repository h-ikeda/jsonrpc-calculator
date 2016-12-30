import unittest
import json
from jsonrpc import dispatcher as d
import funcs

class FuncTests(unittest.TestCase):
    def test_dot_array(self):
        a = d['dot']([[1,2],[3,4]], [[1,3],[2,1]], [[2,1],[5,4]])
        self.assertEqual(a, [[35,25],[87,63]])
        #test json serializable
        self.assertEqual(json.dumps(a), json.dumps([[35,25],[87,63]]))
        
    def test_dot_dict(self):
        a = d['dot'](a=[[1,2],[3,4]], b=[[1,3],[2,1]], c=[[2,1],[5,4]])
        self.assertEqual(a, [[35,25],[87,63]])
        
    def test_inv(self):
        a = d['inv']([[1,0],[0,2]])
        self.assertEqual(a, [[1,0],[0,0.5]])
        #test json serializable
        self.assertEqual(json.loads(json.dumps(a)), json.loads(json.dumps([[1,0],[0,0.5]])))
        
    def test_solve_array(self):
        a = d['solve']([[1,2],[3,4]], [5,11])
        self.assertEqual(a, [1,2])
        #test json serializable
        self.assertEqual(json.loads(json.dumps(a)), json.loads(json.dumps([1,2])))
        
    def test_solve_dict(self):
        a = d['solve'](a=[[1,2],[3,4]], b=[5,11])
        self.assertEqual(a, [1,2])
        
    def test_matrix_rank(self):
        a = d['matrix_rank']([[1,2],[3,5]])
        self.assertEqual(a, 2)
        #test json serializable
        self.assertEqual(json.dumps(a), json.dumps(2))

if __name__ == '__main__':
    unittest.main()