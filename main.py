import pygame

from src.components.GridBoard import GridBoard
from src.components.Waiter import Waiter
from src.managers.DrawableCollection import DrawableCollection

# create screen consts
from src.managers.TableGenerator import TableGenerator

Scale        = 1.5                  # scale for all images used within project
CellSize     = round(50 * Scale)  # pixel size of 1 square cell in the grid
PaintOffset  = CellSize           # pixel size of paint offset for all drawables
GridCountX   = 15                 # number of columns in grid
GridCountY   = 9                  # number of rows in grid
ScreenWidth  = CellSize * GridCountX + 2 * PaintOffset  # screen width in pixels
ScreenHeight = CellSize * GridCountY + 2 * PaintOffset  # screen height in pixels

# initialize background
gridBoard = GridBoard(ScreenWidth, ScreenHeight)

# initialize drawable objects manager
drawableManager = DrawableCollection()

# initialize waiter component
waiter1 = Waiter(7, 4, 0, GridCountX - 1, 0, GridCountY - 1, CellSize, PaintOffset)
"""
waiter2 = Waiter(0, GridCountY - 1, 0, GridCountX - 1, 0, GridCountY - 1, CellSize, PaintOffset)
waiter3 = Waiter(GridCountX - 1, 0, 0, GridCountX - 1, 0, GridCountY - 1, CellSize, PaintOffset)
waiter4 = Waiter(GridCountX - 1, GridCountY - 1, 0, GridCountX - 1, 0, GridCountY - 1, CellSize, PaintOffset)
"""

# adds waiter to drawable collection
drawableManager.add(waiter1)
"""
drawableManager.add(waiter2)
drawableManager.add(waiter3)
drawableManager.add(waiter4)
"""
# drawableManager.start()

tableGenerator = TableGenerator(GridCountX, GridCountY, 1, GridCountX - 2, 1, GridCountY - 2, CellSize, PaintOffset, drawableManager)
tableGenerator.start()

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tableGenerator.stop()
            drawableManager.stop()
            running = False

    # repaints all objects to the screen
    # is set only on initial paint or after keyboard event or call to forceRepaint()
    if drawableManager.mustRepaint():
        gridBoard.reinitialize()
        gridBoard.draw(drawableManager)
        gridBoard.udpdate()
