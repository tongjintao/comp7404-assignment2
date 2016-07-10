# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"



        score = currentGameState.getScore()
        distGhost = [];
        distGhostNext = [];
        distScaredGhost = [];
        distScaredGhostNext = [];

        #organize a list of distance to the ghost and scared ghost
        for ghostState in newGhostStates:
          if(ghostState.scaredTimer == 0):
            ghostPosition = ghostState.getPosition()
            dg = util.manhattanDistance(ghostPosition, newPos)
            distGhost.append(dg)

            ghostDirection = ghostState.getDirection()
            
            if(ghostDirection == "North"):
              ghostPositionNext = (ghostPosition[0], ghostPosition[1] + 1)
            elif(ghostDirection == "South"):
              ghostPositionNext = (ghostPosition[0],ghostPosition[1] - 1)
            elif(ghostDirection == "East"):
              ghostPositionNext = (ghostPosition[0] + 1, ghostPosition[1])
            elif(ghostDirection == "West"):
              ghostPositionNext = (ghostPosition[0] - 1, ghostPosition[1])
            else:
              ghostPositionNext = ghostPosition

            dgn = util.manhattanDistance(ghostPositionNext, newPos)

            distGhostNext.append(dgn)

          else:
            ghostPosition = ghostState.getPosition()
            dsg = util.manhattanDistance(ghostPosition, newPos)
            distScaredGhost.append(dsg)

            ghostDirection = ghostState.getDirection()
            
            if(ghostDirection == "North"):
              ghostPositionNext = (ghostPosition[0], ghostPosition[1] + 1)
            elif(ghostDirection == "South"):
              ghostPositionNext = (ghostPosition[0],ghostPosition[1] - 1)
            elif(ghostDirection == "East"):
              ghostPositionNext = (ghostPosition[0] + 1, ghostPosition[1])
            elif(ghostDirection == "West"):
              ghostPositionNext = (ghostPosition[0] - 1, ghostPosition[1])
            else:
              ghostPositionNext = ghostPosition

            dsgn = util.manhattanDistance(ghostPositionNext, newPos)

            distScaredGhostNext.append(dsgn)

        #find number of capsule left
        numCapsuleLeft = len(currentGameState.getCapsules())

        foodList = newFood.asList()
        numFoodLeft = len(foodList)
        distFood = [];
        totalDistFood = 0

        #find all the distance to food
        for food in foodList:
          dF = util.manhattanDistance(food, newPos)
          distFood.append(dF)
          totalDistFood += dF

        foodList.append(newPos)
        explored = set()
        mstDistance = 0
        foodListGraph = {}
        
        #initialize distance within food point
        for i in foodList:
            for j in foodList:
                if i != j and (i, j) not in foodListGraph and (j, i) not in foodListGraph:
                  foodListGraph[(i, j)] = util.manhattanDistance(i, j)
                    
        #initialize separate set for each food point
        group = 1
        foodGroup = {}
        for point in foodList:
            foodGroup[point] = group
            group += 1

        #calculate minimum spanning tree distance
        for points, subdistance in sorted(foodListGraph.items(), key = lambda x:x[1]):
            if foodGroup[points[0]] != foodGroup[points[1]]:
                changeValue = foodGroup[points[0]]
                changedValue = foodGroup[points[1]]
                for x in foodList:
                    if foodGroup[x] == changeValue:
                        foodGroup[x] = changedValue

                mstDistance += subdistance

        indexClosestScaredGhost = 0
        indexClosestGhost = 0
        indexClosestFood = 0

        #turn the raw data into index value to prevent 1/0 from happening
        if distScaredGhost:
          indexClosestScaredGhost = 1 / min(distScaredGhost)      

        if distGhost:
          if(min(distGhost)==0 or min(distGhostNext)==0):
            return -float("inf")
          else:  
            indexClosestGhost = 1 / min(distGhost)

        if distFood:
          indexClosestFood = 1 / min(distFood)

        if(distGhost and (min(distGhost)==0 or min(distGhostNext)==0)):
          return -float("inf")
        elif(len(foodList)==0):
          return float("inf")
        else:
          #score -= 1/ min(distGhostNext)
          score -= 200 * indexClosestGhost
          score += 10 * indexClosestScaredGhost 
          score += 10 * indexClosestFood
          score -= 10 * mstDistance
          score -= 20 * numFoodLeft
          score -= 10 * numCapsuleLeft

        # if(action =="Stop"):
        #   score -= 5000
        # print(action)
        # print("position")
        # print(newPos)
        # print("score = minDistFood - mindistGhost - mstDistance - numFoodLeft - numCapupsleLeft")
        # print str(score)," = ", str(indexClosestFood)," - ",str(indexClosestScaredGhost)," - ",str(mstDistance)," - ",str(numFoodLeft)," - ",str(numCapsuleLeft)
        # print("scaredTimer: ")
        # print(ghostState.scaredTimer)
        # print("----------------------")
        
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    #the centralized function that leads to minValue function or maxValue function depending on the agent type
    def minimax(self, gameState, agentIndex, depth):
      if agentIndex >= gameState.getNumAgents():
        agentIndex = 0
        depth += 1

      if depth == self.depth or gameState.isWin() or gameState.isLose():
        #print "agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(self.evaluationFunction(gameState)))
        return self.evaluationFunction(gameState)


      if agentIndex == 0:
        return self.maxValue(gameState, agentIndex, depth)
      else:
        return self.minValue(gameState, agentIndex, depth)

    #the max node
    def maxValue(self, gameState, agentIndex, depth):
      v = -float("inf")

      actions = gameState.getLegalActions(agentIndex)
      actionValue = {}

      for action in actions:
        successorState = gameState.generateSuccessor(agentIndex, action)
        value = self.minimax(successorState, agentIndex + 1, depth)
        v = max(v, value)

      #print "MAX agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(v))        
      return v

    #the min node
    def minValue(self, gameState, agentIndex, depth):
      v = float("inf")

      actions = gameState.getLegalActions(agentIndex)
      actionValue = {}

      for action in actions:
        successorState = gameState.generateSuccessor(agentIndex, action)
        value = self.minimax(successorState, agentIndex + 1, depth)
        v = min(v, value)

      #print "MIN agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(v))
      return v

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        pacman = self.index
        actionValue = {}
        actions = gameState.getLegalActions(pacman)

        for action in actions:
          successorState = gameState.generateSuccessor(pacman, action)
          value = self.minimax(successorState, pacman+1, 0)
          actionValue[action] = value
          #print "%s PRIMARY NODE agentIndex: %s depth: %s score: %s" % (str(action), str(pacman), str(0), str(value))
      
        #print max(actionValue, key= lambda i: actionValue[i])

        return max(actionValue, key= lambda i: actionValue[i])


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def bestAction(self, gameState, pacman, depth, alpha, beta):
      v = -float("inf")

      actionValue = {}
      actions = gameState.getLegalActions(pacman)

      for action in actions:

        # if action == "Stop":
        #   continue

        successorState = gameState.generateSuccessor(pacman, action)
        value = self.minimax(successorState, pacman+1, 0, alpha, beta)
        #print "%s PRIMARY NODE agentIndex: %s depth: %s score: %s" % (str(action), str(pacman), str(0), str(value))
        v = max(v, value)
        actionValue[action] = value
        
        if v > beta:
          return v

        alpha = max(alpha, v)
      #print max(actionValue, key= lambda i: actionValue[i])

      return max(actionValue, key= lambda i: actionValue[i])

    def minimax(self, gameState, agentIndex, depth, alpha, beta):
      if agentIndex >= gameState.getNumAgents():
        agentIndex = 0
        depth += 1

      if depth == self.depth or gameState.isWin() or gameState.isLose():
        #print "agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(self.evaluationFunction(gameState)))
        return self.evaluationFunction(gameState)

      if agentIndex == 0:
        return self.maxValue(gameState, agentIndex, depth, alpha, beta)
      else:
        return self.minValue(gameState, agentIndex, depth, alpha, beta)

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
      v = -float("inf")

      actions = gameState.getLegalActions(agentIndex)
      
      for action in actions:
        successorState = gameState.generateSuccessor(agentIndex, action)
        value = self.minimax(successorState, agentIndex + 1, depth, alpha, beta)
        v = max(v, value)

        if v > beta:
          return v

        alpha = max(alpha, v)

      #print "MAX agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(v))        
      return v

    def minValue(self, gameState, agentIndex, depth, alpha, beta):
      v = float("inf")

      actions = gameState.getLegalActions(agentIndex)

      for action in actions:
        successorState = gameState.generateSuccessor(agentIndex, action)
        value = self.minimax(successorState, agentIndex + 1, depth, alpha, beta)
        v = min(v, value)

        if v < alpha:
          return v;

        beta = min(beta, v)

      #print "MIN agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(v))
      return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        pacman = self.index

        return self.bestAction(gameState, pacman, 0, -float("inf"),float("inf") )


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, gameState, agentIndex, depth):
      if agentIndex >= gameState.getNumAgents():
        agentIndex = 0
        depth += 1

      if depth == self.depth or gameState.isWin() or gameState.isLose():
        #print "agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(self.evaluationFunction(gameState)))
        return self.evaluationFunction(gameState)

      if agentIndex == 0:
        return self.maxValue(gameState, agentIndex, depth)
      else:
        return self.expectValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
      v = -float("inf")

      actions = gameState.getLegalActions(agentIndex)

      for action in actions:
        successorState = gameState.generateSuccessor(agentIndex, action)
        value = self.expectimax(successorState, agentIndex + 1, depth)
        v = max(v, value)

      #print "MAX agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(v))        
      return v

    def expectValue(self, gameState, agentIndex, depth):
      v = float("inf")

      actions = gameState.getLegalActions(agentIndex)
      totalValue = 0

      for action in actions:
        successorState = gameState.generateSuccessor(agentIndex, action)
        totalValue += self.expectimax(successorState, agentIndex + 1, depth)
        
      v = totalValue / len(actions)

      #print "EXPECTED agentIndex: %s depth: %s score: %s" % (str(agentIndex), str(depth), str(v))
      return v

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman = self.index
        actionValue = {}
        actions = gameState.getLegalActions(pacman)

        for action in actions:
          successorState = gameState.generateSuccessor(pacman, action)
          value = self.expectimax(successorState, pacman+1, 0)
          actionValue[action] = value
          #print "%s PRIMARY NODE agentIndex: %s depth: %s score: %s" % (str(action), str(pacman), str(0), str(value))
      
        #print max(actionValue, key= lambda i: actionValue[i])

        return max(actionValue, key= lambda i: actionValue[i])

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    score = currentGameState.getScore()
    distGhost = [];
    distGhostNext = [];
    distScaredGhost = [];
    distScaredGhostNext = [];

    for ghostState in newGhostStates:
      if(ghostState.scaredTimer == 0):
        ghostPosition = ghostState.getPosition()
        dg = util.manhattanDistance(ghostPosition, newPos)
        distGhost.append(dg)

        ghostDirection = ghostState.getDirection()
        
        if(ghostDirection == "North"):
          ghostPositionNext = (ghostPosition[0], ghostPosition[1] + 1)
        elif(ghostDirection == "South"):
          ghostPositionNext = (ghostPosition[0],ghostPosition[1] - 1)
        elif(ghostDirection == "East"):
          ghostPositionNext = (ghostPosition[0] + 1, ghostPosition[1])
        elif(ghostDirection == "West"):
          ghostPositionNext = (ghostPosition[0] - 1, ghostPosition[1])
        else:
          ghostPositionNext = ghostPosition

        dgn = util.manhattanDistance(ghostPositionNext, newPos)

        distGhostNext.append(dgn)

      else:
        ghostPosition = ghostState.getPosition()
        dsg = util.manhattanDistance(ghostPosition, newPos)
        distScaredGhost.append(dsg)

        ghostDirection = ghostState.getDirection()
        
        if(ghostDirection == "North"):
          ghostPositionNext = (ghostPosition[0], ghostPosition[1] + 1)
        elif(ghostDirection == "South"):
          ghostPositionNext = (ghostPosition[0],ghostPosition[1] - 1)
        elif(ghostDirection == "East"):
          ghostPositionNext = (ghostPosition[0] + 1, ghostPosition[1])
        elif(ghostDirection == "West"):
          ghostPositionNext = (ghostPosition[0] - 1, ghostPosition[1])
        else:
          ghostPositionNext = ghostPosition

        dsgn = util.manhattanDistance(ghostPositionNext, newPos)

        distScaredGhostNext.append(dsgn)


    numCapsuleLeft = len(currentGameState.getCapsules())

    foodList = newFood.asList()
    numFoodLeft = len(foodList)
    distFood = [];
    totalDistFood = 0

    for food in foodList:
      dF = util.manhattanDistance(food, newPos)
      distFood.append(dF)
      totalDistFood += dF

    foodList.append(newPos)
    explored = set()
    mstDistance = 0
    foodListGraph = {}
    
    #initialize distance within food point
    for i in foodList:
        for j in foodList:
            if i != j and (i, j) not in foodListGraph and (j, i) not in foodListGraph:
              foodListGraph[(i, j)] = util.manhattanDistance(i, j)
                
    #initialize separate set for each food point
    group = 1
    foodGroup = {}
    for point in foodList:
        foodGroup[point] = group
        group += 1

    #calculate minimum spanning tree distance
    for points, subdistance in sorted(foodListGraph.items(), key = lambda x:x[1]):
        if foodGroup[points[0]] != foodGroup[points[1]]:
            changeValue = foodGroup[points[0]]
            changedValue = foodGroup[points[1]]
            for x in foodList:
                if foodGroup[x] == changeValue:
                    foodGroup[x] = changedValue

            mstDistance += subdistance

    indexClosestScaredGhost = 0
    indexClosestGhost = 0
    indexClosestFood = 0

    if distScaredGhost:
      indexClosestScaredGhost = 1 / min(distScaredGhost)      

    if distGhost:
      if(min(distGhost)==0 or min(distGhostNext)==0):
        return -float("inf")
      else:  
        indexClosestGhost = 1 / min(distGhost)

    if distFood:
      indexClosestFood = 1 / min(distFood)

    if(distGhost and (min(distGhost)==0 or min(distGhostNext)==0)):
      return -float("inf")
    elif(len(foodList)==0):
      return float("inf")
    else:
      #score -= 1/ min(distGhostNext)
      score -= 200 * indexClosestGhost
      score += 10 * indexClosestScaredGhost 
      score += 10 * indexClosestFood
      score -= 10 * mstDistance
      score -= 20 * numFoodLeft
      score -= 10 * numCapsuleLeft

    # if(action =="Stop"):
    #   score -= 5000
    #print(action)
    print("position")
    print(newPos)
    print("score = minDistFood - mindistGhost - mstDistance - numFoodLeft - numCapupsleLeft")
    print str(score)," = ", str(indexClosestFood)," - ",str(indexClosestScaredGhost)," - ",str(mstDistance)," - ",str(numFoodLeft)," - ",str(numCapsuleLeft)
    print("scaredTimer: ")
    print(ghostState.scaredTimer)
    print("----------------------")
    
    return score



# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

