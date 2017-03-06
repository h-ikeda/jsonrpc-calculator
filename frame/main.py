#
# The data structure of 'model' is below:
#
#     'nodes' : { id(hashable): { x:Real, y:Real, z:Real } }
#     'lines' : { id(hashable): { n1:id, n2:id, EA:Real } }
#     'boundaries' : { id(hashable): { node:id, x:Real or Bool, y:Real or Bool, z:Real or Bool, rx:Real or Bool, ry:Real or Bool, rz:Real or Bool } }
#     'nodeLoads' : { id(hashable): { node:id, x:Real, y:Real, z:Real, rx:Real, ry:Real, rz:Real } }
#

import numpy as np
from scipy.linalg import solve
from . import line
from .model import Model


def calculate(model):
    fixed_coodinates = set()
    for boundary in model['boundaries'].values():
        for coo in ('x', 'y', 'z', 'rx', 'ry', 'rz'):
            if boundary[coo] and isinstance(boundary[coo], bool):
                fixed_coodinates.add((boundary['node'], coo))
    indexes = {(node, coo) for node in model['nodes'] for coo in ('x', 'y', 'z', 'rx', 'ry', 'rz')}
    indexes -= fixed_coodinates
    indexes = {pair: i for i, pair in enumerate(indexes)}
    K = np.zeros((len(indexes), ) * 2)
    for key, tline in model['lines'].items():
        n = tline['n1'], tline['n2']
        n1 = model['nodes'][n[0]]
        n2 = model['nodes'][n[1]]
        v = [n2[coo] - n1[coo] for coo in ('x', 'y', 'z')]
        E = tline['EA']
        G = 0
        A = 1
        for i, Ki in enumerate(line.stiffnessGlobal(v[0], v[1], v[2], E, G, A)):
            for k1, d1 in enumerate(('x', 'y', 'z', 'rx', 'ry', 'rz')):
                for k2, d2 in enumerate(('x', 'y', 'z', 'rx', 'ry', 'rz')):
                    if (n[i // 2], d1) in indexes and (n[i % 2], d2) in indexes:
                        a = indexes[(n[i // 2], d1)]
                        b = indexes[(n[i % 2], d2)]
                        K[a][b] += Ki[k1][k2]
    P = np.zeros(len(indexes))
    for node_load in model['nodeLoads'].values():
        for d in ('x', 'y', 'z', 'rx', 'ry', 'rz'):
            if (node_load['node'], d) in indexes:
                i = indexes[(node_load['node'], d)]
                P[i] += node_load[d]
    D = solve(K, P, overwrite_a=True, overwrite_b=True)
    R = {}
    for node_id, coodinate in indexes:
        if node_id in R:
            R[node_id][coodinate] = D[indexes[(node_id, coodinate)]]
        else:
            R[node_id] = {coodinate: D[indexes[(node_id, coodinate)]]}
    return {'displacements': R}


def frame_calculate(frameModel):
    inputModel = Model(frameModel, allow_overwrite=True)
    K = np.zeros((inputModel.effective_count(), ) * 2)
    for key, tline in inputModel.lines.items():
        n = (tline['n1'], tline['n2'])
        v = inputModel.line_vector(key)
        E = tline['EA']
        G = 0
        A = 1
        for i, Ki in enumerate(line.stiffnessGlobal(v[0], v[1], v[2], E, G, A)):
            for k1, d1 in enumerate(('x', 'y', 'z', 'rx', 'ry', 'rz')):
                for k2, d2 in enumerate(('x', 'y', 'z', 'rx', 'ry', 'rz')):
                    a = inputModel.effective_indexof(n[i // 2], d1)
                    b = inputModel.effective_indexof(n[i % 2], d2)
                    if a >= 0 and b >= 0:
                        K[a][b] += Ki[k1][k2]
    P = np.zeros(inputModel.effective_count())
    for node_load in inputModel.nodeLoads.values():
        for d in ('x', 'y', 'z', 'rx', 'ry', 'rz'):
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
