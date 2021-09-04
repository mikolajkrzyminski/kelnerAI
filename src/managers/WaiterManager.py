import threading
import time
import sys
from math import sqrt

from src.components.Table import Status
from src.algorithms.AStar.Finder import Finder


# creates new thread
class WaiterManager (threading.Thread):

    def __init__(self, drawableManager, waiters):
        super().__init__()
        self.__drawableManager = drawableManager
        self.__waiters = waiters
        self.__runThread = True

    def __getDistance(self, waiter, tupleXY):
        dx = waiter.getX() - tupleXY[0]
        dy = waiter.getY() - tupleXY[1]
        return sqrt(dx * dx + dy * dy)

    def __sortTargets(self, waiter, targets):
        return sorted(targets, key=lambda target: self.__getDistance(waiter, (target[0], target[1])))

    def __getTargets(self, waiter, finder):
        found = []
        tables = self.__drawableManager.getTables(Status.Ready)
        if tables:
            origin = (waiter.getX(), waiter.getY())
            for table in tables:
                if table.hasOrder():
                    targets = finder.getNeighbours((table.getX(), table.getY()), False)
                    for target in targets:
                        if target == origin:
                            return []
                        else:
                            found.append(target)
        return self.__sortTargets(waiter, found)

    def __getNearestTargetPath(self, waiter):
        distance = sys.maxsize
        nearestTargetPath = None
        reservedPlaces = self.__drawableManager.getReservedPlaces(waiter)
        finder = Finder(reservedPlaces)
        origin = (waiter.getX(), waiter.getY())
        targets = self.__getTargets(waiter, finder)
        for target in targets:
            if distance > self.__getDistance(waiter, target):
                path = finder.getPath(origin, target, True)
                if path:
                    result = len(path)
                    if result < distance:
                        distance = result
                        nearestTargetPath = path

        return nearestTargetPath

    def __changeWaiterDirection(self, waiter, x, y):
        targetDirection = x - waiter.getX(), y - waiter.getY()
        originDirection = waiter.getDirection()
        while originDirection is not None:
            originDirection = waiter.getNextDirection(originDirection, targetDirection, True)
            if originDirection is not None:
                time.sleep(0.3)
                waiter.setDirection(originDirection[0], originDirection[1])
                self.__drawableManager.forceRepaint()

    def __moveWaiter(self, waiter, x, y):
        time.sleep(0.4)
        self.__drawableManager.moveWaiter(waiter, x, y)
        self.__drawableManager.forceRepaint()

    def __collectOrder(self, waiter):
        doCollectOrder = True
        while doCollectOrder:
            tables = self.__drawableManager.getNearestTables(waiter, Status.Ready)
            turns = sys.maxsize
            lessTurnsTable = None
            originDirection = waiter.getDirection()

            for table in tables:
                targetDirection = table.getX() - waiter.getX(), table.getY() - waiter.getY()
                result = Finder.getTurnsCount(originDirection, targetDirection, True)
                if result < turns:
                    turns = result
                    lessTurnsTable = table

            if lessTurnsTable is not None:
                tables.remove(lessTurnsTable)
                self.__changeWaiterDirection(waiter, lessTurnsTable.getX(), lessTurnsTable.getY())

                order = lessTurnsTable.getOrder()
                if order is not None:
                    waiter.addOrder(lessTurnsTable, order)
                    time.sleep(2)
                    lessTurnsTable.setStatus(Status.Waiting)
                    self.__drawableManager.forceRepaint()
            doCollectOrder = len(tables) > 0

    # changes the status of a random table from NotReady to Ready
    def run(self):
        while self.__runThread:
            if self.__waiters:
                for waiter in self.__waiters:
                    path = self.__getNearestTargetPath(waiter)
                    waiter.setPath([] if path is None else path)

                    if not waiter.isPathEmpty():
                        step = waiter.popStepFromPath()
                        self.__changeWaiterDirection(waiter, step[0], step[1])
                        self.__moveWaiter(waiter, step[0], step[1])

                    if waiter.isPathEmpty():
                        self.__collectOrder(waiter)

    def stop(self):
        self.__runThread = False
