from jsonrpc import dispatcher as d

import numpy as np
from numpy.linalg import norm
from scipy.linalg import solve

directions = ('x', 'y', 'z', 'rx', 'ry', 'rz')

def effectiveCoodinates(nodes, boundaries):
    t = {b['node']:{d for d in directions if isinstance(b[d], bool) and b[d]} for b in boundaries}
    return tuple((n['recid'],d) for n in nodes for d in directions if n['recid'] not in t or d not in t[n['recid']])

def itemById(items, recid):
    for item in items:
        if item['recid'] == recid:
            return item
            
def transformMatrixLocalToGlobal(vectorZ, vectorX = None):
    if np.allclose(vectorZ[:2],(0,0)):
        t = tuple(i / t for i,t in zip(vectorX[:2], (norm(vectorX[:2]),)*2)) if vectorX is not None else (1,0)
        s = np.sign(vectorZ[2])
        return (
            (t[0], -s*t[1], 0) * 2,
            (t[1],  s*t[0], 0) * 2,
            (   0,       0, s) * 2
        ) * 2
    len = norm(vectorZ)
    plen = norm(vectorZ[:2])
    if vectorX is not None:
        z = vectoZ / norm(vectorZ)
        x = vectorX - np.dot(vectorX, z) * z
        cZ0 = (np.transpose(x[:2],(1,0)) - vectorZ[:2])/plen/norm(x)
        sZ0 = np.sqrt((1-cZ0)*(1+cZ0))
        return (
            (-vectorZ[1] / plen * cZ0 -vectorZ[0] / plen * vectorZ[2] / len * sZ0, vectorZ[1] / plen * sZ0 -vectorZ[0] / plen * vectorZ[2] / len * cZ0, vectorZ[0] / len)*2,
            (vectorZ[0] / plen * cZ0 -vectorZ[1] / plen * vectorZ[2] / len * sZ0, -vectorZ[0] / plen * sZ0 -vectorZ[1] / plen * vectorZ[2] / len * cZ0, vectorZ[1] / len)*2,
            (plen / len * sZ0, plen / len * cZ0, vectorZ[2] / len)*2
        )*2
    return (
        (-vectorZ[1] / plen, -vectorZ[0] / plen * vectorZ[2] / len, vectorZ[0] / len) * 2,
        (vectorZ[0] / plen, -vectorZ[1] / plen * vectorZ[2] / len, vectorZ[1] / len) * 2,
        (0, plen / len, vectorZ[2] / len) * 2
    ) * 2

def lineStiffnessGlobal(vector, EA):
    L = norm(vector)
    K11 = np.array((
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,-EA/L,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0)
    ))
    K12 = np.array((
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,EA/L,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0)
    ))
    K21 = np.array((
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,EA/L,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0)
    ))
    K22 = np.array((
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,-EA/L,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0)
    ))
    t = np.array(transformMatrixLocalToGlobal(vector))
    return (np.dot(np.dot(t,K11),t.T), np.dot(np.dot(t,K12),t.T)), (np.dot(np.dot(t,K21),t.T), np.dot(np.dot(t,K22),t.T))

@d.add_method
def frame_calculate(model):
    indexList = effectiveCoodinates(model['nodes'], model['boundaries'])
    K = np.zeros((len(indexList),)*2)
    for line in model['lines']:
        n = (itemById(model['nodes'],line['n1']), itemById(model['nodes'],line['n2']))
        v = (n[1]['x']-n[0]['x'],n[1]['y']-n[0]['y'],n[1]['z']-n[0]['z'])
        EA = line['EA']
        for i, Ki in enumerate(lineStiffnessGlobal(v, EA)):
            for j, Kij in enumerate(Ki):
                for k1, d1 in enumerate(directions):
                    for k2, d2 in enumerate(directions):
                        try:
                            a = indexList.index((n[i]['recid'],d1))
                            b = indexList.index((n[j]['recid'],d2))
                        except ValueError:
                            continue
                        K[a][b] += Kij[k1][k2]                            
    P = np.zeros(len(indexList))
    for nodeLoad in model['nodeLoads']:
        for d in directions:
            try:
                i = indexList.index((nodeLoad['node'],d))
            except ValueError:
                continue
            P[i] -= nodeLoad[d]
    D = solve(K,P)
    R = {}
    for i, d in zip(indexList, D):
        if i[0] not in R:
            R[i[0]] = {i[1]:d}
        else:
            R[i[0]][i[1]] = d
    return {'displacements':R}