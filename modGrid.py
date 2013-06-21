#!/usr/bin/python
import random
from modPlayer import *
from modWall import *
from modEmpty import *
from modBeast import *
from modRock import *

class Grid:
    MOVE_N = (0,-1) # Label movements
    MOVE_NE = (1,-1)
    MOVE_E = (1,0)
    MOVE_SE = (1,1)
    MOVE_S = (0,1)
    MOVE_SW = (-1,1)
    MOVE_W = (-1,0)
    MOVE_NW = (-1,-1)

    def __init__(self, xsize=38, ysize=21): #original beastgrid was 21 by 38 playable squares
        self.grid = [[Empty() for col in range(xsize+2)] for row in range(ysize+2)]
        self.rows = ysize+2 #add extra top and bottom rows to be filled with wall elements
        self.cols = xsize+2 #add extra left and right columns to be filled with wall elements
        for i in range(ysize+2):
            self.grid[i][0] = Wall() # set fixed wall left
            self.grid[i][xsize+1] = Wall() # set fixed wall right
        for i in range(xsize+2):
            self.grid[0][i] = Wall() # set fixed wall top
            self.grid[ysize+1][i] = Wall() # set fixed wall bottom


    def addElement(self, elt, x, y):
        if(str(self.grid[x][y].type) != Empty().type):
            return False
            pass #New objects can not be placed on top of each other
        else:
            self.grid[x][y] = elt
            return True


    def moveRock(self, elt, d):
        curpos = self.getElementPosition(elt)
        newpos = ( curpos[0] + d[0], curpos[1] + d[1] )
        secondpos = ( newpos[0] + d[0], newpos[1] + d[1] )
        if(str(self.grid[newpos[1]][newpos[0]].type) == Wall().type):
            pass # Do not move to newpos as no element stand on Wall().
        elif(str(self.grid[newpos[1]][newpos[0]].type) == Beast().type): #Let's see if the beast can be squashed
            if(str(self.grid[secondpos[1]][secondpos[0]].type) == Rock().type): #Beast is enclosed between two rocks and will be squashed
                self.grid[curpos[1]][curpos[0]] = Empty()
                self.grid[newpos[1]][newpos[0]].isAlive = False #Kill beast
                self.grid[newpos[1]][newpos[0]] = elt #Splat!
            elif(str(self.grid[secondpos[1]][secondpos[0]].type) == Wall().type): #Beast is enclosed between a rock and a wall and will be squashed
                self.grid[curpos[1]][curpos[0]] = Empty()
                self.grid[newpos[1]][newpos[0]].isAlive = False #Kill beast
                self.grid[newpos[1]][newpos[0]] = elt #Splat!
#            elif(str(self.grid[secondpos[1]][secondpos[0]].type) == Beast().type): #Beast is enclosed between a rock and another beast and will be squashed
#                self.grid[curpos[1]][curpos[0]] = Empty()
#                self.grid[newpos[1]][newpos[0]].isAlive = False #Kill beast
#                self.grid[newpos[1]][newpos[0]] = elt #Splat!
            else:
                pass #Beast cannot be squashed as nothing is standing behind it to squash it with.
        elif(str(self.grid[newpos[1]][newpos[0]].type) == Rock().type): #Move second Rock() along further in the same direction
            self.moveRock(self.grid[newpos[1]][newpos[0]], d) #Move Rock() further in the same direction
            if(str(self.grid[newpos[1]][newpos[0]].type) == Empty().type): # If the moving of the rock was possible, follow behind it
                self.grid[curpos[1]][curpos[0]] = Empty()
                self.grid[newpos[1]][newpos[0]] = elt
            else:
                pass #moving did not happen as the last element was probably a Wall()
        else: # The rock can be moved as nothing is blocking it's path
            self.grid[curpos[1]][curpos[0]] = Empty()
            self.grid[newpos[1]][newpos[0]] = elt




    def movePlayer(self, elt, d):
        curpos = self.getElementPosition(elt)
        newpos = ( curpos[0] + d[0], curpos[1] + d[1] )
        if(str(self.grid[newpos[1]][newpos[0]].type) == Wall().type):
            pass # Do not move to newpos as no element stand on Wall().
        elif(str(self.grid[newpos[1]][newpos[0]].type) == Beast().type): #Oops, you stept on a beast
            elt.isAlive = False # Bye bye, player
        elif(str(self.grid[newpos[1]][newpos[0]].type) == Rock().type):
            self.moveRock(self.grid[newpos[1]][newpos[0]], d) #Move Rock() further in the same direction
            if(str(self.grid[newpos[1]][newpos[0]].type) == Empty().type): # If the moving of the rock was possible, follow behind it
                self.grid[curpos[1]][curpos[0]] = Empty()
                self.grid[newpos[1]][newpos[0]] = elt
            else:
                pass # moving did not happen as the last element was probably a Wall()
        else: # The player can be moved as nothing is blocking it's path
            self.grid[curpos[1]][curpos[0]] = Empty()
            self.grid[newpos[1]][newpos[0]] = elt

    def moveBeast(self, elt, p):
        curpos = self.getElementPosition(elt)
        newpos = curpos
        playerpos = self.getElementPosition(p)
        # Some dumb "AI" that lets the beast move in the direction of the player. obstacles are not taken in account.
        if(playerpos[0] == curpos[0]):
            if(playerpos[1] < curpos[1]): #North
                newpos = [curpos[0], curpos[1] - 1]
            elif(playerpos[1] > curpos[1]): #South
                newpos = [curpos[0], curpos[1] + 1]
            else:
                print "Ooops, failure in vertical Beast movement. This status should not be reached!"
                pass #This status should not be reached
        elif(playerpos[0] > curpos[0]):
            if(playerpos[1] < curpos[1]): #NorthEast
                newpos = [curpos[0] + 1 , curpos[1] - 1]
            elif(playerpos[1] == curpos[1]): #East
                newpos = [curpos[0] + 1, curpos[1]]
            elif(playerpos[1] > curpos[1]): #SouthEast
                newpos = [curpos[0] + 1, curpos[1] + 1]
            else:
                print "Ooops, failure in Beast movement to the East. This status should not be reached!"
                pass #This status should not be reached
        elif(playerpos[0] < curpos[0]):
            if(playerpos[1] > curpos[1]): #SoutWest
                newpos = [curpos[0] - 1, curpos[1] + 1]
            elif(playerpos[1] == curpos[1]): #West
                newpos = [curpos[0] - 1, curpos[1]]
            elif(playerpos[1] < curpos[1]): #NorthWest
                newpos = [curpos[0] - 1, curpos[1] - 1]
            else:
                print "Ooops, failure in Beast movement to the West. This status should not be reached!"
                pass #This status should not be reached
        else:
            print "Ooops, failure in Beast movement. This status should not be reached! is Player still alive and present?"
            pass #This status should not be reached

        # Now check if the chosen next position contains an object
        if(str(self.grid[newpos[1]][newpos[0]].type) == Wall().type):
            pass # Do not move to newpos as no element stand on Wall().
        elif(str(self.grid[newpos[1]][newpos[0]].type) == Beast().type):
            pass # Beasts do not kill each other and don't step on each other.
        elif(str(self.grid[newpos[1]][newpos[0]].type) == Rock().type):
            pass # Beast can not push rocks
        elif(str(self.grid[newpos[1]][newpos[0]].type) == Player().type):
            self.grid[curpos[1]][curpos[0]] = Empty()
            self.grid[newpos[1]][newpos[0]].isAlive = False #Kill player
            self.grid[newpos[1]][newpos[0]] = elt #Splat!
        else: # The beast can be moved as nothing is blocking it's path
            self.grid[curpos[1]][curpos[0]] = Empty()
            self.grid[newpos[1]][newpos[0]] = elt


    def getElementPosition(self, elt):
        y = 0
        while y < self.rows:
            x = 0
            while x < self.cols:
                if self.grid[y][x] == elt:
                    return x,y
                x += 1
            y += 1

    def renderGrid(self):
        y = 0
        while y < self.rows:
            x = 0
            while x < self.cols:
                print self.grid[y][x].type,
                x += 1
            y += 1
            print

    def renderGridAscii(self):
        y = 0
        while y < self.rows:
            stringprint = ''
            x = 0
            while x < self.cols:
                stringprint+=self.grid[y][x].symbol
                x += 1
            print stringprint
            y += 1

    def fillGridRocks(self):
        amount = (self.rows -2) * (self.cols -2) / 3 # calculate amount of Rock() to be placed
        i = 0
        while(i < amount):
            r = Rock()
            if(self.addElement(r, random.randint(1,self.rows - 2), random.randint(1, self.cols -2))): # Try to place a Rock() in a random location on the grid within the walls
                i+=1
            else:
                pass # placing Rock() failed because position was already taken by non-Empty() element.

    def fillGridRandomWalls(self):
        amount = (self.rows -2) / 2 # calculate amount of Wall() to be placed
        i = 0
        while(i < amount):
            r = Wall()
            if(self.addElement(r, random.randint(1,self.rows - 2), random.randint(1, self.cols -2))): # Try to place a Wall() in a random location on the grid within the walls
                i+=1
            else:
                pass # placing Wall() failed because position was already taken by non-Empty() element.
        print i
