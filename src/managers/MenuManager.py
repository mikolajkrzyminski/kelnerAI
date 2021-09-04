import random


# contains all dishes and generates random order for the table
class MenuManager:

    # consts, min and max dishes ordered by the people sitting by the same table
    __MinDishes = 1
    __MaxDishes = 3

    def __init__(self):
        self.__menuCard = ["PORK",
                           "FRENCH FRIES",
                           "PIZZA",
                           "CHICKEN",
                           "RIBS",
                           "FISH",
                           "SPAGHETTI",
                           "BEEF",
                           "STEAK",
                           "SALAD",
                           "GRILLED VEGETABLES",
                           "VEAL",
                           "CHOPS",
                           "EMPTY PLATE",
                           "BEER",
                           "CAKE"]

    # generator
    def generateOrder(self):
        count = random.randint(self.__MinDishes, self.__MaxDishes)
        order = []
        for _ in range(0, count):
            order += [(self.__menuCard[random.randint(0, len(self.__menuCard) - 1)])]
        return order
