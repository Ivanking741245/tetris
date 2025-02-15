from . import Tiles, constants
from typing import List
import random
class Board:
    loadedTiles: List[Tiles.Tile]
    def __init__(self, rows:int, cols:int) -> None:
        self.rows = rows
        self.cols = cols
        self.reset()
    
    def reset(self) -> None:
        self.score = 0
        self.clearCount = 0
        self.heldTile = None
        self.loadedTiles = []
        self.fillPreloadTiles()
        self.board = []
        self.fillEmptyRows()
        self.cursor_x = self.cols // 2 - self.loadedTiles[0].size // 2
        self.cursor_y = -self.loadedTiles[0].offsetT
        self.fallCounter = 0
        self.lockCounter = 0
        self.alive = True
    def fillEmptyRows(self) -> None:
        for i in range(self.rows - len(self.board)):
            self.board.insert(0, [None,]*self.cols)
    def fillPreloadTiles(self) -> None:
        if len(self.loadedTiles) <= len(Tiles.ALL):
            group = [i() for i in Tiles.ALL]
            random.shuffle(group)
            self.loadedTiles.extend(group)
        #random不重複
    def checkClear(self):
        count = 0
        for i in range(len(self.board)-1, -1, -1):
            if all(self.board[i]):
                self.board.pop(i)
                count += 1
        self.score += [0, 40, 100, 300, 1200][count]
        self.clearCount += count
        self.fillEmptyRows()
    def checkCollision(self, x:int, y:int, checkD:bool = True, checkL:bool = True, checkR:bool = True) -> bool:
        if checkD:
            if y+self.loadedTiles[0].size - self.loadedTiles[0].offsetD > self.rows:
                return True
        if checkL:
            if x + self.loadedTiles[0].offsetL < 0:
                return True
        if checkR:
            if x + self.loadedTiles[0].size - self.loadedTiles[0].offsetR > self.cols:
                return True
        Lx, Rx = max(x, 0), min(x+self.loadedTiles[0].size, self.cols)
        Ly, Ry = max(y, 0), min(y+self.loadedTiles[0].size, self.rows)
        for yy in range(Ly, Ry):
            for xx in range(Lx, Rx):
                if self.board[yy][xx] and self.loadedTiles[0].mass[yy-y][xx-x]:
                    return True
        return False
    
    def lock(self, instant):
        if not self.alive: return
        if self.checkCollision(self.cursor_x, self.cursor_y+1):
            self.lockCounter += 1
        else:
            self.lockCounter = 0
        if self.lockCounter == constants.LOCK_DELAY or instant:
            self.lockCounter = 0
            x, y = self.cursor_x, self.cursor_y
            Lx, Rx = max(x, 0), min(x+self.loadedTiles[0].size, self.cols)
            Ly, Ry = max(y, 0), min(y+self.loadedTiles[0].size, self.rows)
            for yy in range(Ly, Ry):
                for xx in range(Lx, Rx):
                    if self.loadedTiles[0].mass[yy-y][xx-x]:
                        self.board[yy][xx] = self.loadedTiles[0].color
            self.checkClear()
            self.loadedTiles.pop(0)
            self.fillPreloadTiles()
            self.cursor_y = -self.loadedTiles[0].offsetT
            self.cursor_x = self.cols // 2 - self.loadedTiles[0].size // 2
            if self.checkCollision(self.cursor_x, self.cursor_y):
                self.alive = False
        
    def fall(self):
        if not self.alive: return
        if self.checkCollision(self.cursor_x, self.cursor_y+1):
            return self.lock(instant=False)
        self.cursor_y += 1

    def drop(self):
        if not self.alive: return
        while not self.checkCollision(self.cursor_x, self.cursor_y+1):
            self.cursor_y += 1
        self.lock(instant=True)

    def move(self, direction):
        if not self.alive: return
        if self.checkCollision(self.cursor_x+direction, self.cursor_y):
            return
        self.cursor_x += direction
    def rotate(self, direction):
        self.loadedTiles[0].rotate(direction)
        if self.checkCollision(self.cursor_x, self.cursor_y):
            self.loadedTiles[0].rotate(-direction)
    def hold(self):
        if not self.alive: return
        if not self.heldTile: 
            self.heldTile = self.loadedTiles.pop(0)
        else:
            self.heldTile, self.loadedTiles[0] = self.loadedTiles[0], self.heldTile
        self.fillPreloadTiles()
        self.cursor_x = self.cols // 2 - self.loadedTiles[0].size // 2
        self.cursor_y = -self.loadedTiles[0].offsetT
    def update(self):
        if not self.alive: return
        self.fallCounter += 1
        if self.fallCounter == constants.FALL_DELAY:
            self.fall()
            self.fallCounter = 0
        