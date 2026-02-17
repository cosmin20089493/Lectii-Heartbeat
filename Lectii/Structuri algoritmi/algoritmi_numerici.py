# === Algoritmi Numerici: Criba Eratostene ===
# Criba lui Eratostene - generează toți primii <= n
def criba(n):
    prim = [True for _ in range(n+1)]
    prim[0], prim[1] = False, False
    p = 2
    while p * p <= n:
        if prim[p]:
            for i in range(p * p, n+1, p):
                prim[i] = False
        p += 1
    return [i for i, is_prim in enumerate(prim) if is_prim]

# Exemplu de utilizare pentru Criba Eratostene
print("Numere prime până la 30:", criba(30))  # Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


# === Algoritmi Numerici: Euclid ===
# Algoritmul lui Euclid - cel mai mare divizor comun (GCD)
def euclid(a, b):
    while b:
        a, b = b, a % b
    return a

# Exemplu de utilizare pentru Euclid
a, b = 60, 48
print(f"GCD({a}, {b}) =", euclid(a, b))  # Output: 12


# === Algoritmi Numerici: Euclid Extins ===
# Algoritmul lui Euclid extins - returnează (gcd, x, y) astfel încât ax + by = gcd
def euclid_extins(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = euclid_extins(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return d, x, y

# Exemplu de utilizare pentru Euclid Extins
a, b = 30, 20
d, x, y = euclid_extins(a, b)
print(f"GCD({a}, {b}) = {d}, cu x = {x}, y = {y}")  # Output: GCD(30,20)=10, x,y astfel încât 30x + 20y = 10


# === Algoritmi Numerici: Exponentiere Rapida ===
# Exponențiere rapidă (a^b mod m) - log(b)
def exp_rapida(a, b, mod):
    rezultat = 1
    a = a % mod
    while b > 0:
        if b % 2 == 1:
            rezultat = (rezultat * a) % mod
        a = (a * a) % mod
        b //= 2
    return rezultat

# Exemplu de utilizare pentru Exponentiere Rapida
a, b, mod = 3, 13, 17
print(f"{a}^{b} mod {mod} =", exp_rapida(a, b, mod))  # Output: 12


# === Algoritmi Numerici: Radacina Primitiva ===
# Găsește o rădăcină primitivă modulo p (simplificat)
def este_prim(p):
    if p < 2: return False
    for i in range(2, int(p**0.5)+1):
        if p % i == 0:
            return False
    return True

def gaseste_radacina(p):
    if not este_prim(p):
        return -1
    phi = p - 1
    factori = set()
    n = phi
    i = 2
    while i*i <= n:
        if n % i == 0:
            factori.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factori.add(n)
    for r in range(2, p):
        ok = True
        for f in factori:
            if pow(r, phi // f, p) == 1:
                ok = False
                break
        if ok:
            return r
    return -1

# Exemplu de utilizare pentru Radacina Primitiva
p = 17
print(f"Rădăcină primitivă modulo {p}:", gaseste_radacina(p))  # Output: de ex. 3


