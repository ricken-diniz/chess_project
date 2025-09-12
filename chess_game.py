from pieces_movement import *
from utils import *

class Game():
    def __init__(self):
        self.chessboard = get_initial_game(Piece)

    def move_piece(self, piece_arrange, movement):
        i, j = piece_arrange
        l, c = movement

        if type(self.chessboard[i][j]) == Piece:
            
            if self.chessboard[i][j].piece_map[l][c] in [1,3]:
                piece = self.chessboard[i][j].piece
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
                    
                return True
            
            return False




def main():
    turns = [None, 'white', 'black']
    turn = 1 
    left_hook = True
    right_hook = True
    incheck = False
    game = Game()

    while True:
        show_chessboard(game.chessboard)

        piece_arrange = (int(input('peça i:')), int(input('peça j:')))
        movement = (int(input('destino i:')), int(input('destino j:')))

        if game.move_piece(piece_arrange, movement):
            print('Movimentando...')
        else:
            print('Tente novamente')



if __name__ == '__main__':
    main()