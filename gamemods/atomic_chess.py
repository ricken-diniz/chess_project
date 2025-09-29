from gamemods.chess import Chess
from pieces_movement import Piece
from utils import has_check,update_all_moves,deepcopy_list

class AtomicChess(Chess):

    def move_piece(self, piece_arrange, movement, turn):
        i, j = piece_arrange
        l, c = movement

        if type(self.chessboard[i][j]) == Piece:
            
            if self.chessboard[i][j].piece_map[l][c] in [1,3,4]:
                color = self.chessboard[i][j].piece_color
                piece = self.chessboard[i][j].piece

                if self.chessboard[i][j].piece_map[l][c] == 4 and piece.lower() == 'k':
                    if not self.hook(l, c, color):
                        return False
                    
                if not self.validate_move(i, j, l, c, turn):
                    return 'Você não pode mover para essa casa, seu rei ficará em xeque!'
                
                if self.king_captured(turn):
                    return 'End Game'

                self.check_hook(piece, i, j, color) 

                if piece.lower() == 'p' and (l-i)*color == 2:
                    if c > 0:
                        left_position = self.chessboard[l][c-1] 
                        if type(left_position) == Piece and left_position.piece.lower() == 'p' and left_position.piece_color != color:
                            left_position.piece_map[l-1*color][c] = 4 

                    if c < len(self.chessboard) - 1:
                        right_position = self.chessboard[l][c+1] 
                        if type(right_position) == Piece and right_position.piece.lower() == 'p' and right_position.piece_color != color: 
                            right_position.piece_map[l-1*color][c] = 4 
                

                if turn == 1:
                    ik, jk = self.white_king_position
                    if (ik, jk) != (-1,-1) and has_check(ik, jk, self.chessboard, -turn):
                        self.white_check = True

                if turn == -1:
                    ik, jk = self.black_king_position
                    if (ik, jk) != (-1,-1) and has_check(ik, jk, self.chessboard, -turn):
                        self.black_check = True

                if self.black_check or self.white_check:
                    if self.has_mate(turn, self.chessboard[l][c]):
                        return 'End Game'
                    
                return True
            
            return False

    def validate_move(self, i, j, l, c, turn):   
        cb = self.copy_chessboard()
        wk = deepcopy_list(self.white_kills)
        bk = deepcopy_list(self.black_kills)
        color = cb[i][j].piece_color
        piece = cb[i][j].piece
        piece_map = cb[i][j].piece_map

        atomic_houses = [
            (l-1,c-1),
            (l+1,c+1),
            (l  ,c+1),
            (l  ,c-1),
            (l-1,c  ),
            (l+1,c  ),
            (l-1,c+1),
            (l+1,c-1),
            (l  ,c  ),
        ] if piece.lower() != 'k' else [(l,c)]

        if piece_map[l][c] == 3 or piece_map[l][c] == 4 and piece.lower() == 'p':
            for m, n in atomic_houses:
                if m >= 0 and m <= 7 and n >= 0 and n <= 7 and type(cb[m][n]) == Piece and not (cb[m][n].piece.lower() == 'k' and cb[m][n].piece_color == turn):
                    if color == 1:
                        bk.append(cb[m][n].piece) 
                    elif color == -1:
                        wk.append(cb[m][n].piece) 
                    cb[m][n] = '.'

        cb[i][j] = '.'        
        if piece.lower() == 'k' or piece_map[l][c] == 1:
            p        = Piece(l, c, cb, piece)
            cb[l][c] = p 
        
        update_all_moves(cb)

        if self.conclude_move(piece, cb, wk, bk, l, c, turn):
            return True
        return False
    
    def king_captured(self, turn):
        has_king = True
        for k in range(len(self.chessboard)):
            for x in range(len(self.chessboard[k])):
                position = self.chessboard[k][x]
                if type(position) == Piece and position.piece.lower() == 'k' and position.piece_color == -turn:
                    has_king = False

        return has_king
        