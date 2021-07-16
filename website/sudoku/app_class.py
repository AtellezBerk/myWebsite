from bs4 import BeautifulSoup
from website.sudoku.settings import *
from website.sudoku.buttonClass import *
from copy import deepcopy


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = board
        self.selected = None
        self.mousePos = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.playingButtons = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont("comicsans", cellSize // 2)
        self.grid = []
        self.getPuzzle("2")
        self.load()
        self.board_copy = None
        self.check_once = False

    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()

    ###### PLAYING STATE FUNCTIONS #####

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


            if not self.check_once:
                self.checkAllCells()
                self.check_once = True

            # User clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playingButtons:
                        if button.highlighted:
                            button.click()

            # User types a key
            if event.type == pygame.KEYDOWN:
                x = self.selected[0]
                y = self.selected[1]
                if self.selected is not None and [x, y] not in self.lockedCells:
                    if self.isInt(event.unicode):
                        # cell changed

                        self.grid[y][x] = int(event.unicode)
                        self.cellChanged = True

    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)

        if self.cellChanged:
            self.incorrectCells = []
            if self.allCellsDone():
                # Check if board is correct
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    self.finished = True

    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)

        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.incorrectCells)

        if self.selected and self.selected not in self.lockedCells:
            temp_num = self.grid[self.selected[1]][self.selected[0]]
            if temp_num != 0:
                for y, row in enumerate(self.grid):
                    for x, num in enumerate(row):
                        if self.grid[x][y] == temp_num:
                            self.highlightNum(self.window, (y, x))

        self.drawNumbers(self.window)

        self.drawGrid(self.window)
        pygame.display.update()
        self.cellChanged = False

    ##### BOARD CHECKING FUNCTIONS #####
    def allCellsDone(self):
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    def checkAllCells(self):
        if self.board_copy is None:
            self.board_copy = deepcopy(self.grid)

            self.solve()

        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] != 0 and self.grid[i][j] != self.board_copy[i][j]:
                    self.incorrectCells.append([j, i])

    def solve(self):
        find = find_empty(self.board_copy, self.incorrectCells)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.board_copy, i, (row, col)):
                self.board_copy[row][col] = i

                if self.solve():
                    return True

                self.board_copy[row][col] = 0

        return False

    ##### HELPER FUNCTIONS #####
    def getPuzzle(self, difficulty):
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
        soup = BeautifulSoup(html_doc)
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f10', 'f11',
               'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f20', 'f21', 'f22', 'f23',
               'f24', 'f25', 'f26', 'f27', 'f28', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35',
               'f36', 'f37', 'f38', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47',
               'f48', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f60',
               'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f70', 'f71', 'f72',
               'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f80', 'f81', 'f82', 'f83', 'f84',
               'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index // 9][index % 9] = int(cell['value'])
            except:
                pass
        self.grid = board
        self.board_copy = None
        self.load()

    def shadeIncorrectCells(self, window, incorrect):
        for cell in incorrect:
            pygame.draw.rect(window, INCORRECTCELLCOLOR,
                             (cell[0] * cellSize + gridPos[0], cell[1] * cellSize + gridPos[1], cellSize, cellSize))

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLCOLOR,
                             (cell[0] * cellSize + gridPos[0], cell[1] * cellSize + gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        for y, row in enumerate(self.grid):
            for x, num in enumerate(row):
                if num != 0:
                    pos = [(x * cellSize) + gridPos[0], (y * cellSize) + gridPos[1]]
                    self.textToScreen(window, str(num), pos)

    # Draw on certain position
    def drawNumber(self, window, x, y, num):
        pos = [(x * cellSize) + gridPos[0], (y * cellSize) + gridPos[1]]
        if num != 0:
            self.textToScreen(window, str(num), pos)
        else:
            pygame.draw.rect(window, WHITE,
                             ((x * cellSize) + gridPos[0], (y * cellSize) + gridPos[1], cellSize, cellSize))
            # Draw rectangle
            pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]),
                             (gridPos[0] + (x * cellSize), gridPos[1] + 450), 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (y * cellSize)),
                             (gridPos[0] + 450, gridPos[1] + +(y * cellSize)), 2 if y % 3 == 0 else 1)

    def drawSelection(self, window, pos):
        pygame.draw.rect(window, LIGHTBLUE,
                         ((pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))

    def highlightNum(self, window, pos):

        pygame.draw.rect(window, PURPLE,
                         ((pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)
        for x in range(9):
            pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]),
                             (gridPos[0] + (x * cellSize), gridPos[1] + 450), 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)),
                             (gridPos[0] + 450, gridPos[1] + +(x * cellSize)), 2 if x % 3 == 0 else 1)

    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1] + gridSize:
            return False
        return ((self.mousePos[0] - gridPos[0]) // cellSize, (self.mousePos[1] - gridPos[1]) // cellSize)

    def loadButtons(self):
        self.playingButtons.append(Button(20, 40, WIDTH // 7, 40,
                                          function=self.checkAllCells,
                                          color=(207, 68, 68),
                                          text="Check"))
        self.playingButtons.append(Button(140, 40, WIDTH // 7, 40,
                                          color=(27, 142, 207),
                                          function=self.getPuzzle,
                                          params="1",
                                          text="Easy"))
        self.playingButtons.append(Button(WIDTH // 2 - (WIDTH // 7) // 2, 40, WIDTH // 7, 40,
                                          color=(27, 142, 207),
                                          function=self.getPuzzle,
                                          params="2",
                                          text="Medium"))
        self.playingButtons.append(Button(380, 40, WIDTH // 7, 40,
                                          color=(27, 142, 207),
                                          function=self.getPuzzle,
                                          params="3",
                                          text="Hard"))
        self.playingButtons.append(Button(500, 40, WIDTH // 7, 40,
                                          color=(27, 142, 207),
                                          function=self.getPuzzle,
                                          params="4",
                                          text="Evil"))
        self.playingButtons.append(Button(WIDTH // 2 - (WIDTH // 7) // 2, 555, 600 // 7, 40,
                                          color=(240, 86, 14),
                                          function=self.solve_board,
                                          params=0,
                                          text="Give up?"))

    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    def load(self):
        self.playingButtons = []
        self.loadButtons()
        self.lockedCells = []
        self.incorrectCells = []
        self.finished = False

        # Setting locked cells from original board
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx, yidx])

    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False

    def solve_board(self):
        for pos in self.incorrectCells:
            self.grid[pos[0]][pos[1]] = 0
            self.drawNumber(self.window, pos[0], pos[1], 0)
        self.incorrectCells.clear()

        find = find_empty(self.grid, self.incorrectCells)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if valid(self.grid, i, (row, col)):
                self.grid[row][col] = i
                self.drawNumber(self.window, col, row, i)
                pygame.display.update()
                #pygame.time.delay(10)

                if self.solve_board():
                    return True

                self.grid[row][col] = 0
                self.drawNumber(self.window, col, row, 0)
                pygame.display.update()

        return False


def find_empty(board, incorrectCells):
    for pos in incorrectCells:
        board[pos[0]][pos[1]] = 0
    incorrectCells.clear()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def run_game():
    app = App()
    app.run()



