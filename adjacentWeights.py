    
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
        
    def adjacentWeights(self, view):
      maxDist = (int)(len(view)/2)
      length = len(view)
      weights = [[0 for x in range(length)] for y in range(length)]
      for x in range(maxDist):
        # - Up
        for y in range(length):
          weights[x][y] = self.getWeightAvg(view, x, y, length, maxDist)

        nx = length - x - 1
        # - Down
        for y in range(length):
          weights[nx][y] = self.getWeightAvg(view, nx, y, length, maxDist)

        ny = x
        # | Left
        for nx in range(length):
          weights[nx][ny] = self.getWeightAvg(view, nx, ny, length, maxDist)

        ny = length - x - 1
        # | Right
        for nx in range(length):
          weights[nx][ny] = self.getWeightAvg(view, nx, ny, length, maxDist)
      return weights

    def getMarkerValue(self, view, x, y):
      if(len(view[x][y][2]) == 0): 
        return 0
      minColor = min(view[x][y][2])
      return {
        '0': 1,
        '1': 4,
        '2': 9,
        '3': 16,
        '4': 25
      }[minColor]

    def getWeightAvg(self, view, x, y, length, maxDist):
      if(view[x][y][0].GetType() == TileType.Mountain):
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
            adjWeight += self.getWeight(view, x, y)
            adjNum += 1
      if(adjNum > 0):
        adjWeight /= adjNum
      return (curWeight + adjWeight) / 2

    def dist(self, x, y, length):
      return min(abs(x-length/2), abs(y-length/2))

    def getWeight(self, view, x, y):
      totalWeight = self.getMarkerValue(view, x, y)
      if(totalWeight > 0): return totalWeight
      totalWeight = 3
      if(view[x][y][0].GetType() == TileType.Resource):
        totalWeight += 10
      return totalWeight