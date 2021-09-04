import random
from enum import Enum
from threading import Lock
from src.components.Drawable import Drawable
from src.managers.ImageCache import ImageCache, Images


# status of the table
class Status(Enum):
    NotReady = 0
    Ready    = 1
    Waiting  = 2
    Served   = 3


class Table(Drawable):

    def __init__(self, minX, maxX, minY, maxY, cellSize, offset):
        # call base class constructor
        super().__init__(0, 0, minX, maxX, minY, maxY, cellSize, offset)
        self.__status = Status.NotReady
        self.__order = []
        self.__guests = self.__getRandomGuests()
        self.__tableLock = Lock()

    @staticmethod
    def __getRandomGuests():
        possibleGuests = [Images.Guest1, Images.Guest2, Images.Guest3]
        guests = []
        guestCount = random.randint(1, len(possibleGuests))
        for _ in range(guestCount):
            guests.insert(0, possibleGuests[random.randint(0, len(possibleGuests) - 1)])
        return guests

    # waiter collects orders from table
    def getOrder(self):
        order = None
        if self.__tableLock.acquire(False):
            try:
                if self.isStatus(Status.Ready) and self.hasOrder():
                    order = self.__order
                    self.setOrder([])
            finally:
                self.__tableLock.release()
        return order

    def setOrder(self, order):
        self.__order = order

    def hasOrder(self):
        return [] != self.__order

    def isStatus(self, status):
        return status == self.__status

    def setStatus(self, status):
        self.__status = status

    def __getImage(self, imageKind):
        if imageKind in [Images.Guest1, Images.Guest2, Images.Guest3, Images.Plate]:
            size = int(self.getCellSize() / 3)
        else:
            size = int(1.4 * self.getCellSize())
        return ImageCache.getInstance().getImage(imageKind, size, size)

    # draws only table
    def draw(self, screen):
        xBase = self.getX() * self.getCellSize() + self.getOffset()
        yBase = self.getY() * self.getCellSize() + self.getOffset()
        tableXYOffset = int(0.2 * self.getCellSize())
        screen.blit(self.__getImage(Images.Table), (xBase - tableXYOffset, yBase - tableXYOffset))

    # draws images related to the status of a table
    # the method is called in the second turn when all tables are already painted
    def drawAux(self, screen):
        xBase = self.getX() * self.getCellSize() + self.getOffset()
        yBase = self.getY() * self.getCellSize() + self.getOffset()

        guest1XOffset = 0
        guest2XOffset = int((1 / 3) * self.getCellSize())
        guest3XOffset = int((2 / 3) * self.getCellSize())
        guest4XOffset = int((1 / 9) * self.getCellSize())
        guest5XOffset = int((5 / 9) * self.getCellSize())
        guestsYOffset = int(0.1 * self.getCellSize())
        tableXYOffset = int(0.2 * self.getCellSize())

        if len(self.__guests) == 1:
            screen.blit(self.__getImage(self.__guests[0]), (xBase + guest2XOffset, yBase - guestsYOffset))
        elif len(self.__guests) == 2:
            screen.blit(self.__getImage(self.__guests[0]), (xBase + guest4XOffset, yBase - guestsYOffset))
            screen.blit(self.__getImage(self.__guests[1]), (xBase + guest5XOffset, yBase - guestsYOffset))
        elif len(self.__guests) == 3:
            screen.blit(self.__getImage(self.__guests[0]), (xBase + guest1XOffset, yBase - guestsYOffset))
            screen.blit(self.__getImage(self.__guests[1]), (xBase + guest2XOffset, yBase - guestsYOffset))
            screen.blit(self.__getImage(self.__guests[2]), (xBase + guest3XOffset, yBase - guestsYOffset))

        if self.isStatus(Status.NotReady):
            screen.blit(self.__getImage(Images.Menu), (xBase - tableXYOffset, yBase - tableXYOffset))
        elif self.isStatus(Status.Ready):
            screen.blit(self.__getImage(Images.Check), (xBase - tableXYOffset, yBase - tableXYOffset))
        elif self.isStatus(Status.Waiting):
            platesYOffset = int(0.3 * self.getCellSize())
            imagePlate = self.__getImage(Images.Plate)
            if len(self.__guests) == 1:
                screen.blit(imagePlate, (xBase + guest2XOffset, yBase + platesYOffset))
            elif len(self.__guests) == 2:
                screen.blit(imagePlate, (xBase + guest4XOffset, yBase + platesYOffset))
                screen.blit(imagePlate, (xBase + guest5XOffset, yBase + platesYOffset))
            elif len(self.__guests) == 3:
                screen.blit(imagePlate, (xBase + guest1XOffset, yBase + platesYOffset))
                screen.blit(imagePlate, (xBase + guest2XOffset, yBase + platesYOffset))
                screen.blit(imagePlate, (xBase + guest3XOffset, yBase + platesYOffset))
