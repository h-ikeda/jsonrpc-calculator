# coding: UTF-8

from unittest import TestCase
from frame import section


class LineTests(TestCase):
    def test_h_section_properties(self):
        a = section.h_section_properties(200, 100, 5.5, 8, 8)
        self.assertAlmostEqual(2666.9380702, a['Ax'])
        self.assertAlmostEqual(1600, a['Ay'])
        self.assertAlmostEqual(1100, a['Az'])
        self.assertAlmostEqual(18056554.032244, a['Iy'])
        self.assertAlmostEqual(1337138.8731901, a['Iz'])
        self.assertAlmostEqual(44337.6666667, a['J'])
        self.assertAlmostEqual(180565.5403224, a['Zy'])
        self.assertAlmostEqual(26742.7774638, a['Zz'])
        self.assertAlmostEqual(82.2831616, a['iy'])
        self.assertAlmostEqual(22.391428, a['iz'])


    def test_t_section_properties(self):
        a = section.t_section_properties(100, 100, 5.5, 8, 8)
        self.assertAlmostEqual(1333.4690351, a['Ax'])
        self.assertAlmostEqual(800, a['Ay'])
        self.assertAlmostEqual(550, a['Az'])
        self.assertAlmostEqual(1141077.4657765, a['Iy'])
        self.assertAlmostEqual(668569.4365951, a['Iz'])
        self.assertAlmostEqual(14836.9687553, a['Zy'])
        self.assertAlmostEqual(13371.3887319, a['Zz'])
        self.assertAlmostEqual(29.2527094, a['iy'])
        self.assertAlmostEqual(22.391428, a['iz'])
