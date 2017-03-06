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
from . import line
from . import model


def frame_calculate(frameModel):
    inputModel = model.Model(frameModel, allow_overwrite=True)
    K = np.zeros((inputModel.effective_count(), ) * 2)
    for key, tline in inputModel.lines.items():
        n = (tline['n1'], tline['n2'])
        v = inputModel.line_vector(key)
        E = tline['EA']
        G = 0
        A = 1
        for i, Ki in enumerate(line.stiffnessGlobal(v[0], v[1], v[2], E, G, A)):
            for k1, d1 in enumerate(model.coodinates):
                for k2, d2 in enumerate(model.coodinates):
                    a = inputModel.effective_indexof(n[i // 2], d1)
                    b = inputModel.effective_indexof(n[i % 2], d2)
                    if a >= 0 and b >= 0:
                        K[a][b] += Ki[k1][k2]
    P = np.zeros(inputModel.effective_count())
    for node_load in inputModel.nodeLoads.values():
        for d in model.coodinates:
            i = inputModel.effective_indexof(node_load['node'], d)
            if i >= 0:
                P[i] += node_load[d]
    D = solve(K, P, overwrite_a=True, overwrite_b=True)
    R = {}
    for node_id, coodinate in inputModel.effective_coodinates():
        if node_id in R:
            R[node_id][coodinate] = D[inputModel.effective_indexof(node_id, coodinate)]
        else:
            R[node_id] = {coodinate: D[inputModel.effective_indexof(node_id, coodinate)]}
    return {'displacements': R}
