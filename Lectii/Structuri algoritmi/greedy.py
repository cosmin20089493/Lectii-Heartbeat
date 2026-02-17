# === Greedy: Coin Change ===
# Coin Change - greedy (funcționează corect doar cu monede canonice)
def coin_change(monede, suma):
    monede.sort(reverse=True)
    rezultat = []
    for m in monede:
        while suma >= m:
            suma -= m
            rezultat.append(m)
    if suma == 0:
        return rezultat
    else:
        return []  # Nu se poate face suma exact

# Exemplu de utilizare pentru Coin Change
monede = [1, 5, 10, 25]
suma = 63
print("Monede utilizate:", coin_change(monede, suma))  # Output: [25, 25, 10, 1, 1, 1]


# === Greedy: Huffman ===
# Huffman Coding - codificare optimă pentru caractere cu frecvențe diferite
import heapq

class NodHuffman:
    def __init__(self, simbol, frecventa):
        self.simbol = simbol
        self.frecventa = frecventa
        self.st = None
        self.dr = None
    def __lt__(self, alt):  # necesar pentru heapq
        return self.frecventa < alt.frecventa

def huffman(frecvente):
    heap = [NodHuffman(symb, freq) for symb, freq in frecvente.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        st = heapq.heappop(heap)
        dr = heapq.heappop(heap)
        intermediar = NodHuffman(None, st.frecventa + dr.frecventa)
        intermediar.st = st
        intermediar.dr = dr
        heapq.heappush(heap, intermediar)
    return heap[0]

def genereaza_coduri(nod, cod="", coduri={}):
    if nod is None:
        return
    if nod.simbol is not None:
        coduri[nod.simbol] = cod
    genereaza_coduri(nod.st, cod + "0", coduri)
    genereaza_coduri(nod.dr, cod + "1", coduri)
    return coduri

# Exemplu de utilizare pentru Huffman
frecvente = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
arbore = huffman(frecvente)
coduri = genereaza_coduri(arbore)
print("Coduri Huffman:", coduri)


# === Greedy: Interval Scheduling ===
# Interval Scheduling - selectează maximul de intervale care nu se suprapun
def interval_scheduling(intervale):
    intervale.sort(key=lambda x: x[1])  # sortăm după final
    rezultat = []
    end_time = 0
    for inceput, sfarsit in intervale:
        if inceput >= end_time:
            rezultat.append((inceput, sfarsit))
            end_time = sfarsit
    return rezultat

# Exemplu de utilizare pentru Interval Scheduling
intervale = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
rezultat = interval_scheduling(intervale)
print("Intervale selectate:", rezultat)  # Output: [(1, 4), (5, 7), (8, 9)]


