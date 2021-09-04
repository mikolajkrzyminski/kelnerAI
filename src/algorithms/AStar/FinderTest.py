import random
from kelner.src.algorithms.AStar.Finder import Finder


class FinderTest(Finder):

    def __init__(self, table):
        super().__init__(table)

    def __setValues(self, xys, v):
        if xys is not None:
            for xy in xys:
                self._set(xy[0], xy[1], v)

    def print(self, xys):
        self.__setValues(xys, 2)
        for row in self._table:
            for col in row:
                v = ' ' if col == 0 else '#' if col == 1 else 'O'
                print('|', v, sep='', end='')
            print('|')
        self.__setValues(xys, 0)

    def getRandomTuple(self):
        while True:
            x = random.randint(self._xMin, self._xMax)
            y = random.randint(self._yMin, self._yMax)
            if self._get(x, y) == 0:
                break
        return x, y

    def getRandomBorderTuple(self):
        xSet = [self._xMin, self._xMax]
        ySet = [self._yMin, self._yMax]
        while True:
            x = random.randint(self._xMin, self._xMax)
            y = random.randint(self._yMin, self._yMax)
            if (x in xSet or y in ySet) and self._get(x, y) == 0:
                break
        return x, y

    def fillRandom(self):
        for _ in range(120):
            while True:
                x = random.randint(self._xMin, self._xMax)
                y = random.randint(self._yMin, self._yMax)
                if self._get(x, y) == 0:
                    break
            self._set(x, y, 1)


"""
cols = 20
rows = 20
table = [[0] * cols for i in range(rows)]
finder = FinderTest(table)
finder.fillRandom()
originXY = finder.getRandomBorderTuple()
targetXY = finder.getRandomBorderTuple()
result = finder.getPath(originXY, targetXY, True)
finder.print(result)
"""

table = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
         [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
         [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
         [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
         [0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
         [1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
         [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
         [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]]

finder = FinderTest(table)
originXY = ( 6, 19)
targetXY = (13,  0)
result = finder.getPath(originXY, targetXY, True)
finder.print(result)
