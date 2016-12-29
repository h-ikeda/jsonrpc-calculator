import unittest
from jsonrpc import dispatcher as d
import funcs

class FuncTests(unittest.TestCase):
    def test_dot_array(self):
        a = d['dot']([[1,2],[3,4]], [[1,3],[2,1]], [[2,1],[5,4]])
        self.assertEqual(a, [[35,25],[87,63]])
        
    def test_dot_dict(self):
        a = d['dot'](a=[[1,2],[3,4]], b=[[1,3],[2,1]], c=[[2,1],[5,4]])
        self.assertEqual(a, [[35,25],[87,63]])

if __name__ == '__main__':
    unittest.main()