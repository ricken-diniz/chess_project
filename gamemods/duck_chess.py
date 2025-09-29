from gamemods.chess import Chess
from pieces_movement import Piece
from utils import deepcopy_list, get_square_matrix, update_all_moves

class DuckPiece(Piece):
    def __init__(self, i, j, chessboard, piece, piece_map = None):
        self.pieceGameObject = DuckPiece
        black_pieces = ['k','q','r','b','n','p']

        self.piece_arrange  = (i, j)
        self.piece_color    = 1 if piece in black_pieces else -1
        self.chessboard     = chessboard
        self.piece_map      = get_square_matrix(8)
        self.piece          = piece
        self.defs = {
            'r': self.spawn_pointers_rook,
            'n': self.spawn_pointers_horse,
            'b': self.spawn_pointers_bishop,
            'q': self.spawn_pointers_queen,
            'k': self.spawn_pointers_king,
            'p': self.spawn_pointers_pawn,
        }

        if not piece_map is None:
            self.piece_map = deepcopy_list(piece_map)

        elif self.piece.lower() != 'duck':
            self.defs[self.piece.lower()]()
        
        self.piece_map[i][j] = 2

    def update_move(self):
        i, j = self.piece_arrange
        if self.piece.lower() != 'duck':
            self.defs[self.piece.lower()]()
        self.piece_map[i][j] = 2

    def verify_has_piece(self, i, j, ispawn = False):
        if type(self.chessboard[i][j]) == DuckPiece and self.chessboard[i][j].piece == 'duck' or type(self.chessboard[i][j]) == str and self.chessboard[i][j] == 'duck':
            return True
        
        return super().verify_has_piece(i, j, ispawn)
            

class DuckChess(Chess):
    def __init__(self, gamemod='duckchess'):
        super().__init__(gamemod, DuckPiece)
    
    def move_duck(self, duck_position, movement, turn):
        i, j = duck_position
        l, c = movement
        cb = self.copy_chessboard()

        cb[i][j] = '.'
        p        = self.pieceGameObject(l, c, cb, 'duck')
        cb[l][c] = p
        update_all_moves(cb)

        if turn == 1:
            ik,jk = self.black_king_position
            il,jl = self.white_king_position
        elif turn == -1:
            ik,jk = self.white_king_position
            il,jl = self.black_king_position

        atacking_enemies = self.has_check(ik, jk, cb, turn)

        if type(cb[il][jl]) == self.pieceGameObject:
            cb[il][jl].piece_map = get_square_matrix(8) 
            cb[il][jl].update_move() 
            atacking_friends = self.has_check(il, jl, cb, -turn)
            
        if (ik,jk) != (-1,-1) and len(atacking_enemies) > 0:
            return 'Você não pode mover para essa casa, seu rei ficará em xeque!'

        self.chessboard = cb
        if len(atacking_friends) > 0 and self.has_mate(turn, atacking_friends):
            return 'End Game'
        
        return True
            
