# === Algoritmul Bfs ===
# Breadth-First Search (BFS) - parcurgere pe niveluri
from collections import deque

def bfs(graf, start):
    vizitat = set()
    coada = deque([start])
    while coada:
        nod = coada.popleft()
        if nod not in vizitat:
            print(nod, end=' ')
            vizitat.add(nod)
            for vecin in graf[nod]:
                if vecin not in vizitat:
                    coada.append(vecin)

# Exemplu de utilizare pentru Bfs
graf = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
print("BFS:")
bfs(graf, 'A')  # Output: A B C D


# === Algoritmul Dfs ===
# Depth-First Search (DFS) - parcurgere în adâncime
def dfs(graf, nod, vizitat=None):
    if vizitat is None:
        vizitat = set()
    print(nod, end=' ')
    vizitat.add(nod)
    for vecin in graf[nod]:
        if vecin not in vizitat:
            dfs(graf, vecin, vizitat)

# Exemplu de utilizare pentru Dfs
graf = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
print("DFS:")
dfs(graf, 'A')  # Output: A B D C


# === Algoritmul Dijkstra ===
# Dijkstra - cel mai scurt drum de la sursă la toate nodurile
import heapq

def dijkstra(graf, start):
    dist = {nod: float('inf') for nod in graf}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        curent_dist, nod = heapq.heappop(heap)
        for vecin, cost in graf[nod]:
            if dist[nod] + cost < dist[vecin]:
                dist[vecin] = dist[nod] + cost
                heapq.heappush(heap, (dist[vecin], vecin))
    return dist

# Exemplu de utilizare pentru Dijkstra
graf = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2)], 'C': []}
dist = dijkstra(graf, 'A')
print("Dijkstra:", dist)  # Output: {'A': 0, 'B': 1, 'C': 3}


# === Algoritmul Bellman Ford ===
# Bellman-Ford - funcționează și cu ponderi negative
def bellman_ford(noduri, muchii, start):
    dist = {nod: float('inf') for nod in noduri}
    dist[start] = 0
    for _ in range(len(noduri) - 1):
        for u, v, cost in muchii:
            if dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
    return dist

# Exemplu de utilizare pentru Bellman Ford
noduri = ['A', 'B', 'C']
muchii = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 4)]
dist = bellman_ford(noduri, muchii, 'A')
print("Bellman-Ford:", dist)  # Output: {'A': 0, 'B': 1, 'C': 3}


# === Algoritmul Floyd Warshall ===
# Floyd-Warshall - toate perechile de noduri
def floyd_warshall(graf, n):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, cost in graf:
        dist[u][v] = cost
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# Exemplu de utilizare pentru Floyd Warshall
graf = [(0, 1, 4), (0, 2, 11), (1, 2, 2)]
dist = floyd_warshall(graf, 3)
print("Floyd-Warshall:")
for rand in dist:
    print(rand)


# === Algoritmul A Star ===
# A* (A star) - algoritm de căutare informată cu euristică
import heapq

def a_star(graf, start, goal, heuristica):
    heap = [(0, start)]
    venit = {start: None}
    cost = {start: 0}
    while heap:
        _, curent = heapq.heappop(heap)
        if curent == goal:
            break
        for vecin, c in graf[curent]:
            nou_cost = cost[curent] + c
            if vecin not in cost or nou_cost < cost[vecin]:
                cost[vecin] = nou_cost
                prioritate = nou_cost + heuristica[vecin]
                heapq.heappush(heap, (prioritate, vecin))
                venit[vecin] = curent
    return venit, cost

# Exemplu de utilizare pentru A Star
graf = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2)], 'C': []}
heuristica = {'A': 3, 'B': 1, 'C': 0}
venit, cost = a_star(graf, 'A', 'C', heuristica)
print("A* cost:", cost['C'])  # Output: 3


# === Algoritmul Prim ===
# Algoritmul lui Prim - arbore parțial minim (MST)
import heapq

def prim(graf, start):
    mst = []
    vizitat = set([start])
    heap = [(cost, start, vecin) for vecin, cost in graf[start]]
    heapq.heapify(heap)
    while heap:
        cost, frm, to = heapq.heappop(heap)
        if to not in vizitat:
            vizitat.add(to)
            mst.append((frm, to, cost))
            for vecin, c in graf[to]:
                if vecin not in vizitat:
                    heapq.heappush(heap, (c, to, vecin))
    return mst

# Exemplu de utilizare pentru Prim
graf = {
    'A': [('B', 1), ('C', 3)],
    'B': [('A', 1), ('C', 1)],
    'C': [('A', 3), ('B', 1)]
}
mst = prim(graf, 'A')
print("Prim:", mst)  # Output: [('A', 'B', 1), ('B', 'C', 1)]


# === Algoritmul Kruskal ===
# Algoritmul lui Kruskal - arbore parțial minim (MST) folosind reuniune și intersecție
def kruskal(noduri, muchii):
    parinte = {nod: nod for nod in noduri}

    def gaseste(x):
        while parinte[x] != x:
            x = parinte[x]
        return x

    def uneste(x, y):
        parinte[gaseste(x)] = gaseste(y)

    mst = []
    muchii.sort(key=lambda x: x[2])  # sortăm după cost
    for u, v, cost in muchii:
        if gaseste(u) != gaseste(v):
            uneste(u, v)
            mst.append((u, v, cost))
    return mst

# Exemplu de utilizare pentru Kruskal
noduri = ['A', 'B', 'C']
muchii = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 4)]
mst = kruskal(noduri, muchii)
print("Kruskal:", mst)  # Output: [('A', 'B', 1), ('B', 'C', 2)]


