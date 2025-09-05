def spawn_pointers_bishop(i,j, M):
    M[i][j] = 2

    greater = i if i > j else j
    less = i if i < j else j
    primary_d_coefficient = greater - less
    secondary_d_coefficient = i + j - (len(M) - 1)

    for _ in range(len(M)-primary_d_coefficient):
        lin, col = (_, (_+primary_d_coefficient)) if j > i else ((_+primary_d_coefficient), _)
        M[lin][col] = 1

    for _ in range(len(M)-abs(secondary_d_coefficient)):
        lin, col = (_, (len(M)-1-_-abs(secondary_d_coefficient))) if secondary_d_coefficient < 0 else ((_+ abs(secondary_d_coefficient)), (len(M)-1-_))
        M[lin][col] = 1

def spawn_pointers_rook(i,j, M):
    M[i][j] = 2

    for index in range(len(M[i])):
        M[i][index] = 1
        M[index][j] = 1

def spawn_pointers_queen(i,j, M):
    spawn_pointers_rook(i,j, M)
    spawn_pointers_bishop(i,j, M)

def spawn_pointers_horse(i,j,M):
    M[i][j] = 2
    l = len(M)

    houses = [
        (i-2,j-1),
        (i+2,j-1),
        (i-2,j+1),
        (i+2,j+1),
        (i-1,j-2),
        (i+1,j-2),
        (i-1,j+2),
        (i+1,j+2),
    ]

    for t in houses:
        i,j = t
        if i >= 0 and j >= 0 and i < l and j < l:
            M[i][j] = 1

def spawn_pointers_K(i,j,M):
    M[i][j] = 2
    l = len(M)

    houses = [
        (i-1,j-1),
        (i+1,j+1),
        (i  ,j+1),
        (i  ,j-1),
        (i-1,j  ),
        (i+1,j  ),
        (i-1,j+1),
        (i+1,j-1),
    ]

    for t in houses:
        i,j = t
        if i >= 0 and j >= 0 and i < l and j < l:
            M[i][j] = 1

def spawn_pointers_P(i,j,M,color = 1):
    if color == 1 and i == (len(M) - 1) or color == -1 and i == 0:
        spawn_pointers_queen(i,j,M)
        return
    elif color == 1 and i == 1 or color == -1 and i == len(M) - 2:
        step = 2
    else:
        step = 1

    for _ in range(1,step+1):
        M[i + (_*color)][j] = 1