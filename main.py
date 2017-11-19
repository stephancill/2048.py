from random import randrange
from random import random
from itertools import chain
import sys

class Board(object):
    size = 0
    tiles = None
    score = 0
    
    def __init__(self, size):
        self.size = size
        self.tiles = [[None for i in range(size)] for j in range(size)]

    def introduce(self):
        # Find empty spaces on board
        spaces = self.findSpaces()
        if not spaces:
            return

        coord = spaces[randrange(len(spaces))]
        new = 3 if random() > 0.5 else 6
        self.tiles[coord[1]][coord[0]] = new

    def gameOver(self):
        print("Game over... Score: {}".format(self.score))
        sys.exit() 

    def move(self, move):
        # Valid moves: "up", "down", "left", "right"
        moves = {
            "up"    : ("vertical", -1),
            "down"  : ("vertical", 1),
            "left"  : ("horizontal", -1),
            "right" : ("horizontal", 1),
        }

        axis, direction = moves[move]

        tiles = self.tiles.copy()

        if axis == "vertical":
            tiles = list(zip(*tiles))

        for index, row in enumerate(tiles):
            row = [t for t in row if t]
            new_row = []

            if axis == "vertical":
                row = row[::-direction]

            if len(row) > 1:
                while len(row) > 1:
                    if row[0] == row[1]:
                        new_row.append(row[0]*2)
                        self.score += row[0]*2
                        row.remove(row[0])
                        row.remove(row[0])
                    else:
                        new_row.append(row[0])
                        row.remove(row[0])
                
            new_row += row
            
            if axis == "vertical":
                new_row = new_row[::-direction]

            if direction == -1:
                new_row += [None] * (self.size - len(new_row))
            else:
                new_row = ([None] * (self.size - len(new_row))) + new_row
            
            tiles[index] = new_row

        if axis == "vertical":
            tiles = list([list(t) for t in zip(*tiles)])
        
        changed = False
        for i in range(self.size):
            if tiles[i] != self.tiles[i]:
                changed = True
    
        if changed:
            self.tiles = tiles
            self.introduce()
            if not len(self.findSpaces()):
                self.gameOver()


    def render(self):
        print("Score: {}".format(self.score))
        for row in self.tiles:
            print(str("\t\t").join([str(t) if t else "_" for t in row]))
            print("\n")
    
    def findSpaces(self):
        return list(chain(*[[(x, y) for x in range(self.size) if self.tiles[y][x] == None] for y in range(self.size)]))

def main():
    board = Board(4)
    board.introduce()
    board.introduce()
    
    board.render()

    keys = {
        "w": "up",
        "a": "left",
        "s": "down",
        "d": "right"
    }

    while True:
        inp = input("Move (WASD)\n> ")
        if inp.lower() in keys:
            board.move(keys[inp.lower()])
            board.render()



if __name__ == '__main__':
    main()