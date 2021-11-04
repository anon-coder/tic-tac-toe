def checkWinner(table:list[list[str]], symbol:str) -> bool: #returns True if player with 'symbol' has won, False if not.
    winning_comb = [symbol]*3
    
    if winning_comb in table: #check rows
        return True

    for col in range(3): #check columns
        if table[0][col] == table[1][col] == table[2][col] == symbol:
            return True

    if symbol == table[0][2] == table[1][1] == table[2][0]: #check secondary diagonal
        return True

    if symbol == table[0][0] == table[1][1] == table[2][2]: #check main diagonal
        return True
    
    return False

def printTable(table:list[list[str]]):
    for row in table:
        print(row)

def getSymbol(curr_player:bool) -> str:
    return 'X' if curr_player else 'O'

def scorePosition(table:list[list[int]]) -> int: #returns 10 if player with 'X' has won, -10 if opponent has won, 0 if draw, None if not a terminal position
    if checkWinner(table,'X'): #'X' won
        return 10
    if checkWinner(table,'O'): #'O' won
        return -10
    if all(None not in table[i] for i in range(3)): #no empty squares, draw
        return 0
    return None

def bestMove(table:list[list[int]],curr_player:bool) -> tuple: #returns best move for current player (using minimax)
    symbol = getSymbol(curr_player)
    bestScore = -100 if curr_player else 100 #First player (X) is maximizer, second player (O) is minimizer
    topMove = None
    for i in range(3):
        for j in range(3):

            if table[i][j] == None:
                table[i][j] = symbol #making a temporary move

                if curr_player:
                    curr_score = MiniMax(table,0,False)
                    if bestScore<curr_score:
                        bestScore = curr_score
                        topMove = i,j
                        
                else:
                    curr_score = MiniMax(table,0,True)
                    if bestScore>curr_score:
                        bestScore = curr_score
                        topMove = i,j
                table[i][j] = None #undoing the move
    return topMove,bestScore

def MiniMax(table:list[list[int]],depth:int,toMaximize:bool) -> int: #returns a score for the current position in table using recursion and the heuristic of score - depth.
    curr_score = scorePosition(table)
    if curr_score != None:  #if it isnt None
        if curr_score == 10:
            curr_score -= depth
        elif curr_score == -10:
            curr_score += depth
        # print("Terminal stage:")
        # printTable(table)
        # print(curr_score)
        return curr_score
        
    if toMaximize: #trying to maximize the score
        bestScore = -100

        for i in range(3):
            for j in range(3):

                if table[i][j] == None:

                    table[i][j] = 'X' #making a temporary move
                    curr_score = MiniMax(table,depth+1,False)
                    bestScore = max(bestScore,curr_score)
                    table[i][j] = None #undoing the move

    else: #trying to minimize the score
        bestScore = 100

        for i in range(3):
            for j in range(3):

                if table[i][j] == None:

                    table[i][j] = 'O' #making a temporary move
                    curr_score = MiniMax(table,depth+1,True)
                    bestScore = min(bestScore,curr_score)
                    table[i][j] = None #undoing the move

    # print("Nonterminal:")
    # printTable(table)
    # print(bestScore)
    return bestScore
                    
table = [[None]*3 for _ in range(3)]
