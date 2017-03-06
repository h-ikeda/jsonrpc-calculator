from unittest import TestCase
from frame import model


class ModelTests(TestCase):

    __model = model.Model({
        'nodes': [
            {'recid': 0, 'x': 0, 'y': 0, 'z': 0},
            {'recid': 1, 'x': 0, 'y': 0, 'z': 1}
        ],
        'lines': [
            {'recid': 0, 'n1': 0, 'n2': 1, 'EA': 1}
        ],
        'boundaries': [
            {'recid': 0, 'node': 0, 'x': True, 'y': True, 'z': True, 'rx': True, 'ry': True, 'rz': True},
            {'recid': 1, 'node': 1, 'x': True, 'y': True, 'z': 0, 'rx': True, 'ry': True, 'rz': True}
        ],
        'nodeLoads': [
                {'recid': 0, 'node': 1, 'x': 0, 'y': 1, 'z': 1, 'rx': 0, 'ry': 0, 'rz': -1}
        ]
    })

    def test_init_model(self):
        self.assertEqual(self.__model.nodes[1], {'x': 0, 'y': 0, 'z': 1})
        self.assertEqual(self.__model.boundaries[0], {'node': 0, 'x': True, 'y': True, 'z': True, 'rx': True, 'ry': True, 'rz': True})

    def test_effective_coodinates(self):
        self.assertEqual(tuple(self.__model.effective_coodinates()), ((1, 'z'),))
