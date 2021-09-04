import threading
import time
import random
from src.components.Table import Status


# creates new thread
class TableManager (threading.Thread):

    def __init__(self, drawableManager, menuManager):
        super().__init__()
        self.__drawableManager = drawableManager
        self.__menuManager = menuManager
        self.__runThread = True

    # changes the status of a random table from NotReady to Ready
    def run(self):
        while self.__runThread:
            tables = self.__drawableManager.getTables(Status.NotReady)
            if tables:
                tableIndex = random.randint(0, len(tables) - 1)
                table = tables[tableIndex]
                time.sleep(3)
                table.setOrder(self.__menuManager.generateOrder())
                table.setStatus(Status.Ready)
                self.__drawableManager.forceRepaint()

    def stop(self):
        self.__runThread = False
