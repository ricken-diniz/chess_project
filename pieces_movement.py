from utils import affine_function, get_square_matrix, deepcopy_list, has_check, has_king

class Piece():

    def __init__(self, i, j, chessboard, piece, piece_map = None):
        self.pieceGameObject = Piece
        white_pieces = ['K','Q','R','B','N','P']
        black_pieces = ['k','q','r','b','n','p']

        self.piece_arrange  = (i, j)
        self.piece_color    = -1 if piece in white_pieces else 1 if piece in black_pieces else Exception
        self.chessboard     = chessboard
        self.piece_map      = get_square_matrix(8)
        self.piece          = piece
        self.defs = {
            'r': self.spawn_pointers_rook,
            'n': self.spawn_pointers_horse,
            'b': self.spawn_pointers_bishop,
            'q': self.spawn_pointers_queen,
            'k': self.spawn_pointers_king,
            'p': self.spawn_pointers_pawn
        }

        if not piece_map is None:
            self.piece_map = deepcopy_list(piece_map)
        else:
            self.defs[self.piece.lower()]()
            self.piece_map[i][j] = 2

    def verify_has_piece(self, i, j, ispawn = False):
        white_pieces = ['K','Q','R','B','N','P']
        black_pieces = ['k','q','r','b','n','p']
        piece        = None

        if type(self.chessboard[i][j]) == self.pieceGameObject:
            piece = self.chessboard[i][j].piece

        elif type(self.chessboard[i][j]) == str and (self.chessboard[i][j] in white_pieces or self.chessboard[i][j] in black_pieces):
            piece = self.chessboard[i][j]


        if piece is not None:

            if piece in white_pieces and self.piece_color == -1 or piece in black_pieces and self.piece_color == 1:
                if not ispawn:
                    self.piece_map[i][j] = 5
                return 'Not'
            
            elif piece in white_pieces and self.piece_color == 1 or piece in black_pieces and self.piece_color == -1:
                if not ispawn:
                    self.piece_map[i][j] = 3
                return 'Yes'
        

        return False

    def show_map(self):
        M = []

        for i in range(len(self.piece_map)):
            line = []
            for j in range(len(self.piece_map[i])):
                
                if self.piece_map[i][j] == 1:
                    line.append(f'\033[94m{1}\033[0m')
                    
                elif self.piece_map[i][j] == 2:
                    line.append(f'\033[91m{2}\033[0m')
                    
                elif self.piece_map[i][j] in [3,4]:
                    line.append(f'\033[95m{self.piece_map[i][j]}\033[0m')
                    
                else:
                    line.append(f'{self.piece_map[i][j]}')

            M.append(line)

        return M

    def update_move(self):
        i, j = self.piece_arrange
        self.defs[self.piece.lower()]()
        self.piece_map[i][j] = 2

    def clone(self):
        i, j = self.piece_arrange
        return self.pieceGameObject(i, j, self.chessboard, self.piece, self.piece_map)


    def spawn_pointers_bishop(self):
        i, j = self.piece_arrange
        M = self.piece_map

        greater = i if i > j else j
        less    = i if i < j else j

        l = len(M) - 1

        primary_diagonal_coefficient    = greater - less
        secondary_diagonal_coefficient  = i + j - l

        pdc = primary_diagonal_coefficient
        sdc = secondary_diagonal_coefficient

        for _ in range(less - 1, -1, -1):
            lin, col = affine_function(1, _, pdc)
            lin, col    = (lin, col)     if j > i else     (col, lin)
            if log := self.verify_has_piece(lin, col):   
                if log == 'Yes' and lin > 0 and col > 0 and has_king(self.chessboard[lin][col]):
                    self.piece_map[lin-1][col-1] = 7
                break
            M[lin][col] = 1

        for _ in range(less + 1, len(M) - pdc):
            lin, col = affine_function(1, _, pdc)
            lin, col    = (lin, col)    if j > i else     (col, lin)
            if log := self.verify_has_piece(lin, col):     
                if log == 'Yes' and lin < 7 and col < 7 and has_king(self.chessboard[lin][col]):
                    self.piece_map[lin+1][col+1] = 7   
                break
            M[lin][col] = 1


        if sdc <= 0:
            range_up = range(i - 1, -1, -1)
            range_down = range(i + 1, len(M) + sdc)
        else:
            range_up = range(i - 1, sdc - 1, -1)
            range_down = range(i + 1, len(M))

        for _ in range_up:
            lin, col = affine_function(-1, _, l + sdc)
            if log := self.verify_has_piece(lin, col):
                if log == 'Yes' and lin > 0 and col < 7 and has_king(self.chessboard[lin][col]):
                    self.piece_map[lin-1][col+1] = 7         
                break
            M[lin][col] = 1

        for _ in range_down:
            lin, col = affine_function(-1, _, l + sdc)
            if log := self.verify_has_piece(lin, col): 
                if log == 'Yes' and lin < 7 and col > 0 and has_king(self.chessboard[lin][col]):
                    self.piece_map[lin+1][col-1] = 7             
                break
            M[lin][col] = 1

    def spawn_pointers_rook(self):
        i, j = self.piece_arrange
        M = self.piece_map

        for _ in range(i-1, -1,-1):
            if log := self.verify_has_piece(_, j):
                if log == 'Yes' and _ > 0 and has_king(self.chessboard[_][j]):
                    self.piece_map[_ - 1][j] = 7
                break
            M[_][j] = 1

        for _ in range(i+1, len(M)):
            if log := self.verify_has_piece(_, j):  
                if log == 'Yes' and _ < 7 and has_king(self.chessboard[_][j]):
                    self.piece_map[_ + 1][j] = 7
                break 
            M[_][j] = 1

        for _ in range(j-1, -1,-1):
            if log := self.verify_has_piece(i, _): 
                if log == 'Yes' and _ > 0 and has_king(self.chessboard[i][_]):
                    self.piece_map[i][_ - 1] = 7
                break
            M[i][_] = 1
        
        for _ in range(j+1, len(M)):
            if log := self.verify_has_piece(i, _):   
                if log == 'Yes' and _ < 7 and has_king(self.chessboard[i][_]):
                    self.piece_map[i][_ + 1] = 7
                break 
            M[i][_] = 1

    def spawn_pointers_queen(self):
        self.spawn_pointers_rook()
        self.spawn_pointers_bishop()
        self.piece = 'Q' if self.piece_color == -1 else 'q'

    def spawn_pointers_horse(self):
        i, j    = self.piece_arrange
        M       = self.piece_map
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

                if self.verify_has_piece(i, j):            
                    continue

                M[i][j] = 1

    def spawn_pointers_king(self):
        i, j    = self.piece_arrange
        M       = self.piece_map
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
                
                if has_check(i, j, self.chessboard, self.piece_color):
                    continue

                if self.verify_has_piece(i, j):            
                    continue

                M[i][j] = 1

    def spawn_pointers_pawn(self):
        color   = self.piece_color
        i, j    = self.piece_arrange
        M       = self.piece_map

        if color == 1 and i == (len(M) - 1) or color == -1 and i == 0:
            self.spawn_pointers_queen()
            return
        
        elif color == 1 and i == 1 or color == -1 and i == len(M) - 2:
            step = 2

        else:
            step = 1

        for _ in range(1,step+1):
            
            if _ != 2:
                if j > 0:
                    self.piece_map[i + (_*color)][j-1] = 5
                    self.verify_has_piece(i + (_*color), j-1)
                    
                if j < len(M) - 1:
                    self.piece_map[i + (_*color)][j+1] = 5
                    self.verify_has_piece(i + (_*color), j+1)

            if self.verify_has_piece(i + (_*color), j, True):
                break

            M[i + (_*color)][j] = 1