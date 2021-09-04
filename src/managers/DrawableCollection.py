import random
from threading import Lock

from src.components.Table import Table
from src.components.Waiter import Waiter


# drawable objects manager
from src.managers.MenuManager import MenuManager
from src.managers.TableManager import TableManager
from src.managers.WaiterManager import WaiterManager


class DrawableCollection:
    # const, minimal distance between objects
    __MinDistanceX = 1
    __MinDistanceY = 0

    def __init__(self):
        # collection that holds all drawable objects
        self.__mustRepaint = True
        self.__drawables = []
        self.__waiterLock = Lock()
        self.__tasks = []

    def start(self):
        waiters = self.getWaiters()
        for waiter in waiters:
            # new thread controlling waiter
            waiterTask = WaiterManager(self, [waiter])
            self.__tasks.append(waiterTask)
        # initialize menu manager
        menuManager = MenuManager()
        # new thread controlling tables
        tableTask = TableManager(self, menuManager)
        self.__tasks.append(tableTask)

        for task in self.__tasks:
            task.start()

    def stop(self):
        for task in self.__tasks:
            task.stop()

    # adds drawable objects to the collection
    def add(self, drawable):
        self.__drawables.append(drawable)

    # generates and sets random (x, y) and cheks if it's not occupied by other object
    def generatePosition(self, drawable):
        isPositionUnique = False
        attempt = 0
        while not isPositionUnique:
            x = random.randint(drawable.getMinX(), drawable.getMaxX())
            y = random.randint(drawable.getMinY(), drawable.getMaxY())
            isPositionUnique = True
            for item in self.__drawables:
                if abs(item.getX() - x) <= self.__MinDistanceX and abs(item.getY() - y) <= self.__MinDistanceY:
                    isPositionUnique = False
                    break
            if isPositionUnique:
                drawable.setX(x)
                drawable.setY(y)
                return True
            else:
                attempt += 1
                if attempt > 40:
                    return False

    # checks if position (x,y) is not occupied by other object
    def isPositionAvailable(self, x, y):
        isPositionAvailable = True
        for item in self.__drawables:
            if item.getX() == x and item.getY() == y:
                isPositionAvailable = False
                break
        return isPositionAvailable

    # deletes all tables
    def delTables(self):
        self.__drawables = [drawable for drawable in  self.__drawables if not isinstance(drawable, Table)]

    # gets all tables by status from collection
    def getTables(self, status):
        result = []
        for item in self.__drawables:
            if status is None or isinstance(item, Table) and item.isStatus(status):
                result += [item]
        return result

    # gets all waiters from collection
    def getWaiters(self):
        result = []
        for item in self.__drawables:
            if isinstance(item, Waiter):
                result += [item]
        return result

    # returns table: 0 - position is available, 1 - position is occupied
    def getReservedPlaces(self, waiter):
        cols = waiter.getMaxX() - waiter.getMinX() + 1
        rows = waiter.getMaxY() - waiter.getMinY() + 1
        reservedPlaces = [[0] * cols for _ in range(rows)]
        tables = self.getTables(None)
        if tables:
            for table in tables:
                reservedPlaces[table.getY()][table.getX()] = 1
        waiters = self.getWaiters()
        if waiters:
            for other in waiters:
                if other is not waiter:
                    reservedPlaces[other.getY()][other.getX()] = 1
        return reservedPlaces

    def getNearestTables(self, waiter, tableStatus):
        nearestTables = []
        tables = self.getTables(tableStatus)
        for table in tables:
            if (table.getX() == waiter.getX() and abs(table.getY() - waiter.getY()) == 1) or\
               (table.getY() == waiter.getY() and abs(table.getX() - waiter.getX()) == 1):
                nearestTables.append(table)
        return nearestTables

    def moveWaiter(self, someWaiter, x, y):
        isPositionAvailable = True
        waiters = self.getWaiters()
        self.__waiterLock.acquire()
        try:
            for waiter in waiters:
                if waiter is not someWaiter:
                    if waiter.getX() == x and waiter.getY() == y:
                        isPositionAvailable = False
                        break
            if isPositionAvailable:
                someWaiter.setX(x)
                someWaiter.setY(y)
        finally:
            self.__waiterLock.release()

    # the method is called externally and forces repainting
    def forceRepaint(self):
        self.__mustRepaint = True

    # returns boolean value: True if objects should be repainted otherwise False
    def mustRepaint(self):
        return self.__mustRepaint

    # draws all objects stored in collection
    def draw(self, screen):
        for item in self.__drawables:
            item.draw(screen)
        for item in self.__drawables:
            item.drawAux(screen)
        self.__mustRepaint = False
