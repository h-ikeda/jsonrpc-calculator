from scipy.linalg import block_diag
from frame.matrix import transformMatrix
from numpy import dot
from numpy.linalg import norm


def stiffness_local(L, E, G, Ax, Iz=0, Iy=0, Ay=0, Az=0, J=0):
    if Ay == 0:
        Ay = Ax
    if Az == 0:
        Az = Ax
    phiY = 12. * Iz / G / Ay / L / L * E if Iz != 0 else 0.
    phiZ = 12. * Iy / G / Az / L / L * E if Iy != 0 else 0.
    a = float(Ax) / L * E
    s = float(J) / L * G
    kzPre = Iz / (phiY + 1) / L / L * E
    kyPre = Iy / (phiZ + 1) / L / L * E
    kz11 = kzPre * 12
    kz12 = L * kzPre * 6
    kz13 = -kz11
    kz14 = kz12
    kz22 = (phiY + 4) * kzPre * L * L
    kz23 = -kz12
    kz24 = (2 - phiY) * kzPre * L * L
    kz33 = kz11
    kz34 = kz23
    kz44 = kz22
    ky11 = kyPre * 12
    ky12 = -L * kyPre * 6
    ky13 = -ky11
    ky14 = ky12
    ky22 = (phiZ + 4) * kyPre * L * L
    ky23 = -ky12
    ky24 = (2 - phiZ) * kyPre * L * L
    ky33 = ky11
    ky34 = ky23
    ky44 = ky22
    yield (
        (a, 0, 0, 0, 0, 0),
        (0, kz11, 0, 0, 0, kz12),
        (0, 0, ky11, 0, ky12, 0),
        (0, 0, 0, s, 0, 0),
        (0, 0, ky12, 0, ky22, 0),
        (0, kz12, 0, 0, 0, kz22)
    )
    yield (
        (-a, 0, 0, 0, 0, 0),
        (0, kz13, 0, 0, 0, kz14),
        (0, 0, ky13, 0, ky14, 0),
        (0, 0, 0, -s, 0, 0),
        (0, 0, ky23, 0, ky24, 0),
        (0, kz23, 0, 0, 0, kz24)
    )
    yield (
        (-a, 0, 0, 0, 0, 0),
        (0, kz13, 0, 0, 0, kz23),
        (0, 0, ky13, 0, ky23, 0),
        (0, 0, 0, -s, 0, 0),
        (0, 0, ky14, 0, ky24, 0),
        (0, kz14, 0, 0, 0, kz24)
    )
    yield (
        (a, 0, 0, 0, 0, 0),
        (0, kz33, 0, 0, 0, kz34),
        (0, 0, ky33, 0, ky34, 0),
        (0, 0, 0, s, 0, 0),
        (0, 0, ky34, 0, ky44, 0),
        (0, kz34, 0, 0, 0, kz44)
    )


def stiffness_global(x, y, z, E, G, Ax, Iz=0, Iy=0, Ay=0, Az=0, theta=0, J=0):
    t = block_diag(*(transformMatrix(x, y, z, theta),) * 2)
    r = t.transpose()
    for m in stiffness_local(norm((x, y, z)), E, G, Ax, Iz, Iy, Ay, Az, J):
        yield dot(dot(t, m), r)
