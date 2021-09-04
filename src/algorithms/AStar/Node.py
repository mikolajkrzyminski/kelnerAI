from math import sqrt


class Node:

    def __init__(self, parent, x, y, distance):
        self.parent = parent
        self.x = x
        self.y = y
        self.distance = distance
        self.estimated = distance

    # returns distance from the object to other node
    def getDistanceTo(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx * dx + dy * dy)
        # abs(dx) + abs(dy)

    def getDirection(self):
        if self.parent is None:
            return 0, 0
        else:
            return self.x - self.parent.x, self.y - self.parent.y

    # used by str() method to represent the object
    def __repr__(self):
        return "%s:%s" % (self.x, self.y)

    # generates hash key for Set
    def __hash__(self):
        return hash(str(self))

    # operator (==) for Set (determines if the object equals other node)
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    # operator (>) for PriorityQueue comparison (determines the objects order)
    def __gt__(self, other):
        return self.estimated > other.estimated
