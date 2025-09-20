from pieces_movement import *
from utils import *
import os

class Game():
    def __init__(self):
        self.chessboard = get_initial_game(Piece)
        self.white_kills = []
        self.black_kills = []
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
            
            
            if self.chessboard[i][j].piece_map[l][c] in [1,3,4]:
                color                   = self.chessboard[i][j].piece_color
                piece                   = self.chessboard[i][j].piece

                if self.chessboard[i][j].piece_map[l][c] == 3:
                    if color == 1:
                        self.black_kills.append(self.chessboard[l][c].piece)
                    elif color == -1:
                        self.white_kills.append(self.chessboard[l][c].piece)

                if self.chessboard[i][j].piece_map[l][c] == 4 and piece.lower() == 'p':
                    if color == 1:
                        self.black_kills.append('P')
                    elif color == -1:
                        self.white_kills.append('p')
                    self.chessboard[l-1*color][c] = '.'

                elif self.chessboard[i][j].piece_map[l][c] == 4 and piece.lower() == 'k':
                    if not self.hook(l, c, color):
                                                                            
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
            
            return False

        if c == 6:
            for _ in range(5, c + 1):
                if type(self.chessboard[l][_]) == Piece or has_check(l, _, self.chessboard, color):
                    
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

    os.system('clear')
    while True:
        print('Black: ' + " ".join(game.black_kills))
        print()
        show_chessboard(game.chessboard)
        print('White: ' + " ".join(game.white_kills))
        print()

        print(f'Vez das {turns[turn]}.')
        piece_arrange = input('Selecione sua peça: ')
        if (arrange := get_arrange(piece_arrange)) != False:
            i, j = arrange
            piece_arrange = arrange
        else:
            os.system('clear')
            print('Selecione uma coordenada válida!')
            print()
            continue

        if game.chessboard[i][j] == '.':
            os.system('clear')
            print('Selecione uma peça, você selecionou um espaço vazio...')
            print()
            continue
        elif game.chessboard[i][j].piece_color != turn:
            os.system('clear')
            print(f'Agora é vez das {turns[turn]}, jogue com uma peça válida!')
            print()
            continue
        
        os.system('clear')
        print('Black: ' + " ".join(game.black_kills))
        print()
        show_movies(game.chessboard, game.chessboard[i][j].piece_map)
        print('White: ' + " ".join(game.white_kills))
        print()
        
        movement = input('Selecione o destino (ou digite C para escolher outra peça): ')
        if movement.lower() == 'c':
            continue

        if (arrange := get_arrange(movement)) != False:
            movement = arrange
        else:
            print('Selecione uma coordenada válida!')
            continue


        if game.move_piece(piece_arrange, movement):
            print('Movimentando...')
            turn = turn * -1
        else:
            print('Tente novamente')



if __name__ == '__main__':
    main()