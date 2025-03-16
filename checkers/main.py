from board_operations import generate_board, print_board
import copy

board = generate_board()
memoization_dict = {}

def static_eval(board):
    elo = 0
    if (board[0][0][0] == True and board[0][0][1] == False and board[0][2][0] == True and board[0][2][1] == False and board[0][4][0] == True and board[0][4][1] == False and board[0][6][0] == True and board[0][6][1] == False):
        elo += 200
    if (board[7][1][0] == True and board[7][1][1] == True and board[7][3][0] == True and board[7][3][1] == True and board[7][5][0] == True and board[7][5][1] == True and board[7][7][0] == True and board[7][7][1] == True):
        elo -= 200  
    for i in range(0, 8, 2):
        if board[0][i][0] == True:
            if board[0][i][1] == False:
                elo += 50
                if (board[0][i][2] == True):
                    elo += 30
            else:
                elo -= 30
    for i in range(1, 7, 2):
        if board[7][i][0] == True:
            if board[7][i][1] == False:
                elo += 30
                if (board[6][i-1][0] == True and board[6][i-1][1] == False):
                    elo += 5
                if (board[6][i+1][0] == True and board[6][i+1][1] == False):
                    elo += 5
            else:
                elo -= 50
                if (board[7][i][2] == True):
                    elo -= 30
                if (board[6][i-1][0] == True and board[6][i-1][1] == True):
                    elo -= 5
                if (board[6][i+1][0] == True and board[6][i+1][1] == True):
                    elo -= 5
    if board[7][7][0] == True:
        if board[7][7][1] == False:
            elo += 30
            if (board[6][6][0] == True and board[6][6][1] == False):
                elo += 5
        else:
            elo -= 50
            if (board[7][7][2] == True):
                elo -= 30
            if (board[6][6][0] == True and board[6][6][1] == True):
                elo -= 5
    for i in range(1, 7, 2):
        for j in range(1, 7, 2):
            if (board[i][j][0] == True):
                if (board[i][j][1] == False):
                    elo += 2
                    if (board[i][j][2] == True):
                        elo += 30
                    if (board[i-1][j-1][0] == True and board[i-1][j-1][1] == False):
                        elo += 5
                    if (board[i-1][j+1][0] == True and board[i-1][j+1][1] == False):
                        elo += 5
                else:
                    elo -= 2
                    if (board[i][j][2] == True):
                        elo -= 30
                    if (board[i-1][j-1][0] == True and board[i-1][j-1][1] == True):
                        elo -= 5
                    if (board[i-1][j+1][0] == True and board[i-1][j+1][1] == True):
                        elo -= 5
        if (board[i][7][0] == True):
            if (board[i][7][1] == False):
                elo += 16
                if (board[i][7][2] == True):
                    elo += 30
                if (board[i-1][6][0] == True and board[i-1][6][1] == False):
                    elo += 5
            else:
                elo -= 16
                if (board[i][7][2] == True):
                    elo -= 30
                if (board[i-1][6][0] == True and board[i-1][6][1] == True):
                    elo -= 5
    for i in range(2, 8, 2): 
        for j in range(2, 8, 2):
            if (board[i][j][0] == True):
                if (board[i][j][1] == False):
                    elo += 2
                    if (board[i][j][2] == True):
                        elo += 30
                    if (board[i-1][j-1][0] == True and board[i-1][j-1][1] == False):
                        elo += 5
                    if (board[i-1][j+1][0] == True and board[i-1][j+1][1] == False):
                        elo += 5
                else:
                    elo -= 2
                    if (board[i][j][2] == True):
                        elo -= 30
                    if (board[i-1][j-1][0] == True and board[i-1][j-1][1] == True):
                        elo -= 5
                    if (board[i-1][j+1][0] == True and board[i-1][j+1][1] == True):
                        elo -= 5                       
        if (board[i][0][0] == True):
            if (board[i][0][1] == False):
                elo += 16
                if (board[i][0][2] == True):
                    elo += 30
                if (board[i-1][1][0] == True and board[i-1][1][1] == False):
                    elo += 5
            else:
                elo -= 16
                if (board[i][0][2] == True):
                    elo -= 30
                if (board[i-1][1][0] == True and board[i-1][1][1] == True):
                    elo -= 5                
    return elo

def moves_for_piece(board, white, king, y, x, allow_single_jump):
    moves_to_ret = []
    if allow_single_jump:
        if board[y][x][0] == False:
            return moves_to_ret
    if white:
        if king:
            if allow_single_jump:
                if (x > 0 and y > 0 and board[y-1][x-1][0] == False):
                    moves_to_ret.append([y-1, x-1])
                if (x > 0 and y < 7 and board[y+1][x-1][0] == False):
                    moves_to_ret.append([y+1, x-1])
                if (x < 7 and y < 7 and board[y+1][x+1][0] == False):
                    moves_to_ret.append([y+1, x+1])
                if (x < 7 and y > 0 and board[y-1][x+1][0] == False):
                    moves_to_ret.append([y-1, x+1])
            if (x < 6 and y > 1 and board[y-1][x+1][0] == True and board[y-1][x+1][1] == False and board[y-2][x+2][0] == False):
                board[y-1][x+1][0] = False
                moves = moves_for_piece(board, white, king, y-2, x+2, False)
                if not moves:
                    moves_to_ret.append([y-2, x+2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y-2, x+2]+move) 
                board[y-1][x+1][0] = True
            if (x > 1 and y > 1 and board[y-1][x-1][0] == True and board[y-1][x-1][1] == False and board[y-2][x-2][0] == False):
                board[y-1][x-1][0] = False
                moves = moves_for_piece(board, white, king, y-2, x-2, False)
                if not moves:
                    moves_to_ret.append([y-2, x-2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y-2, x-2]+move)
                board[y-1][x-1][0] = True
            if (x > 1 and y < 6 and board[y+1][x-1][0] == True and board[y+1][x-1][1] == False and board[y+2][x-2][0] == False):
                board[y+1][x-1][0] = False
                moves = moves_for_piece(board, white, king, y+2, x-2, False)
                if not moves:
                    moves_to_ret.append([y+2, x-2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y+2, x-2]+move)
                board[y+1][x-1][0] = True
            if (x < 6 and y < 6 and board[y+1][x+1][0] == True and board[y+1][x+1][1] == False and board[y+2][x+2][0] == False):
                board[y+1][x+1][0] = False
                moves = moves_for_piece(board, white, king, y+2, x+2, False)
                if not moves:
                    moves_to_ret.append([y+2, x+2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y+2, x+2]+move)
                board[y+1][x+1][0] = True  
        else:
            if (x > 0 and board[y-1][x-1][0] == False):
                if allow_single_jump:
                    if y == 1:
                        moves_to_ret.append([y-1, x-1, True])
                    else:
                        moves_to_ret.append([y-1, x-1])
            if (x > 1 and y > 1 and board[y-1][x-1][0] == True and board[y-1][x-1][1] == False and board[y-2][x-2][0] == False):
                if (y == 2):
                    moves_to_ret.append([y-2, x-2, True])
                else:
                    board[y-1][x-1][0] = False
                    moves = moves_for_piece(board, white, king, y-2, x-2, False)
                    if not moves:
                        moves_to_ret.append([y-2, x-2])
                    else:
                        for move in moves:
                            if (move != None):
                                moves_to_ret.append([y-2, x-2]+move)
                    board[y-1][x-1][0] = True
            if (x < 7 and board[y-1][x+1][0] == False):
                if allow_single_jump:
                    if y == 1:
                        moves_to_ret.append([y-1, x+1, True])
                    else:
                        moves_to_ret.append([y-1, x+1])
            if (x < 6 and y > 1 and board[y-1][x+1][0] == True and board[y-1][x+1][1] == False and board[y-2][x+2][0] == False):
                if (y == 2):
                    moves_to_ret.append([y-2, x+2, True])
                else:
                    board[y-1][x+1][0] = False
                    moves = moves_for_piece(board, white, king, y-2, x+2, False)
                    if not moves:
                        moves_to_ret.append([y-2, x+2])
                    else:
                        for move in moves:
                            if (move != None):
                                moves_to_ret.append([y-2, x+2]+move)
                    board[y-1][x+1][0] = True  
    else:
        if king:
            if allow_single_jump:
                if (x > 0 and y > 0 and board[y-1][x-1][0] == False):
                    moves_to_ret.append([y-1, x-1])
                if (x > 0 and y < 7 and board[y+1][x-1][0] == False):
                    moves_to_ret.append([y+1, x-1])
                if (x < 7 and y < 7 and board[y+1][x+1][0] == False):
                    moves_to_ret.append([y+1, x+1])
                if (x < 7 and y > 0 and board[y-1][x+1][0] == False):
                    moves_to_ret.append([y-1, x+1])
            if (x < 6 and y > 1 and board[y-1][x+1][0] == True and board[y-1][x+1][1] == True and board[y-2][x+2][0] == False):
                board[y-1][x+1][0] = False
                moves = moves_for_piece(board, white, king, y-2, x+2, False)
                if not moves:
                    moves_to_ret.append([y-2, x+2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y-2, x+2]+move)
                board[y-1][x+1][0] = True
            if (x > 1 and y > 1 and board[y-1][x-1][0] == True and board[y-1][x-1][1] == True and board[y-2][x-2][0] == False):
                board[y-1][x-1][0] = False
                moves = moves_for_piece(board, white, king, y-2, x-2, False)
                if not moves:
                    moves_to_ret.append([y-2, x-2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y-2, x-2]+move)
                board[y-1][x-1][0] = True
            if (x > 1 and y < 6 and board[y+1][x-1][0] == True and board[y+1][x-1][1] == True and board[y+2][x-2][0] == False):
                board[y+1][x-1][0] = False
                moves = moves_for_piece(board, white, king, y+2, x-2, False)
                if not moves:
                    moves_to_ret.append([y+2, x-2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y+2, x-2]+move)
                board[y+1][x-1][0] = True
            if (x < 6 and y < 6 and board[y+1][x+1][0] == True and board[y+1][x+1][1] == True and board[y+2][x+2][0] == False):
                board[y+1][x+1][0] = False
                moves = moves_for_piece(board, white, king, y+2, x+2, False)
                if not moves:
                    moves_to_ret.append([y+2, x+2])
                else:
                    for move in moves:
                        if (move != None):
                            moves_to_ret.append([y+2, x+2]+move)
                board[y+1][x+1][0] = True  
        else:
            if (x > 0 and board[y+1][x-1][0] == False):
                if allow_single_jump:
                    if y == 6:
                        moves_to_ret.append([y+1, x-1, True])
                    else:
                        moves_to_ret.append([y+1, x-1])
            if (x > 1 and y < 6 and board[y+1][x-1][0] == True and board[y+1][x-1][1] == True and board[y+2][x-2][0] == False):
                if (y == 5):
                    moves_to_ret.append([y+2, x-2, True])
                else:
                    board[y+1][x-1][0] = False
                    moves = moves_for_piece(board, white, king, y+2, x-2, False)
                    if not moves:
                        moves_to_ret.append([y+2, x-2])
                    else:
                        for move in moves:
                            if (move != None):
                                moves_to_ret.append([y+2, x-2]+move)
                    board[y+1][x-1][0] = True
            if (x < 7 and board[y+1][x+1][0] == False):
                if allow_single_jump:
                    if y == 6:
                        moves_to_ret.append([y+1, x+1, True])
                    else:
                        moves_to_ret.append([y+1, x+1])
            if (x < 6 and y < 6 and board[y+1][x+1][0] == True and board[y+1][x+1][1] == True and board[y+2][x+2][0] == False):
                if (y == 5):
                    moves_to_ret.append([y+2, x+2, True])
                else:
                    board[y+1][x+1][0] = False
                    moves = moves_for_piece(board, white, king, y+2, x+2, False)
                    if not moves:
                        moves_to_ret.append([y+2, x+2])
                    else:
                        for move in moves:
                            if (move != None):
                                moves_to_ret.append([y+2, x+2]+move)
                    board[y+1][x+1][0] = True 
    return moves_to_ret

def is_terminal(board):
    terminal = True
    for i in range(8):
            for j in range(8):
                if board[i][j][0]:
                    if not (not moves_for_piece(board, board[i][j][1], board[i][j][2], i, j, True)):
                        terminal = False
                        break
    return terminal 

def apply_move(board_passed, y, x, move):
    if move == None:
        return board_passed
    board = copy.deepcopy(board_passed)
    left_moves = len(move)
    if left_moves%2 == 1:
        board[y][x][2] = True
        left_moves -= 1
    i = 0
    while left_moves > 0:
        if abs(y-move[i]) == 2:
            board[move[i]][move[i+1]] = board[y][x].copy()
            board[y][x][0] = False
            board[y+(move[i]-y)//2][x+(move[i+1]-x)//2][0] = False
            y = move[i]
            x = move[i+1]
            i += 2
            left_moves -= 2
            continue
        else:
            board[move[i]][move[i+1]] = board[y][x].copy()
            board[y][x][0] = False
            break
    return board

def board_to_tuple(board):
    return tuple(tuple(cell) for row in board for cell in row)
        
def minimax(board, depth, alpha, beta, maximizing_player):
    global memoization_dict
    if depth == 0 or is_terminal(board):
        return static_eval(board), None

    board_tuple = board_to_tuple(board)
    
    if (board_tuple, depth, alpha, beta, maximizing_player) in memoization_dict:
        return memoization_dict[(board_tuple, depth, alpha, beta, maximizing_player)]
    
    best_move = None
    
    if maximizing_player:
        max_eval = float('-inf')
        for i in range(8):
            for j in range(8):
                if board[i][j][0]:
                    if (board[i][j][1] == False):
                        for move in moves_for_piece(board, board[i][j][1], board[i][j][2], i, j, True):
                            if move != None:
                                new_board = apply_move(board, i, j, move)
                                eval, _,  = minimax(new_board, depth - 1, alpha, beta, False)
                                if eval > max_eval:
                                    max_eval = eval
                                    if move == None:
                                        move = [i, j]
                                    else:
                                        move = move + [i, j]
                                    best_move = move
                                alpha = max(alpha, eval)
                                if beta <= alpha:
                                    break
        memoization_dict[(board_tuple, depth, alpha, beta, maximizing_player)] = (max_eval, best_move)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for i in range(8):
            for j in range(8):
                if board[i][j][0]:
                    if (board[i][j][1] == True):
                        for move in moves_for_piece(board, board[i][j][1], board[i][j][2], i, j, True):
                            if move != None:
                                new_board = apply_move(board, i, j, move)
                                eval, _ = minimax(new_board, depth - 1, alpha, beta, True)
                                if eval < min_eval:
                                    min_eval = eval
                                    if move == None:
                                        move = [i, j]
                                    else:
                                        move = move+[i, j]
                                    best_move = move
                                beta = min(beta, eval)
                                if beta <= alpha:
                                    break
        memoization_dict[(board_tuple, depth, alpha, beta, maximizing_player)] = (min_eval, best_move)
        return min_eval, best_move  

def get_board():
    return board
def set_board(boardPassed):
    global board
    board = boardPassed
def print_board_main():
    print_board(board)

def play_move():
    global board
    board_elo = 0
    for i in range(8):
            for j in range(8):
                if board[i][j][0]:
                    if (board[i][j][2] == True):
                        board_elo += 2
                    else:
                        board_elo += 1
    if (board_elo > 12): 
        minimaxx = minimax(board, 4, float('-inf'), float('inf'), True)[1]
        if minimaxx != None:
            if len(minimaxx) > 2:
                move = minimaxx[:len(minimaxx)-2]
        else:
            return
        board = apply_move(board, minimaxx[len(minimaxx)-2], minimaxx[len(minimaxx)-1], move)
    elif (board_elo > 6):
        minimaxx = minimax(board, 5, float('-inf'), float('inf'), True)[1]
        if minimaxx != None:
            if len(minimaxx) > 2:
                move = minimaxx[:len(minimaxx)-2]
        else:
            return
        board = apply_move(board, minimaxx[len(minimaxx)-2], minimaxx[len(minimaxx)-1], move)
    elif (board_elo > 0):
        minimaxx = minimax(board, 6, float('-inf'), float('inf'), True)[1]
        if minimaxx != None:
            if len(minimaxx) > 2:
                move = minimaxx[:len(minimaxx)-2]
        else:
            return
        board = apply_move(board, minimaxx[len(minimaxx)-2], minimaxx[len(minimaxx)-1], move)
        
def can_move(white):
    for i in range(8):
            for j in range(8):
                if board[i][j][0] and board[i][j][1] == white:
                    if not(not moves_for_piece(board, white, board[i][j][2], i, j, True)):
                        return True
    return False

if __name__ == "__main__":
    pass
    
