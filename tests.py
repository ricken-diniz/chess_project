from pieces_movement import *
from aux_functions import *

class FeaturesTests():

    def test_simple_moves(d, points, ispawn = False):
        for tuple in points:
            i,j,n = tuple

            M = get_square_matrix(8)  

            d(i,j,M) if not ispawn else d(i,j,M,n)
            show_matrix(M)
            print(tuple)
            for l in M:
                print(' '.join(l))
            print()

    def test_compound_moves(d, points):
        for tuple in points:
            i,j,n = tuple

            chessboard = get_game_example() 
            M = get_square_matrix(8)   

            d(i,j,M,chessboard,n)
            show_matrix(M)
            print(tuple)
            for l in M:
                print(' '.join(l))
            print()

    def test_initial_game(defs):
        chessboard = get_game_example()

        for lin in range(len(chessboard)):
            for col in range(len(chessboard[lin])):

                try:
                    color = check_color(chessboard[lin][col])
                    for k in chessboard[lin][col].keys():
                        piece = k
                        break
                    chessboard[lin][col][piece] = get_square_matrix(8)

                    defs[piece.lower()](lin,col, chessboard[lin][col][piece],chessboard, color)

                except Exception as x:
                    continue

        return chessboard

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
    
    # with FeaturesTests as ft:

    # # ==================Simple Moves==================
    #     for e in defs.keys():
    #         piece = f'  {e}  '
    #         print(f'\n{'':=^30}\n')
    #         print(f'{piece:=^30}\n')
    #         if e == 'pawn':
    #             ft.test_simple_moves(defs[e], points, True)
    #         else:
    #             ft.test_simple_moves(defs[e], points)

    # # ==================Compound Moves==================
    #     for e in defs.keys():
    #         piece = f'  {e}  '
    #         print(f'\n{'':=^30}\n')
    #         print(f'{piece:=^30}\n')
    #         # if e == 'pawn':
    #         #     ft.test_compound_moves(defs[e], points, True)
            
    #         ft.test_compound_moves(defs[e], points)


    # ==================Initial Game==================
    chessboard = get_initial_game(defs)

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



if __name__ == '__main__':
    main()