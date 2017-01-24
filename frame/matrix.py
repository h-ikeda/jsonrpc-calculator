import numpy as np
from numpy.linalg import norm


def localToGlobalTransformer(vectorZ, vectorX=None):
    if np.allclose(vectorZ[:2], (0, 0)):
        t = tuple(i / t for i, t in zip(vectorX[:2], (norm(vectorX[:2]),)*2)) if vectorX is not None else (1, 0)
        s = np.sign(vectorZ[2])
        return (
            (t[0], -s*t[1], 0) * 2,
            (t[1],  s*t[0], 0) * 2,
            (0, 0, s) * 2
        ) * 2
    length = norm(vectorZ)
    plen = norm(vectorZ[:2])
    if vectorX is not None:
        z = vectorZ / length
        x = vectorX - np.dot(vectorX, z) * z
        cZ0 = (np.transpose(x[:2], (1, 0)) - vectorZ[:2]) / plen / norm(x)
        sZ0 = np.sqrt((1 - cZ0) * (1 + cZ0))
        return (
            (-vectorZ[1] / plen * cZ0 - vectorZ[0] / plen * vectorZ[2] / length * sZ0, vectorZ[1] / plen * sZ0 - vectorZ[0] / plen * vectorZ[2] / length * cZ0, vectorZ[0] / length) * 2,
            (vectorZ[0] / plen * cZ0 - vectorZ[1] / plen * vectorZ[2] / length * sZ0, -vectorZ[0] / plen * sZ0 - vectorZ[1] / plen * vectorZ[2] / length * cZ0, vectorZ[1] / length) * 2,
            (plen / length * sZ0, plen / length * cZ0, vectorZ[2] / length)*2
        ) * 2
    return (
        (-vectorZ[1] / plen, -vectorZ[0] / plen * vectorZ[2] / length, vectorZ[0] / length) * 2,
        (vectorZ[0] / plen, -vectorZ[1] / plen * vectorZ[2] / length, vectorZ[1] / length) * 2,
        (0, plen / length, vectorZ[2] / length) * 2
    ) * 2


def lineStiffnessGlobal(vector, EA):
    L = norm(vector)
    K11 = np.array((
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, -EA/L, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0)
    ))
    K12 = np.array((
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, EA/L, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0)
    ))
    K21 = np.array((
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, EA/L, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0)
    ))
    K22 = np.array((
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, -EA/L, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0)
    ))
    t = np.array(localToGlobalTransformer(vector))
    return (np.dot(np.dot(t, K11), t.T), np.dot(np.dot(t, K12), t.T)), (np.dot(np.dot(t, K21), t.T), np.dot(np.dot(t, K22), t.T))
