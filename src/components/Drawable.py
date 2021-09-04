class Drawable:

    def __init__(self, x, y, minX, maxX, minY, maxY, cellSize, offset):
        self.__minX = minX
        self.__maxX = maxX
        self.__minY = minY
        self.__maxY = maxY
        self.__x = x
        self.__y = y
        self.__cellSize = cellSize  # cell size in pixels
        self.__offset = offset      # paint offset in pixels

    def setX(self, x):
        if x < self.__minX or self.__maxX < x:
            return False
        else:
            self.__x = x
            return True

    def setY(self, y):
        if y < self.__minY or self.__maxY < y:
            return False
        else:
            self.__y = y
            return True

    def isPositionCorrect(self, x, y):
        return self.__minX <= x <= self.__maxX and self.__minY <= y <= self.__maxY

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getMinX(self):
        return self.__minX

    def getMaxX(self):
        return self.__maxX

    def getMinY(self):
        return self.__minY

    def getMaxY(self):
        return self.__maxY

    def getCellSize(self):
        return self.__cellSize

    def getOffset(self):
        return self.__offset

    def draw(self, screen):
        pass

    def drawAux(self, screen):
        pass
