# coding: UTF-8

from unittest import TestCase
from frame import main
import frame


class FrameTests(TestCase):

    __model = {
        'nodes': {
            '0': {'x': 0, 'y': 0, 'z': 0},
            '1': {'x': 0, 'y': 0, 'z': 1}
        },
        'lines': {
            '0': {'n1': '0', 'n2': '1', 'section': '0', 'material': '0'}
        },
        'sections': {
            '0': {'shape': 'H', 'H': 3.2, 'B': 3.125, 'tw': 0.125, 'tf': 0.1}
        },
        'materials': {
            '0': {'E': 1, 'G': 1}
        },
        'boundaries': {
            '0': {'node': '0', 'x': True, 'y': True, 'z': True, 'rx': True, 'ry': True, 'rz': True},
            '1': {'node': '1', 'x': True, 'y': True, 'z': 0, 'rx': True, 'ry': True, 'rz': True}
        },
        'nodeloads': {
            '0': {'node': '1', 'x': 0, 'y': 1, 'z': 1, 'rx': 0, 'ry': 0, 'rz': -1}
        }
    }


    def test_items_keys_values(self):
        items = 'a', 'bb', None, 45, 'N'
        expected_items = (0, 'a'), (1, 'bb'), (3, 45), (4, 'N')
        expected_keys = 0, 1, 3, 4
        expected_values = 'a', 'bb', 45, 'N'
        # タプルの場合
        item_tuple = items
        a = main.items(item_tuple)
        for i, j in zip(a, expected_items):
            self.assertEqual(i, j)
        a = main.keys(item_tuple)
        for i, j in zip(a, expected_keys):
            self.assertEqual(i, j)
        a = main.values(item_tuple)
        for i, j in zip(a, expected_values):
            self.assertEqual(i, j)
        # リストの場合
        item_list = list(items)
        a = main.items(item_list)
        for i, j in zip(a, expected_items):
            self.assertEqual(i, j)
        a = main.keys(item_list)
        for i, j in zip(a, expected_keys):
            self.assertEqual(i, j)
        a = main.values(item_list)
        for i, j in zip(a, expected_values):
            self.assertEqual(i, j)
        # 辞書の場合
        item_dict = {i: item for i, item in enumerate(items)}
        a = main.items(item_dict)
        for i, j in zip(a, expected_items):
            self.assertEqual(i, j)
        a = main.keys(item_dict)
        for i, j in zip(a, expected_keys):
            self.assertEqual(i, j)
        a = main.values(item_dict)
        for i, j in zip(a, expected_values):
            self.assertEqual(i, j)
        # ジェネレータの場合
        item_gen = (item for item in items)
        a = main.items(item_gen)
        for i, j in zip(a, expected_items):
            self.assertEqual(i, j)
        a = main.keys(item_gen)
        for i, j in zip(a, expected_keys):
            self.assertEqual(i, j)
        a = main.values(item_gen)
        for i, j in zip(a, expected_values):
            self.assertEqual(i, j)


    def test_calculate(self):
        a = frame.calculate(self.__model)
        self.assertEqual(a, {'displacements': {'1': {'z': 1}}})

