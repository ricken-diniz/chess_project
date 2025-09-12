def get_square_matrix(n):
    M = [[0 for _ in range(n)] for _ in range(n)]
    return M

def get_initial_game(Piece: object):
    chessboard   = get_chessboard('str')
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
        pieces = [None, ['K','Q','R','B','H','P'], ['k','q','r','b','h','p']]

        for l in range(len(chessboard)):
            for c in range(len(chessboard)):
                if type(chessboard[l][c]) is dict:
                    for k in chessboard[l][c].keys():
                        if k in pieces[-turn]:

                            enimy_piece_map = chessboard[l][c][k]
                            if enimy_piece_map[i][j] in [1,3]:
                                return True

                            break
        
        return False

