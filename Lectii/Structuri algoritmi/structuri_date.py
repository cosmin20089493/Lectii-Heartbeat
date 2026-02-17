# === Liste ===
# Liste simple: fiecare nod pointează spre următorul
class NodSimplu:
    def __init__(self, val):
        self.val = val
        self.urm = None

# Liste duble: fiecare nod pointează spre următorul și precedent
class NodDublu:
    def __init__(self, val):
        self.val = val
        self.urm = None
        self.prev = None

# Liste circulare: ultimul nod pointează înapoi la primul
class NodCircular:
    def __init__(self, val):
        self.val = val
        self.urm = self  # la început, se referă la sine

# Exemplu de utilizare pentru Liste
# Liste simple
a = NodSimplu(1)
a.urm = NodSimplu(2)
print("Listă simplă:", a.val, "->", a.urm.val)

# Liste duble
b = NodDublu(1)
c = NodDublu(2)
b.urm = c
c.prev = b
print("Listă dublă:", b.val, "<->", b.urm.val)

# Liste circulare
d = NodCircular(1)
e = NodCircular(2)
d.urm = e
e.urm = d
print("Listă circulară:", d.val, "->", d.urm.val, "->", d.urm.urm.val)


# === Stiva Coada ===
# Stivă (LIFO - Last In, First Out)
class Stiva:
    def __init__(self):
        self.items = []

    def push(self, item):  # adaugă un element
        self.items.append(item)

    def pop(self):  # scoate ultimul element
        return self.items.pop()

# Coada (FIFO - First In, First Out)
from collections import deque

class Coada:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):  # adaugă la sfârșit
        self.items.append(item)

    def dequeue(self):  # scoate de la început
        return self.items.popleft()

# Exemplu de utilizare pentru Stiva Coada
# Stivă
s = Stiva()
s.push(10)
s.push(20)
print("Pop din stivă:", s.pop())  # 20

# Coada
c = Coada()
c.enqueue(5)
c.enqueue(15)
print("Dequeue din coadă:", c.dequeue())  # 5


# === Arbore Binar ===
# Arbore binar: fiecare nod are maxim doi copii
class NodArbore:
    def __init__(self, val):
        self.val = val
        self.stanga = None
        self.dreapta = None

# Inserare în arbore binar de căutare
def inserare(nod, val):
    if nod is None:
        return NodArbore(val)
    if val < nod.val:
        nod.stanga = inserare(nod.stanga, val)
    else:
        nod.dreapta = inserare(nod.dreapta, val)
    return nod

# Căutare într-un arbore binar
def cauta(nod, val):
    if nod is None or nod.val == val:
        return nod
    if val < nod.val:
        return cauta(nod.stanga, val)
    return cauta(nod.dreapta, val)

# Ștergere nod din arbore binar
def sterge(nod, val):
    if nod is None:
        return nod
    if val < nod.val:
        nod.stanga = sterge(nod.stanga, val)
    elif val > nod.val:
        nod.dreapta = sterge(nod.dreapta, val)
    else:
        if nod.stanga is None:
            return nod.dreapta
        elif nod.dreapta is None:
            return nod.stanga
        succesor = nod.dreapta
        while succesor.stanga:
            succesor = succesor.stanga
        nod.val = succesor.val
        nod.dreapta = sterge(nod.dreapta, succesor.val)
    return nod

# Exemplu de utilizare pentru Arbore Binar
# Construire arbore binar și operații
radacina = None
for val in [8, 3, 10, 1, 6, 14]:
    radacina = inserare(radacina, val)

nod_gasit = cauta(radacina, 6)
print("Căutat 6:", nod_gasit.val if nod_gasit else "Nu a fost găsit")

radacina = sterge(radacina, 10)
print("Șters 10. Căutare 10 după ștergere:", cauta(radacina, 10))


