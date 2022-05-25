import csp
from functools import reduce
from random import random, shuffle, randint, choice

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
def checkNeighbour(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    dx, dy = x1 - x2, y1 - y2
    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

#generate random cages
def generateCages(size):
    puzzle = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)] #container have same size of puzzle
    
    for _ in range(size): #Shuffle the board
        shuffle(puzzle)

    #Initialize the 'uncaged' set with all cell coordinates
    for c1 in range(size):
        for c2 in range(size):
            if random() > 0.5:
                for r in range(size):
                    puzzle[r][c1], puzzle[r][c2] = puzzle[r][c2], puzzle[r][c1]
    puzzle = {(j + 1, i + 1): puzzle[i][j] for i in range(size) for j in range(size)}
    uncaged = sorted(puzzle.keys(), key=lambda var: var[1])
    cageList = []
    
    while uncaged: #'uncaged' list is empty
        cageList.append([])
        cageSize = randint(1, 4)
        cell = uncaged[0]
        uncaged.remove(cell)
        cageList[-1].append(cell)
        for _ in range(cageSize - 1):
            adjs = [other for other in uncaged if checkNeighbour(cell, other)]
            cell = choice(adjs) if adjs else None
            if not cell:
                break
            uncaged.remove(cell)           
            cageList[-1].append(cell)
            
        cageSize = len(cageList[-1])
        if cageSize == 1: #no operation and the reuslt = element of cageList
            cell = cageList[-1][0]
            cageList[-1] = ((cell, ), '.', puzzle[cell])
            continue 
        elif cageSize == 2: #div operation if the elements can be divided.. if not operation will be sub
            fst, snd = cageList[-1][0], cageList[-1][1]
            if puzzle[fst] / puzzle[snd] > 0 and not puzzle[fst] % puzzle[snd]:
                operator = "/" 
            else:
                operator = "-" 
        else: #operation is addition or multiplication
            operator = choice("+*")

        target = reduce(operation(operator), [puzzle[cell] for cell in cageList[-1]])
        cageList[-1] = (tuple(cageList[-1]), operator, int(target))

    return cageList

def parseCagesToGuiFormat(cageList): #parse output cage and its background to be one list to display in gui
    w, h = size,size
    cageMatrix = [[0 for x in range(w)] for y in range(h)] 
    cageColorMatrix = [[0 for x in range(w)] for y in range(h)] 
    for i in range(len(cageList)):
        for j in range(len(cageList[i][0])):
            cageColorMatrix[cageList[i][0][j][1]-1][cageList[i][0][j][0]-1]=colorList[i%15]
            if j==0:
             cageMatrix[cageList[i][0][j][0]-1][cageList[i][0][j][1]-1]=cageList[i][1]+str(cageList[i][2])  
            else:
             cageMatrix[cageList[i][0][j][0]-1][cageList[i][0][j][1]-1]=""
    
    cagesParsed=[]
    cageColorList = [] 
    for i in range(size):
        for j in range(size):
           cagesParsed.append(cageMatrix[i][j])
           cageColorList.append(cageColorMatrix[i][j])
    return cagesParsed,cageColorList

def parseResultsToGuiFormat(res): #parse solution be one list to display in gui
    w, h = size,size
    resultMatrix = [[0 for x in range(w)] for y in range(h)]
    for (place, value) in res.items():
        for i in range(len(place)):
            resultMatrix[place[i][0]-1][place[i][1]-1]=value[i]
    
    return resultMatrix
Toka Hefny
def validate(size, cageList):
    outOfBounds = lambda xy: xy[0] < 1 or xy[0] > size or xy[1] < 1 or xy[1] > size
    mentioned = set()
    for i in range(len(cageList)):
        members, operator, target = cageList[i]
        cageList[i] = (tuple(set(members)), operator, target)
        members, operator, target = cageList[i]
        
        if operator not in "+-*/.":
            print("Operation", operator, "of clique", cageList[i], "is unacceptable", file=stderr)
            exit(1)
        problematic = list(filter(outOfBounds, members))
        
        if problematic:
            print("Members", problematic, "of clique", cageList[i], "are out of bounds", file=stderr)
            exit(2)
        problematic = mentioned.intersection(set(members))
        
        if problematic:
            print("Members", problematic, "of clique", cageList[i], "are cross referenced", file=stderr)
            exit(3)
        mentioned.update(set(members))
    indexes = range(1, size + 1)
    problematic = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)

    if problematic:
        print("Positions", problematic, "were not mentioned in any clique", file=stderr)
        exit(4)
def RowXorCol(xy1, xy2):
    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])
