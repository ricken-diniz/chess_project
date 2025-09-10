from pieces_movement import *
from aux_functions import *
from chess_game import *

class FeaturesTests():
    def __init__(self, defs, points):
        self.defs = defs
        self.points = points

    def validate_initial_game(self):
        chessboard = get_initial_game(self.defs)

        maps = []
        for line in chessboard:
            lin = []
            for e in line:
                if type(e) == dict:
                    for k in e.keys():  
                        lin.append(k)
                        break
                    maps.append(e)
                else:
                    lin.append(e)

            print(' '.join(lin))

        for e in maps:
            for k in e.keys():
                piece = k
                break

            print(f'\n{'':=^30}\n')
            print(f'{piece:=^30}\n')

            show_matrix(e[piece])

            for lin in e[piece]:
                for _ in range(len(lin)):
                    lin[_] = str(lin[_])
                print(' '.join(lin))

    def validate_has_check(self):
        chessboard = get_empty_example()
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

            M                               = get_square_matrix(8)
            chessboard[0][0]                = {}
            chessboard[0][0]['ispinned']    = False
            spawn_pointers_queen(0, 0, M, chessboard, qcolor)

            M                               = get_square_matrix(8)
            chessboard[7][0]                = {}
            chessboard[7][0]['ispinned']    = False
            spawn_pointers_rock(7, 0, M, chessboard, rcolor)

            if has_check(7, 7, chessboard, turn) == hcheck:
                print(f'cases[{count}]: validated')
            else:
                print(f'cases[{count}]: invalidated')

            count += 1

    def validate_moves(self, compound = False):
        for function in self.defs.keys():
            piece = f'  {[function]}  '
            print(f'\n{'':=^30}\n')
            print(f'{piece:=^30}\n')
            function = function.lower()
            chessboard = get_game_example()

            self.test_compound_moves(chessboard, function, compound)

    def test_compound_moves(self, chessboard, function, compound):
        for tuple in self.points:
            if not compound:
                chessboard = get_empty_example()

            i,j,n = tuple

            M = get_square_matrix(8)   

            self.defs[function](i,j,M,chessboard,n)
            show_matrix(M)

            if n == 1:
                color = 'branca'
            else: 
                color = 'preta'

            print(f'Peça {function} na posição - {i}, {j} - de cor {color}')

            for l in M:
                print(' '.join(l))
            print()


def main():
    
    M = []
    points = [
        (6,4,1),
        (5,3,1),
        (5,3,-1),
        (0,3,-1),
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
    defs = {
        'k': spawn_pointers_king,
        'q': spawn_pointers_queen,
        'r': spawn_pointers_rock,
        'b': spawn_pointers_bishop,
        'h': spawn_pointers_horse,
        'p': spawn_pointers_pawn,
    }

    ft = FeaturesTests(defs, points)

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