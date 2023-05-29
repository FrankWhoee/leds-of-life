#!/usr/bin/env python
import time
import sys
from datetime import datetime

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import random

random.seed(time.time())

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
options.disable_hardware_pulsing = True

matrix = RGBMatrix(options = options)

life = [[[0,0]] * options.cols for i in range(options.rows)]

MAX_AGE = 20

def applyToEveryCell(fn, grid):
    changed_values = []
    for r in range(len(life)):
        for c in range(len(life[r])):
            val = fn(grid,r,c)
            if val is not None:
                changed_values.append((fn(grid,r,c), r, c))
    for point in changed_values:
        if point[0] == 1:
            grid[point[1]][point[2]] = [1,MAX_AGE]
        else:
           grid[point[1]][point[2]] = [0,0] 
    return changed_values

def randomizeCell(grid, r,c):
    return 1 if random.random() < 0.3 else 0

def addRandomCell(grid, r,c):
    liveNeighbours = getLiveNeighbours(grid,r,c)
    if liveNeighbours > 0:
        return 1 if random.random() < 0.05 else grid[r][c][0]

def getLiveNeighbours(grid, r,c):
    alive = 0
    neighbours = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
    for n in neighbours:
        dr = n[0]
        dc = n[1]
        r1 = r + dr
        c1 = c + dc

        if (r1 < 0 or r1 >= len(grid) or c1 < 0 or c1 >= len(grid[0])):
            continue
        if grid[r1][c1][0] == 1:
            alive += 1

    return alive

def lifeCell(grid, r,c):
    liveNeighbours = getLiveNeighbours(grid,r,c)
    if grid[r][c][0] == 1:
        if liveNeighbours < 2 or liveNeighbours > 3:
            return 0
    elif grid[r][c][0] == 0 and liveNeighbours == 3:
            return 1
    return None

def ageCell(grid, r, c):
    if grid[r][c][0] == 1:
        grid[r][c][1] -= 1
    if grid[r][c][1] <= 0:
        return 0
    

def getPopulation(grid):
    pop = 0
    for r in grid:
        for c in r:
            if c[0] == 1:
                pop += 1
    return pop

applyToEveryCell(randomizeCell, life)

def constructCanvas():
    global life
    canvas = matrix.CreateFrameCanvas()

    def helper(grid, r, c):
        if grid[r][c][0] == 1:
            age_multiplier = grid[r][c][1]/MAX_AGE
            canvas.SetPixel(r,c, int(255 * age_multiplier),int(125 * age_multiplier),0)
    
    applyToEveryCell(helper, life)
    return canvas

def canvasClear():
    global life
    canvas = matrix.CreateFrameCanvas()

    def helper(grid, r,c):
        grid[r][c][0] = 0
        grid[r][c][1] = 0
        canvas.SetPixel(r,c,0,0,0)
    applyToEveryCell(helper,life)

    return canvas


try:
    print("Press CTRL-C to stop.")
    prev = None
    prevPrev = None
    now = datetime.now().time()
    print(now.hour)
    boardOn = now.hour < 23 and now.hour >= 9
    idleCount = 7
    while(True):
        matrix.SwapOnVSync(constructCanvas())
        applyToEveryCell(ageCell, life)
        now = datetime.now().time()
        if now.hour == 22 and now.minute >= 30:
            boardOn = False
        elif now.hour == 9:
            boardOn = True
        if not boardOn:
            time.sleep(10)
            matrix.SwapOnVSync(canvasClear())
            continue
        curr = applyToEveryCell(lifeCell,life)
        if len(curr) == 0:
            applyToEveryCell(randomizeCell, life)
        elif prev == curr or curr == prevPrev:
            idleCount -= 1
        if idleCount <= 0:
            applyToEveryCell(addRandomCell, life)
            idleCount = 7
        prevPrev = prev
        prev = curr
        pop = getPopulation(life)
        time.sleep(25/(pop + 50))
except KeyboardInterrupt:
    sys.exit(0)
