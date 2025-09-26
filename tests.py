from pieces_movement import *
from utils import *

class FeaturesTests():
    def __init__(self, points):
        self.points = points

    def validate_initial_game(self):
        chessboard = get_initial_game(Piece)

        show_chessboard(chessboard)

    def validate_has_check(self):
        chessboard = get_chessboard('empty')
        cases = [

            # validated
            (1 , 1, 1, False),
            (-1,-1, 1, True),
            (-1, 1, 1, True),
            (1 ,-1, 1, True),
            (1 ,-1,-1, True),
            (1 , 1,-1, True),
            (-1,-1,-1, False),
            (-1, 1,-1, True),
            
            # invalidated
            (1 , 1, 1, True),
            (-1,-1, 1, False),
            (-1, 1, 1, False),
            (1 ,-1, 1, False),
            (1 ,-1,-1, False),
            (1 , 1,-1, False),
            (-1,-1,-1, True),
            (-1, 1,-1, False),
        ]

        count = 0

        for tuple in cases:
            qcolor, rcolor, turn, hcheck = tuple

            queen = 'Q' if qcolor == -1 else 'q'
            rook = 'R' if rcolor == -1 else 'r'

            p = Piece(0, 0, chessboard, queen)
            chessboard[0][0] = p

            p = Piece(7, 0, chessboard, rook)
            chessboard[7][0] = p

            if has_check(7, 7, chessboard, turn) == hcheck:
                print(f'cases[{count}]: validated')
            else:
                print(f'cases[{count}]: invalidated')

            count += 1

    def validate_moves(self, compound = False):
        for piece in ['r','n','b','q','k','p']:

            formatation = f'   {piece}   '
            print(f'\n{'':=^30}\n')
            print(f'{formatation:=^30}\n')

            for tuple in self.points:
                if not compound:
                    chessboard = get_initial_game(Piece,'empty')    
                else:
                    chessboard = get_initial_game(Piece)


                i,j,n = tuple
                if n == 1:
                    piece = piece.upper()
                    color = 'branca'
                else: 
                    piece = piece.lower()
                    color = 'preta'

                chessboard[i][j] = '.'
                p = Piece(i, j, chessboard, piece)
                chessboard[i][j] = p
                M = chessboard[i][j].show_map()


                print(f'Peça {piece} na posição - {i}, {j} - de cor {color}')

                for l in M:
                    print(' '.join(l))
                print()


def main():
    
    points = [
        (6,4,1),
        (5,3,1),
        (5,3,-1),
        (2,3,-1),
        (3,4,-1),
        (6,5,1),
        (6,7,1),
        (5,5,-1),
        (5,4,-1),
        (0,0,1),
        (1,1,1),
        (2,2,1),
        (3,3,1),
        (4,0,1),
        (5,0,1),
        (6,0,1),
        (7,0,1),
        ]

    ft = FeaturesTests(points)

    print()
    print('Mensagem do Sistema')
    print('Informações úteis')
    print('Valor 1: casa habilitada para movimentar')
    print('Valor 2: casa ocupada pela peça')
    print('Valor 3: casa habilitada para comer')
    print('Valor 4: movimento especial')
    print('Valor 5: próxima casa desabilitada para movimentar')
    print()
    while (res := input('\nQual funcionalidade você quer testar?\n1. Movimento simples\n2. Movimento composto\n3. Game inicial\n4. Check\n\n > ')) != 'q':

        if res == '1':
            ft.validate_moves()

        elif res == '2':
            ft.validate_moves(True)

        elif res == '3':
            ft.validate_initial_game()

        elif res == '4':
            ft.validate_has_check()

        else:
            print('Insira uma entrada válida...\n')
            continue

if __name__ == '__main__':
    main()