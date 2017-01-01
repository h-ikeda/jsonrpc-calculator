from jsonrpc import dispatcher as d

import numpy as np
import scipy as sp
from numpy import linalg
from scipy import linalg

from functools import reduce

@d.add_method
def dot(*a, **k):
    alist = sorted(k)
    a = list(a)
    a.extend(map(lambda key: k[key], alist))
    return reduce(np.dot, a).tolist()

@d.add_method
def solve(*a, **k):
    return sp.linalg.solve(*a, **k).tolist()
