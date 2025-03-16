from tabulate import tabulate

# polje - 3 (prvo polje 1 ako je zauzeto, drugo polje 1 ako je beli igrac na njemu, trece polje 1 ako je kraljica, sve u suprotnom 0)
def generate_board():
    board = [
        [[True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False]],
        [[False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False]],
        [[True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False]],
        [[False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False]],
        [[False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False]],
        [[False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False]],
        [[True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False]],
        [[False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False]]
    ]
    return board

def print_board(board):
    def field_to_str(field):
        if not field[0]:
            return ' '  
        if field[1]: 
            return 'WK' if field[2] else 'W'
        else:  
            return 'BK' if field[2] else 'B'
    
    printable_board = [[field_to_str(field) for field in row] for row in board]
    
    print(tabulate(printable_board, tablefmt="grid"))
    
if __name__ == "__main__":
    pass


 
# board = [
#         [[True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False], [True, False, False], [False, False, False]],
#         [[False, False, False], [True, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [True, False, False]],
#         [[True, False, False], [False, False, False], [True, False, False], [False, False, False], [False, False, False], [False, False, False], [True, False, False], [False, False, False]],
#         [[False, False, False], [False, False, False], [False, False, False], [True, False, False], [False, False, False], [False, False, False], [False, False, False], [True, False, False]],
#         [[True, True, False], [False, False, False], [True, False, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False]],
#         [[False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False]],
#         [[False, False, False], [False, False, False], [True, True, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False]],
#         [[False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False], [False, False, False], [True, True, False]]
#     ]