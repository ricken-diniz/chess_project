from gamemods.chess import Chess
from pieces_movement import Piece
from utils import deepcopy_list, get_square_matrix

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
    def __init__(self, gamemod='duckdefensecheck'):
        super().__init__(gamemod, DuckPiece)
    
