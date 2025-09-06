def get_square_matrix(n):
    M = [[0 for _ in range(n)] for _ in range(n)]
    return M

def get_initial_example():
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

    return chessboard

def get_game_example():
    chessboard = [
        [{'R':1},{'H':1},{'B':1},{'Q':1},{'K':1},{'B':1},{'H':1},{'R':1}],

        [{'P':1},{'P':1},{'P':1},{'P':1},{'P':1},{'P':1},{'P':1},{'P':1}],

        [  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

        [  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

        [  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

        [  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ,  '.'  ],

        [{'p':1},{'p':1},{'p':1},{'p':1},{'p':1},{'p':1},{'p':1},{'p':1}],

        [{'r':1},{'h':1},{'b':1},{'q':1},{'k':1},{'b':1},{'h':1},{'r':1}],
    ]

    return chessboard

def deepcopy(M):
    matrix = []

    for i in range(len(M)):
        matrix.append([])
        for e in [i]:
            matrix[i].append(e)

    return matrix

def show_matrix(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            
            if M[i][j] == 1:
                M[i][j] = f'\033[94m{1}\033[0m'
            elif M[i][j] == 2:
                M[i][j] = f'\033[91m{2}\033[0m'
            elif M[i][j] == 3:
                M[i][j] = f'\033[95m{3}\033[0m'
            else:
                M[i][j] = f'{M[i][j]}'

def affine_function(a, x, b):
    y = a*x + b

    return x, y

def check_color(piece):
    if type(piece) == str:
        return Exception('Nenhuma peça selecionada')

    white_pieces = ['K','Q','R','B','H','P']
    black_pieces = ['k','q','r','b','h','p']

    for k in piece.keys():
        if k in white_pieces:
            return 1
        elif k in black_pieces:
            return -1
    
    return Exception('Peça mal formulada')