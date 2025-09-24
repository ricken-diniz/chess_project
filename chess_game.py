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
        self.white_check = False 
        self.black_check = False 
        self.white_king_position = (7,4)
        self.black_king_position = (-1,-1)
        self.white_king_position = (-1,-1)

        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard[i])):
                if type(self.chessboard[i][j]) == Piece and self.chessboard[i][j].piece.lower() == 'k':
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

        if type(self.chessboard[i][j]) == Piece:
            
            if self.chessboard[i][j].piece_map[l][c] in [1,3,4]:
                color = self.chessboard[i][j].piece_color
                piece = self.chessboard[i][j].piece

                if self.chessboard[i][j].piece_map[l][c] == 4 and piece.lower() == 'k':
                    if not self.hook(l, c, color):
                        return False
                    
                if not self.validate_move(i, j, l, c, turn):
                    return 'Você não pode mover para essa casa, seu rei ficará em xeque!'
                
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
                

                # piece_map = self.chessboard[l][c].piece_map
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
                if type(self.chessboard[i][j]) == Piece and self.chessboard[i][j].piece.lower() == 'k' and self.chessboard[i][j].piece_color == color:
                    ik, jk = self.chessboard[i][j].piece_arrange


        if has_check(ik, jk, self.chessboard, color):
            
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

        if not(iwk,jwk) == (-1,-1):
            if self.white_left_hook:
                self.chessboard[iwk][jwk].piece_map[7][2] = 4

            if self.white_right_hook:
                self.chessboard[iwk][jwk].piece_map[7][6] = 4

        if not(ibk,jbk) == (-1,-1):
            if self.black_left_hook:
                self.chessboard[ibk][jbk].piece_map[0][2] = 4
                
            if self.black_right_hook:
                self.chessboard[ibk][jbk].piece_map[0][6] = 4
            
    def validate_move(self, i, j, l, c, turn):   
        cb = deepcopy(self.chessboard)
        wk = deepcopy_list(self.white_kills)
        bk = deepcopy_list(self.black_kills)

        for ix in range(len(cb)):
            for jx in range(len(cb[ix])):
                if type(cb[ix][jx]) == Piece:
                    cb[ix][jx] = self.chessboard[ix][jx].clone()


        color = cb[i][j].piece_color
        piece = cb[i][j].piece

        if cb[i][j].piece_map[l][c] == 3:
            if color == 1:
                bk.append(cb[l][c].piece) #
            elif color == -1:
                wk.append(cb[l][c].piece) #

        if cb[i][j].piece_map[l][c] == 4 and piece.lower() == 'p':
            if color == 1:
                bk.append('P') #
            elif color == -1:
                wk.append('p') #
            cb[l-1*color][c] = '.'


        cb[i][j] = '.' #
        p        = Piece(l, c, cb, piece)
        cb[l][c] = p #
        

        for lin in range(len(cb)):
            for col in range(len(cb[lin])):
                if type(cb[lin][col]) == Piece:
                    cb[lin][col].chessboard = deepcopy(cb[l][c].chessboard) #
                    cb[lin][col].piece_arrange = (lin, col) #
                    cb[lin][col].piece_map = get_square_matrix(8) #
                    cb[lin][col].update_move() #

        if p.piece.lower() == 'k':
            ik, jk = l, c
        else:
            if turn == 1:
                ik,jk = self.black_king_position
            elif turn == -1:
                ik,jk = self.white_king_position

        print(ik,jk)
        if (ik,jk) == (-1,-1) or not has_check(ik, jk, cb, turn):
            print('x')
            if turn == -1:
                self.white_check = False
                if p.piece.lower() == 'k':
                    self.white_king_position = ik, jk
            elif turn == 1:
                self.black_check = False
                if p.piece.lower() == 'k':
                    self.black_king_position = ik, jk

            self.chessboard = cb
            self.white_kills = wk
            self.black_kills = bk
            return True
        
        return False

    def has_mate(self, turn, enemy_piece: Piece):
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
                if type(self.chessboard[i][j]) == Piece and self.chessboard[i][j].piece_color == -turn:
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
                if self.chessboard[k][x].piece_map[ie][je] in [3]:
                    count += 1


        if count == 0:
            return True
        return False


def alert_check(game: Game):
    if game.white_check:
        output = '\nO rei branco está em \033[91mxeque\033[0m!\n'
        return output
    if game.black_check:
        output = '\nO rei preto está em \033[91mxeque\033[0m!\n'
        return output
    return False

def main():
    cleaner = ('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    os.system('clear')
    if os.path.exists('/tmp/fifow'):
        os.remove('/tmp/fifow')
    if os.path.exists('/tmp/fifor'):
        os.remove('/tmp/fifor')
    os.mkfifo('/tmp/fifow')
    os.mkfifo('/tmp/fifor')
    os.system('clear')

    turns = [None, 'pretas', 'brancas']
    turn = -1 
    game = Game()
    print('Esperando o oponente conectar...')
    fr = open('/tmp/fifor')
    with open('/tmp/fifow', 'w') as fw:
        fw.write(cleaner)
        fw.write('Partida iniciada!')
        fw.flush()
        outputfunction = [None, fw.write, print]
        while True:
            for k in [1,-1]:
                output = alert_check(game)
                if output:
                    outputfunction[k](output)

                outputfunction[k]('\nPretas: ' + " ".join(game.black_kills) + '\n')
                output = show_chessboard(game.chessboard)
                outputfunction[k](output)
                outputfunction[k]('\nBrancas: ' + " ".join(game.white_kills) + '\n')
                outputfunction[k](f'Vez das {turns[turn]}, aguarde o oponente.')
                fw.flush()

            if stalemate(turn, game.chessboard):
                outputfunction[turn](f'\n\n\033[95mEmpate\033[0m por afogamento das {turns[turn]}.\n')
                outputfunction[-turn](f'\n\n\033[95mEmpate\033[0m por afogamento das {turns[turn]}.\n')
                fw.flush()
                break


            if turn == -1:
                piece_arrange = input('Selecione sua peça: ')
            elif turn == 1:
                fw.write('\nSelecione sua peça: \n')
                piece_arrange = fr.readline()

            if 'desisto' in piece_arrange.lower():
                outputfunction[turn](f'\n\n\033[95mXeque mate\033[0m, vitória das {turns[-turn]}\n')
                outputfunction[-turn](f'\n\n\033[95mXeque mate\033[0m, vitória das {turns[-turn]}\n')
                fw.flush()
                break
            elif 'empate' in piece_arrange.lower():
                if turn == -1:
                    fw.write(f'\nO oponente sugeriu empate, aceitar? (sim/não)')
                    fw.flush()
                    response = fr.readline()
                elif turn == 1:
                    response = input(f'\nO oponente sugeriu empate, aceitar? (sim/não): ')

                if 'sim' in response.lower():
                    outputfunction[turn](f'\n\n\033[95mEmpate\033[0m, ninguém venceu.\n')
                    outputfunction[-turn](f'\n\n\033[95mEmpate\033[0m, ninguém venceu.\n')
                    fw.flush()
                    break
                else:
                    outputfunction[turn](cleaner)
                    outputfunction[-turn](cleaner)
                    outputfunction[turn](f'\n\nEmpate negado\n')
                    outputfunction[-turn](f'\n\nEmpate negado\n')
                    continue

            if (arrange := get_arrange(piece_arrange)) != False:
                i, j = arrange
                piece_arrange = arrange
            else:
                outputfunction[turn](cleaner)
                outputfunction[-turn](cleaner)
                outputfunction[turn]('\nSelecione uma coordenada válida!' + '\n')
                fw.flush()
                continue

            if game.chessboard[i][j] == '.':
                outputfunction[turn](cleaner)
                outputfunction[-turn](cleaner)
                outputfunction[turn]('\nSelecione uma peça, você selecionou um espaço vazio...' + '\n')
                fw.flush()
                continue
            elif game.chessboard[i][j].piece_color != turn:
                outputfunction[turn](cleaner)
                outputfunction[-turn](cleaner)
                outputfunction[turn](f'\nAgora é vez das {turns[turn]}, jogue com uma peça válida!' + '\n')
                fw.flush()
                continue
            
            for k in [1,-1]:
                outputfunction[k](cleaner)
                output = alert_check(game)
                if output:
                    outputfunction[k](output)

                outputfunction[k]('\nPretas: ' + " ".join(game.black_kills) + '\n')
                output = show_movies(game.chessboard, game.chessboard[i][j].piece_map)
                outputfunction[k](output)
                outputfunction[k]('\nBrancas: ' + " ".join(game.white_kills) + '\n')
                outputfunction[k](f'Vez das {turns[turn]}, aguarde o oponente.')
                fw.flush()
            
            if turn == -1:
                movement = input('Selecione o destino (ou digite C para escolher outra peça): ')
                fw.flush()
            elif turn == 1:
                fw.write('\nSelecione o destino (ou digite C para escolher outra peça): \n')
                fw.flush()
                movement = fr.readline()

            if movement.lower() == 'c':
                outputfunction[turn](cleaner)
                outputfunction[-turn](cleaner)
                continue

            if (arrange := get_arrange(movement)) != False:
                movement = arrange

            else:
                outputfunction[turn](cleaner)
                outputfunction[-turn](cleaner)
                outputfunction[turn]('\nSelecione uma coordenada válida!' + '\n')
                fw.flush()
                continue


            if not (log := game.move_piece(piece_arrange, movement, turn)) is False:

                if log == 'End Game':
                    for k in [1,-1]:
                        outputfunction[k](cleaner)
                        outputfunction[k]('\nPretas: ' + " ".join(game.black_kills) + '\n')
                        output = show_chessboard(game.chessboard)
                        outputfunction[k](output)
                        outputfunction[k]('\nBrancas: ' + " ".join(game.white_kills) + '\n')
                        outputfunction[k](f'\n\n\033[95mXeque mate\033[0m, vitória das {turns[turn]}\n')
                        fw.flush()
                    break

                elif log == 'Você não pode mover para essa casa, seu rei ficará em xeque!':
                    
                    outputfunction[turn](cleaner)
                    outputfunction[-turn](cleaner)
                    outputfunction[turn]('\n'+log+'\n')
                    fw.flush()
                    continue
                
                outputfunction[turn](cleaner)
                outputfunction[-turn](cleaner)
                outputfunction[turn]('Movimentando...' + '\n')
                fw.flush()
                turn = turn * -1

            else:
                outputfunction[turn](cleaner)
                outputfunction[-turn](cleaner)
                outputfunction[turn]('Tente novamente' + '\n')
                fw.flush()



if __name__ == '__main__':
    main()