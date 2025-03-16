import os
import pygame
from pygame.locals import *
from main import get_board, moves_for_piece, apply_move, set_board, play_move, can_move

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)
SQUARE_SIZE = SCREEN_WIDTH // 8

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Checkers Sweets")
script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, 'sweets_logo.png')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
def get_available_moves(board, piece_pos):
    return moves_for_piece(board, board[piece_pos[0]][piece_pos[1]][1], board[piece_pos[0]][piece_pos[1]][2], piece_pos[0], piece_pos[1], True)

def draw_available_moves(board, selected_piece):
    if selected_piece:
        available_moves = massacre_available_moves_fun(get_available_moves(board, selected_piece))
        for move_pos in available_moves:
            if move_pos != None:
                pygame.draw.circle(screen, GREEN, (move_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2, move_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 5)

def get_clicked_piece(mouse_pos):
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    if 0 <= row < 8 and 0 <= col < 8:
        return row, col
    return None

def draw_alert(text):
    alert_rect = pygame.Rect(150, 250, 300, 100)
    pygame.draw.rect(screen, GRAY, alert_rect)
    pygame.draw.rect(screen, BLACK, alert_rect, 2)
    
    font = pygame.font.Font(None, 36)
    alert_text = font.render(text, True, BLACK)
    text_rect = alert_text.get_rect(center=alert_rect.center)
    
    screen.blit(alert_text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                waiting = False

def draw_board(board, selected_piece):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece[0]:  
                piece_color = WHITE if piece[1] else BLACK
                piece_radius = SQUARE_SIZE // 3
                pygame.draw.circle(screen, piece_color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), piece_radius)
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), piece_radius + 3, 3)  
                if selected_piece == (row, col):  
                    pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), piece_radius + 3, 3)  
                if piece[2]:  
                    king_radius = SQUARE_SIZE // 6
                    pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), king_radius)
                    pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), king_radius + 2, 2)  

def is_sublist(list1, list2):
    len_list1 = len(list1)
    len_list2 = len(list2)

    for i in range(len_list2 - len_list1 + 1):
        if list2[i:i + len_list1] == list1:
            return list2[:i + len_list1]
    
    return None

def first_step_available_moves_fun(available_moves):
    moves_to_ret = []
    for move in available_moves:
        if (len(move) == 3):
            moves_to_ret.append(move)
        else:
            moves_to_ret.append([move[0], move[1]])
    return moves_to_ret
                
def massacre_available_moves_fun(available_moves):
    moves_to_ret = []
    for move2 in available_moves:
        move = move2.copy()
        while len(move) != 0:
            if (len(move) == 3):
                moves_to_ret.append(move)
                break
            moves_to_ret.append([move[0], move[1]])
            move = move[2:]
    return moves_to_ret

def main():
    running = True
    selected_piece = None  
    available_moves = []
    play  = True
    set_play = False
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and play: 
                mouse_pos = pygame.mouse.get_pos()
                old_selected_piece = selected_piece
                selected_piece = get_clicked_piece(mouse_pos)
                first_step_available_moves = first_step_available_moves_fun(available_moves)
                massacre_available_moves = massacre_available_moves_fun(available_moves)
                if [selected_piece[0], selected_piece[1]] in first_step_available_moves and selected_piece != old_selected_piece:
                    set_board(apply_move(get_board(), old_selected_piece[0], old_selected_piece[1], [selected_piece[0], selected_piece[1]]))
                    available_moves = []
                    set_play = True
                    continue
                if [selected_piece[0], selected_piece[1]] in massacre_available_moves and selected_piece != old_selected_piece:
                    for move in available_moves:
                        potential_move = is_sublist([selected_piece[0], selected_piece[1]], move)
                        if (potential_move != None):
                            set_board(apply_move(get_board(), old_selected_piece[0], old_selected_piece[1], potential_move))
                            available_moves = []
                            set_play = True
                            continue
                if [selected_piece[0], selected_piece[1], True] in massacre_available_moves and selected_piece != old_selected_piece:
                    for move in available_moves:
                        potential_move = is_sublist([selected_piece[0], selected_piece[1], True], move)
                        if (potential_move != None):
                            set_board(apply_move(get_board(), old_selected_piece[0], old_selected_piece[1], potential_move))
                            available_moves = []
                            set_play = True
                            continue
                if [selected_piece[0], selected_piece[1]] in first_step_available_moves and selected_piece != old_selected_piece:
                    set_board(apply_move(get_board(), old_selected_piece[0], old_selected_piece[1], [selected_piece[0], selected_piece[1]]))
                    available_moves = []
                    set_play = True
                if [selected_piece[0], selected_piece[1]] in available_moves and selected_piece != old_selected_piece: 
                    set_board(apply_move(get_board(), old_selected_piece[0], old_selected_piece[1], [selected_piece[0], selected_piece[1]]))
                    available_moves = []
                    set_play = True
                if [selected_piece[0], selected_piece[1], True] in available_moves and selected_piece != old_selected_piece: 
                    set_board(apply_move(get_board(), old_selected_piece[0], old_selected_piece[1], [selected_piece[0], selected_piece[1], True]))
                    available_moves = []
                    set_play = True
                else:
                    if (get_board()[selected_piece[0]][selected_piece[1]][0] == False or (get_board()[selected_piece[0]][selected_piece[1]][0] and get_board()[selected_piece[0]][selected_piece[1]][1] == False)):
                        available_moves = []
                        selected_piece = None
                        continue
                    available_moves = get_available_moves(get_board(), selected_piece)

        screen.fill(BLACK)
        draw_board(get_board(), selected_piece)
        draw_available_moves(get_board(), selected_piece)
        
        if not play:
            if not can_move(False):
                draw_alert("Epic win!")
            play_move()
            play = True
            
        if set_play:
            play = False
            set_play = False
        else:
            if not can_move(play):
                if play:
                    draw_alert("You have lost!")
                else:
                    draw_alert("Epic win!")
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()