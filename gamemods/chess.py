from pieces_movement import Piece
from utils import get_initial_game,deepcopy_list,has_check,get_square_matrix, update_all_moves

class Chess():
    def __init__(self, gamemod = 'normalgame', pieceGameObject = Piece):
        self.pieceGameObject = pieceGameObject
        self.chessboard = get_initial_game(self.pieceGameObject, gamemod)
        self.white_kills = []
        self.black_kills = []
        self.white_left_hook = True
        self.white_right_hook = True
        self.black_left_hook = True
        self.black_right_hook = True
        self.white_check = False 
        self.black_check = False 
        self.white_king_position = (7,4)
        self.black_king_position = (-1,-1)
        self.white_king_position = (-1,-1)

        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard[i])):
                if type(self.chessboard[i][j]) == self.pieceGameObject and self.chessboard[i][j].piece.lower() == 'k':
                    if self.chessboard[i][j].piece_color == 1:
                        self.black_king_position = (i,j)
                        if (i,j) == (0,4):
                            self.chessboard[i][j].piece_map[0][6] = 4
                            self.chessboard[i][j].piece_map[0][2] = 4
                    elif self.chessboard[i][j].piece_color == -1:
                        self.white_king_position = (i,j)
                        if (i,j) == (7,4):
                            self.chessboard[i][j].piece_map[7][6] = 4
                            self.chessboard[i][j].piece_map[7][2] = 4

    def move_piece(self, piece_arrange, movement, turn):
        i, j = piece_arrange
        l, c = movement

        if type(self.chessboard[i][j]) == self.pieceGameObject and (self.chessboard[i][j].piece_map[l][c] in [1,3,4] or self.chessboard[i][j].piece == 'duck'):
            piece = self.chessboard[i][j].piece

            if self.chessboard[i][j].piece_map[l][c] == 4 and piece.lower() == 'k':
                if not self.hook(l, c, turn):
                    return False
                
            if not self.validate_move(i, j, l, c, turn):
                return 'Você não pode mover para essa casa, seu rei ficará em xeque!'
            
            if piece.lower() in ['k','r']:
                self.check_hook(piece, i, j, turn) 

            if piece.lower() == 'p' and (l-i)*turn == 2:
                if c > 0:
                    left_position = self.chessboard[l][c-1] 
                    if type(left_position) == self.pieceGameObject and left_position.piece.lower() == 'p' and left_position.piece_color != turn:
                        left_position.piece_map[l-1*turn][c] = 4 

                if c < len(self.chessboard) - 1:
                    right_position = self.chessboard[l][c+1] 
                    if type(right_position) == self.pieceGameObject and right_position.piece.lower() == 'p' and right_position.piece_color != turn: 
                        right_position.piece_map[l-1*turn][c] = 4 
            

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

    def hook(self, l, c, color):

        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard[i])):
                if type(self.chessboard[i][j]) == self.pieceGameObject and self.chessboard[i][j].piece.lower() == 'k' and self.chessboard[i][j].piece_color == color:
                    ik, jk = self.chessboard[i][j].piece_arrange


        if has_check(ik, jk, self.chessboard, color):
            
            return False

        if c == 6:
            for _ in range(5, c + 1):
                if type(self.chessboard[l][_]) == self.pieceGameObject or has_check(l, _, self.chessboard, color):
                    
                    return False
                
            if l == 7 and self.white_right_hook:
                self.chessboard[l][7] = '.'
                rook = 'R'
                king = 'K'
            elif l == 0 and self.black_right_hook:
                self.chessboard[l][7] = '.'
                rook = 'r'
                king = 'k'

            col_rook = 5

        elif c == 2:
            for _ in range(3, c - 1, - 1):
                if type(self.chessboard[l][_]) == self.pieceGameObject or has_check(l, _, self.chessboard, color):
                    
                    return False
                
            if l == 7 and self.white_left_hook:
                self.chessboard[l][0] = '.'
                rook = 'R'
                king = 'K'
            elif l == 0 and self.black_left_hook:
                self.chessboard[l][0] = '.'
                rook = 'r'
                king = 'k'
            
            col_rook = 3

        self.chessboard[l][col_rook] = self.pieceGameObject(l, col_rook, self.chessboard, rook)
        self.chessboard[l][c] = self.pieceGameObject(l, c, self.chessboard, king)
        return True

    def check_hook(self, piece, i, j, color):
        iwk, jwk = self.white_king_position
        ibk, jbk = self.black_king_position

        if piece.lower() == 'k':
            if color == 1:
                self.black_left_hook = False
                self.black_right_hook = False

            if color == -1:
                self.white_left_hook = False
                self.white_right_hook = False

        elif piece == 'r' and (i, j) == (0, 0):
            self.black_left_hook = False

        elif piece == 'r' and (i, j) == (0, 7):
            self.black_right_hook = False

        elif piece == 'R' and (i, j) == (7, 0):
            self.white_left_hook = False

        elif piece == 'R' and (i, j) == (7, 7):
            self.white_right_hook = False

        if not(iwk,jwk) == (-1,-1) and (iwk,jwk) == (7,4):
            if self.white_left_hook:
                self.chessboard[iwk][jwk].piece_map[7][2] = 4

            if self.white_right_hook:
                self.chessboard[iwk][jwk].piece_map[7][6] = 4

        if not(ibk,jbk) == (-1,-1) and (ibk,jbk) == (0,4):
            if self.black_left_hook:
                self.chessboard[ibk][jbk].piece_map[0][2] = 4
                
            if self.black_right_hook:
                self.chessboard[ibk][jbk].piece_map[0][6] = 4
            
    def validate_move(self, i, j, l, c, turn):   
        cb = self.copy_chessboard()
        wk = deepcopy_list(self.white_kills)
        bk = deepcopy_list(self.black_kills)
        color = cb[i][j].piece_color
        piece = cb[i][j].piece
        piece_map = cb[i][j].piece_map

        if piece_map[l][c] == 3:
            if color == 1:
                bk.append(cb[l][c].piece)
            elif color == -1:
                wk.append(cb[l][c].piece)

        if piece_map[l][c] == 4 and piece.lower() == 'p':
            if color == 1:
                bk.append('P')
            elif color == -1:
                wk.append('p')
            cb[l-1*color][c] = '.'


        cb[i][j] = '.'
        p        = self.pieceGameObject(l, c, cb, piece)
        cb[l][c] = p
        
        update_all_moves(cb)

        if self.conclude_move(piece, cb, wk, bk, l, c, turn):
            return True
        return False

    def has_mate(self, turn, enemy_piece):
        count = 0

        if turn == 1:
            ik, jk = self.white_king_position
        elif turn == -1:
            ik, jk = self.black_king_position
        
        if (ik,jk) == (-1,-1):
            return False

        ie, je = enemy_piece.piece_arrange

        king_map = self.chessboard[ik][jk].piece_map

        for i in range(len(king_map)):
            for j in range(len(king_map[i])):
                if king_map[i][j] in [1,3] and not has_check(i, j, self.chessboard, -turn):
                    count += 1


        friend_pieces_arranges = []
        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard[i])):
                if type(self.chessboard[i][j]) == self.pieceGameObject and self.chessboard[i][j].piece_color == -turn:
                    friend_pieces_arranges.append((i,j))

        if enemy_piece.piece.lower() in ['r', 'q']:
            if jk == je:
                if ik > ie:
                    enemy_range = range(ie, ik)
                else:
                    enemy_range = range(ie, ik, -1)
                for i in enemy_range:
                    for k, x in friend_pieces_arranges:
                        if self.chessboard[k][x].piece_map[i][jk] in [1, 3, 4]:
                            count += 1

            elif ik == ie:
                if jk > je:
                    enemy_range = range(je, jk)
                else:
                    enemy_range = range(je, jk, -1)
                for j in enemy_range:
                    for k, x in friend_pieces_arranges:
                        if self.chessboard[k][x].piece_map[ik][j] in [1, 3, 4]:
                            count += 1

        if enemy_piece.piece.lower() in ['b', 'q']:
            direction_i = 1 if ik > ie else -1
            direction_j = 1 if jk > je else -1

            if ik > ie:
                enemy_range = range(0, ik-ie)
            else:
                enemy_range = range(0, ie-ik)
            for i in enemy_range:
                for k, x in friend_pieces_arranges:
                    if self.chessboard[k][x].piece_map[ie + i*direction_i][je + i*direction_j] in [1, 3, 4]:
                        count += 1

        if enemy_piece.piece.lower() in ['h', 'p']:
            for k, x in friend_pieces_arranges:
                if self.chessboard[k][x].piece_map[ie][je] == 3:
                    count += 1

        if enemy_piece.piece.lower() == 'p':
            for k, x in friend_pieces_arranges:
                if self.chessboard[k][x].piece.lower() == 'p' and self.chessboard[k][x].piece_map[ie-turn][je] == 4:
                    count += 1

        if count == 0:
            return True
        return False

    def alert_check(self):
        if self.white_check:
            output = '\nO rei branco está em \033[91mxeque\033[0m!\n'
            return output
        if self.black_check:
            output = '\nO rei preto está em \033[91mxeque\033[0m!\n'
            return output
        return False

    def copy_chessboard(self):
        cb = []

        for i in range(len(self.chessboard)):
            line = []
            for j in range(len(self.chessboard[i])):
                if type(self.chessboard[i][j]) == self.pieceGameObject:
                    line.append(self.chessboard[i][j].clone())
                else:
                    line.append(self.chessboard[i][j])
            cb.append(line)

        return cb

    def conclude_move(self, piece, cb, wk, bk, l, c, turn):
        if turn == 1:
            ik,jk = self.black_king_position
            il,jl = self.white_king_position
        elif turn == -1:
            ik,jk = self.white_king_position
            il,jl = self.black_king_position
            
        if piece.lower() == 'k':
            ik, jk = l, c

        if (ik,jk) == (-1,-1) or not has_check(ik, jk, cb, turn):
            if type(cb[il][jl]) == self.pieceGameObject:
                cb[il][jl].piece_map = get_square_matrix(8) 
                cb[il][jl].update_move() 

            if turn == -1:
                self.white_check = False
                if piece.lower() == 'k':
                    self.white_king_position = ik, jk
            elif turn == 1:
                self.black_check = False
                if piece.lower() == 'k':
                    self.black_king_position = ik, jk

            self.chessboard = cb
            self.white_kills = wk
            self.black_kills = bk
            return True
        
        return False
