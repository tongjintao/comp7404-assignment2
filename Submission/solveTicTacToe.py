import random, util
import copy

def isValidMove(move, boards, validBoards):

  if len(move) < 2:
    return False

  if(move[0] == 'A' or move[0] == 'B' or move[0] == 'C' ):
    if not validBoards[move[0]]:
      return False
    if move[1].isdigit():  
      num = int(move[1])
    if(num >=0 and num <9): 
      if boards[move[0]][num] != "X":      
        return True
  return False

def makeMove(move, boards):
  newBoards = copy.deepcopy(boards)
  num = int(move[1])
  newBoards[move[0]][num] = "X"
  return newBoards

  
def drawBoard(boards, validBoards):    
  print "A:      B:      C:"
  for i in range(3):
    for c in 'ABC':
      for j in range(3):
        if validBoards[c]:
          print boards[c][j+i*3],
        else:
          print "+",
      print " ",
    print 

def checkEndGame(boards, validBoards):
  for c in 'ABC':
    for i in range(3):
      if validBoards[c]:    
        if(boards[c][3*i] == "X" and boards[c][3*i+1] == "X" and boards[c][3*i+2] == "X" ):
          validBoards[c] = False
        if(boards[c][i] == "X" and boards[c][i+3] == "X" and boards[c][i+6] == "X"):
          validBoards[c] = False
    if validBoards[c]:
      if(boards[c][0] == "X" and boards[c][4] == "X" and boards[c][8] == "X"):
        validBoards[c] = False
      if(boards[c][2] == "X" and boards[c][4] == "X" and boards[c][6] == "X"):
        validBoards[c] = False

  for c in 'ABC':
    if validBoards[c] == True:
      return False
  return True

def generateLegalMove(boards, validBoards):
  legalMoves = []
  for c in 'ABC':
    for i in range(9):
      move = c + str(i) 
      if isValidMove(move, boards, validBoards):
        legalMoves.append(move)
  return legalMoves

def clockwise(board):
  newBoard = [str(i) for i in range(9)]

  if board[0] == "X":
    newBoard[2] = "X"
  if board[1] == "X":
    newBoard[5] = "X"
  if board[2] == "X":
    newBoard[8] = "X"
  if board[3] == "X":
    newBoard[1] = "X"
  if board[4] == "X":
    newBoard[4] = "X"
  if board[5] == "X":
    newBoard[7] = "X"
  if board[6] == "X":
    newBoard[0] = "X"
  if board[7] == "X":
    newBoard[3] = "X"
  if board[8] == "X":
    newBoard[6] = "X"

  return newBoard


def reflect(board):
  newBoard = [str(i) for i in range(9)]

  if board[0] == "X":
    newBoard[2] = "X"
  if board[1] == "X":
    newBoard[1] = "X"
  if board[2] == "X":
    newBoard[0] = "X"
  if board[3] == "X":
    newBoard[5] = "X"
  if board[4] == "X":
    newBoard[4] = "X"
  if board[5] == "X":
    newBoard[3] = "X"
  if board[6] == "X":
    newBoard[8] = "X"
  if board[7] == "X":
    newBoard[7] = "X"
  if board[8] == "X":
    newBoard[6] = "X"

  return newBoard

def evaluateBoard(board):
  boardList = []
  boardList.append(['0', '1', '2', '3', '4', '5', '6', '7', '8', 'c']) #blank
  boardList.append(['X', '1', '2', '3', '4', '5', '6', '7', '8', '1']) #corner
  boardList.append(['0', 'X', '2', '3', '4', '5', '6', '7', '8', '1']) #one
  boardList.append(['0', '1', '2', '3', 'X', '5', '6', '7', '8', 'cc']) #middle
  boardList.append(['X', 'X', '2', '3', '4', '5', '6', '7', '8', 'ad']) #two
  boardList.append(['X', '1', 'X', '3', '4', '5', '6', '7', '8', 'b']) #two
  boardList.append(['X', '1', '2', '3', 'X', '5', '6', '7', '8', 'b']) #two
  boardList.append(['X', '1', '2', '3', '4', 'X', '6', '7', '8', 'b']) #two
  boardList.append(['X', '1', '2', '3', '4', '5', '6', '7', 'X', 'a']) #two
  boardList.append(['0', 'X', '2', 'X', '4', '5', '6', '7', '8', 'a']) #two
  boardList.append(['0', 'X', '2', '3', 'X', '5', '6', '7', '8', 'b']) #two
  boardList.append(['0', 'X', '2', '3', '4', '5', '6', 'X', '8', 'a']) #two
  boardList.append(['X', 'X', '2', 'X', '4', '5', '6', '7', '8', 'b']) #three
  boardList.append(['X', 'X', '2', '3', 'X', '5', '6', '7', '8', 'ab']) #three
  boardList.append(['X', 'X', '2', '3', '4', 'X', '6', '7', '8', 'd']) #three
  boardList.append(['X', 'X', '2', '3', '4', '5', 'X', '7', '8', 'a']) #three
  boardList.append(['X', 'X', '2', '3', '4', '5', '6', 'X', '8', 'd']) #three
  boardList.append(['X', 'X', '2', '3', '4', '5', '6', '7', 'X', 'd']) #three
  boardList.append(['X', '1', 'X', '3', 'X', '5', '6', '7', '8', 'a']) #three
  boardList.append(['X', '1', 'X', '3', '4', '5', 'X', '7', '8', 'ab']) #three
  boardList.append(['X', '1', 'X', '3', '4', '5', '6', 'X', '8', 'a']) #three
  boardList.append(['X', '1', '2', '3', 'X', 'X', '6', '7', '8', 'a']) #three
  boardList.append(['X', '1', '2', '3', '4', 'X', '6', 'X', '8', '1']) #three
  boardList.append(['0', 'X', '2', 'X', 'X', '5', '6', '7', '8', 'ab']) #three
  boardList.append(['0', 'X', '2', 'X', '4', 'X', '6', '7', '8', 'b']) #three
  boardList.append(['X', 'X', '2', 'X', 'X', '5', '6', '7', '8', 'a']) #four
  boardList.append(['X', 'X', '2', 'X', '4', 'X', '6', '7', '8', 'a']) #four
  boardList.append(['X', 'X', '2', 'X', '4', '5', '6', '7', 'X', 'a']) #four
  boardList.append(['X', 'X', '2', '3', 'X', 'X', '6', '7', '8', 'b']) #four
  boardList.append(['X', 'X', '2', '3', 'X', '5', 'X', '7', '8', 'b']) #four
  boardList.append(['X', 'X', '2', '3', '4', 'X', 'X', '7', '8', 'b']) #four
  boardList.append(['X', 'X', '2', '3', '4', 'X', '6', 'X', '8', 'ab']) #four
  boardList.append(['X', 'X', '2', '3', '4', 'X', '6', '7', 'X', 'ab']) #four
  boardList.append(['X', 'X', '2', '3', '4', '5', 'X', 'X', '8', 'b']) #four
  boardList.append(['X', 'X', '2', '3', '4', '5', 'X', '7', 'X', 'b']) #four
  boardList.append(['X', 'X', '2', '3', '4', '5', '6', 'X', 'X', 'a']) #four
  boardList.append(['X', '1', 'X', '3', 'X', '5', '6', 'X', '8', 'b']) #four
  boardList.append(['X', '1', 'X', '3', '4', '5', 'X', '7', 'X', 'a']) #four
  boardList.append(['X', '1', '2', '3', 'X', 'X', '6', 'X', '8', 'b']) #four
  boardList.append(['0', 'X', '2', 'X', '4', 'X', '6', 'X', '8', 'a']) #four
  boardList.append(['X', 'X', '2', 'X', '4', 'X', '6', '7', 'X', 'b']) #five
  boardList.append(['X', 'X', '2', '3', 'X', 'X', 'X', '7', '8', 'a']) #five
  boardList.append(['X', 'X', '2', '3', '4', 'X', 'X', 'X', '8', 'a']) #five
  boardList.append(['X', 'X', '2', '3', '4', 'X', 'X', '7', 'X', 'a']) #five
  boardList.append(['X', 'X', '2', 'X', '4', 'X', '6', 'X', 'X', 'a']) #six

  score = ""

  for refBoard in boardList:
      if(board==refBoard[:9] or board == clockwise(refBoard[:9]) or board == clockwise(clockwise(refBoard[:9])) or board == clockwise(clockwise(clockwise(refBoard[:9]))) ):
        score = refBoard[9]
      elif(board==reflect(refBoard[:9]) or board == clockwise(reflect(refBoard[:9])) or board == clockwise(clockwise(reflect(refBoard[:9]))) or board == clockwise(clockwise(clockwise(reflect(refBoard[:9])))) ):
        score = refBoard[9]
  return score

def evaluateGame(boards, validBoards):
  scoreList = {'a':0, 'b':0, 'c':0, 'd':0}
  totalScore = ''
  
  for c in 'ABC':
    if validBoards[c]:
      score = evaluateBoard(boards[c])
      totalScore += score
      #print c, " ", score

  #print "totalScore: ", totalScore

  for c in totalScore:
    if not c == '1':
      scoreList[c] += 1

  if scoreList == {'a':0, 'b':0, 'c':2, 'd':0}:
    return 100
  elif scoreList == {'a':1, 'b':0, 'c':0, 'd':0}:
    return 100
  elif scoreList == {'a':0, 'b':2, 'c':0, 'd':0}:
    return 100
  elif scoreList == {'a':0, 'b':1, 'c':1, 'd':0}:
    return 100
  else:
    return 0
    
def makeAIMove(turn, boards, validBoards):
  legalMoves = generateLegalMove(boards, validBoards)
  moveValue = {}
  winingMove = []

  for move in legalMoves:
    #print move
    newBoards = copy.deepcopy(boards)
    newValidBoards = copy.deepcopy(validBoards)
    newBoards = makeMove(move, newBoards)
    gameEnd = checkEndGame(newBoards, newValidBoards)
    #drawBoard(newBoards, newValidBoards)
    score = evaluateGame(newBoards, newValidBoards)
    #print score
    moveValue[move] = score
    if score == 100:
      winingMove.append(move)

  if len(winingMove) == 0:
    print "WTF? why no wining move"
  return random.choice(winingMove)
  #return max(moveValue, key=lambda i: moveValue[i])

print "Welcome to 3-Board Misere Tic-Tac-Toe"
AImoveFirst = True
turn = "AI"

while True:
  boards = {}
  validBoards = {}
  for c in 'ABC':
   boards[c] = [str(i) for i in range(9)]
   validBoards[c] = True
 
  if AImoveFirst:
    turn = "AI" 
  else: 
    turn = "Player"

  gameEnd = False

  while not gameEnd:
    if turn == "AI":
      move = makeAIMove(turn, boards, validBoards)
      print "AI made this move: ", move
    else:
      move = raw_input("Your move: ")
      while not isValidMove(move, boards, validBoards):
        print ("This is not a valid move")
        move = raw_input("Your move: ")

    boards = makeMove(move, boards)
    gameEnd = checkEndGame(boards, validBoards)
    drawBoard(boards, validBoards)

    if turn == "AI":
      turn = "Player"
    else:
      turn ="AI"

    if gameEnd:
      print turn, " wins!"

  replay = raw_input("Want to play again?: [Y/N] ")

  if replay == "N":
    break





