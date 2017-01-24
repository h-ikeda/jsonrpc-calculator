import numpy as np


class Line:

    def __init__(self, vector, section, material, beta):
        self.__vector = np.array(vector)
        self.__section = section
        self.__material = material
        self.__beta = beta

    class Section:

        def __init__(self, line_type, **data):
            self.__type = line_type
            self.__data = data
