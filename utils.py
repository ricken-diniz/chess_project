def get_square_matrix(n):
    M = [[0 for _ in range(n)] for _ in range(n)]
    return M

def get_initial_game(Piece: object, gametype):
    chessboard   = get_chessboard(gametype)
    white_pieces = ['K','Q','R','B','N','P']
    black_pieces = ['k','q','r','b','n','p']

    for lin in range(len(chessboard)):
        for col in range(len(chessboard[lin])):

            piece = chessboard[lin][col]
            if piece in white_pieces or piece in black_pieces:

                p                    = Piece(lin, col, chessboard, piece)
                chessboard[lin][col] = p

    return chessboard

def get_chessboard(chessboard_type = 'normalgame'):
    if chessboard_type == 'empty':
        chessboard = [['.' for _ in range(8)] for _ in range(8)]

    elif chessboard_type == 'normalgame':
        chessboard = [
            ['r','n','b','q','k','b','n','r'],

            ['p','p','p','p','p','p','p','p'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['P','P','P','P','P','P','P','P'],

            ['R','N','B','Q','K','B','N','R'],
        ]

    elif chessboard_type == 'hook':
        chessboard = [
            ['r','.','.','.','k','.','.','r'],

            ['p','p','.','p','p','p','p','p'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','n','.','.','.','.'],

            ['P','q','R','P','P','P','P','P'],

            ['R','.','.','.','K','.','.','R'],
        ]

    elif chessboard_type == 'shepherd':
        chessboard = [
            ['r','.','b','q','k','b','n','r'],

            ['.','p','p','p','.','p','p','p'],

            ['p','.','n','.','.','.','.','.'],

            ['.','.','.','.','p','.','.','.'],

            ['.','.','B','.','P','.','.','.'],

            ['.','.','.','.','.','Q','.','.'],

            ['P','P','P','P','.','P','P','P'],

            ['R','N','B','.','K','.','N','R'],
        ]

    elif chessboard_type == 'tower':
        chessboard = [
            ['r','r','r','r','r','r','r','r'],

            ['r','r','r','r','r','r','r','r'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['R','R','R','R','R','R','R','R'],

            ['R','R','R','R','R','R','R','R'],
        ]

    elif chessboard_type == 'matchenpassant':
        chessboard = [
            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','p','p'],

            ['.','.','.','.','.','.','p','k'],

            ['.','.','.','.','.','p','.','P'],

            ['.','.','.','.','.','.','.','B'],

            ['.','.','.','.','.','.','P','.'],

            ['K','.','.','.','B','.','.','.'],
        ]
    elif chessboard_type == 'continuouscheck':
        chessboard = [
            ['.','.','.','.','.','B','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','k','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],
        ]
    elif chessboard_type == 'pinnedpiece':
        chessboard = [
            ['.','.','.','.','.','B','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','n','.','.','.','.','.'],

            ['.','k','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],
        ]
    elif chessboard_type == 'promotepawn':
        chessboard = [
            ['.','.','.','.','.','.','.','.'],

            ['.','P','.','.','.','.','.','p'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],
        ]
    elif chessboard_type == 'stalemate':
        chessboard = [
            ['.','.','.','.','.','.','.','K'],

            ['.','.','.','.','.','.','.','.'],

            ['R','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','k','.','.','.','.','q','.'],

            ['.','.','.','.','.','.','.','.'],
        ]
    elif chessboard_type == 'defenseandattack':
        chessboard = [
            ['.','.','.','.','.','.','.','k'],

            ['.','.','.','.','.','.','.','.'],

            ['q','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','K','.','.','Q','.'],

            ['.','.','.','.','.','.','.','.'],
        ]
    elif chessboard_type == 'crazymate':
        chessboard = [
            ['.','.','.','.','.','.','r','k'],

            ['.','.','.','.','.','.','p','p'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','R'],

            ['.','.','.','K','.','.','.','Q'],

            ['.','.','.','.','.','.','.','.'],
        ]
    return chessboard

def show_chessboard(chessboard):
    r = [None, '\033[48;5;250m', '\033[48;5;65m']
    controller = 1
    output = ''
    i_axis = 8
    for line in chessboard:
        lin = []
        controller = -controller
        empty_space = '       '
        empty_line = '\n  ' + 4 * (r[controller] + empty_space + r[-controller] + empty_space) + '\033[0m'
        output += empty_line

        for e in line:

            if type(e) != str:
                if e.piece_color == -1:
                    e = f'{r[controller]}\033[38;5;88m   {e.piece}   \033[0m'
                else:
                    e = f'{r[controller]}\033[38;5;0m   {e.piece}   \033[0m'
                lin.append(e)

            else:
                lin.append(f'{r[controller]}       \033[0m')
            
            controller = -controller

        output += f'\n{i_axis} '+''.join(lin)
        output += empty_line
        i_axis -= 1

    output += '\n     A      B      C      D      E      F      G      H\n'

    return output

def show_movies(chessboard, piece_map):
    r = [None, '\033[48;5;250m', '\033[48;5;65m']
    controller = 1
    output = ''
    i_axis = 8
    for i in range(len(chessboard)):
        lin = []
        controller = -controller
        empty_space = '       '
        empty_line = '\n  ' + 4 * (r[controller] + empty_space + r[-controller] + empty_space) + '\033[0m'
        output += empty_line

        for j in range(len(chessboard[i])):
            if type(chessboard[i][j]) != str:
                e = chessboard[i][j]
                if e.piece_color == -1:
                    e = f'{r[controller]}\033[38;5;88m   {e.piece}   \033[0m'
                else:
                    e = f'{r[controller]}\033[38;5;0m   {e.piece}   \033[0m'
                
            else:
                e = f'{r[controller]}       \033[0m'
            
            if piece_map[i][j] == 1:
                lin.append(f'{r[controller]}\033[94m   *   \033[0m')
                
            elif piece_map[i][j] == 2:
                e = f'{r[controller]}\033[38m   {chessboard[i][j].piece}   \033[0m'
                lin.append(e)
                
            elif piece_map[i][j] in [3,4]:
                if type(chessboard[i][j]) != str:
                    e = f'{r[controller]}\033[95m   {chessboard[i][j].piece}   \033[0m'
                else:
                    e = f'{r[controller]}\033[95m   x   \033[0m'
                lin.append(e)
                
            else:
                lin.append(e)

                
            controller = -controller
        
        output += f'\n{i_axis} '+''.join(lin)
        output += empty_line
        i_axis -= 1
        
    output += '\n\n     A      B      C      D      E      F      G      H\n'
    return output

def deepcopy(M):

    matrix = []

    for lin in M:
        line = []
        for i in range(len(lin)):
            line.append(lin[i])
        matrix.append(line)

    return matrix

def deepcopy_list(l):

    new_list = []

    for e in l:
        new_list.append(e)
    
    return new_list

def affine_function(a, x, b):
    y = a*x + b
    return x, y

def has_check(i, j, chessboard, turn):
        
        for l in range(len(chessboard)):
            for c in range(len(chessboard)):
                if type(chessboard[l][c]) != str and chessboard[l][c].piece_color != turn:
                        enimy_piece_map = chessboard[l][c].piece_map
                        if enimy_piece_map[i][j] in [3,5,7] or chessboard[l][c].piece.lower() != 'p' and enimy_piece_map[i][j] == 1:
                            return True
        
        return False

def get_arrange(coordinates):
    letters = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7
    }
    numbers = {
        '8': 0,
        '7': 1,
        '6': 2,
        '5': 3,
        '4': 4,
        '3': 5,
        '2': 6,
        '1': 7,
    }

    if len(coordinates) >= 2 and coordinates[0].upper() in 'ABCDEFGH' and coordinates[1] in '12345678':
        return numbers[coordinates[1]], letters[coordinates[0].upper()]
    
    else:
        return False
    
def stalemate(turn, chessboard):
    count = 0

    for i in range(len(chessboard)):
        for j in range(len(chessboard[i])):
            if type(chessboard[i][j]) != str and chessboard[i][j].piece_color == turn:
                for lin in chessboard[i][j].piece_map:
                    if 1 in lin or 3 in lin or 4 in lin and chessboard[i][j].piece.lower() == 'p':
                        count += 1

    if count > 0:
        return False
    return True

def has_king(piece):
    if type(piece) != str and piece.piece.lower() == 'k' or type(piece) == str and piece.lower() == 'k':
        return True
    return False

def update_all_moves(cb):
    for lin in range(len(cb)):
        for col in range(len(cb[lin])):
            if type(cb[lin][col]) != str:
                cb[lin][col].chessboard = deepcopy(cb)
                cb[lin][col].piece_arrange = (lin, col)
                cb[lin][col].piece_map = get_square_matrix(8)
                cb[lin][col].update_move()
