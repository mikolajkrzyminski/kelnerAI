import random
import math
from queue import PriorityQueue
from src.algorithms.GATableGenerator.Individual import Individual
from src.algorithms.AStar.Finder import Finder
from gui.GAdialog.GADefaults import CrossingOverMethod, MutationMethod, SelectionMethod


class GATableGenerator:

    def __init__(self, gridCols, gridRows, params):
        self.gridCols = gridCols
        self.gridRows = gridRows
        self.params = params
        self.currentGenerationNumber = 0
        self.population = None
        self.bestFitnesses = []
        self.worstFitnesses = []
        self.bestTables = []
        self.worstTables = []

    def generateTables(self):
        table = [[0] * self.gridCols for i in range(self.gridRows)]
        for _ in range(self.params.runTablesCount):
            isPositionUnique = False
            while not isPositionUnique:
                x = random.randint(0, self.gridCols - 1)
                y = random.randint(0, self.gridRows - 1)
                if (x, y) not in self.params.forbiddenPlaces and table[y][x] == 0:
                    isPositionUnique = True
                    table[y][x] = 1
        return table

    def getIndividual(self, table):
        origin = (7, 4)
        finder = Finder(table)
        fitnessScore = 0
        tablesCount = 0
        for y in range(self.gridRows):
            for x in range(self.gridCols):
                if table[y][x] == 1:
                    tablesCount += 1
                    targets = finder.getNeighbours((x, y), False)
                    for target in targets:
                        if origin == target:
                            fitnessScore += 1
                            break
                        else:
                            path = finder.getPath(origin, target, True)
                            if path != []:
                                fitnessScore += 1
                                break
        individual = Individual(table, fitnessScore - (tablesCount - fitnessScore), tablesCount)
        return individual

    def updateStats(self):
        bestIndividual = self.getBestIndividual()
        worstIndividual = self.getWorstIndividual()
        self.bestFitnesses.append(bestIndividual.getFitness())
        self.bestTables.append(bestIndividual.getTablesCount())
        self.worstFitnesses.append(worstIndividual.getFitness())
        self.worstTables.append(worstIndividual.getTablesCount())

    def firstPopulation(self):
        self.population = PriorityQueue()
        for _ in range(self.params.runPopulationSize):
            self.population.put(self.getIndividual(self.generateTables()))
        self.currentGenerationNumber = 0
        self.bestFitnesses = []
        self.worstFitnesses = []
        self.bestTables = []
        self.worstTables = []
        self.updateStats()

    def getPopulationQueue(self):
        queue = PriorityQueue()
        for item in self.population.queue:
            queue.put(item)
        return queue

    def getPopulationSortedArray(self):
        queue = self.getPopulationQueue()
        array = []
        while not queue.empty():
            array.append(queue.get())
        return array

    def arrayToQueue(self, array):
        queue = PriorityQueue()
        for item in array:
            queue.put(item)
        return queue

    def selectParentsByRoulette(self):
        populationArray = self.getPopulationSortedArray()
        parents = []
        delta = populationArray[len(populationArray) - 1].getFitness()
        if delta > 0:
            delta = 0
        else:
            delta = abs(delta) + 1
        fitnessSum = 0
        for individual in populationArray:
            fitnessSum += individual.getFitness() + delta
        for _ in range(2):
            draw = random.uniform(0, 1)
            accumulated = 0
            for individual in populationArray:
                probability = float(individual.getFitness() + delta) / fitnessSum
                accumulated += probability
                if draw <= accumulated:
                    parents.append(individual)
                    fitnessSum -= (individual.getFitness() + delta)
                    populationArray.remove(individual)
                    break
        return parents

    def selectParentsByTournament(self):
        parents = []
        competitorsNum = math.ceil(0.25 * self.params.runPopulationSize)
        if competitorsNum < self.params.minPopulationSize:
            competitorsNum = self.params.minPopulationSize - 1
        population = self.getPopulationSortedArray()
        parent = self.arrayToQueue(random.sample(population, competitorsNum)).get()
        population.remove(parent)
        parents.append(parent)
        parents.append(self.arrayToQueue(random.sample(population, competitorsNum)).get())
        return parents

    def quadrant(self, parentL, parentR):
        childTables = [[0] * self.gridCols for i in range(self.gridRows)]
        for row in range(self.gridRows):
            for col in range(self.gridCols):
                if (row <= math.floor((self.gridRows - 1) / 2.0)) and (col <= math.ceil((self.gridCols - 1) / 2.0)) or \
                        (row > math.floor((self.gridRows - 1) / 2.0)) and (col > math.ceil((self.gridCols - 1) / 2.0)):
                    childTables[row][col] = parentL.getTables()[row][col]
                else:
                    childTables[row][col] = parentR.getTables()[row][col]
        return childTables

    def singleVerticalDiv(self, parentL, parentR):
        childTables = [[0] * self.gridCols for i in range(self.gridRows)]
        divX = random.randint(1, self.gridCols - 2)
        for row in range(self.gridRows):
            for col in range(self.gridCols):
                if col <= divX:
                    childTables[row][col] = parentL.getTables()[row][col]
                else:
                    childTables[row][col] = parentR.getTables()[row][col]
        return childTables

    def singleHorizontalDiv(self, parentL, parentR):
        childTables = [[0] * self.gridCols for i in range(self.gridRows)]
        divY = random.randint(1, self.gridRows - 2)
        for row in range(self.gridRows):
            for col in range(self.gridCols):
                if row <= divY:
                    childTables[row][col] = parentL.getTables()[row][col]
                else:
                    childTables[row][col] = parentR.getTables()[row][col]
        return childTables

    def doubleVerticalDiv(self, parentL, parentR):
        childTables = [[0] * self.gridCols for i in range(self.gridRows)]
        divC = math.ceil((self.gridCols - 1) / 2)
        divX1 = random.randint(1, divC - 1)
        divX2 = random.randint(divC + 1, self.gridCols - 2)
        for row in range(self.gridRows):
            for col in range(self.gridCols):
                if divX1 <= col < divX2:
                    childTables[row][col] = parentL.getTables()[row][col]
                else:
                    childTables[row][col] = parentR.getTables()[row][col]
        return childTables

    def doubleHorizontalDiv(self, parentL, parentR):
        childTables = [[0] * self.gridCols for i in range(self.gridRows)]
        divC = math.ceil((self.gridRows - 1) / 2)
        divY1 = random.randint(1, divC - 1)
        divY2 = random.randint(divC + 1, self.gridRows - 2)
        for row in range(self.gridRows):
            for col in range(self.gridCols):
                if divY1 <= row < divY2:
                    childTables[row][col] = parentL.getTables()[row][col]
                else:
                    childTables[row][col] = parentR.getTables()[row][col]
        return childTables

    def randomChoice(self, parentL, parentR):
        childTables = [[0] * self.gridCols for i in range(self.gridRows)]
        parents = [parentL.getTables(), parentR.getTables()]
        for row in range(self.gridRows):
            for col in range(self.gridCols):
                childTables[row][col] = random.choice(parents)[row][col]
        return childTables

    def procreate(self):
        if self.params.runSelectionMethod == SelectionMethod.Roulette:
            parentLeft, parentRight = self.selectParentsByRoulette()
        elif self.params.runSelectionMethod == SelectionMethod.Tournament:
            parentLeft, parentRight = self.selectParentsByTournament()
        child = None
        if self.params.runCrossingOverMethod == CrossingOverMethod.FixedQuadrant:
            child = self.quadrant(parentLeft, parentRight)
        elif self.params.runCrossingOverMethod == CrossingOverMethod.SingleVerticalDiv:
            child = self.singleVerticalDiv(parentLeft, parentRight)
        elif self.params.runCrossingOverMethod == CrossingOverMethod.SingleHorizontalDiv:
            child = self.singleHorizontalDiv(parentLeft, parentRight)
        elif self.params.runCrossingOverMethod == CrossingOverMethod.DoubleVerticalDiv:
            child = self.doubleVerticalDiv(parentLeft, parentRight)
        elif self.params.runCrossingOverMethod == CrossingOverMethod.DoubleHorizontalDiv:
            child = self.doubleHorizontalDiv(parentLeft, parentRight)
        elif self.params.runCrossingOverMethod == CrossingOverMethod.RandomChoice:
            child = self.randomChoice(parentLeft, parentRight)
        return child

    def getRandTuple(self):
        isPlaceAvailable = False
        while not isPlaceAvailable:
            randX = random.randint(0, self.gridCols - 1)
            randY = random.randint(0, self.gridRows - 1)
            isPlaceAvailable = (randX, randY) not in self.params.forbiddenPlaces
        return randX, randY

    def mutateFlip(self, tables):
        mutatedTables = tables
        numberOfMutation = random.randint(0, self.params.runMutation)
        for _ in range(numberOfMutation):
            randX, randY = self.getRandTuple()
            if mutatedTables[randY][randX] == 1:
                mutatedTables[randY][randX] = 0
            else:
                mutatedTables[randY][randX] = 1
        return mutatedTables

    def mutateSwap(self, tables):
        mutatedTables = tables
        numberOfMutation = random.randint(0, self.params.runMutation)
        for _ in range(numberOfMutation):
            randX1, randY1 = self.getRandTuple()
            randX2, randY2 = self.getRandTuple()
            value = mutatedTables[randY1][randX1]
            mutatedTables[randY1][randX1] = mutatedTables[randY2][randX2]
            mutatedTables[randY2][randX2] = value
        return mutatedTables

    def makeNextGeneration(self):
        tablesArray = []
        eliteSize = math.ceil((self.params.runPopulationSize * self.params.runElitism) / 100.0)
        for _ in range(self.params.runPopulationSize - eliteSize):
            if self.params.runMutationMethod == MutationMethod.Flip:
                mutated = self.mutateFlip(self.procreate())
            elif self.params.runMutationMethod == MutationMethod.Swap:
                mutated = self.mutateSwap(self.procreate())
            tablesArray.append(mutated)
        eliteArray = []
        for _ in range(eliteSize):
            eliteArray.append(self.population.get())
        self.population = PriorityQueue()
        for individual in eliteArray:
            self.population.put(individual)
        for table in tablesArray:
            self.population.put(self.getIndividual(table))
        self.currentGenerationNumber += 1
        self.updateStats()

    def canGenerate(self):
        return self.currentGenerationNumber < self.params.runGenerationsNumber

    def getBestIndividual(self):
        population = self.getPopulationQueue()
        return population.get()

    def getWorstIndividual(self):
        population = self.getPopulationSortedArray()
        return population[len(population) - 1]

    def printBest(self):
        populationBest = self.getBestIndividual()
        populationBest.print(self.currentGenerationNumber)

    def printPopulation(self):
        queue = self.getPopulationQueue()
        while not queue.empty():
            individual = queue.get()
            individual.print(self.currentGenerationNumber)
        print('---------------------------------------')

    def makeAllGenerations(self):
        self.printBest()
        while self.canGenerate():
            self.makeNextGeneration()
            self.printBest()
