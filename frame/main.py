#
# model is dictionary includes:
#
#     nodes : An array of { recid:Int, x:Real, y:Real, z:Real}
#     lines : An array of { recid:Int, n1:Int, n2:Int, EA:Real}
#     boundaries : An array of { recid:Int, node:Int, x:Real or Bool, y:Real or Bool, z:Real or Bool, rx:Real or Bool, ry:Real or Bool, rz:Real or Bool}
#     nodeLoads : An array of { recid:Int, node:Int, x:Real, y:Real, z:Real, rx:Real, ry:Real, rz:Real}
#

import numpy as np
from scipy.linalg import solve
from . import matrix

directions = ('x', 'y', 'z', 'rx', 'ry', 'rz')


def effectiveCoodinates(nodes, boundaries):
    t = {b['node']: {d for d in directions if isinstance(b[d], bool) and b[d]} for b in boundaries}
    return tuple((n['recid'], d) for n in nodes for d in directions if n['recid'] not in t or d not in t[n['recid']])


def itemById(items, recid):
    for item in items:
        if item['recid'] == recid:
            return item

transformMatrixLocalToGlobal = matrix.localToGlobalTransformer

lineStiffnessGlobal = matrix.lineStiffnessGlobal


def frame_calculate(model):
    indexList = effectiveCoodinates(model['nodes'], model['boundaries'])
    K = np.zeros((len(indexList), )*2)
    for line in model['lines']:
        n = (itemById(model['nodes'], line['n1']), itemById(model['nodes'], line['n2']))
        v = (n[1]['x']-n[0]['x'], n[1]['y']-n[0]['y'], n[1]['z']-n[0]['z'])
        EA = line['EA']
        for i, Ki in enumerate(lineStiffnessGlobal(v, EA)):
            for j, Kij in enumerate(Ki):
                for k1, d1 in enumerate(directions):
                    for k2, d2 in enumerate(directions):
                        try:
                            a = indexList.index((n[i]['recid'], d1))
                            b = indexList.index((n[j]['recid'], d2))
                        except ValueError:
                            continue
                        K[a][b] += Kij[k1][k2]
    P = np.zeros(len(indexList))
    for nodeLoad in model['nodeLoads']:
        for d in directions:
            try:
                i = indexList.index((nodeLoad['node'], d))
            except ValueError:
                continue
            P[i] -= nodeLoad[d]
    D = solve(K, P)
    R = {}
    for i, d in zip(indexList, D):
        if i[0] not in R:
            R[i[0]] = {i[1]: d}
        else:
            R[i[0]][i[1]] = d
    return {'displacements': R}
