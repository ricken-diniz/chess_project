from pieces_movement import *
from utils import *

class Game():
    def __init__(self):
        self.chessboard = get_initial_game(Piece)
        self.white_left_hook = True
        self.white_right_hook = True
        self.black_left_hook = True
        self.black_right_hook = True

        self.chessboard[0][4].piece_map[0][6] = 4
        self.chessboard[0][4].piece_map[0][2] = 4
        self.chessboard[7][4].piece_map[7][6] = 4
        self.chessboard[7][4].piece_map[7][2] = 4

    def move_piece(self, piece_arrange, movement):
        i, j = piece_arrange
        l, c = movement

        if type(self.chessboard[i][j]) == Piece:
            print('a')
            
            if self.chessboard[i][j].piece_map[l][c] in [1,3,4]:
                color                   = self.chessboard[i][j].piece_color
                piece                   = self.chessboard[i][j].piece

                if self.chessboard[i][j].piece_map[l][c] == 4 and piece.lower() == 'p':
                    self.chessboard[l-1*color][c] = '.'
                elif self.chessboard[i][j].piece_map[l][c] == 4 and piece.lower() == 'k':
                    if not self.hook(l, c, color):
                        print('b')
                        return False
                self.chessboard[i][j]   = '.'
                p                       = Piece(l, c, self.chessboard, piece)
                self.chessboard[l][c]   = p
                

                for lin in range(len(self.chessboard)):
                    for col in range(len(self.chessboard[lin])):
                        if type(self.chessboard[lin][col]) == Piece:
                            self.chessboard[lin][col].chessboard = deepcopy(self.chessboard[l][c].chessboard)
                            self.chessboard[lin][col].piece_arrange = (lin, col)
                            self.chessboard[lin][col].piece_map = get_square_matrix(8)
                            self.chessboard[lin][col].update_move()
                
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

                
                    
                return True
            
            return False

    def hook(self, l, c, color):
        if has_check(l, 4, self.chessboard, color):
            print('c')
            return False

        if c == 6:
            for _ in range(5, c + 1):
                if type(self.chessboard[l][_]) == Piece or has_check(l, _, self.chessboard, color):
                    print('d')
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
                if type(self.chessboard[l][_]) == Piece or has_check(l, _, self.chessboard, color):
                    print('e')
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

        self.chessboard[l][col_rook] = Piece(l, col_rook, self.chessboard, rook)
        self.chessboard[l][c] = Piece(l, c, self.chessboard, king)
        return True

    def check_hook(self, piece, i, j, color):

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

        if self.white_left_hook:
            self.chessboard[7][4].piece_map[7][2] = 4

        if self.white_right_hook:
            self.chessboard[7][4].piece_map[7][6] = 4

        if self.black_left_hook:
            self.chessboard[0][4].piece_map[0][2] = 4
            
        if self.black_right_hook:
            self.chessboard[0][4].piece_map[0][6] = 4
            
        

        



def main():
    turns = [None, 'pretas', 'brancas']
    turn = -1 
    incheck = False 
    game = Game()

    while True:
        show_chessboard(game.chessboard)

        piece_arrange = input('Selecione sua peça: ')
        if (arrange := get_arrange(piece_arrange)) != False:
            i, j = arrange
            piece_arrange = arrange
        else:
            print('Selecione uma coordenada válida!')
            continue

        if game.chessboard[i][j] == '.':
            print('Selecione uma peça, você selecionou um espaço vazio...')
            continue
        elif game.chessboard[i][j].piece_color != turn:
            print(f'Agora é vez das {turns[turn]}, jogue com uma peça válida!')
            continue
        
        show_movies(game.chessboard, game.chessboard[i][j].piece_map)
        movement = input('Selecione o destino: ')
        if (arrange := get_arrange(movement)) != False:
            movement = arrange
        else:
            print('Selecione uma coordenada válida!')
            continue

        if game.move_piece(piece_arrange, movement):
            print('Movimentando...')
        else:
            print('Tente novamente')



if __name__ == '__main__':
    main()