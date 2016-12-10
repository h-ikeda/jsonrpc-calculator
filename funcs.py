from jsonrpc import dispatcher as d

import numpy as np
import scipy as sp
from scipy import linalg

@d.add_method
def inv(*a, **k):
    return sp.linalg.inv(*a, **k).tolist()

@d.add_method
def solve(*a, **k):
    return sp.linalg.solve(*a, **k).tolist()

@d.add_method
def solve_banded(*a, **k):
    return sp.linalg.solve_banded(*a, **k).tolist()
    
@d.add_method
def solveh_banded(*a, **k):
    return sp.linalg.solveh_banded(*a, **k).tolist()

@d.add_method
def solve_circulant(*a, **k):
    return sp.linalg.solve_circulant(*a, **k).tolist()

@d.add_method
def solve_triangular(*a, **k):
    return sp.linalg.solve_triangular(*a, **k).tolist()

@d.add_method
def solve_toeplitz(*a, **k):
    for i,j in zip(a,('c', 'r', 'b', 'check_finite')):
        k[j]=i
    k['c_or_cr'] = (k.pop('c'), k.pop('r')) if 'r' in k else k.pop('c')
    k['b'] = np.array(k['b'])
    return sp.linalg.solve_toeplitz(**k).tolist()

d.add_method(sp.linalg.det, 'det')
d.add_method(sp.linalg.norm, 'norm')


