# === Backtracking: Labirint ===
# Rezolvarea unui labirint (matrice 0/1) cu backtracking
def labirint(matrice, x, y, sol):
    N = len(matrice)
    if x == y == N - 1 and matrice[x][y] == 1:
        sol[x][y] = 1
        return True
    if 0 <= x < N and 0 <= y < N and matrice[x][y] == 1:
        sol[x][y] = 1
        if labirint(matrice, x + 1, y, sol): return True
        if labirint(matrice, x, y + 1, sol): return True
        sol[x][y] = 0  # backtrack
    return False

# Exemplu de utilizare pentru Labirint
matrice = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 1]
]
sol = [[0]*4 for _ in range(4)]
if labirint(matrice, 0, 0, sol):
    for rand in sol:
        print(rand)
else:
    print("Fără soluție")


# === Backtracking: N Queens ===
# Problema N-Reginelor: așezarea reginelor pe o tablă NxN
def este_valid(tabla, rand, col):
    for i in range(rand):
        if tabla[i] == col or            tabla[i] - i == col - rand or            tabla[i] + i == col + rand:
            return False
    return True

def n_queens(n, rand=0, tabla=[]):
    if rand == n:
        print(tabla)
        return
    for col in range(n):
        if este_valid(tabla, rand, col):
            n_queens(n, rand + 1, tabla + [col])

# Exemplu de utilizare pentru N Queens
n = 4
n_queens(n)  # Afișează toate soluțiile pentru 4 regine


# === Backtracking: Perm Combi Aranj ===
# Permutări: toate ordonările posibile ale unei liste
def permutari(arr, path=[], used=None):
    if used is None:
        used = [False] * len(arr)
    if len(path) == len(arr):
        print(path)
        return
    for i in range(len(arr)):
        if not used[i]:
            used[i] = True
            permutari(arr, path + [arr[i]], used)
            used[i] = False

# Combinări: alege k elemente din n
def combinari(arr, k, start=0, path=[]):
    if len(path) == k:
        print(path)
        return
    for i in range(start, len(arr)):
        combinari(arr, k, i + 1, path + [arr[i]])

# Aranjamente: ca permutările, dar doar pentru k elemente
def aranjamente(arr, k, path=[], used=None):
    if used is None:
        used = [False] * len(arr)
    if len(path) == k:
        print(path)
        return
    for i in range(len(arr)):
        if not used[i]:
            used[i] = True
            aranjamente(arr, k, path + [arr[i]], used)
            used[i] = False

# Exemplu de utilizare pentru Perm Combi Aranj
arr = [1, 2, 3]
print("Permutări:")
permutari(arr)

print("Combinări de 2:")
combinari(arr, 2)

print("Aranjamente de 2:")
aranjamente(arr, 2)


# === Backtracking: Sudoku Solver ===
# Solvator Sudoku prin backtracking
def este_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num or            board[3*(row//3)+i//3][3*(col//3)+i%3] == num:
            return False
    return True

def rezolva_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if este_valid(board, row, col, num):
                        board[row][col] = num
                        if rezolva_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Exemplu de utilizare pentru Sudoku Solver
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
if rezolva_sudoku(board):
    for rand in board:
        print(rand)
else:
    print("Nu există soluție")


