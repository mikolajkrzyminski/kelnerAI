import gc
import math
import threading
import PySimpleGUI as sg
import time
from tkinter import messagebox, Tk
from src.components.Table import Table
from src.algorithms.GATableGenerator.GATableGenerator import GATableGenerator
from gui.GAdialog.GADialog import GADialog
from gui.GAdialog.GADefaults import GADefaults
from gui.chart.Plots import Plots


# creates new thread
class TableGenerator (threading.Thread):

    def __init__(self, gridCols, gridRows, minX, maxX, minY, maxY, cellSize, paintOffset, drawableManager):
        super().__init__()
        self.__minX = minX
        self.__maxX = maxX
        self.__minY = minY
        self.__maxY = maxY
        self.__cellSize = cellSize
        self.__paintOffset = paintOffset
        self.__drawableManager = drawableManager
        self.__runThread = True
        self.__defaults = GADefaults()
        self.__gaTableGenerator = GATableGenerator(gridCols, gridRows, self.__defaults)

    def __randomTables(self):
        # initialize a number of tables given in range
        for i in range(0, 40):
            table = Table(self.__minX, self.__maxX, self.__minY, self.__maxY, self.__cellSize, self.__paintOffset)
            if self.__drawableManager.generatePosition(table):
                self.__drawableManager.add(table)

    def __geneticTables(self):
        bestIndividual = self.__gaTableGenerator.getBestIndividual()
        for row in range(self.__gaTableGenerator.gridRows):
            for col in range(self.__gaTableGenerator.gridCols):
                if bestIndividual.getTables()[row][col] == 1:
                    table = Table(0, self.__gaTableGenerator.gridCols - 1, 0, self.__gaTableGenerator.gridRows - 1, self.__cellSize, self.__paintOffset)
                    table.setX(col)
                    table.setY(row)
                    self.__drawableManager.add(table)

    def __ask(self, info):
        window = Tk()
        window.attributes('-topmost', 'true')
        window.wm_withdraw()
        result = messagebox.askquestion(info + '\n', "Czy nowa generacja?", parent=window)
        window.destroy()
        return result == 'yes'

    def __askIfAgain(self):
        window = Tk()
        window.attributes('-topmost', 'true')
        window.wm_withdraw()
        result = messagebox.askquestion("Potwierdź", "Czy powtórzyć proces?", parent=window)
        window.destroy()
        return result == 'yes'

    def __plot(self):
        plot = Plots(self.__gaTableGenerator.currentGenerationNumber,
                     self.__gaTableGenerator.bestFitnesses, self.__gaTableGenerator.bestTables,
                     self.__gaTableGenerator.worstFitnesses, self.__gaTableGenerator.worstTables,
                     self.__defaults.getInfo())
        plot.draw()

    def run(self):
        while self.__runThread:
            again = True
            GADialog(self.__defaults)
            self.__gaTableGenerator.firstPopulation()
            while again:
                self.__drawableManager.delTables()
                self.__geneticTables()
                self.__drawableManager.forceRepaint()
                if self.__gaTableGenerator.canGenerate():
                    if self.__gaTableGenerator.currentGenerationNumber % self.__defaults.runInfoFold != 0 or\
                            self.__ask(self.__gaTableGenerator.getBestIndividual().getInfo(self.__gaTableGenerator.currentGenerationNumber)):
                        self.__gaTableGenerator.makeNextGeneration()
                    else:
                        self.__drawableManager.start()
                        self.stop()
                        again = False
                        self.__plot()
                else:
                    self.__plot()
                    if not self.__askIfAgain():
                        self.__drawableManager.start()
                        self.stop()
                    again = False



    def stop(self):
        self.__runThread = False
