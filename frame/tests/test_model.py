from unittest import TestCase
from frame import model


class ModelTests(TestCase):
    def test_itemById(self):
        items = [{'recid':1,'data':True},{'recid':31,'data':24.8},{'recid':11,'data':12.8},{'recid':44,'data':'string'}]
        a = model.itemById(items, 11)
        self.assertEqual(a, {'recid':11,'data':12.8})

    def test_effectiveCoodinates(self):
        nodes = [{'recid':0,'x':-5.4,'y':3.2,'z':4.2},{'recid':1,'x':0,'y':-3.2,'z':1.5},{'recid':3,'x':-2.4,'y':-3.8,'z':9.9}]
        boundaries = [{'recid':0,'node':1,'x':100,'y':0,'z':False,'rx':-15,'ry':True,'rz':False},{'recid':2,'node':0,'x':0,'y':0,'z':True,'rx':False,'ry':False,'rz':1}]
        a = model.effectiveCoodinates(nodes, boundaries)
        self.assertEqual(a, ((0,'x'),(0,'y'),(0,'rx'),(0,'ry'),(0,'rz'),(1,'x'),(1,'y'),(1,'z'),(1,'rx'),(1,'rz'),(3,'x'),(3,'y'),(3,'z'),(3,'rx'),(3,'ry'),(3,'rz')))
