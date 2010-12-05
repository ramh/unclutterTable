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
        maxY = 300
        maxZ = 300
        colorlist = ["green", "red", "yellow", "gray", "black"]

        self.numobjects = random.randint(1, maxobjects-1)
        self.ids = range(0, self.numobjects)
        self.positions  = []
        self.dimensions = []
        self.colors = []
        for i in range(0, self.numobjects):
            # Random Position
            rand_position = [random.randint(0, maxX), random.randint(0, maxY), random.randint(0, maxZ)]
            self.positions.append(rand_position)
            # Random Dimension
            maxX_dimension = maxX - rand_position[0]
            maxY_dimension = maxY - rand_position[1]
            maxZ_dimension = maxZ - rand_position[2]
            rand_dimension = [random.randint(0, maxX_dimension), random.randint(0, maxY_dimension), random.randint(0, maxZ_dimension)]
            self.dimensions.append(rand_dimension)
            # Random Colour
            self.colors.append(colorlist[random.randint(0, len(colorlist)-1)])

    def manualConf(self):
        self.numobjects = 3
        self.ids = [0, 1, 2]
        self.positions  = [ [10, 0, 0], [30, 60, 30], [20, 50, 0] ]
        self.dimensions = [ [40, 40, 40], [20, 20, 20], [40, 40, 30] ]
        self.colors = [ "green", "yellow", "red"]

    def sortonY(self):
        for i in range(0, len(self.positions)-1):
            for j in range(1, len(self.positions)):
                if(self.positions[i][1] < self.positions[j][1]):
                    tmp = self.positions[i]; self.positions[i] = self.positions[j]; self.positions[j] = tmp
                    tmp = self.dimensions[i]; self.dimensions[i] = self.dimensions[j]; self.dimensions[j] = tmp
                    tmp = self.colors[i]; self.colors[i] = self.colors[j]; self.colors[j] = tmp
                    tmp = self.ids[i]; self.ids[i] = self.ids[j]; self.ids[j] = tmp

    def sortonZ(self):
        for i in range(0, len(self.positions)-1):
            for j in range(1, len(self.positions)):
                if(self.positions[i][2] > self.positions[j][2]):
                    tmp = self.positions[i]; self.positions[i] = self.positions[j]; self.positions[j] = tmp
                    tmp = self.dimensions[i]; self.dimensions[i] = self.dimensions[j]; self.dimensions[j] = tmp
                    tmp = self.colors[i]; self.colors[i] = self.colors[j]; self.colors[j] = tmp
                    tmp = self.ids[i]; self.ids[i] = self.ids[j]; self.ids[j] = tmp

    def printConf(self):
        print "Numobjects : %s" % self.numobjects
        print "Ids : %s" % self.ids
        print "Positions : %s" % self.positions
        print "Dimensions : %s" % self.dimensions
        print "Colors: %s" % self.colors

# Instantiate TableInfo
tableinfo = TableInfo(set_manual=True)
#tableinfo = TableInfo()

