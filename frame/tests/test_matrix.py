# coding: UTF-8

from unittest import TestCase
from frame import matrix
from numpy import allclose
from math import radians


class MatrixTests(TestCase):
    def test_transform_matrix(self):
        # Y軸周りに-90度回転
        a = matrix.transformMatrix(0, 0, 2.85, 0)
        self.assertTrue(allclose((
            (0., 0., 1.),
            (0., 1., 0.),
            (-1., 0., 0.)), a))
        # Y軸周りに90度回転
        a = matrix.transformMatrix(0, 0, -1.2, 0)
        self.assertTrue(allclose((
            (0., 0., -1.),
            (0., 1., 0.),
            (1., 0., 0.)), a))
        # Y軸周りに-arctan(3/4)回転
        a = matrix.transformMatrix(4, 0, 3, 0)
        self.assertTrue(allclose((
            (4./5, 0., 3./5),
            (0., 1., 0.),
            (-3./5, 0., 4./5)), a))
        # Z軸周りに90回転
        a = matrix.transformMatrix(0, 40.2, 0, 0)
        self.assertTrue(allclose((
            (0., 1., 0.),
            (-1., 0., 0.),
            (0., 0., 1.)), a))
        # Z軸周りに-90回転
        a = matrix.transformMatrix(0, -0.018, 0, 0)
        self.assertTrue(allclose((
            (0., -1., 0.),
            (1., 0., 0.),
            (0., 0., 1.)), a))
        # Z軸周りにarctan(3/4)回転
        a = matrix.transformMatrix(4, 3, 0, 0)
        self.assertTrue(allclose((
            (4./5, 3./5, 0.),
            (-3./5, 4./5, 0.),
            (0., 0., 1.)), a))
        # X軸周りに90度回転
        a = matrix.transformMatrix(20591281, 0, 0, radians(90))
        self.assertTrue(allclose((
            (1., 0., 0.),
            (0., 0., 1.),
            (0., -1., 0.)), a))
        # YZ平面上に回転
        a = matrix.transformMatrix(0, -4, -3, 0)
        self.assertTrue(allclose((
            (0., -4./5, -3./5),
            (0., 3./5, -4./5),
            (1., 0., 0.)), a))
