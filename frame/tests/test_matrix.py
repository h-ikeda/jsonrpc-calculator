from unittest import TestCase
import numpy as np
from frame import matrix


class MatrixTests(TestCase):
    def test_localToGlobalTransformer(self):
        a = matrix.localToGlobalTransformer([0,0,2.85])
        self.assertTrue(np.allclose(a, ((1,0,0)*2,(0,1,0)*2,(0,0,1)*2)*2))
        a = matrix.localToGlobalTransformer([0,0,-1.2])
        self.assertTrue(np.allclose(a, ((1,0,0)*2,(0,-1,0)*2,(0,0,-1)*2)*2))
        a = matrix.localToGlobalTransformer([4,0,3])
        self.assertTrue(np.allclose(a, ((0,-3./5,4./5)*2,(1,0,0)*2,(0,4./5,3./5)*2)*2))
        a = matrix.localToGlobalTransformer([0,-4,-3])
        self.assertTrue(np.allclose(a, ((1,0,0)*2,(0,-3./5,-4./5)*2,(0,4./5,-3./5)*2)*2))
