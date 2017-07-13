from random import randint
from BaseAI import BaseAI

class ComputerAI(BaseAI):
    def getMove(self, grid):
        cells = grid.getAvailableCells()
        if cells:
        	return cells[randint(0, len(cells) - 1)]
        else:
        	return None
