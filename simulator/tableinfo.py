""" Configuration of the table state from FRONT VIEW """
import random

class TableInfo:
    def __init__(self, set_manual=False):
        if set_manual:
            self.manualConf()
        else:
            self.randomConf()
        self.printConf()

    def randomConf(self):
        maxobjects = 5
        maxX = 300
        maxZ = 300
        colorlist = ["green", "red", "yellow", "gray", "black"]

        self.numobjects = random.randint(1, maxobjects-1)
        self.positions  = []
        self.dimensions = []
        self.colors = []
        for i in range(0, self.numobjects):
            # Random Position
            rand_position = [random.randint(0, maxX), random.randint(0, maxZ)]
            self.positions.append(rand_position)
            # Random Dimension
            maxX_dimension = maxX - rand_position[0]
            maxZ_dimension = maxZ - rand_position[1]
            rand_dimension = [random.randint(0, maxX_dimension), random.randint(0, maxZ_dimension)]
            self.dimensions.append(rand_dimension)
            # Random Colour
            self.colors.append(colorlist[random.randint(0, len(colorlist)-1)])

    def manualConf(self):
        self.numobjects = 2
        self.positions  = [ [10, 0], [20, 0] ]
        self.dimensions = [ [40, 40], [40, 40] ]
        self.colors = [ "green", "red" ]

    def printConf(self):
        print "Numobjects : %s" % self.numobjects
        print "Positions : %s" % self.positions
        print "Dimensions : %s" % self.dimensions
        print "Colors: %s" % self.colors

