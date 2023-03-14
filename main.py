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
    acc = True
    for r in range(len(life)):
        for c in range(len(life[r])):
            val = fn(grid,r,c)
            acc &= True if val is None else val
    return acc

def randomizeCell(grid, r,c):
    grid[r][c] = 1 if random.random() < 0.3 else 0

def addRandomCell(grid, r,c):
    liveNeighbours = getLiveNeighbours(grid,r,c)
    if liveNeighbours > 0:
        grid[r][c] = 1 if random.random() < 1 else grid[r][c]

def getLiveNeighbours(grid, r,c):
    alive = 0
    for ri in range(-1,2):
        for ci in range(-1,2):
            if ri != 0 and ci != 0 and r + ri >= 0 and r + ri < len(grid) and c + ci >= 0 and c + ci < len(grid[r]) and grid[r + ri][c + ci] == 1:
                alive += 1
    return alive

def lifeCell(grid, r,c):
    liveNeighbours = getLiveNeighbours(grid,r,c)
    if grid[r][c] == 1:
        if liveNeighbours < 2 or liveNeighbours > 3:
            grid[r][c] = 0
            return False
    else:
        if liveNeighbours == 3:
            grid[r][c] = 1
            return False

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

    # Infinitely loop through the gif
    while(True):
        if applyToEveryCell(lifeCell,life):
            applyToEveryCell(addRandomCell, life)
        matrix.SwapOnVSync(constructCanvas())
        time.sleep(0.05)
except KeyboardInterrupt:
    sys.exit(0)