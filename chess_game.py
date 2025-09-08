def has_check(i, j, chessboard, turn):
    pieces = [None, ['K','Q','R','B','H','P'], ['k','q','r','b','h','p']]

    for l in range(len(chessboard)):
        for c in range(len(chessboard)):
            if type(chessboard[l][c]) is dict:
                for k in chessboard[l][c].keys():
                    if k in pieces[-turn]:

                        enimy_piece_map = chessboard[l][c][k]
                        if enimy_piece_map[i][j] in [1,3]:
                            return True

                        break
    
    return False
    # ...

def main():
    turns = [None, 'white', 'black']
    turn = 1 
    left_hook = True
    right_hook = True
    incheck = False


if __name__ == '__main__':
    main()