coodinates = ('x', 'y', 'z', 'rx', 'ry', 'rz')
coodinates_d = coodinates[:3]


class Model:

    def __init__(self, inputModel, allow_overwrite=False):
        #
        # Copy inputModel. Deep copy if overwrite is not allowed.
        #
        if allow_overwrite:
            self.__data = inputModel
        else:
            import copy
            self.__data = copy.deepcopy(inputModel)
        #
        # Restructure model.
        # From
        # { 'name': [ { 'recid': ID, 'x': X, 'y': Y, ... } ] }
        # to
        # { 'name': { ID: {'x': X, 'y': Y, ... } } }
        #
        for name in self.__data:
            self.__data[name] = {data.pop('recid'): data for data in self.__data[name]}
            setattr(self, name, self.__data[name])
        #
        # Create fixed coodinates set.
        #
        fixedCoodinates = {(boundary['node'], c) for boundary in self.boundaries.values() for c in coodinates if boundary[c] and isinstance(boundary[c], bool)}
        #
        # Give unique numbers to node and coodinate pairs, except fixed ones.
        #
        self.__index = {(node, c) for node in self.nodes for c in coodinates}
        self.__index -= fixedCoodinates
        self.__index = {pair: i for i, pair in enumerate(self.__index)}

    def effective_indexof(self, node_id, coodinate):
        return self.__index.get((node_id, coodinate), -1)

    def effective_count(self):
        return len(self.__index)

    def effective_coodinates(self):
        return self.__index

    def line_vector(self, line_id):
        n1 = self.lines[line_id]['n1']
        n2 = self.lines[line_id]['n2']
        return tuple(self.nodes[n2][c] - self.nodes[n1][c] for c in coodinates_d)
