# === Divide et Impera: Merge Sort ===
# Merge Sort - divide et impera
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# Exemplu de utilizare pentru Merge Sort
arr = [38, 27, 43, 3, 9, 82, 10]
merge_sort(arr)
print("Merge Sort:", arr)  # Output: [3, 9, 10, 27, 38, 43, 82]


# === Divide et Impera: Quick Sort ===
# Quick Sort - divide et impera
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    lesser = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    return quick_sort(lesser) + [pivot] + quick_sort(greater)

# Exemplu de utilizare pentru Quick Sort
arr = [10, 7, 8, 9, 1, 5]
sorted_arr = quick_sort(arr)
print("Quick Sort:", sorted_arr)  # Output: [1, 5, 7, 8, 9, 10]


# === Divide et Impera: Karatsuba ===
# Algoritmul Karatsuba pentru înmulțirea rapidă a două numere mari
def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y
    n = max(len(str(x)), len(str(y)))
    n2 = n // 2
    high1, low1 = divmod(x, 10**n2)
    high2, low2 = divmod(y, 10**n2)
    z0 = karatsuba(low1, low2)
    z1 = karatsuba((low1 + high1), (low2 + high2))
    z2 = karatsuba(high1, high2)
    return (z2 * 10**(2*n2)) + ((z1 - z2 - z0) * 10**n2) + z0

# Exemplu de utilizare pentru Karatsuba
x = 12345678
y = 87654321
print("Karatsuba multiplication:", karatsuba(x, y))  # Output: 1082152022374638


