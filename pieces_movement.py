from aux_functions import affine_function

def verify_has_piece(i, j, M, chessboard, color):
    white_pieces = ['K','Q','R','B','H','P']
    black_pieces = ['k','q','r','b','h','p']
    piece        = None
    white        = False
    black        = False


    if type(chessboard[i][j]) == dict:
        for k in chessboard[i][j].keys():
            if (white := k in white_pieces) or (black := k in black_pieces):
                piece = k

    elif type(chessboard[i][j]) == str and (white := chessboard[i][j] in white_pieces) or (black := chessboard[i][j] in black_pieces):
        piece = chessboard[i][j]


    print(white, black, piece)
    if piece is not None:
        if piece in white_pieces and white or piece in black_pieces and black:
            return True
        
        else:
            M[i][j] = 3
            return True
    

    return False



def spawn_pointers_bishop(i,j, M,chessboard, color):
    piece                   = 'B' if color == 1 else 'b'
    chessboard[i][j][piece] = M

    greater = i if i > j else j
    less    = i if i < j else j

    l = len(M) - 1

    primary_diagonal_coefficient    = greater - less
    secondary_diagonal_coefficient  = i + j - l

    pdc = primary_diagonal_coefficient
    sdc = secondary_diagonal_coefficient

    for _ in range(less - 1, -1, -1):
        x, y = affine_function(1, _, pdc)
        lin, col    = (x, y)     if j > i else     (y, x)
        
        if verify_has_piece(lin, col, M, chessboard, color):            
            break

        M[lin][col] = 1

    for _ in range(less + 1, len(M) - pdc):
        x, y = affine_function(1, _, pdc)
        lin, col    = (x, y)     if j > i else     (y, x)
        
        if verify_has_piece(lin, col, M, chessboard, color):            
            break

        M[lin][col] = 1


    if sdc <= 0:
        for _ in range(i - 1, -1, -1):
            x, y = affine_function(-1, _, l + sdc)
            lin, col    = (x, y)

            if verify_has_piece(lin, col, M, chessboard, color):            
                break

            M[lin][col] = 1

        for _ in range(i + 1, len(M) + sdc):
            x, y = affine_function(-1, _, l + sdc)
            lin, col    = (x, y)

            if verify_has_piece(lin, col, M, chessboard, color):            
                break

            M[lin][col] = 1
        
        # for _ in range()

    else:
        for _ in range(i, sdc - 1, -1):
            x, y = affine_function(-1, _, l + sdc)
            lin, col    = (x, y)

            if verify_has_piece(lin, col, M, chessboard, color):            
                break

            M[lin][col] = 1

        for _ in range(i, len(M)):
            x, y = affine_function(-1, _, l + sdc)
            lin, col    = (x, y)

            if verify_has_piece(lin, col, M, chessboard, color):            
                break

            M[lin][col] = 1

    M[i][j] = 2

def spawn_pointers_rock(i, j, M, chessboard, color):
    piece                   = 'R' if color == 1 else 'r'
    chessboard[i][j][piece] = M

    for _ in range(i-1, -1,-1):

        if verify_has_piece(_, j, M, chessboard, color):            
            break
        
        M[_][j] = 1

    for _ in range(i+1, len(M)):

        if verify_has_piece(_, j, M, chessboard, color):            
            break
        
        M[_][j] = 1

    for _ in range(j-1, -1,-1):

        if verify_has_piece(i, _, M, chessboard, color):            
            break

        M[i][_] = 1
    
    for _ in range(j+1, len(M)):

        if verify_has_piece(i, _, M, chessboard, color):            
            break 

        M[i][_] = 1

    M[i][j] = 2

def spawn_pointers_queen(i, j, M, chessboard, color):
    spawn_pointers_rock(i,j, M, chessboard, color)
    spawn_pointers_bishop(i,j, M, chessboard, color)

    piece                   = 'Q' if color == 1 else 'q'
    chessboard[i][j][piece] = M

def spawn_pointers_horse(i, j, M, chessboard, color):
    piece                   = 'H' if color == 1 else 'h'
    chessboard[i][j][piece] = M

    M[i][j] = 2
    l       = len(M)

    houses = [
        (i-2,j-1),
        (i+2,j-1),
        (i-2,j+1),
        (i+2,j+1),
        (i-1,j-2),
        (i+1,j-2),
        (i-1,j+2),
        (i+1,j+2),
    ]

    for t in houses:
        i,j = t

        if i >= 0 and j >= 0 and i < l and j < l:

            if verify_has_piece(i, j, M, chessboard, color):            
                continue

            M[i][j] = 1

def spawn_pointers_king(i, j, M, chessboard, color):
    piece                   = 'K' if color == 1 else 'k'
    chessboard[i][j][piece] = M
    
    
    M[i][j] = 2
    l       = len(M)

    houses = [
        (i-1,j-1),
        (i+1,j+1),
        (i  ,j+1),
        (i  ,j-1),
        (i-1,j  ),
        (i+1,j  ),
        (i-1,j+1),
        (i+1,j-1),
    ]

    for t in houses:
        i,j = t
        if i >= 0 and j >= 0 and i < l and j < l:

            if verify_has_piece(i, j, M, chessboard, color):            
                continue

            M[i][j] = 1

def spawn_pointers_pawn(i, j, M, chessboard, color):
    piece                   = 'P' if color == 1 else 'p'
    chessboard[i][j][piece] = M

    M[i][j] = 2

    if color == 1 and i == (len(M) - 1) or color == -1 and i == 0:
        spawn_pointers_queen(i, j, M, chessboard, color)
        return
    
    elif color == 1 and i == 1 or color == -1 and i == len(M) - 2:
        step = 2

    else:
        step = 1


    for _ in range(1,step+1):

        if verify_has_piece(i + (_*color), j, M, chessboard, color):
            return
        
        M[i + (_*color)][j] = 1