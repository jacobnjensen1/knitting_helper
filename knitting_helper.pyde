#TODO: add EvenMirror, and wrapper above that and OddMirror
#TODO: add csv handling
import time
from re import match

WIDTH_HEIGHT = 1000
NUM_COL_ROWS = 23
WIDTH_COL_ROWS = float(WIDTH_HEIGHT) / NUM_COL_ROWS

class OneSquare(object):
    def __init__(self, minXPos, maxXPos, minYPos, maxYPos, square_width_height):
        self.filledIn = False
        self.minXPos = minXPos
        self.maxXPos = maxXPos
        self.minYPos = minYPos
        self.maxYPos = maxYPos
        self.square_width_height = square_width_height
        self._updateColor()
    
    def toggleFill(self):
        self.filledIn = not self.filledIn
        self._updateColor()
    
    def _updateColor(self):
        if self.filledIn:
            fill(0)
        else:
            fill(255)
        rect(self.minXPos, self.minYPos, self.square_width_height, self.square_width_height)
        
class Squares(object):
    def __init__(self, width_height, num_col_rows, width_col_rows):
        self.posRanges = [(width_col_rows * (i - 1),width_col_rows * i) for i in range(1,NUM_COL_ROWS + 1)]
        self.squareList = [[OneSquare(xRef[0], xRef[1], yRef[0], yRef[1], width_col_rows) for yRef in self.posRanges] for xRef in self.posRanges]
    
    def getIndexesAtPos(self, xPos, yPos):
        xIndex = [loopedPos[0] <= xPos <= loopedPos[1] for loopedPos in self.posRanges].index(True)
        yIndex = [loopedPos[0] <= yPos <= loopedPos[1] for loopedPos in self.posRanges].index(True)
        return (xIndex, yIndex)
    
    def toggleSquareAtPos(self, xPos, yPos):
        xIndex = [loopedPos[0] <= xPos <= loopedPos[1] for loopedPos in self.posRanges].index(True)
        yIndex = [loopedPos[0] <= yPos <= loopedPos[1] for loopedPos in self.posRanges].index(True)
        self.squareList[xIndex][yIndex].toggleFill()
    
    def toggleSquareAtIndex(self, xIndex, yIndex):
        self.squareList[xIndex][yIndex].toggleFill()

class OddMirror(object):
    def __init__(self, width_height, num_col_rows, width_col_rows):
        self.squares = Squares(width_height, num_col_rows, width_col_rows)
        self.num_col_rows = num_col_rows
    
    def clickOnPos(self, xPos, yPos):
        xIndex, yIndex = self.squares.getIndexesAtPos(xPos, yPos)
        # if is along middle (non-mirrored) x index
        if xIndex == self.num_col_rows / 2:
            if yIndex == self.num_col_rows / 2:
                #at middle
                self.squares.toggleSquareAtIndex(xIndex, yIndex)
                return
            self.squares.toggleSquareAtIndex(xIndex, yIndex)
            self.squares.toggleSquareAtIndex(xIndex, self._getMirrorOfIndex(yIndex))
            return
        if yIndex == self.num_col_rows / 2:
            self.squares.toggleSquareAtIndex(xIndex, yIndex)
            self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), yIndex)
            return
        self.squares.toggleSquareAtIndex(xIndex, yIndex)
        self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), yIndex)
        self.squares.toggleSquareAtIndex(xIndex, self._getMirrorOfIndex(yIndex))
        self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), self._getMirrorOfIndex(yIndex))
        return
    
    def _getMirrorOfIndex(self, index):
        middle = self.num_col_rows / 2
        if index == middle:
            return index
        if index < middle:
            return middle + (middle - index)
        else:
            return middle - (index - middle)

class RotationalMirror(object):
    def __init__(self, width_height, num_col_rows, width_col_rows):
        self.squares = Squares(width_height, num_col_rows, width_col_rows)
        self.num_col_rows = num_col_rows
        
    def clickOnPos(self, xPos, yPos):
        #NOT DONE
        xIndex, yIndex = self.squares.getIndexesAtPos(xPos, yPos)
        # if is along middle (non-mirrored) x index
        if xIndex == self.num_col_rows / 2:
            if yIndex == self.num_col_rows / 2:
                #at middle
                self.squares.toggleSquareAtIndex(xIndex, yIndex)
                return
            self.squares.toggleSquareAtIndex(xIndex, yIndex)
            self.squares.toggleSquareAtIndex(yIndex, xIndex)
            self.squares.toggleSquareAtIndex(xIndex, self._getMirrorOfIndex(yIndex))
            self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(yIndex), xIndex)
            return
        if yIndex == self.num_col_rows / 2:
            self.squares.toggleSquareAtIndex(xIndex, yIndex)
            self.squares.toggleSquareAtIndex(yIndex, xIndex)
            self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), yIndex)
            self.squares.toggleSquareAtIndex(yIndex, self._getMirrorOfIndex(xIndex))
            return
        if xIndex == yIndex or xIndex == self._getMirrorOfIndex(yIndex):
            #on diagonal
            self.squares.toggleSquareAtIndex(xIndex, yIndex)
            self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), yIndex)
            self.squares.toggleSquareAtIndex(xIndex, self._getMirrorOfIndex(yIndex))
            self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), self._getMirrorOfIndex(yIndex))
            return
            
        self.squares.toggleSquareAtIndex(xIndex, yIndex)
        self.squares.toggleSquareAtIndex(yIndex, xIndex)
        self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), yIndex)
        self.squares.toggleSquareAtIndex(yIndex, self._getMirrorOfIndex(xIndex))
        self.squares.toggleSquareAtIndex(xIndex, self._getMirrorOfIndex(yIndex))
        self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(yIndex), xIndex)
        self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(xIndex), self._getMirrorOfIndex(yIndex))
        self.squares.toggleSquareAtIndex(self._getMirrorOfIndex(yIndex), self._getMirrorOfIndex(xIndex))
        return
    
    def _getMirrorOfIndex(self, index):
        middle = self.num_col_rows / 2
        if index == middle:
            return index
        if index < middle:
            return middle + (middle - index)
        else:
            return middle - (index - middle)

def redoDimensions(newDims):
    print("HI")
    background(255)
    newWidth = float(WIDTH_HEIGHT) / newDims
    for pos in [newWidth * i for i in range(0, newDims + 1)]:
        line(0, pos, WIDTH_HEIGHT, pos)
        line(pos, 0, pos, WIDTH_HEIGHT)
    global squares
    squares = RotationalMirror(WIDTH_HEIGHT, newDims, newWidth)

def setup():
    size(WIDTH_HEIGHT + 1, WIDTH_HEIGHT + 1)
    background(255)
    for pos in [WIDTH_COL_ROWS * i for i in range(0,NUM_COL_ROWS + 1)]:
        line(0, pos, WIDTH_HEIGHT, pos)
        line(pos, 0, pos, WIDTH_HEIGHT)
    #TODO: make this not global
    
    global squares
    global keypressHandler
    squares = RotationalMirror(WIDTH_HEIGHT, NUM_COL_ROWS, WIDTH_COL_ROWS)
    keypressHandler = KeypressHandler()
    
    
def draw():
    pass
    
def mouseClicked():
    squares.clickOnPos(mouseX, mouseY)
    
class KeypressHandler(object):
    def __init__(self):
        self._string = ""
        self._lastChange = 0
    
    def pressKey(self, keyString):
        print(time.time())
        print(self._lastChange)
        if (time.time() - self._lastChange) < 5:
            self._string += keyString
        else:
             self._string = keyString
        self._lastChange = time.time()
        print(self._string)
        self._handleString()
    
    def _handleString(self):
        if match("d(\d+)\n", self._string):
            newDims = int(match("d(\d+)\n", self._string).group(1))
            print(newDims)
            redoDimensions(newDims)
            self._string = ""
    
def keyPressed():
    keypressHandler.pressKey(key)
