from queue import PriorityQueue
from src.algorithms.AStar.Node import Node


class Finder:

    def __init__(self, table):
        self._table = table
        self._xMin = 0
        self._yMin = 0
        self._xMax = len(table[0]) - 1
        self._yMax = len(table) - 1

    def _set(self, x, y, v):
        self._table[y][x] = v

    def _get(self, x, y):
        return self._table[y][x]

    # returns right position relative to the node
    def __incXnopY(self, node, direction, isDiagonal, neighbours):
        if node.x < self._xMax and self._get(node.x + 1, node.y) == 0:
            turnsCount = self.getTurnsCount(direction, (1, 0), isDiagonal)
            neighbours.append(Node(node, node.x + 1, node.y, node.distance + turnsCount + 1))

    # returns left position relative to the node
    def __decXnopY(self, node, direction, isDiagonal, neighbours):
        if self._xMin < node.x and self._get(node.x - 1, node.y) == 0:
            turnsCount = self.getTurnsCount(direction, (-1, 0), isDiagonal)
            neighbours.append(Node(node, node.x - 1, node.y, node.distance + turnsCount + 1))

    # returns top position relative to the node
    def __nopXincY(self, node, direction, isDiagonal, neighbours):
        if node.y < self._yMax and self._get(node.x, node.y + 1) == 0:
            turnsCount = self.getTurnsCount(direction, (0, 1), isDiagonal)
            neighbours.append(Node(node, node.x, node.y + 1, node.distance + turnsCount + 1))

    # returns bottom position relative to the node
    def __nopXdecY(self, node, direction, isDiagonal, neighbours):
        if self._yMin < node.y and self._get(node.x, node.y - 1) == 0:
            turnsCount = self.getTurnsCount(direction, (0, -1), isDiagonal)
            neighbours.append(Node(node, node.x, node.y - 1, node.distance + turnsCount + 1))

    # returns left top position relative to the node
    def __decXdecY(self, node, direction, isDiagonal, neighbours):
        if (self._xMin < node.x and self._yMin < node.y and
                self._get(node.x - 1, node.y - 1) == 0 and
                self._get(node.x - 1, node.y) == 0 and
                self._get(node.x, node.y - 1) == 0):
            turnsCount = self.getTurnsCount(direction, (-1, -1), isDiagonal)
            neighbours.append(Node(node, node.x - 1, node.y - 1, node.distance + turnsCount + 2))

    # returns left bottom position relative to the node
    def __decXincY(self, node, direction, isDiagonal, neighbours):
        if (self._xMin < node.x and node.y < self._yMax and
                self._get(node.x - 1, node.y + 1) == 0 and
                self._get(node.x - 1, node.y) == 0 and
                self._get(node.x, node.y + 1) == 0):
            turnsCount = self.getTurnsCount(direction, (-1, 1), isDiagonal)
            neighbours.append(Node(node, node.x - 1, node.y + 1, node.distance + turnsCount + 2))

    # returns right bottom position relative to the node
    def __incXincY(self, node, direction, isDiagonal, neighbours):
        if (node.x < self._xMax and node.y < self._yMax and
                self._get(node.x + 1, node.y + 1) == 0 and
                self._get(node.x + 1, node.y) == 0 and
                self._get(node.x, node.y + 1) == 0):
            turnsCount = self.getTurnsCount(direction, (1, 1), isDiagonal)
            neighbours.append(Node(node, node.x + 1, node.y + 1, node.distance + turnsCount + 2))

    # returns right top position relative to the node
    def __incXdecY(self, node, direction, isDiagonal, neighbours):
        if (node.x < self._xMax and self._yMin < node.y and
                self._get(node.x + 1, node.y - 1) == 0 and
                self._get(node.x + 1, node.y) == 0 and
                self._get(node.x, node.y - 1) == 0):
            turnsCount = self.getTurnsCount(direction, (1, -1), isDiagonal)
            neighbours.append(Node(node, node.x + 1, node.y - 1, node.distance + turnsCount + 2))

    # returns all plausible positions relative to the node
    def __getNeighbours(self, node, isDiagonal):
        direction = node.getDirection()
        neighbours = []
        self.__nopXincY(node, direction, isDiagonal, neighbours)
        self.__incXnopY(node, direction, isDiagonal, neighbours)
        self.__decXnopY(node, direction, isDiagonal, neighbours)
        self.__nopXdecY(node, direction, isDiagonal, neighbours)
        if isDiagonal:
            self.__decXdecY(node, direction, isDiagonal, neighbours)
            self.__decXincY(node, direction, isDiagonal, neighbours)
            self.__incXincY(node, direction, isDiagonal, neighbours)
            self.__incXdecY(node, direction, isDiagonal, neighbours)
        return neighbours

    # main algorithm - simplification of well known A*
    def __getPath(self, origin, target, isDiagonal):
        Q = PriorityQueue()
        V = set()
        Q.put(origin)
        while not Q.empty():
            head = Q.get()
            if head == target:
                return head
            V.add(head)
            for node in self.__getNeighbours(head, isDiagonal):
                if node not in V:
                    node.estimated = node.distance + node.getDistanceTo(target)
                    Q.put(node)
                    V.add(node)
        return None

    # returns the number of turns to change direction from old to new
    @staticmethod
    def getTurnsCount(oldDirection, newDirection, isDiagonal):
        if oldDirection == (0, 0) or oldDirection == newDirection:
            return 0
        if 0 == oldDirection[0] + newDirection[0] and 0 == oldDirection[1] + newDirection[1]:
            return 4 if isDiagonal else 2
        return abs(newDirection[0] - oldDirection[0]) + abs(newDirection[1] - oldDirection[1]) if isDiagonal else 1

    # returns neighbours for locationXY-tuple as list of tuple(x,y)
    def getNeighbours(self, locationXY, isDiagonal):
        neighboursXY = []
        location = Node(None, locationXY[0], locationXY[1], 0)
        neighbours = self.__getNeighbours(location, isDiagonal)
        for neighbour in neighbours:
            neighboursXY.append((neighbour.x, neighbour.y))
        return neighboursXY

    # returns the shortest path as list of tuple(x,y) from originXY-tuple to targetXY-tuple
    def getPath(self, originXY, targetXY, isDiagonal):
        origin = Node(None, originXY[0], originXY[1], 0)
        target = Node(None, targetXY[0], targetXY[1], 0)
        result = self.__getPath(origin, target, isDiagonal)
        path = []
        while result is not None:
            if result.parent is not None:
                path.insert(0, (result.x, result.y))
            result = result.parent
        return path
