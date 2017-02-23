# coding: UTF-8

from unittest import TestCase
from frame import matrix
from numpy.testing import *
from math import radians


class MatrixTests(TestCase):
    def test_transformMatrix(self):
        # Y軸周りに-90度回転
        a = matrix.transformMatrix(0, 0, 2.85, 0)
        assert_allclose((
            (0., 0., 1.),
            (0., 1., 0.),
            (-1., 0., 0.)), a)
        # Y軸周りに90度回転
        a = matrix.transformMatrix(0, 0, -1.2, 0)
        assert_allclose((
            (0., 0., -1.),
            (0., 1., 0.),
            (1., 0., 0.)), a)
        # Y軸周りに-arctan(3/4)回転
        a = matrix.transformMatrix(4, 0, 3, 0)
        assert_allclose((
            (4./5, 0., 3./5),
            (0., 1., 0.),
            (-3./5, 0., 4./5)), a)
        # Z軸周りに90回転
        a = matrix.transformMatrix(0, 40.2, 0, 0)
        assert_allclose((
            (0., 1., 0.),
            (-1., 0., 0.),
            (0., 0., 1.)), a)
        # Z軸周りに-90回転
        a = matrix.transformMatrix(0, -0.018, 0, 0)
        assert_allclose((
            (0., -1., 0.),
            (1., 0., 0.),
            (0., 0., 1.)), a)
        # Z軸周りにarctan(3/4)回転
        a = matrix.transformMatrix(4, 3, 0, 0)
        assert_allclose((
            (4./5, 3./5, 0.),
            (-3./5, 4./5, 0.),
            (0., 0., 1.)), a)
        # X軸周りに90度回転
        a = matrix.transformMatrix(20591281, 0, 0, radians(90))
        assert_allclose((
            (1., 0., 0.),
            (0., 0., 1.),
            (0., -1., 0.)), a, atol=1e-15)
        # YZ平面上に回転
        a = matrix.transformMatrix(0, -4, -3, 0)
        assert_allclose((
            (0., -4./5, -3./5),
            (0., 3./5, -4./5),
            (1., 0., 0.)), a)
