"""Blestemul celor Două Papirusuri (Sortarea Dublă)



Poveste:

În templu sunt două papirusuri cu numere. Marele Scrib a pus o regulă absurdă:

- Papirusul A trebuie sortat cu MERGE SORT

- Papirusul B trebuie sortat cu QUICK SORT

După aceea, trebuie să le unești într-o singură listă SORTATĂ CRESCĂTOR, ca să se deschidă ușa.



CERINȚĂ:

Scrie un program care:

1) citește două liste de numere întregi A și B

2) sortează A folosind MERGE SORT (implementat de tine)

3) sortează B folosind QUICK SORT (implementat de tine)

4) interclasează (merge) cele două liste sortate într-una singură, sortată crescător

5) afișează lista finală



RESTRICȚII:

- Fără sort() / sorted()

- Fără clase

- Ai voie: funcții, liste, recursie, if/for/while

- Orice altă “scurtătură” de sortare este interzisă

"""

#Merge Sort pentru papirusulA

def merge_sort(a):
    if len(a) <= 1:  #verificam lungimea listez, in cay ca are 0 sau 1 elemen, este deja sortata.
        return a

#impartim lista in doua jumatati, -metoda merge sort


    mijloc = len(a)//2
    stanga=merge_sort(a[:mijloc])
    dreapta = merge_sort(a[mijloc:])

# "combinam cele doua jumatati sortate)

    return  doua_sortari(stanga, dreapta)

# Quick sort pentru papirusulB

def quicksort(a):
    if len(a) <= 1:
        return a

    #alegem pivotul, ultimul element
    pivot = a[-1]

    mai_mic = []
    egal = []
    mai_mare =[]

    for x in a:
        if x < pivot:
            mai_mic.append(x)
        elif x == pivot:
            egal.append(x)
        else:
            mai_mare.append(x)

    #sortam recursiv partiile

    return quicksort(mai_mic) + egal + quicksort(mai_mare)

#interclasarea a doua liste deja sortate

def doua_sortari(a,b):
    rezultat = []
    i = j = 0

    #comparam element cu element

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            rezultat.append(a[i])
            i += 1
        else:
            rezultat.append(b[j])
            j += 1

    #adaugam ce a ramas
    while i < len(a):
        rezultat.append(a[i])
        i += 1
    while j < len(b):
        rezultat.append(b[j])
        j += 1
    return rezultat


#citim papirusulA si B

n = int(input())
papirusulA = list(map(int, input().split()))

m = int(input())
papirusulB = list(map(int, input().split()))

#sortari

papirusulA = merge_sort(papirusulA)
papirusulB = merge_sort(papirusulB)

#interclasarea finala

final = doua_sortari(papirusulA, papirusulB)

print(*final)



























