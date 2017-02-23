from math import hypot, cos, sin


def transformMatrix(x, y, z, theta):
    c = cos(theta)
    s = sin(theta)
    if (x == 0 and z == 0):
        y = 1. if y > 0 else -1.
        return (
            (0., y, 0.),
            (-y * c, 0., s),
            (y * s, 0., c)
        )
    h = hypot(x, z)
    l = hypot(h, y)
    x /= l
    y /= l
    z /= l
    h /= l
    return (
        (x, y, z),
        (-(x * y * c + z * s) / h, h * c, (x * s - y * z * c) / h),
        ((x * y * s - z * c) / h, -h * s, (x * c + y * z * s) / h)
    )
