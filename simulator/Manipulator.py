from TableInfo import *

class Manipulator:
    @staticmethod
    def removeObject(index):
        tableinfo.numobjects -= 1
        objId = tableinfo.ids.pop(index)
        tableinfo.positions.pop(index)
        tableinfo.dimensions.pop(index)
        tableinfo.colors.pop(index)
        tableinfo.full_occ_list.pop(index)
        tableinfo.part_occ_list.pop(index)
        tableinfo.latticeids.pop(index)

        for pol in tableinfo.part_occ_list:
            pol.remove(objId)
        for fol in tableinfo.full_occ_list:
            fol.remove(objId)
