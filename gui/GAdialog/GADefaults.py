from enum import Enum


class CrossingOverMethod:
    FixedQuadrant = 0
    SingleHorizontalDiv = 1
    SingleVerticalDiv = 2
    DoubleHorizontalDiv = 3
    DoubleVerticalDiv = 4
    RandomChoice = 5


class SelectionMethod:
    Roulette = 0
    Tournament = 1


class MutationMethod:
    Flip = 0
    Swap = 1


class GADefaults:

    def __init__(self):
        self.defCrossingOverMethods = [("pojedynczy poziomy", CrossingOverMethod.SingleHorizontalDiv),
                                       ("pojedynczy pionowy", CrossingOverMethod.SingleVerticalDiv),
                                       ("podwójny poziomy", CrossingOverMethod.DoubleHorizontalDiv),
                                       ("podwójny pionowy", CrossingOverMethod.DoubleVerticalDiv),
                                       ("ćwiartki", CrossingOverMethod.FixedQuadrant),
                                       ("losowe", CrossingOverMethod.RandomChoice)]


        self.defSelectionMethods = [("ruletka", SelectionMethod.Roulette),
                                   ("turniej", SelectionMethod.Tournament)]

        self.defMutationMethods = [("inwersja", MutationMethod.Flip),
                                   ("wymiana", MutationMethod.Swap)]

        self.windowName = "Algorytm genetyczny - parametry"
        self.windowGeometry = "400x400"
        
        self.minTablesCount = 1
        self.maxTablesCount = 80
        self.defTablesCount = 20
        self.runTablesCount = self.defTablesCount
        self.sliderNameTablesCount = "stoliki"
        
        self.minPopulationSize = 4
        self.maxPopulationSize = 30
        self.defPopulationSize = 5
        self.runPopulationSize = self.defPopulationSize
        self.sliderNamePopulationSize = "populacja"
        
        self.minMutation = 0
        self.maxMutation = 10
        self.defMutation = 1
        self.runMutation = self.defMutation
        self.sliderNameMutation = "mutacje"
        
        self.minGenerationsNumber = 1
        self.maxGenerationsNumber = 1000
        self.defGenerationsNumber = 20
        self.runGenerationsNumber = self.defGenerationsNumber
        self.sliderNameGenerationsNumber = "pokolenia"

        self.defInfoFold = 5
        self.runInfoFold = self.defInfoFold
        self.sliderInfoFold = "co ile"

        self.defSelectionMethod = SelectionMethod.Tournament
        self.runSelectionMethod = self.defSelectionMethod
        self.radioSelectionMethodName = "metoda selekcji"

        self.defCrossingOverMethod = CrossingOverMethod.SingleHorizontalDiv
        self.runCrossingOverMethod = self.defCrossingOverMethod
        self.radioCrossingOverMethodName = "metoda krzyżowania"

        self.defMutationMethod = MutationMethod.Swap
        self.runMutationMethod = self.defMutationMethod
        self.radioMutationMethodName = "metoda mutacji"

        self.minElitism = 0
        self.maxElitism = 50
        self.defElitism = 0
        self.runElitism = self.defElitism
        self.sliderElitismName = "elitarność [%]"

        self.forbiddenPlaces = [(7, 4)]

        self.buttonStartName = "generuj"
        self.buttonDefaultsName = "przywróć"

    def getInfo(self):
        return "populacja: " + str(self.runPopulationSize) \
            + ", pokolenia: " + str(self.runGenerationsNumber) \
            + ", stoliki: " + str(self.runTablesCount) \
            + ", mutacje: " + str(self.runMutation)
