from TableInfo import *

class Manipulator:
    @staticmethod
    def removeObject(index):
        tableinfo.numobjects -= 1
        tableinfo.ids.pop(index)
        tableinfo.positions.pop(index)
        tableinfo.dimensions.pop(index)
        tableinfo.colors.pop(index)

