# === Programare Dinamică: Fibonacci ===
# Fibonacci cu programare dinamică (memorare)
def fibonacci(n):
    if n == 0: return 0
    if n == 1: return 1
    dp = [0] * (n+1)
    dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Exemplu de utilizare pentru Fibonacci
n = 10
print(f"Fibonacci({n}) =", fibonacci(n))  # Output: 55


# === Programare Dinamică: Knapsack ===
# Problema rucsacului 0/1
def knapsack(W, greutati, valori, n):
    dp = [[0 for x in range(W + 1)] for x in range(n + 1)]
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif greutati[i-1] <= w:
                dp[i][w] = max(valori[i-1] + dp[i-1][w - greutati[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]

# Exemplu de utilizare pentru Knapsack
valori = [60, 100, 120]
greutati = [10, 20, 30]
capacitate = 50
n = len(valori)
print("Knapsack:", knapsack(capacitate, greutati, valori, n))  # Output: 220


# === Programare Dinamică: Lcs ===
# Longest Common Subsequence (LCS)
def lcs(X, Y):
    m = len(X)
    n = len(Y)
    dp = [[0] * (n + 1) for i in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if X[i] == Y[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[m][n]

# Exemplu de utilizare pentru Lcs
X = "AGGTAB"
Y = "GXTXAYB"
print("LCS length:", lcs(X, Y))  # Output: 4


# === Programare Dinamică: Lis ===
# Longest Increasing Subsequence (LIS)
def lis(arr):
    n = len(arr)
    dp = [1] * n
    for i in range(1, n):
        for j in range(0, i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# Exemplu de utilizare pentru Lis
arr = [10, 22, 9, 33, 21, 50, 41, 60]
print("LIS length:", lis(arr))  # Output: 5


# === Programare Dinamică: Sum Max Sir ===
# Suma maximă a unui subșir contiguu (Kadane's Algorithm)
def suma_maxima_sir(arr):
    max_curent = max_total = arr[0]
    for i in range(1, len(arr)):
        max_curent = max(arr[i], max_curent + arr[i])
        max_total = max(max_total, max_curent)
    return max_total

# Exemplu de utilizare pentru Sum Max Sir
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print("Suma maximă a subșirului:", suma_maxima_sir(arr))  # Output: 6


