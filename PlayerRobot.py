from robot import Robot
from constants import Actions, TileType, MarkerType
import random
import time
import sys

##########################################################################
# One of your team members, Chris Hung, has made a starter bot for you.  #
# Unfortunately, he is busy on vacation so he is unable to aid you with  #
# the development of this bot.                                           #
#                                                                        #
# Make sure to read the README for the documentation he left you         #
#                                                                        #
# @authors: christoh, [TEAM_MEMBER_1], [TEAM_MEMBER_2], [TEAM_MEMBER_3]  #
# @version: 2/4/17                                                       #
#                                                                        #
# README - Introduction                                                  #
#                                                                        #
# Search the README with these titles to see the descriptions.           #
##########################################################################

# !!!!! Make your changes within here !!!!!
class player_robot(Robot):
    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        ##############################################
        # A couple of variables - read what they do! # 
        #                                            #
        # README - My_Robot                          #
        ##############################################
        self.toHome = []             
        self.numturns = 0            
        self.goinghome = False;      
        self.targetPath = None
        self.targetDest = (0,0)

    # A couple of helper functions (Implemented at the bottom)
    def OppositeDir(self, direction):
        return # See below

    def ViewScan(self, view):
        return # See below

    def FindRandomPath(self, view):
        return # See below

    def UpdateTargetPath(self):
        return # See below

    def adjacentWeights(self, view):
        return
    def getMove(self, view):
        return
    def getWeightAvg(self, view):
        return
    def dist(self, x, y, length):
        return
    def getWeight(self, view, x, y):
        return


    ###########################################################################################
    # This function is called every iteration. This method receives the current robot's view  #
    # and returns a tuple of (move_action, marker_action).                                    #
    #                                                                                         #
    # README - Get_Move                                                                       #
    ###########################################################################################

    # Returns opposite direction
    def OppositeDir(self, prevAction):
        if(prevAction == Actions.MOVE_N):
            return Actions.MOVE_S
        elif(prevAction == Actions.MOVE_NE):
            return Actions.MOVE_SW
        elif(prevAction == Actions.MOVE_E):
            return Actions.MOVE_W
        elif(prevAction == Actions.MOVE_SE):
            return Actions.MOVE_NW
        elif(prevAction == Actions.MOVE_S):
            return Actions.MOVE_N
        elif(prevAction == Actions.MOVE_SW):
            return Actions.MOVE_NE
        elif(prevAction == Actions.MOVE_W):
            return Actions.MOVE_E
        elif(prevAction == Actions.MOVE_NW):
            return Actions.MOVE_SE
        else:
            return Actions.MOVE_S

    # Scans the entire view for resource searching
    # REQUIRES: view (see call location)
    def ViewScan(self, view):
        viewLen = len(view)
        queue = [[(0,0)]]
        deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        visited = set()
        visited.add((0,0))

        targetDepleted = (view[self.targetDest[0]][self.targetDest[1]][0].GetType() == TileType.Resource and
                         view[self.targetDest[0]][self.targetDest[1]][0].AmountRemaining() <= 0)

        # BFS TO find the next resource within your view
        if(self.targetPath == None or targetDepleted):
            while(len(queue)>0):
                path = queue[0]
                loc = path[0]
                queue = queue[1:]
                viewIndex = (loc[0] + viewLen//2,loc[1]+viewLen//2)
                if (view[viewIndex[0]][viewIndex[1]][0].GetType() == TileType.Resource and
                    view[viewIndex[0]][viewIndex[1]][0].AmountRemaining() > 0):
                    # print(path)
                    self.targetPath = path[1:]
                    self.targetDest = path[0]
                    return
                elif(view[viewIndex[0]][viewIndex[1]][0].CanMove()):
                    for i in range(8):
                        x = loc[0] + deltas[i][0]
                        y = loc[1] + deltas[i][1]
                        if(abs(x) <= viewLen//2 and abs(y) <= viewLen//2):
                            if((x,y) not in visited):
                                queue.append([(x,y)] + path[1:] + [deltas[i]])
                                visited.add((x,y))

        return

    # Picks a random move based on the view - don't crash into mountains!
    # REQUIRES: view (see call location)
    def FindRandomPath(self, view):
        viewLen = len(view)

        while(True):
            actionToTake = random.choice([Actions.MOVE_E,Actions.MOVE_N,
                                          Actions.MOVE_S,Actions.MOVE_W,
                                          Actions.MOVE_NW,Actions.MOVE_NE,
                                          Actions.MOVE_SW,Actions.MOVE_SE])
            if ((actionToTake == Actions.MOVE_N and view[viewLen//2-1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_S and view[viewLen//2+1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_E and view[viewLen//2][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_W and view[viewLen//2][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NW and view[viewLen//2-1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NE and view[viewLen//2-1][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SW and view[viewLen//2+1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SE and view[viewLen//2+1][viewLen//2+1][0].CanMove()) ):
               return actionToTake

        return None

    # Returns actionToTake
    # REQUIRES: self.targetPath != []
    def UpdateTargetPath(self):
        actionToTake = None
        (x, y) = self.targetPath[0]

        if(self.targetPath[0] == (1,0)):
            actionToTake = Actions.MOVE_S
        elif(self.targetPath[0] == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.targetPath[0] == (0,1)):
            actionToTake = Actions.MOVE_E
        elif(self.targetPath[0] == (-1,1)):
            actionToTake = Actions.MOVE_NE
        elif(self.targetPath[0] == (-1,0)):
            actionToTake = Actions.MOVE_N
        elif(self.targetPath[0] == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.targetPath[0] == (0,-1)):
            actionToTake = Actions.MOVE_W
        elif(self.targetPath[0] == (1,-1)):
            actionToTake = Actions.MOVE_SW

        # Update destination using path
        self.targetDest = (self.targetDest[0]-x, self.targetDest[1]-y)
        # We will continue along our path    
        self.targetPath = self.targetPath[1:]

        return actionToTake

    def adjacentWeights(self, view):
      maxDist = (int)(len(view)/2)
      length = len(view)
      weights = [[0 for x in range(length)] for y in range(length)]
      for x in range(maxDist+1):
        # - Up
        for y in range(length):
          weights[x][y] = self.getWeightAvg(view, x, y, length, maxDist, weights)

        nx = length - x - 1
        # - Down
        for y in range(length):
          weights[nx][y] = self.getWeightAvg(view, nx, y, length, maxDist, weights)

        ny = x
        # | Left
        for nx in range(length):
          weights[nx][ny] = self.getWeightAvg(view, nx, ny, length, maxDist, weights)

        ny = length - x - 1
        # | Right
        for nx in range(length):
          weights[nx][ny] = self.getWeightAvg(view, nx, ny, length, maxDist, weights)
      multiplier = 45
      multiplier2 = 25
      weights = [x[maxDist-1:maxDist+2] for x in weights[maxDist-1:maxDist+2]]
      if(len(self.toHome) != 0):
          prevAction = self.toHome[-1]
          if(prevAction == Actions.MOVE_N):
              weights[0][1] *= multiplier
              weights[2][1] /= multiplier
              weights[0][0] *= multiplier2
              weights[2][2] /= multiplier2
              weights[0][2] *= multiplier2
              weights[2][0] /= multiplier2
          elif(prevAction == Actions.MOVE_NE):
              weights[0][2] *= multiplier
              weights[2][0] /= multiplier
              weights[0][1] *= multiplier2
              weights[2][1] /= multiplier2
              weights[1][2] *= multiplier2
              weights[1][0] /= multiplier2
          elif(prevAction == Actions.MOVE_E):
              weights[1][2] *= multiplier
              weights[1][0] /= multiplier
              weights[0][2] *= multiplier2
              weights[2][0] /= multiplier2
              weights[2][2] *= multiplier2
              weights[0][0] /= multiplier2
          elif(prevAction == Actions.MOVE_SE):
              weights[2][2] *= multiplier 
              weights[0][0] /= multiplier
              weights[2][1] *= multiplier2
              weights[0][1] /= multiplier2
              weights[1][2] *= multiplier2
              weights[1][0] /= multiplier2
          elif(prevAction == Actions.MOVE_S):
              weights[2][1] *= multiplier
              weights[0][1] /= multiplier
              weights[2][2] *= multiplier2
              weights[0][0] /= multiplier2
              weights[2][0] *= multiplier2
              weights[0][2] /= multiplier2
          elif(prevAction == Actions.MOVE_SW):
              weights[2][0] *= multiplier
              weights[0][2] /= multiplier
              weights[1][0] *= multiplier2
              weights[1][2] /= multiplier2
              weights[2][1] *= multiplier2
              weights[0][1] /= multiplier2
          elif(prevAction == Actions.MOVE_W):
              weights[1][0] *= multiplier
              weights[1][2] /= multiplier
              weights[2][0] *= multiplier2
              weights[0][2] /= multiplier2
              weights[0][0] *= multiplier2
              weights[2][2] /= multiplier2
          elif(prevAction == Actions.MOVE_NW):
              weights[0][0] *= multiplier
              weights[2][2] /= multiplier
              weights[0][1] *= multiplier2
              weights[2][1] /= multiplier2
              weights[1][0] *= multiplier2
              weights[1][2] /= multiplier2
      return weights

    def getMarkerValue(self, view, x, y):
      if(len(view[x][y][2]) == 0): 
        return 0
      colorAr = [x.GetColor() for x in view[x][y][2]]
      minColor = min(colorAr)
      return [0.1,0.4,1.5,6,20][minColor]

    def getWeightAvg(self, view, x, y, length, maxDist, weights):
      if(view[x][y][0].GetType() == TileType.Mountain):
        return 0
      if(not view[x][y][0].CanMove()):
        return 0
      curDist = self.dist(x, y, length)
      if(curDist == maxDist):
        return self.getWeight(view, x, y)
      curWeight = self.getWeight(view, x, y)
      adjWeight = 0
      adjNum = 0
      for x in range(x-1, x+1):
        for y in range(y-1, y+1):
          if(self.dist(x, y, length) > curDist):
            adjWeight += weights[x][y]
            adjNum += 1
      if(adjNum > 0):
        adjWeight /= adjNum
      return (curWeight + adjWeight) / 2

    def dist(self, x, y, length):
      return min(abs(x-length/2), abs(y-length/2))

    def getWeight(self, view, x, y):
      totalWeight = self.getMarkerValue(view, x, y)
      if(totalWeight > 0): return totalWeight
      totalWeight = 4
      if(view[x][y][0].GetType() == TileType.Resource):
        resource = view[x][y][0].Value()*view[x][y][0].AmountRemaining()
        resource = (resource + 2) / 3
        totalWeight += resource * resource
      return totalWeight

    def determine_flag(self, weight):
        cutoffs = [0.5, 2, 8, 32]
        if (weight > cutoffs[3]):
            return MarkerType.ORANGE
        elif (weight > cutoffs[2]):
            return MarkerType.BLUE
        elif (weight > cutoffs[1]):
            return MarkerType.GREEN
        elif (weight > cutoffs[0]):
            return MarkerType.YELLOW
        else:
            return MarkerType.RED

    def marker_to_flag(self, marker):
        if (marker == MarkerType.RED):
            return Actions.DROP_RED
        elif (marker == MarkerType.BLUE):
            return Actions.DROP_BLUE
        elif (marker == MarkerType.YELLOW):
            return Actions.DROP_YELLOW
        elif (marker == MarkerType.GREEN):
            return Actions.DROP_GREEN
        elif (marker == MarkerType.ORANGE):
            return Actions.DROP_ORANGE
        else:
            return Actions.DROP_NONE

    def get_move(self, view):
        if(self.storage_remaining() == 0):
            self.goinghome = True
        if(self.goinghome):
            # You are t home
            if(self.toHome == []):
                self.goinghome = False
                return (Actions.DROPOFF, Actions.DROP_NONE)
            # Trace your steps back home
            prevAction = self.toHome.pop()
            revAction = self.OppositeDir(prevAction)
            assert(isinstance(revAction, int))  
            return (revAction, Actions.DROP_NONE)

        adjacentWeights = self.adjacentWeights(view)
        total = 0
        weightList = []
        for i in range (0, 3):
            for j in range(0, 3):
                if (i != 1 or j != 1):
                    total = total + adjacentWeights[i][j]
                    weightList.append(total)
        rand = random.random()*total
        if (rand < weightList[0]):
            action = Actions.MOVE_NW
        elif (rand < weightList[1]):
            action = Actions.MOVE_N
        elif (rand < weightList[2]):
            action = Actions.MOVE_NE
        elif (rand < weightList[3]):
            action = Actions.MOVE_W
        elif (rand < weightList[4]):
            action = Actions.MOVE_E
        elif (rand < weightList[5]):
            action = Actions.MOVE_SW
        elif (rand < weightList[6]):
            action = Actions.MOVE_S
        else:
            action = Actions.MOVE_SE
        cur = int(len(view)/2)
        currentTile = view[cur][cur][0]
        dropFlag = self.marker_to_flag(self.determine_flag(adjacentWeights[1][1]))
        tileType = currentTile.GetType()
        if (tileType == TileType.Base and self.held_value() > 0):
            return (Actions.DROPOFF, dropFlag)
        elif (tileType == TileType.Resource and currentTile.AmountRemaining() > 0):
            return (Actions.MINE, dropFlag)
        else:
            self.toHome.append(action)
            return (action, dropFlag)
