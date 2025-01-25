import pygame
import copy

# The Sudoku puzzle must be given in this format where '0' represents empty squares
SUDOKU_PUZZLE: list[list[int]] = [
    [3, 0, 0, 8, 0, 1, 0, 0, 2],
    [2, 0, 1, 0, 3, 0, 6, 0, 4],
    [0, 0, 0, 2, 0, 4, 0, 0, 0],
    [8, 0, 9, 0, 0, 0, 1, 0, 6],
    [0, 6, 0, 0, 0, 0, 0, 5, 0],
    [7, 0, 2, 0, 0, 0, 4, 0, 9],
    [0, 0, 0, 5, 0, 9, 0, 0, 0],
    [9, 0, 4, 0, 8, 0, 7, 0, 5],
    [6, 0, 0, 1, 0, 7, 0, 0, 3]
]

class AI:
    def __init__(self) -> None:
        self.board = copy.deepcopy(SUDOKU_PUZZLE)
        self.freeCells = []
        self.possibleSolves = {}

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    self.freeCells.append((row, col))
                    self.possibleSolves[(row, col)] = list(self.checkPossible(row, col))

        self.solveBoard()

    def checkPossible(self, x: int, y: int) -> set[int]:
        possible = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            
        for i in range(9):
            if self.board[i][y] in possible:
                possible.remove(self.board[i][y])

            if self.board[x][i] in possible:
                possible.remove(self.board[x][i])

        cellBlockX = (x // 3) * 3
        cellBlockY = (y // 3) * 3

        for addX in range(3):
            for addY in range(3):
                if self.board[cellBlockX + addX][cellBlockY + addY] in possible:
                    possible.remove(self.board[cellBlockX + addX][cellBlockY + addY])

        return possible
    
    def canPlace(self, x: int, y:int, val: int) -> bool:

        for i in range(9):
            if self.board[i][y] == val or self.board[x][i] == val:
                return False
            
        cellBlockX = (x // 3) * 3
        cellBlockY = (y // 3) * 3
        
        for addX in range(3):
            for addY in range(3):
                if self.board[cellBlockX + addX][cellBlockY + addY] == val:
                    return False
                
        return True

    def solveBoard(self) -> None:
        def solveOnes():
            _tempDict = copy.deepcopy(self.possibleSolves)
            for cell in _tempDict:
                x = cell[0]
                y = cell[1]

                opts = self.possibleSolves[cell]

                if len(opts) == 1 and self.board[x][y] == 0:
                    self.placeChoice(x, y, opts[0])
                    self.possibleSolves.pop(cell)

        solveOnes()
        allCells = list(self.possibleSolves.keys())
        size = len(allCells) - 1
        idx = 0

        while idx <= size and idx >= 0:
            isPlaced: bool = False
            cell: tuple = allCells[idx]
            x = cell[0]
            y = cell[1]
            values: list = self.possibleSolves[cell]
            valIdx: int = 0

            if self.board[x][y] != 0:
                valIdx = values.index(self.board[x][y])

            while valIdx <= len(values) - 1:
                if self.canPlace(x, y, values[valIdx]):
                    self.placeChoice(x, y, values[valIdx])
                    isPlaced = True
                    break
                else: valIdx += 1

            if isPlaced: idx += 1
            else:
                self.board[x][y] = 0 
                idx -= 1

    def placeChoice(self, xCord: int, yCord: int, value: int) -> None:
        self.board[xCord][yCord] = value
        updateDisplay(self.board)
        pygame.time.delay(100)

pygame.init()
SCREEN_SIZE = 450
CELL_SIZE = SCREEN_SIZE // 9

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Sudoku Solver")
font = pygame.font.Font(None, 40)

def drawGrid():
    for i in range(10):
        lineWidth = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, (255, 255, 255), (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE), lineWidth)
        pygame.draw.line(screen, (255, 255, 255), (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE), lineWidth)

def updateDisplay(board):
    screen.fill((0, 0, 0))
    drawGrid()
    for row in range(9):
        for col in range(9):
            value = board[row][col]
            if value != 0:
                text = font.render(str(value), True, (255, 255, 255))
                textRect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, textRect)
    pygame.display.flip()

def main():
    solve = AI()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    updateDisplay(SUDOKU_PUZZLE)
    main()
