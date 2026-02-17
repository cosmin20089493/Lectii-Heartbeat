# === Bubble Sort ===
# Bubble Sort: compară elementele adiacente și le interschimbă dacă sunt în ordine greșită.
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # Ultimele i elemente sunt deja sortate
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                # Schimbă elementele dacă sunt în ordine greșită
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Exemplu de utilizare pentru Bubble Sort
arr = [5, 2, 9, 1, 5, 6]
bubble_sort(arr)
print("Bubble Sort:", arr)  # [1, 2, 5, 5, 6, 9]


# === Counting Sort ===
# Counting Sort: numără aparițiile fiecărui element și le rearanjează în ordine
def counting_sort(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    idx = 0
    for i in range(len(count)):
        while count[i] > 0:
            arr[idx] = i
            idx += 1
            count[i] -= 1

# Exemplu de utilizare pentru Counting Sort
arr = [4, 2, 2, 8, 3, 3, 1]
counting_sort(arr)
print("Counting Sort:", arr)  # [1, 2, 2, 3, 3, 4, 8]


# === Heap Sort ===
# Heap Sort: construiește un max-heap și extrage pe rând elementele maxime
def heapify(arr, n, i):
    largest = i  # presupunem că rădăcina e cea mai mare
    l = 2*i + 1   # indexul fiului stâng
    r = 2*i + 2   # indexul fiului drept
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    # Construim heap-ul
    for i in range(n//2 -1, -1, -1):
        heapify(arr, n, i)
    # Extragem elementele unul câte unul
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# Exemplu de utilizare pentru Heap Sort
arr = [12, 11, 13, 5, 6, 7]
heap_sort(arr)
print("Heap Sort:", arr)  # [5, 6, 7, 11, 12, 13]


# === Insertion Sort ===
# Insertion Sort: inserează fiecare element în poziția corectă din partea sortată a listei
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]  # elementul curent
        j = i - 1
        # mutăm elementele mai mari decât key la o poziție înainte
        while j >=0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

# Exemplu de utilizare pentru Insertion Sort
arr = [9, 5, 1, 4, 3]
insertion_sort(arr)
print("Insertion Sort:", arr)  # [1, 3, 4, 5, 9]


# === Merge Sort ===
# Merge Sort: divide lista în două, sortează recursiv și apoi îmbină
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]  # prima jumătate
        R = arr[mid:]  # a doua jumătate
        merge_sort(L)  # sortăm recursiv jumătățile
        merge_sort(R)
        i = j = k = 0
        # Îmbinăm cele două jumătăți sortate
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        # Adăugăm elementele rămase
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
print("Merge Sort:", arr)  # [3, 9, 10, 27, 38, 43, 82]


# === Quick Sort ===
# Quick Sort: alege un pivot, sortează recursiv elementele mai mici și mai mari
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]  # alegem primul element ca pivot
    lesser = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    # sortăm recursiv și îmbinăm
    return quick_sort(lesser) + [pivot] + quick_sort(greater)

# Exemplu de utilizare pentru Quick Sort
arr = [10, 7, 8, 9, 1, 5]
sorted_arr = quick_sort(arr)
print("Quick Sort:", sorted_arr)  # [1, 5, 7, 8, 9, 10]


# === Radix Sort ===
# Radix Sort: sortează cifră cu cifră începând de la cea mai puțin semnificativă
def counting_sort_exp(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in arr:
        count[(i // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        idx = (arr[i] // exp) % 10
        output[count[idx] - 1] = arr[i]
        count[idx] -= 1
        i -= 1
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort_exp(arr, exp)
        exp *= 10

# Exemplu de utilizare pentru Radix Sort
arr = [170, 45, 75, 90, 802, 24, 2, 66]
radix_sort(arr)
print("Radix Sort:", arr)  # [2, 24, 45, 66, 75, 90, 170, 802]


# === Selection Sort ===
# Selection Sort: selectează cel mai mic element și îl plasează în poziția corectă
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i  # presupunem că elementul curent este minimul
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # schimbăm elementul minim cu primul element nesortat
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# Exemplu de utilizare pentru Selection Sort
arr = [64, 25, 12, 22, 11]
selection_sort(arr)
print("Selection Sort:", arr)  # [11, 12, 22, 25, 64]


