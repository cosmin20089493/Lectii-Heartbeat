"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime, timedelta

class GenLiterar(Enum):
    FICTIUNE = auto()
    NON_FICTIUNE = auto()
    STIINTIFIC = auto()
    TEHNIC = auto()
    POEZIE = auto()


class StareExemplar(Enum):
    DISPONIBIL = "disponibil"
    IMPRUMUTAT = "imprumutat"
    DETERIORAT = "deteriorat"
    PIERDUT = "pierdut"


@dataclass
class Autor:
    nume: str
    prenume: str
    nationalitate: str = "Necunoscuta"
    carti_publicate: list = []

    def nume_complet(self):
        return f"{self.prenume} {self.nume}"

    def __hash__(self):
        return hash((self.nume, self.prenume))

    def __eq__(self, other):
        if isinstance(other, Autor):
            return self.nume == other.nume and self.prenume == other.prenume
        return NotImplemented


class PublicatieMeta(type):
    _registru = {}

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        isbn = args[0] if args else kwargs.get('isbn')
        if isbn:
            cls._registru[isbn] = instance
        return instance

    def get_by_isbn(cls, isbn):
        return cls._registru.get(isbn)


class Publicatie(ABC, metaclass=PublicatieMeta):
    def __init__(self, isbn, titlu, autor, an_publicare, gen):
        self._isbn = isbn
        self._titlu = titlu
        self._autor = autor
        self._an_publicare = an_publicare
        self._gen = gen
        self._exemplare = []

    @property
    def isbn(self):
        return self._isbn

    @property
    def titlu(self):
        return self._titlu

    @abstractmethod
    def get_tip(self):
        pass

    @abstractmethod
    def calculeaza_penalizare(self, zile_intarziere):
        pass

    def adauga_exemplar(self, stare=StareExemplar.DISPONIBIL):
        self._exemplare.append(stare)

    def exemplare_disponibile(self):
        return sum(1 for e in self._exemplare if e == "disponibil")

    def __eq__(self, other):
        if isinstance(other, Publicatie):
            return self._isbn == other._isbn
        return NotImplemented

    def __hash__(self):
        return hash(self._isbn)

    def __lt__(self, other):
        if isinstance(other, Publicatie):
            return self._titlu < other._titlu
        return NotImplemented

    def __str__(self):
        return f"{self.get_tip()}: '{self._titlu}' de {self._autor.nume_complet()} ({self._an_publicare})"

    def __repr__(self):
        return f"{self.__class__.__name__}(isbn='{self._isbn}', titlu='{self._titlu}')"


class Carte(Publicatie):
    def __init__(self, isbn, titlu, autor, an_publicare, gen, numar_pagini):
        super().__init__(isbn, titlu, autor, an_publicare, gen)
        self._numar_pagini = numar_pagini

    def get_tip(self):
        return "Carte"

    def calculeaza_penalizare(self, zile_intarziere):
        return zile_intarziere * 0.50

    def __add__(self, other):
        if isinstance(other, Carte):
            return self._numar_pagini + other._numar_pagini
        return NotImplemented


class Revista(Publicatie):
    def __init__(self, isbn, titlu, autor, an_publicare, gen, numar_editie, luna):
        super().__init__(isbn, titlu, autor, an_publicare, gen)
        self._numar_editie = numar_editie
        self._luna = luna

    def get_tip(self):
        return "Revista"

    def calculeaza_penalizare(self, zile_intarziere):
        return zile_intarziere * 0.25


@dataclass
class Imprumut:
    publicatie: Publicatie
    cititor: str
    data_imprumut: datetime = field(default_factory=datetime.now)
    data_scadenta: datetime = None
    data_returnare: datetime = None
    _activ: bool = True

    def __post_init__(self):
        if self.data_scadenta is None:
            self.data_scadenta = self.data_imprumut + timedelta(days=14)

    def zile_intarziere(self):
        if self.data_returnare:
            diff = self.data_returnare - self.data_scadenta
        else:
            diff = datetime.now() - self.data_scadenta
        return max(0, diff)

    def penalizare(self):
        zile = self.zile_intarziere()
        return self.publicatie.calculeaza_penalizare(zile)

    @property
    def activ(self):
        return self._activ

    def returneaza(self):
        self.data_returnare = datetime.now()
        self._activ = False


class Biblioteca:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, nume):
        self.nume = nume
        self._publicatii = {}
        self._imprumuturi = []
        self._cititori = set()

    def adauga_publicatie(self, publicatie):
        self._publicatii[publicatie.isbn] = publicatie

    def inregistreaza_cititor(self, nume):
        self._cititori.add(nume)

    def imprumuta(self, isbn, cititor):
        if cititor not in self._cititori:
            raise ValueError(f"Cititorul '{cititor}' nu este inregistrat!")

        publicatie = self._publicatii.get(isbn)
        if publicatie is None:
            raise ValueError(f"Publicatia cu ISBN '{isbn}' nu exista!")

        if publicatie.exemplare_disponibile() <= 0:
            raise ValueError("Nu exista exemplare disponibile!")

        for i, stare in enumerate(publicatie._exemplare):
            if stare == StareExemplar.DISPONIBIL:
                publicatie._exemplare[i] = StareExemplar.IMPRUMUTAT
                break

        imprumut = Imprumut(publicatie, cititor)
        self._imprumuturi.append(imprumut)
        return imprumut

    def returneaza(self, isbn, cititor):
        for imp in self._imprumuturi:
            if imp.publicatie.isbn == isbn and imp.cititor == cititor and imp.activ:
                imp.returneaza()
                for i, stare in enumerate(imp.publicatie._exemplare):
                    if stare == StareExemplar.IMPRUMUTAT:
                        imp.publicatie._exemplare[i] = StareExemplar.DISPONIBIL
                        break
                return imp.penalizare()
        raise ValueError("Imprumutul nu a fost gasit!")

    def publicatii_gen(self, gen):
        return [p for p in self._publicatii.values() if p._gen == gen]

    def __iter__(self):
        return BibliotecaIterator(self._publicatii)

    def __contains__(self, isbn):
        return isbn in self._publicatii

    def __len__(self):
        return len(self._publicatii)

    def __getitem__(self, isbn):
        return self._publicatii[isbn]


class BibliotecaIterator:
    def __init__(self, publicatii):
        self._publicatii = list(publicatii.values())
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._publicatii):
            result = self._publicatii[self._index]
            self._index += 1
            return result
        raise StopIteration


bib1 = Biblioteca("Biblioteca Centrala")
bib2 = Biblioteca("Biblioteca Filiala")

a1 = Autor("Eminescu", "Mihai", "Romana")
a2 = Autor("Eliade", "Mircea", "Romana")
a3 = Autor("Eminescu", "Mihai", "Romana")
print(f"Autori egali: {a1 == a3}")
print(f"Carti a1: {a1.carti_publicate}, Carti a3: {a3.carti_publicate}")
a1.carti_publicate.append("Poezii")
print(f"Dupa append - Carti a1: {a1.carti_publicate}, Carti a3: {a3.carti_publicate}")

c1 = Carte("978-1", "Poezii", a1, 1883, GenLiterar.POEZIE, 200)
c2 = Carte("978-2", "Nuvele", a2, 1935, GenLiterar.FICTIUNE, 350)
r1 = Revista("978-3", "Science Monthly", a2, 2024, GenLiterar.STIINTIFIC, 42, "Ianuarie")

c1.adauga_exemplar()
c1.adauga_exemplar()
c2.adauga_exemplar()
r1.adauga_exemplar()

bib1.adauga_publicatie(c1)
bib1.adauga_publicatie(c2)
bib1.adauga_publicatie(r1)

bib1.inregistreaza_cititor("Popescu Ion")
imp = bib1.imprumuta("978-1", "Popescu Ion")
print(f"Exemplare disponibile c1: {c1.exemplare_disponibile()}")
print(f"Zile intarziere: {imp.zile_intarziere()}")

pen = bib1.returneaza("978-1", "Popescu Ion")
print(f"Penalizare: {pen} RON")

print(f"Carti gen POEZIE: {bib1.publicatii_gen(GenLiterar.POEZIE)}")
print(f"Pagini c1 + c2: {c1 + c2}")

for pub in sorted(bib1):
    print(pub)

by_isbn = Carte.get_by_isbn("978-1")
print(f"Gasit by ISBN: {by_isbn}")

"""

# Ex3 refacut de la 0, cu comentarii la fiecare linie, in stil "GRESIT/CORECT"
from abc import ABC, abstractmethod, ABCMeta      # import pentru clase abstracte + metaclasa corecta (ABCMeta)
from dataclasses import dataclass, field          # import pentru dataclass + field (liste default corecte)
from enum import Enum, auto                       # import pentru Enum + auto (valori automate)
from datetime import datetime, timedelta          # import pentru timp (imprumut, scadenta, intarziere)


class GenLiterar(Enum):                            # enum: set de valori fixe pentru gen literar
    FICTIUNE = auto()                              # valoare automata
    NON_FICTIUNE = auto()                          # valoare automata
    STIINTIFIC = auto()                            # valoare automata
    TEHNIC = auto()                                # valoare automata
    POEZIE = auto()                                # valoare automata


class StareExemplar(Enum):                         # enum: starea unui exemplar (o bucata fizica)
    DISPONIBIL = "disponibil"                      # poate fi imprumutat
    IMPRUMUTAT = "imprumutat"                      # este deja luat
    DETERIORAT = "deteriorat"                      # nu se mai poate da
    PIERDUT = "pierdut"                            # nu mai exista


@dataclass                                         # dataclass: face automat __init__ + repr
class Autor:                                       # clasa pentru autor
    nume: str                                      # nume (ex: Eminescu)
    prenume: str                                   # prenume (ex: Mihai)
    nationalitate: str = "Necunoscuta"             # default daca nu trimitem nimic
    # GRESIT: carti_publicate: list = []  (lista se imparte intre toate obiectele)
    carti_publicate: list = field(default_factory=list)  # CORECT: fiecare autor are lista lui

    def nume_complet(self):                        # metoda pentru numele complet
        return f"{self.prenume} {self.nume}"       # returnam prenume + nume

    def __hash__(self):                            # ca sa poata intra in set/dict
        return hash((self.nume, self.prenume))     # hash stabil pe tuple

    def __eq__(self, other):                       # comparatie intre autori
        if isinstance(other, Autor):               # verificam tipul
            return self.nume == other.nume and self.prenume == other.prenume  # comparatie
        return NotImplemented                      # altfel, nu stim compara


# GRESIT (in varianta ta): class PublicatieMeta(type):  -> conflict cu ABCMeta (ABC are ABCMeta)
class PublicatieMeta(ABCMeta):                     # CORECT: metaclasa compatibila cu ABC (nu mai apare metaclass conflict)
    _registru = {}                                 # registru: isbn -> instanta (Carte/Revista)

    def __call__(cls, *args, **kwargs):            # se apeleaza cand faci Carte(...), Revista(...)
        instance = super().__call__(*args, **kwargs)  # cream instanta normal (apeleaza __init__)
        isbn = args[0] if args else kwargs.get("isbn")  # luam isbn: primul argument sau din kwargs
        if isbn:                                   # daca exista isbn
            cls._registru[isbn] = instance         # salvam instanta in registru
        return instance                            # returnam instanta

    def get_by_isbn(cls, isbn):                    # metoda de cautare in registru
        return cls._registru.get(isbn)             # returnam instanta sau None


class Publicatie(ABC, metaclass=PublicatieMeta):   # clasa abstracta + metaclasa pentru registru ISBN
    def __init__(self, isbn, titlu, autor, an_publicare, gen):  # constructor publicatie
        self._isbn = isbn                          # salvam isbn
        self._titlu = titlu                        # salvam titlu
        self._autor = autor                        # salvam autor (obiect Autor)
        self._an_publicare = an_publicare          # salvam anul
        self._gen = gen                            # salvam genul (GenLiterar)
        self._exemplare = []                       # lista de stari (StareExemplar)

    @property                                     # property: accesam cu publicatie.isbn
    def isbn(self):                               # getter isbn
        return self._isbn                         # returnam isbn

    @property                                     # property: accesam cu publicatie.titlu
    def titlu(self):                              # getter titlu
        return self._titlu                        # returnam titlu

    @abstractmethod                               # obligatoriu pentru copil (Carte/Revista)
    def get_tip(self):                            # returneaza "Carte" sau "Revista"
        pass                                      # implementat in copil

    @abstractmethod                               # obligatoriu pentru copil
    def calculeaza_penalizare(self, zile_intarziere):  # penalizare in functie de zile
        pass                                      # implementat in copil

    def adauga_exemplar(self, stare=StareExemplar.DISPONIBIL):  # adaugam un exemplar
        self._exemplare.append(stare)             # adaugam starea in lista

    def exemplare_disponibile(self):              # cate sunt disponibile
        # GRESIT: e == "disponibil" (string), dar noi stocam Enum (StareExemplar.DISPONIBIL)
        return sum(1 for e in self._exemplare if e == StareExemplar.DISPONIBIL)  # CORECT: comparam Enum

    def __eq__(self, other):                      # egalitate publicatii
        if isinstance(other, Publicatie):         # verificam tipul
            return self._isbn == other._isbn      # egale daca isbn e egal
        return NotImplemented

    def __hash__(self):                           # hash publicatie
        return hash(self._isbn)                   # hash dupa isbn

    def __lt__(self, other):                      # sortare (sorted)
        if isinstance(other, Publicatie):         # verificam tipul
            return self._titlu < other._titlu     # sortam dupa titlu
        return NotImplemented

    def __str__(self):                            # ce se afiseaza la print
        return f"{self.get_tip()}: '{self._titlu}' de {self._autor.nume_complet()} ({self._an_publicare})"

    def __repr__(self):                           # reprezentare utila in debug
        return f"{self.__class__.__name__}(isbn='{self._isbn}', titlu='{self._titlu}')"  # string clar


class Carte(Publicatie):                          # Carte mosteneste Publicatie
    def __init__(self, isbn, titlu, autor, an_publicare, gen, numar_pagini):  # constructor carte
        super().__init__(isbn, titlu, autor, an_publicare, gen)               # apelam constructorul parinte
        self._numar_pagini = numar_pagini           # salvam paginile

    def get_tip(self):                             # implementare tip
        return "Carte"                             # returnam tipul

    def calculeaza_penalizare(self, zile_intarziere):  # penalizare carte
        return zile_intarziere * 0.50              # 0.50 RON/zi

    def __add__(self, other):                      # permite c1 + c2
        if isinstance(other, Carte):               # verificam tipul
            return self._numar_pagini + other._numar_pagini  # suma paginilor
        return NotImplemented


class Revista(Publicatie):                        # Revista mosteneste Publicatie
    def __init__(self, isbn, titlu, autor, an_publicare, gen, numar_editie, luna):  # constructor revista
        super().__init__(isbn, titlu, autor, an_publicare, gen)                     # apelam parintele
        self._numar_editie = numar_editie        # salvam editia
        self._luna = luna                        # salvam luna

    def get_tip(self):                            # implementare tip
        return "Revista"                          # returnam tipul

    def calculeaza_penalizare(self, zile_intarziere):  # penalizare revista
        return zile_intarziere * 0.25             # 0.25 RON/zi


@dataclass                                       # dataclass: simplu pentru date
class Imprumut:                                  # clasa pentru imprumut
    publicatie: Publicatie                       # publicatia imprumutata
    cititor: str                                 # numele cititorului
    data_imprumut: datetime = field(default_factory=datetime.now)  # data imprumut (acum)
    data_scadenta: datetime = None               # scadenta (se calculeaza)
    data_returnare: datetime = None              # data returnarii (cand se returneaza)
    _activ: bool = True                          # daca imprumutul e activ

    def __post_init__(self):                     # ruleaza dupa __init__ facut de dataclass
        if self.data_scadenta is None:           # daca nu avem scadenta
            self.data_scadenta = self.data_imprumut + timedelta(days=14)  # 14 zile default

    def zile_intarziere(self):                   # cate zile intarziere sunt
        if self.data_returnare:                  # daca a fost returnat
            diff = self.data_returnare - self.data_scadenta  # calcul diferenta
        else:                                    # daca nu a fost returnat
            diff = datetime.now() - self.data_scadenta       # diferenta fata de acum

        # GRESIT: return max(0, diff)  (diff e timedelta, nu int)
        return max(0, diff.days)                 # CORECT: folosim .days (int)

    def penalizare(self):                        # calculeaza penalizarea
        zile = self.zile_intarziere()            # luam zilele (int)
        return self.publicatie.calculeaza_penalizare(zile)  # trimitem zilele la publicatie

    @property                                    # property: imp.activ
    def activ(self):                             # getter activ
        return self._activ                       # returnam True/False

    def returneaza(self):                        # actiunea de returnare
        self.data_returnare = datetime.now()     # setam data returnarii
        self._activ = False                      # imprumutul devine inactiv


class Biblioteca:                                # clasa Biblioteca (singleton simplu)
    _instance = None                             # variabila de clasa (tine instanta unica)

    def __new__(cls, *args, **kwargs):           # controleaza crearea instantei
        if cls._instance is None:                # daca nu exista instanta
            cls._instance = super().__new__(cls) # o cream
            cls._instance._initialized = False   # CORECT: ca sa nu re-initializam datele
        return cls._instance                      # returnam aceeasi instanta mereu

    def __init__(self, nume):                    # constructor
        if self._initialized:                    # daca deja initializat
            return                               # iesim, altfel resetam tot
        self.nume = nume                         # nume biblioteca
        self._publicatii = {}                    # isbn -> publicatie
        self._imprumuturi = []                   # lista imprumuturi
        self._cititori = set()                   # set cititori
        self._initialized = True                 # marcam initializat

    def adauga_publicatie(self, publicatie):     # adaugare publicatie
        self._publicatii[publicatie.isbn] = publicatie  # punem in dict dupa isbn

    def inregistreaza_cititor(self, nume):       # inregistrare cititor
        self._cititori.add(nume)                 # adaugam in set

    def imprumuta(self, isbn, cititor):          # imprumutare
        if cititor not in self._cititori:        # verificare cititor
            raise ValueError(f"Cititorul '{cititor}' nu este inregistrat!")  # eroare

        publicatie = self._publicatii.get(isbn)  # cautam publicatia
        if publicatie is None:                   # daca nu exista
            raise ValueError(f"Publicatia cu ISBN '{isbn}' nu exista!")      # eroare

        if publicatie.exemplare_disponibile() <= 0:  # daca nu sunt disponibile
            raise ValueError("Nu exista exemplare disponibile!")            # eroare

        for i, stare in enumerate(publicatie._exemplare):  # cautam un exemplar disponibil
            if stare == StareExemplar.DISPONIBIL:          # daca e disponibil
                publicatie._exemplare[i] = StareExemplar.IMPRUMUTAT  # il marcam imprumutat
                break                                      # iesim

        imprumut = Imprumut(publicatie, cititor)           # cream imprumutul
        self._imprumuturi.append(imprumut)                 # il salvam
        return imprumut                                    # returnam imprumutul

    def returneaza(self, isbn, cititor):                   # returnare
        for imp in self._imprumuturi:                      # cautam imprumutul
            if imp.publicatie.isbn == isbn and imp.cititor == cititor and imp.activ:  # verificam
                imp.returneaza()                           # setam returnat
                for i, stare in enumerate(imp.publicatie._exemplare):  # cautam exemplar imprumutat
                    if stare == StareExemplar.IMPRUMUTAT:  # daca e imprumutat
                        imp.publicatie._exemplare[i] = StareExemplar.DISPONIBIL  # facem disponibil
                        break                              # iesim
                return imp.penalizare()                    # returnam penalizarea
        raise ValueError("Imprumutul nu a fost gasit!")     # daca nu gasim

    def publicatii_gen(self, gen):                         # filtrare dupa gen
        return [p for p in self._publicatii.values() if p._gen == gen]  # returnam lista filtrata

    def __iter__(self):                                    # iterare biblioteca
        return BibliotecaIterator(self._publicatii)        # returnam iterator custom

    def __contains__(self, isbn):                          # "isbn in biblioteca"
        return isbn in self._publicatii                    # verificam in dict

    def __len__(self):                                     # len(biblioteca)
        return len(self._publicatii)                       # cate publicatii avem

    def __getitem__(self, isbn):                           # biblioteca["978-1"]
        return self._publicatii[isbn]                      # returnam publicatia


class BibliotecaIterator:                                  # iterator custom
    def __init__(self, publicatii):                        # constructor iterator
        self._publicatii = list(publicatii.values())       # facem lista din valori
        self._index = 0                                    # index pornire

    def __iter__(self):                                    # iter(self)
        return self                                       # returnam iteratorul

    def __next__(self):                                    # urmatorul element
        if self._index < len(self._publicatii):            # daca mai sunt elemente
            result = self._publicatii[self._index]         # luam elementul curent
            self._index += 1                               # avansam
            return result                                  # returnam elementul
        raise StopIteration                                 # terminam


# TESTARE
bib1 = Biblioteca("Biblioteca Centrala")                   # cream biblioteca (instanta unica)
bib2 = Biblioteca("Biblioteca Filiala")                    # tot aceeasi instanta (nu reseteaza acum)

a1 = Autor("Eminescu", "Mihai", "Romana")                  # autor 1
a2 = Autor("Eliade", "Mircea", "Romana")                   # autor 2
a3 = Autor("Eminescu", "Mihai", "Romana")                  # autor 3 (identic cu a1)

print(f"Autori egali: {a1 == a3}")                         # test egalitate
print(f"Carti a1: {a1.carti_publicate}, Carti a3: {a3.carti_publicate}")  # test lista separata
a1.carti_publicate.append("Poezii")                        # adaugam la a1
print(f"Dupa append - Carti a1: {a1.carti_publicate}, Carti a3: {a3.carti_publicate}")  # a3 nu se schimba

c1 = Carte("978-1", "Poezii", a1, 1883, GenLiterar.POEZIE, 200)          # carte 1
c2 = Carte("978-2", "Nuvele", a2, 1935, GenLiterar.FICTIUNE, 350)        # carte 2
r1 = Revista("978-3", "Science Monthly", a2, 2024, GenLiterar.STIINTIFIC, 42, "Ianuarie")  # revista 1

c1.adauga_exemplar()                                     # exemplar disponibil
c1.adauga_exemplar()                                     # exemplar disponibil
c2.adauga_exemplar()                                     # exemplar disponibil
r1.adauga_exemplar()                                     # exemplar disponibil

bib1.adauga_publicatie(c1)                               # adaugam c1
bib1.adauga_publicatie(c2)                               # adaugam c2
bib1.adauga_publicatie(r1)                               # adaugam r1

bib1.inregistreaza_cititor("Popescu Ion")                # inregistram cititor
imp = bib1.imprumuta("978-1", "Popescu Ion")              # imprumutam c1

print(f"Exemplare disponibile c1: {c1.exemplare_disponibile()}")  # ar trebui 1
print(f"Zile intarziere: {imp.zile_intarziere()}")        # ar trebui 0

pen = bib1.returneaza("978-1", "Popescu Ion")             # returnam
print(f"Penalizare: {pen} RON")                           # probabil 0

print(f"Carti gen POEZIE: {bib1.publicatii_gen(GenLiterar.POEZIE)}")  # filtrare gen
print(f"Pagini c1 + c2: {c1 + c2}")                       # suma pagini

for pub in sorted(bib1):                                 # sortare dupa titlu
    print(pub)                                           # afisare

by_isbn = Carte.get_by_isbn("978-1")                      # cautare in registru metaclasa
print(f"Gasit by ISBN: {by_isbn}")                        # afisare rezultat
