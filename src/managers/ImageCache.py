import pygame
from enum import Enum


# images enum
class Images(Enum):
    Background = 0
    WaiterLeftUp = 1
    WaiterUp = 2
    WaiterRightUp = 3
    WaiterRight = 4
    WaiterRightDown = 5
    WaiterDown = 6
    WaiterLeftDown = 7
    WaiterLeft = 8
    Table = 9
    Menu = 10
    Check = 11
    Plate = 12
    Guest1 = 13
    Guest2 = 14
    Guest3 = 15
    ToolTip = 16


class ImageCache:
    __instance = None

    @staticmethod
    def getInstance():
        if ImageCache.__instance is None:
            ImageCache()
        return ImageCache.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ImageCache.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ImageCache.__instance = self
            self.__font = None
            self.__images = {}
            self.__paths = {Images.Background:       './images/Backgroud.png',
                            Images.WaiterLeftUp:     './images/kelner_full_LU.png',
                            Images.WaiterUp:         './images/kelner_full_U.png',
                            Images.WaiterRightUp:    './images/kelner_full_RU.png',
                            Images.WaiterRight:      './images/kelner_full_R.png',
                            Images.WaiterRightDown:  './images/kelner_full_RD.png',
                            Images.WaiterDown:       './images/kelner_full_D.png',
                            Images.WaiterLeftDown:   './images/kelner_full_LD.png',
                            Images.WaiterLeft:       './images/kelner_full_L.png',
                            Images.Table:            './images/stol.png',
                            Images.Menu:             './images/ksiazka.png',
                            Images.Check:            './images/check.png',
                            Images.Plate:            './images/plate.png',
                            Images.Guest1:           './images/wiking_blond.png',
                            Images.Guest2:           './images/wiking_rudy.png',
                            Images.Guest3:           './images/wiking_rudy2.png',
                            Images.ToolTip:          './images/tooltip.png'}

    def __getFont(self):
        if self.__font is None:
            self.__font = pygame.font.SysFont('comicsansms', 24, True)
        return self.__font

    def getImage(self, imageKind, width, height):
        key = imageKind.name + ':' + str(width) + 'x' + str(height)
        image = self.__images.get(key, None)
        if image is None:
            image = pygame.transform.scale((pygame.image.load(self.__paths[imageKind])), (width, height))
            self.__images[key] = image
        return image

    def getTextImage(self, text, color, height):
        key = text + ':' + str(color) + 'x' + str(height)
        image = self.__images.get(key, None)
        if image is None:
            font = self.__getFont()
            image = font.render(text, False, color)
            size = image.get_size()
            width = int((height / size[1]) * size[0])
            height = int(height)
            image = pygame.transform.scale(image, (width, height))
            self.__images[key] = image
        return image
