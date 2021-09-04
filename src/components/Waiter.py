import random
from src.components.Drawable import Drawable
from src.managers.ImageCache import ImageCache, Images


class Direction:
    LeftUp    = (-1,-1)
    Up        = ( 0,-1)
    RightUp   = ( 1,-1)
    Right     = ( 1, 0)
    RightDown = ( 1, 1)
    Down      = ( 0, 1)
    LeftDown  = (-1, 1)
    Left      = (-1, 0)


class Waiter(Drawable):

    def __init__(self, x, y, minX, maxX, minY, maxY, cellSize, offset):
        # call base class constructor
        super().__init__(x, y, minX, maxX, minY, maxY, cellSize, offset)
        self.__dx = Direction.Down[0]
        self.__dy = Direction.Down[1]
        self.__acceptedOrders = []
        self.__currentPath = []

    def moveUp(self):
        if self.getY() > self.getMinY():
            self.setY(self.getY() - 1)
            self.setX(self.getX())
            return True
        else:
            return False

    def moveDown(self):
        if self.getY() < self.getMaxY():
            self.setY(self.getY() + 1)
            self.setX(self.getX())
            return True
        else:
            return False

    def moveLeft(self):
        if self.getX() > self.getMinX():
            self.setX(self.getX() - 1)
            self.setY(self.getY())
            return True
        else:
            return False

    def moveRight(self):
        if self.getX() < self.getMaxX():
            self.setX(self.getX() + 1)
            self.setY(self.getY())
            return True
        else:
            return False

    def setX(self, x):
        oldX = self.getX()
        if super().setX(x):
            self.__dx = x - oldX
            return True
        else:
            return False

    def setY(self, y):
        oldY = self.getY()
        if super().setY(y):
            self.__dy = y - oldY
            return True
        else:
            return False

    def getDirection(self):
        return self.__dx, self.__dy

    def setDirection(self, dx, dy):
        self.__dx = dx
        self.__dy = dy

    def getNextDirection(self, oldDirectionXY, newDirectionXY, isDiagonal):
        if oldDirectionXY == (0, 0) or oldDirectionXY == newDirectionXY:
            return None
        if 0 == oldDirectionXY[0]:
            if 0 == newDirectionXY[0]:
                return random.choice([-1, 1]), oldDirectionXY[1] if isDiagonal else 0
            else:
                dx = newDirectionXY[0] - oldDirectionXY[0]
                return +1 if dx > 0 else -1, oldDirectionXY[1] if isDiagonal else 0
        if 0 == oldDirectionXY[1]:
            if 0 == newDirectionXY[1]:
                return oldDirectionXY[0] if isDiagonal else 0, random.choice([-1, 1])
            else:
                dy = newDirectionXY[1] - oldDirectionXY[1]
                return oldDirectionXY[0] if isDiagonal else 0, +1 if dy > 0 else -1
        if 0 == oldDirectionXY[0] + newDirectionXY[0] and 0 == oldDirectionXY[1] + newDirectionXY[1]:
            return random.choice([(oldDirectionXY[0], 0), (0, oldDirectionXY[1])])
        else:
            dx = newDirectionXY[0] - oldDirectionXY[0]
            dy = newDirectionXY[1] - oldDirectionXY[1]
            return (0, oldDirectionXY[1]) if abs(dx) > abs(dy) else (oldDirectionXY[0], 0)

    # accepts orders from the table and stores them in queue
    def addOrder(self, table, order):
        self.__acceptedOrders += [(table, order)]

    def isPathEmpty(self):
        return self.__currentPath == []

    def setPath(self, path):
        self.__currentPath = path

    def popStepFromPath(self):
        return self.__currentPath.pop(0)

    def draw(self, screen):
        direction = self.getDirection()
        imageKind = None
        if direction == Direction.LeftUp: 
            imageKind = Images.WaiterLeftUp
        elif direction == Direction.Up:
            imageKind = Images.WaiterUp
        elif direction == Direction.RightUp:
            imageKind = Images.WaiterRightUp
        elif direction == Direction.Right:
            imageKind = Images.WaiterRight
        elif direction == Direction.RightDown:
            imageKind = Images.WaiterRightDown
        elif direction == Direction.Down:
            imageKind = Images.WaiterDown
        elif direction == Direction.LeftDown:
            imageKind = Images.WaiterLeftDown
        elif direction == Direction.Left:
            imageKind = Images.WaiterLeft

        imageWaiter = ImageCache.getInstance().getImage(imageKind, self.getCellSize(), self.getCellSize())
        self.__xBase = self.getX() * self.getCellSize() + self.getOffset()
        self.__yBase = self.getY() * self.getCellSize() + self.getOffset()
        screen.blit(imageWaiter, (self.__xBase, self.__yBase))

    def drawAux(self, screen):
        toolTipWidth = int(0.4 * self.getCellSize())
        toolTipHeight = int(0.2 * self.getCellSize())
        toolTipXOffset = int(0.6 * self.getCellSize())
        toolTipYOffset = - int(0.1 * self.getCellSize())

        imageToolTip = ImageCache.getInstance().getImage(Images.ToolTip, toolTipWidth, toolTipHeight)
        screen.blit(imageToolTip, (self.__xBase + toolTipXOffset, self.__yBase + toolTipYOffset))
        text = str(len(self.__acceptedOrders))
        color = (204, 0, 0)
        height = int(0.95 * toolTipHeight)
        imageText = ImageCache.getInstance().getTextImage(text, color, height)
        size = imageText.get_size()
        textWidth = size[0]
        textHeight = size[1]

        textXOffset = toolTipXOffset + int((toolTipWidth - textWidth) / 2)
        textYOffset = toolTipYOffset + int((toolTipHeight - textHeight) / 2)
        screen.blit(imageText, (self.__xBase + textXOffset, self.__yBase + textYOffset))
