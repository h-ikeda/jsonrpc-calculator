import numpy as np


class Line:
    
    __section
    __material
    __vector
    __beta
    
    def __init__(self, vector, section, material, beta):
        self.__vector = np.array(vector)
        self.__section = section
        self.__material = material
        self.__beta = beta


    class Section:
        
        __type
        __data
        
        def __init__(self, type, **data):
            self.__type = type
            self.__data = data