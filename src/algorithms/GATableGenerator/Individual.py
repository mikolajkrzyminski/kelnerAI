class Individual:

    def __init__(self, table, fitnessScore, tablesCount):
        self.__table = table
        self.__fitnessScore = fitnessScore
        self.__tablesCount = tablesCount

    # operator (>) for PriorityQueue comparison (determines the objects order)
    def __gt__(self, other):
        return self.__fitnessScore < other.__fitnessScore

    def getTables(self):
        return self.__table

    def getTablesCount(self):
        return self.__tablesCount

    def getFitness(self):
        return self.__fitnessScore

    def getInfo(self, generation):
        return f"GENERATION: {generation}, FITNESS: {self.__fitnessScore}, TABLES: {self.__tablesCount}"

    def print(self, generation):
        print(self.getInfo(generation))
        cols = len(self.__table[0])
        rows = len(self.__table)
        for row in range(rows):
            for col in range(cols):
                v = self.__table[row][col]
                v = ' ' if v == 0 else '#' if v == 1 else 'O'
                print('|', v, sep='', end='')
            print('|')