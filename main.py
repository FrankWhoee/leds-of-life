#!/usr/bin/env python
import time
import sys

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

life = [[0] * options.cols for i in range(options.rows)]

def applyToEveryCell(fn, grid):
    changed_values = []
    for r in range(len(life)):
        for c in range(len(life[r])):
            val = fn(grid,r,c)
            if val is not None:
                changed_values.append((fn(grid,r,c), r, c))
    for point in changed_values:
        grid[point[1]][point[2]] = point[0]
    return changed_values

def randomizeCell(grid, r,c):
    return 1 if random.random() < 0.3 else 0

def addRandomCell(grid, r,c):
    liveNeighbours = getLiveNeighbours(grid,r,c)
    if liveNeighbours > 0:
        grid[r][c] = 1 if random.random() < 1 else grid[r][c]

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
        if grid[r1][c1] == 1:
            alive += 1

    return alive

def lifeCell(grid, r,c):
    liveNeighbours = getLiveNeighbours(grid,r,c)
    if grid[r][c] == 1:
        if liveNeighbours < 2 or liveNeighbours > 3:
            return 0
    elif grid[r][c] == 0 and liveNeighbours == 3:
            return 1
    return None
    

applyToEveryCell(randomizeCell, life)

def constructCanvas():
    global life
    canvas = matrix.CreateFrameCanvas()

    def helper(grid, r, c):
        if grid[r][c] == 1:
            canvas.SetPixel(r,c, 255,125,0)
    
    applyToEveryCell(helper, life)
    return canvas

try:
    print("Press CTRL-C to stop.")

    while(True):
        matrix.SwapOnVSync(constructCanvas())
        if applyToEveryCell(lifeCell,life):
            pass
            # applyToEveryCell(addRandomCell, life)
        time.sleep(0.05)
except KeyboardInterrupt:
    sys.exit(0)
