import tkinter
from tkinter import *

from gui.GAdialog.GADefaults import CrossingOverMethod


class GADialog:

    def __init__(self, defaults):
        self.__defaults = defaults
        self.window = tkinter.Tk()
        self.window.attributes('-topmost', 'true')
        self.window.title(defaults.windowName)
        self.__sliderTablesCount = self.__getSlider(0, defaults.minTablesCount, defaults.maxTablesCount, defaults.runTablesCount, defaults.sliderNameTablesCount)
        self.__sliderPopulationSize = self.__getSlider(1, defaults.minPopulationSize, defaults.maxPopulationSize, defaults.runPopulationSize, defaults.sliderNamePopulationSize)
        self.__sliderMutation = self.__getSlider(2,  defaults.minMutation, defaults.maxMutation, defaults.runMutation, defaults.sliderNameMutation)
        self.__sliderGenerationsNumber = self.__getSlider(3, defaults.minGenerationsNumber, defaults.maxGenerationsNumber, defaults.runGenerationsNumber, defaults.sliderNameGenerationsNumber)
        self.__sliderInfoFold = self.__getSlider(4, defaults.minGenerationsNumber,  defaults.maxGenerationsNumber, defaults.runInfoFold, defaults.sliderInfoFold)
        self.__sliderElitism = self.__getSlider(5, defaults.minElitism, defaults.maxElitism, defaults.runElitism, defaults.sliderElitismName)

        self.__radioSelectionMethodValue = IntVar()
        self.__radioSelectionMethodValue.set(self.__defaults.runSelectionMethod)
        self.__getRadioButton(6, defaults.defSelectionMethods, self.__radioSelectionMethodValue, defaults.radioSelectionMethodName)

        self.__radioCrossingOverMethodValue = IntVar()
        self.__radioCrossingOverMethodValue.set(self.__defaults.runCrossingOverMethod)
        self.__getRadioButton(8, defaults.defCrossingOverMethods, self.__radioCrossingOverMethodValue, defaults.radioCrossingOverMethodName)

        self.__radioMutationMethodValue = IntVar()
        self.__radioMutationMethodValue.set(self.__defaults.runMutationMethod)
        self.__getRadioButton(12, defaults.defMutationMethods, self.__radioMutationMethodValue, defaults.radioMutationMethodName)

        self.__buttonDefaults = self.__getButton(15, 0, W, defaults.buttonDefaultsName, self.__setDefaults)
        self.__buttonStart = self.__getButton(15, 1, E,  defaults.buttonStartName, self.__getAllValues)
        self.window.mainloop()
        
    def __getSlider(self, rowNum, minVal, maxVal, runVal, labText):
        label = Label(self.window, text = labText)
        label.grid(row = rowNum, column = 0, sticky = S + W, padx = 5, pady = 5)
        slider = Scale(self.window, variable = IntVar(), from_ = minVal, to = maxVal, orient=HORIZONTAL, length = 200)
        slider.grid(row = rowNum, column = 1, sticky = E, padx = 5, pady = 3)
        slider.set(runVal)
        return slider

    def __getButton(self, rowNum, colNum, stickPos, btnText, action):
        button = Button(self.window, text = btnText, command = action)
        button.grid(row = rowNum, column = colNum, stick = stickPos, columnspan = 2, padx=60, pady=5)
        return button

    def __getRadioButton(self, rowNum, methods, variable, labText):
        label = LabelFrame(self.window, text = labText)
        label.grid(row=rowNum, column=0, columnspan=2,  padx=5, pady=5, sticky=W)
        rowNum += 1
        iteration = 0
        for text, mode in methods:
            radio = Radiobutton(label, text = text, variable = variable, value = mode)
            radio.grid(row = rowNum, column = iteration % 2, sticky = W, padx = 5, pady = 3)
            rowNum += iteration % 2
            iteration += 1

    def __setDefaults(self):
        self.__sliderTablesCount.set(self.__defaults.defTablesCount)
        self.__sliderPopulationSize.set(self.__defaults.defPopulationSize)
        self.__sliderMutation.set(self.__defaults.defMutation)
        self.__sliderGenerationsNumber.set(self.__defaults.defGenerationsNumber)
        self.__sliderInfoFold.set(self.__defaults.defInfoFold)
        self.__sliderElitism.set(self.__defaults.defElitism)
        self.__radioSelectionMethodValue.set(self.__defaults.defSelectionMethod)
        self.__radioCrossingOverMethodValue.set(self.__defaults.defCrossingOverMethod)
        self.__radioMutationMethodValue.set(self.__defaults.defMutationMethod)

    def __getAllValues(self):
        self.__defaults.runTablesCount = self.__sliderTablesCount.get()
        self.__defaults.runPopulationSize = self.__sliderPopulationSize.get()
        self.__defaults.runMutation = self.__sliderMutation.get()
        self.__defaults.runGenerationsNumber = self.__sliderGenerationsNumber.get()
        self.__defaults.runInfoFold = self.__sliderInfoFold.get()
        self.__defaults.runElitism = self.__sliderElitism.get()
        self.__defaults.runSelectionMethod = self.__radioSelectionMethodValue.get()
        self.__defaults.runCrossingOverMethod = self.__radioCrossingOverMethodValue.get()
        self.__defaults.runMutationMethod = self.__radioMutationMethodValue.get()
        self.window.destroy()
