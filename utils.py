

def get_square_matrix(n):
    M = [[0 for _ in range(n)] for _ in range(n)]
    return M

def get_initial_game(Piece: object):
    chessboard   = get_chessboard('hook')
    white_pieces = ['K','Q','R','B','H','P']
    black_pieces = ['k','q','r','b','h','p']

    for lin in range(len(chessboard)):
        for col in range(len(chessboard[lin])):

            piece = chessboard[lin][col]
            if piece in white_pieces or piece in black_pieces:

                p                    = Piece(lin, col, chessboard, piece)
                chessboard[lin][col] = p

    return chessboard

def get_chessboard(chessboard_type = 'dict'):
    if chessboard_type == 'empty':
        chessboard = [['.' for _ in range(8)] for _ in range(8)]

    elif chessboard_type == 'dict':
        chessboard = [
            [{'R':1},{'H':1},{'B':1},{'Q':1},{'K':1},{'B':1},{'H':1},{'R':1}],

            [{'P':1},{'P':1},{'P':1},{'P':1},{'p':1},{'P':1},{'P':1},{'P':1}],

            [  '.'  ,{'p':1},  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

            [  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

            [  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

            [  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

            [{'p':1},{'p':1},{'p':1},{'p':1},{'p':1},{'p':1},{'p':1},{'p':1}],

            [{'r':1},{'h':1},{'b':1},{'q':1},{'k':1},{'b':1},{'h':1},{'r':1}],
        ]

    elif chessboard_type == 'str':
        chessboard = [
            ['R','H','B','Q','K','B','H','R'],

            ['P','P','P','P','P','P','P','P'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['p','p','p','p','p','p','p','p'],

            ['r','h','b','q','k','b','h','r'],
        ]

    elif chessboard_type == 'hook':
        chessboard = [
            ['r','.','.','.','k','.','.','r'],

            ['p','p','p','p','p','p','p','p'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['P','P','P','P','P','P','P','P'],

            ['R','.','.','.','K','.','.','R'],
        ]

    elif chessboard_type == 'tower':
        chessboard = [
            ['R','R','R','R','R','R','R','R'],

            ['R','R','R','R','R','R','R','R'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['.','.','.','.','.','.','.','.'],

            ['r','r','r','r','r','r','r','r'],

            ['r','r','r','r','r','r','r','r'],
        ]

    return chessboard

def show_chessboard(chessboard):
    count = 0
    for line in chessboard:
        lin = []
        for e in line:
            if type(e) != str:
                lin.append(e.piece)
                count += 1
            else:
                lin.append(e)

        print(' '.join(lin))
    print(count)

def show_pieces_map(chessboard):
    for line in chessboard:
        for e in line:

            piece = e.piece
            print(f'\n{'':=^30}\n')
            print(f'{piece:=^30}\n')

            lin = []
            for value in e.piece_map:
                lin.append(str(value))
            
            print(' '.join(lin))

def show_movies(chessboard, piece_map):

    i_axis = 8
    for i in range(len(chessboard)):
        lin = []
        for j in range(len(chessboard[i])):
            if type(chessboard[i][j]) != str:
                e = chessboard[i][j].piece
                
            else:
                e = chessboard[i][j]
            
            if piece_map[i][j] == 1:
                lin.append(f'\033[94m{e}\033[0m')
                
            elif piece_map[i][j] == 2:
                lin.append(f'\033[91m{e}\033[0m')
                
            elif piece_map[i][j] in [3,4]:
                lin.append(f'\033[95m{e}\033[0m')
                
            else:
                lin.append(e)
        
        
        print(f'{i_axis}  '+' '.join(lin))
        i_axis -= 1
        
    print()
    print('   A B C D E F G H')
    print()

def deepcopy(M):

    matrix = []

    for lin in M:
        line = []
        for i in range(len(lin)):
            line.append(lin[i])
        matrix.append(line)

    return matrix

def affine_function(a, x, b):
    y = a*x + b

    return x, y

def has_check(i, j, chessboard, turn):
        for l in range(len(chessboard)):
            for c in range(len(chessboard)):
                if type(chessboard[l][c]) != str:
                    if chessboard[l][c].piece_color != turn:

                        enimy_piece_map = chessboard[l][c].piece_map
                        if enimy_piece_map[i][j] in [1,3]:
                            return True

                        break
        
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

    if len(coordinates) == 2 and coordinates[0].upper() in 'ABCDEFGH' and coordinates[1] in '12345678':
        return numbers[coordinates[1]], letters[coordinates[0].upper()]
    
    else:
        return False