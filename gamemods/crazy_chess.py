from gamemods.chess import Chess
from pieces_movement import Piece
from utils import has_check, get_square_matrix, update_all_moves

class CrazyChess(Chess):
    def has_mate(self, turn, enemy_piece):
        ik, jk = self.white_king_position if turn == 1 else self.black_king_position

        if (ik,jk) == (-1,-1):
            return False 

        if super().has_mate(turn, enemy_piece):
            if not enemy_piece.piece.lower() in ['n','p'] and ((turn == 1 and len(self.white_kills) > 0) or (turn == -1 and len(self.black_kills) > 0)):
                ie, je = enemy_piece.piece_arrange
                euclidean_distance = ((ik - ie)**2 + (jk - je)**2)

                if euclidean_distance > 2:
                    return False

            return 'End Game'
        return False

    def insert_piece(self, captured_piece, arrange, turn):
        piece = captured_piece.upper() if turn == -1 else captured_piece.lower()
        cb = self.copy_chessboard()
        i, j = arrange

        if not type(cb[i][j]) == Piece:
            p        = Piece(i, j, cb, piece)
            cb[i][j] = p

            update_all_moves(cb)
    
            if turn == 1:
                ik,jk = self.black_king_position
                il,jl = self.white_king_position
            elif turn == -1:
                ik,jk = self.white_king_position
                il,jl = self.black_king_position

            if (ik,jk) == (-1,-1) or not has_check(ik, jk, cb, turn):
                cb[il][jl].piece_map = get_square_matrix(8) 
                cb[il][jl].update_move()
                self.chessboard = cb

                if turn == 1:
                    self.black_kills.remove(captured_piece)
                    self.black_check = False
                    ie, je = self.white_king_position
                    if (ie, je) != (-1,-1) and has_check(ie, je, self.chessboard, -turn):
                        self.white_check = True

                if turn == -1:
                    self.white_kills.remove(captured_piece)
                    self.white_check = False
                    ie, je = self.black_king_position
                    if (ie, je) != (-1,-1) and has_check(ie, je, self.chessboard, -turn):
                        self.black_check = True

                if (self.black_check or self.white_check) and self.has_mate(turn, self.chessboard[i][j]):
                    return 'End Game'

                return True
        
        return False