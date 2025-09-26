from gamemods.chess import Chess
from pieces_movement import Piece
from utils import deepcopy, has_check, get_square_matrix

class CrazyChess(Chess):
    def insert_piece(self, captured_piece, arrange, turn):
        piece = captured_piece.upper() if turn == -1 else captured_piece.lower()
        cb = deepcopy(self.chessboard)
        i, j = arrange

        for ix in range(len(cb)):
            for jx in range(len(cb[ix])):
                if type(cb[ix][jx]) == Piece:
                    cb[ix][jx] = self.chessboard[ix][jx].clone()

        if not type(cb[i][j]) == Piece:
            p        = Piece(i, j, cb, piece)
            cb[i][j] = p

            for lin in range(len(cb)):
                for col in range(len(cb[lin])):
                    if type(cb[lin][col]) == Piece:
                        cb[lin][col].chessboard = deepcopy(cb[i][j].chessboard)
                        cb[lin][col].piece_arrange = (lin, col)
                        cb[lin][col].piece_map = get_square_matrix(8)
                        cb[lin][col].update_move()

            if turn == 1:
                ik,jk = self.black_king_position
            elif turn == -1:
                ik,jk = self.white_king_position

            if (ik,jk) == (-1,-1) or not has_check(ik, jk, cb, turn):
                if turn == -1:
                    self.white_kills.remove(captured_piece)
                    self.white_check = False
                elif turn == 1:
                    self.black_kills.remove(captured_piece)
                    self.black_check = False

                self.chessboard = cb

                if turn == 1:
                    ie, je = self.white_king_position
                    if (ie, je) != (-1,-1) and has_check(ie, je, self.chessboard, -turn):
                        self.white_check = True

                if turn == -1:
                    ie, je = self.black_king_position
                    if (ie, je) != (-1,-1) and has_check(ie, je, self.chessboard, -turn):
                        self.black_check = True

                if self.black_check or self.white_check:
                    if self.has_mate(turn, self.chessboard[i][j]):
                        return 'End Game'

                return True
            
            return False
        
        return False