from typing import List
from copy import deepcopy
import random

# I L J T O Z S

class Tile:
    _name: str
    _w: int
    _h: int
    _size: int
    _mass: List[List[int]]
    color: str
    offsetT:int
    offsetD:int
    offsetL:int
    offsetR:int

    def __init__(self) -> None:
        self.name = self._name
        self.w = self._w
        self.h = self._h
        self.size = self._size
        self.mass = deepcopy(self._mass)
        self.setOffset()
    def setOffset(self):
        self.offsetT = self.size
        self.offsetD = self.size
        self.offsetL = self.size
        self.offsetR = self.size
        for y in range(self.size):
            for x in range(self.size):
                if(self.mass[y][x] == 0): continue
                self.offsetT = min(self.offsetT, y)
                self.offsetD = min(self.offsetD, self.size-y-1)
                self.offsetL = min(self.offsetL, x)
                self.offsetR = min(self.offsetR, self.size-x-1)

    def rotateL(self):
        new_matrix = []
        for r in range(self.size):
            new_matrix.append([0]*self.size)
        for i in range(self.size):
            for j in range(self.size):
                new_matrix[i][j] = self.mass[j][self.size-i-1]
        self.mass = new_matrix
        self.setOffset()

    def rotateR(self):
        for i in range(3):
            self.rotateL()

    def rotate(self, direction:int) -> None:
        if(direction < 0): self.rotateL()
        if(direction > 0): self.rotateR()



class Tile_I(Tile):
    _name = "I"
    _w, _h = 4, 1
    _size = 4
    _mass = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    color = "#0f9bd7"

class Tile_J(Tile):
    _name = "J"
    _w, _h = 2, 3
    _size = 3
    _mass = [ 
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]
    color = "#e39f02"

class Tile_L(Tile):
    _name = "L"
    _w, _h = 2, 3
    _size = 3
    _mass = [ 
        [0,1, 0,],
        [0,1, 0,],
        [0,1, 1,]
    ]
    color = "#af298a"

class Tile_O(Tile):
    _name = "O"
    _w, _h = 2, 2
    _size = 2 
    _mass = [ 
        [1, 1],
        [1, 1]
    ]
    color = "#59b101"

class Tile_S(Tile):
    _name = "S"
    _w, _h = 3, 2
    _size = 3
    _mass = [ 
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ]
    color = "#d70f37"

class Tile_T(Tile):
    _name = "T"
    _w, _h = 3, 3
    _size = 3
    _mass = [ 
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    color = "#2141c6"

class Tile_Z(Tile):
    _name = "Z"
    _w, _h = 3, 2
    _size = 3
    _mass = [ 
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
    color = "#e35b02"
ALL = [
    Tile_I,
    Tile_J,
    Tile_L,
    Tile_O,
    Tile_S,
    Tile_T,
    Tile_Z
]