def get_square_matrix(n):
    M = [[0 for _ in range(n)] for _ in range(n)]
    return M

def deepcopy(M):
    matrix = []

    for i in range(len(M)):
        matrix.append([])
        for e in [i]:
            matrix[i].append(e)

    return matrix

def show_matrix(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            
            if M[i][j] == 1:
                M[i][j] = f'\033[94m{1}\033[0m'
            elif M[i][j] == 2:
                M[i][j] = f'\033[91m{2}\033[0m'
            else:
                M[i][j] = f'{M[i][j]}'