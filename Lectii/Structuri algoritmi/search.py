# === Cautare Liniara ===
# Căutare liniară: verifică fiecare element din listă până găsește valoarea căutată
def cautare_liniara(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # returnează indexul elementului
    return -1  # returnează -1 dacă nu a fost găsit

# Exemplu de utilizare pentru Cautare Liniara
arr = [3, 5, 7, 9, 11]
pozitie = cautare_liniara(arr, 7)
print("Poziția elementului 7 este:", pozitie)  # Output: 2


# === Cautare Binara ===
# Căutare binară: funcționează doar pe liste sortate
# Împarte lista în jumătate și caută recursiv în jumătatea corespunzătoare
def cautare_binara(arr, target):
    stanga, dreapta = 0, len(arr) - 1
    while stanga <= dreapta:
        mijloc = (stanga + dreapta) // 2
        if arr[mijloc] == target:
            return mijloc  # găsit
        elif arr[mijloc] < target:
            stanga = mijloc + 1
        else:
            dreapta = mijloc - 1
    return -1  # nu a fost găsit

# Exemplu de utilizare pentru Cautare Binara
arr = [1, 3, 5, 7, 9, 11]
pozitie = cautare_binara(arr, 9)
print("Poziția elementului 9 este:", pozitie)  # Output: 4


# === Cautare In Matrice 1 ===
# Căutare într-o matrice sortată pe linii și coloane
def cautare_in_matrice(matrice, target):
    if not matrice:
        return False
    rows, cols = len(matrice), len(matrice[0])
    row, col = 0, cols - 1
    while row < rows and col >= 0:
        if matrice[row][col] == target:
            return True
        elif matrice[row][col] > target:
            col -= 1
        else:
            row += 1
    return False

# Exemplu de utilizare pentru Cautare In Matrice 1
matrice = [
    [1, 4, 7, 11],
    [2, 5, 8, 12],
    [3, 6, 9, 16],
    [10, 13, 14, 17]
]
gasit = cautare_in_matrice(matrice, 5)
print("Elementul 5 a fost găsit:", gasit)  # Output: True


# === Cautare In Matrice 2 ===
# Căutare într-o matrice sortată pe linii și coloane
# Începe din colțul dreapta sus și se deplasează spre stânga sau jos
def cautare_in_matrice(matrice, target):
    if not matrice or not matrice[0]:
        return False
    randuri = len(matrice)
    coloane = len(matrice[0])
    i, j = 0, coloane - 1
    while i < randuri and j >= 0:
        if matrice[i][j] == target:
            return True
        elif matrice[i][j] > target:
            j -= 1
        else:
            i += 1
    return False

# Exemplu de utilizare pentru Cautare In Matrice 2
matrice = [
    [1, 4, 7, 11],
    [2, 5, 8, 12],
    [3, 6, 9, 16],
    [10, 13, 14, 17]
]
gasit = cautare_in_matrice(matrice, 5)
print("Elementul 5 a fost găsit:", gasit)  # Output: True


