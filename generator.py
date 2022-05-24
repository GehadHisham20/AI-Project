from random import seed, random, shuffle, randint, choice
from functools import reduce
colorList=['#ea8c61','#298c61','#aa8c61','#aa8cac','#ea6261','#FF0000','#008000','#0000FF','#FFFFF0','#808080',
           '#C0C0C0','#FFFF00','#800080','#FFA500','#800000','#FF00FF','#00FFFF','#008080','#808000','#000080']

def getSize(s):
    global size
    size=s

#----------------------------Generator-----------------------------
def operation(operator):
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

# check neighbours
def adjacent(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    dx, dy = x1 - x2, y1 - y2
    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

def generate(size):
    board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]
    for _ in range(size):
        shuffle(board)

    for c1 in range(size):
        for c2 in range(size):
            if random() > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}
    uncaged = sorted(board.keys(), key=lambda var: var[1])
    cliques = []
    while uncaged:
        cliques.append([])
        csize = randint(1, 4)
        cell = uncaged[0]
        uncaged.remove(cell)
        cliques[-1].append(cell)
        for _ in range(csize - 1):
            adjs = [other for other in uncaged if adjacent(cell, other)]
            cell = choice(adjs) if adjs else None
            if not cell:
                break
            uncaged.remove(cell)           
            cliques[-1].append(cell)
            
        csize = len(cliques[-1])
        if csize == 1:
            cell = cliques[-1][0]
            cliques[-1] = ((cell, ), '.', board[cell])
            continue
        elif csize == 2:
            fst, snd = cliques[-1][0], cliques[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/" 
            else:
                operator = "-" 
        else:
            operator = choice("+*")

        target = reduce(operation(operator), [board[cell] for cell in cliques[-1]])
        cliques[-1] = (tuple(cliques[-1]), operator, int(target))

    return cliques

def parseCagesToGuiFormat(cageList):
    w, h = size,size
    cageMatrix = [[0 for x in range(w)] for y in range(h)] 
    cageColorMatrix = [[0 for x in range(w)] for y in range(h)] 
    for i in range(len(cageList)):
        for j in range(len(cageList[i][0])):
            cageColorMatrix[cageList[i][0][j][0]-1][cageList[i][0][j][1]-1]=colorList[i%15]
            if j==0:
             cageMatrix[cageList[i][0][j][0]-1][cageList[i][0][j][1]-1]=cageList[i][1]+str(cageList[i][2])  
            else:
             cageMatrix[cageList[i][0][j][0]-1][cageList[i][0][j][1]-1]=""
    
    puzzleList=[]
    cageColorList = [] 
    for i in range(size):
        for j in range(size):
           puzzleList.append(cageMatrix[i][j])
           cageColorList.append(cageColorMatrix[i][j])
    return puzzleList,cageColorList

def parseResultsToGuiFormat(res):
    w, h = size,size
    resultMatrix = [[0 for x in range(w)] for y in range(h)]
    for (place, value) in res.items():
        for i in range(len(place)):
            resultMatrix[place[i][0]-1][place[i][1]-1]=value[i]
    
    return resultMatrix
