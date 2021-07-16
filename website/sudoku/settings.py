import requests

WIDTH = 600
HEIGHT = 600


#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (96, 216, 232)
PURPLE = (118, 7, 237)
LOCKEDCELLCOLOR = (189, 189, 189)
INCORRECTCELLCOLOR = (195, 121, 121)
RED = (255, 0, 0)

#Boards
testBoard1 = [[0 for x in range(9)] for x in range(9)]
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
board = response.json()['board']
finishedBoard =  [[0,3,4,6,7,8,9,1,2],
                 [6,7,2,1,9,5,3,4,8],
                 [1,9,8,3,4,2,5,6,7],
                 [8,5,9,7,6,1,4,2,3],
                 [4,2,6,8,5,3,7,9,1],
                 [7,1,3,9,2,4,8,5,6],
                 [9,6,1,5,3,7,2,8,4],
                 [2,8,7,4,1,9,6,3,5],
                 [3,4,5,2,8,6,1,7,9]]


#Positions and sizes
gridPos = (75,100)
cellSize = 50
gridSize = cellSize * 9