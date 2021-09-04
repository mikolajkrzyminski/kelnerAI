import os
import platform
from tkinter import Frame, TOP, TclError

import pygame
from src.managers.ImageCache import ImageCache, Images


class GridBoard:

    def __init__(self, _width, _height):
        """
        embed = Frame(window, width=_width, height=_height)
        embed.pack(side=TOP)
        # some SDL magic (don't know how and why this works tbh)
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        """

        pygame.init()  # initialize the pygame
        pygame.display.set_caption("Bardzo mądry kelner")  # window caption
        self.__width = _width
        self.__height = _height
        self.__screen = pygame.display.set_mode((_width, _height))  # initialize screen

    # draws the background
    def reinitialize(self):
        imageBackground = ImageCache.getInstance().getImage(Images.Background, self.__width, self.__height)
        self.__screen.blit(imageBackground, (0, 0))
        """ # code below fills the screen with white and draws grid
        self.__screen.fill((255, 255, 255))
        for x in range(0, self.__width, self.__cellSize):
            pygame.draw.line(self.__screen, (0,0,0), (x,0), (x,(self.__height - 1)))
        for y in range(0, self.__height, self.__cellSize):
            pygame.draw.line(self.__screen, (0,0,0), (0,y), ((self.__width - 1),y))
        """

    # draws object on screen
    def draw(self, component):
        component.draw(self.__screen)

    # updates screen
    def udpdate(self):
        pygame.display.update()
        """
        try:
            self.__window.update()
        except TclError:
            pass
        """
