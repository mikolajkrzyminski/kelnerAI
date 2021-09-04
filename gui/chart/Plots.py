import matplotlib.pyplot as plt


class Plots:

    def __init__(self, generationNumber, bestFitnesses, bestTabless, worstFitnesses, worstTables, title):
        self.__generationsNumber = generationNumber
        self.__bestFitnesses = bestFitnesses
        self.__bestTables = bestTabless
        self.__worstTables = worstTables
        self.__worstFitnesses = worstFitnesses
        self.__title = title

    def draw(self):
        generations = [i for i in range(self.__generationsNumber + 1)]
        plt.figure(num = self.__title)
        plt.plot(generations, self.__bestTables, label = "best tables")
        plt.plot(generations, self.__worstTables, label = "worst tables")
        plt.plot(generations, self.__bestFitnesses, label = "best fitness")
        plt.plot(generations, self.__worstFitnesses, label = "worst fitness")
        plt.legend()
        plt.show()
