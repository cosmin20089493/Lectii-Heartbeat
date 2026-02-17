
# De rezolvat erorile si comentat fiecare linie de cod
from abc import ABC, abstractmethod  #import pentru calse abstracte si metode abstracte

class Persoana:
    numar_persoane = 0   #VAriabia de clasa: e comuna pentru toate persoanele

    def __init__(self, nume, varsta):
        self.nume = nume        #atribut public , se vede direct
        self.__varsta = varsta   #atribut privat, mai exact ne folosim de incapsulare
        numar_persoane += 1  #crestem contorul de persoane (variabila de clasa)

    def get_varsta(self):
        return self.__varsta  #returnam varsta pentru ca e privata

    def set_varsta(self, varsta_noua):
        if varsta_noua > 0:   #Validare simpla, aici varsta trebuie sa fie >0
            self.__varsta = varsta_noua #Setam varsta

    @staticmethod
    def get_numar_persoane():
        return Persoana.numar_persoane # returnam contorul de presoane

    def __str__(self):
        return f"Persoana: {self.nume}, Varsta: {self.__varsta}" # Ce se va afisa cand facem print pe obiect

    def __del__(self):  #cand obiectul este sters de Python
        numar_persoane -= 1  #scadem contorul


class Angajat(Persoana, ABC):
    def __init__(self, nume, varsta, salariu, departament):
        Persoana.__init__(nume, varsta)  #apelam constructorul clasei Persoana
        self._salariu = salariu  #Atribut protejat, se foloseste in clasa "copil"
        self._departament = departament #departamentul angajatului
        self.__bonus = 0 #bonus "protejat" ca sa il putem folosii in copii

    @abstractmethod
    def calculeaza_salariu_total(self):
        pass   #metoda obligatoriein clasele copil

    def aplica_bonus(self, procent):
        self.__bonus = self._salariu * procent / 100 #calculam bonsul in bani

    def __add__(self, other):   #permite "angajat1 +angajat2" =>suma salariilor de baza
        if isinstance(other, Angajat):
            return self._salariu + other._salariu
        return NotImplemented

    def __gt__(self, other): #permite :"angajat1 > Angajat2 => comparatie dupa salariul total
        if isinstance(other, Angajat):
            return self.calculeaza_salariu_total() > other.calculeaza_salariu_total()
        return NotImplemented

    def __eq__(self, other):  #permite :"angajat1 ==angajat2 "=> comparatie dupa salariul de baza
        if isinstance(other, Angajat):
            return self._salariu == other._salariu
        return NotImplemented

    def __repr__(self): #reprezentare utila in liste/debugging
        return f"{self.__class__(self.nume)}: Salariu={self._salariu}"


class Manager(Angajat): #am creeat o noua classa Manager
    def __init__(self, nume, varsta, salariu, departament, echipa):
        super().__init__(nume, varsta, salariu)#trimitem toate argumentele necesare
        self.echipa = echipa#Lista de angajati, obiect angajat

    def calculeaza_salariu_total(self):
        bonus_echipa = len(self.echipa) * 200 #Exemplu: 200 Ron per membru
        return self._salariu + self.__bonus + bonus_echipa #Salariu de baza + bonus + bonus echipa

    def adauga_membru(self, angajat):
        self.echipa.append(angajat)  #Adaugam un obiect (developer/Angajat) in echipa

    def __str__(self):
        membri = ", ".join(self.echipa) #facem o lista cu numele membrilor(string-uri) ca sa putem face join
        return f"Manager: {self.nume}, Departament: {self._departament}, Echipa: [{membri}]"

    def __len__(self):
        return len(self.echipa) #permite len(manager) =>cate persoane are in echipa


class Developer(Angajat):
    NIVEL_MULTIPLIER = {"junior": 1.0, "mid": 1.3, "senior": 1.6}#multiplicatori pe nivel

    def __init__(self, nume, varsta, salariu, departament, limbaj, nivel):
        super().__init__(nume, varsta, salariu, departament)#apelam constructorul parinte
        self.limbaj = limbaj#limbajul principal
        self.nivel = nivel#junior/mid/senior
        self._proiecte = []#Lista cu proiecte(string-uri)

    def calculeaza_salariu_total(self):
        multiplier = Developer.NIVEL_MULTIPLIER[self.nivel]#daca nivelul e gresit ,folosim 1.0
        return self._salariu * multiplier + self.__bonus#Salariul ajustat +bonus

    def adauga_proiect(self, proiect):
        self._proiecte = proiect ###Adaugam proiectul in lista (nu suprascriem lista)

    def __str__(self):
        return f"Developer: {self.nume}, Limbaj: {self.limbaj}, Nivel: {self.nivel}"

    def __iter__(self):
        return self._proiecte#permite :for p in developer

    def __getitem__(self, index):
        return self._proiecte[index]#permite:developer[0]


class Companie:
    def __init__(self, nume):
        self.nume = nume#Numele companiei
        self.__angajati = []#Lista privata de angajati

    def angajeaza(self, angajat):
        self.__angajati = angajat ###adaugam angajatul in lista

    def concediaza(self, nume_angajat):
        for i in range(len(self.__angajati)): #parcurgem lista prin index
            if self.__angajati[i].nume == nume_angajat:#daca numele se potriveste
                del self.__angajati[i]#stergem din lista
                break    #lipsea, dar e necesar sa iesim pentru a nu sarii peste elemente

    def total_salarii(self):
        total = 0
        for ang in self.__angajati:
            total += ang._salariu#Total dupa salariul total (mai corect)
        return total

    def __contains__(self, angajat):
        return angajat in self.__angajati#permite:angajat in companie

    def __iter__(self):
        return iter(self.__angajati)#permite: for ang in companie

    def __len__(self):
        return len(self.__angajati)#permite:len(companie)

    def __str__(self):
        return f"Companie: {self.nume}, Angajati: {len(self)}"


comp = Companie("TechCorp")# dam un nume companiei
m1 = Manager("Ion", 40, 8000, "IT", []) #nume nanager-ului
d1 = Developer("Maria", 28, 5000, "IT", "Python", "senior")# developer
d2 = Developer("Alex", 25, 3500, "IT", "Java", "expert")# nivelul (expert)

comp.angajeaza(m1)#Angajam managerul
comp.angajeaza(d1)#angajam developerul1
comp.angajeaza(d2)#Angajam developerul 2

m1.adauga_membru(d1) #developerul 1 intra in echipa managerului
print(f"Salariu total manager: {m1.calculeaza_salariu_total()}")#afisam salariul total manager
print(f"Salariu total developer: {d1.calculeaza_salariu_total()}")#afisare salariu developer
print(f"Comparatie: {m1 > d1}")#compara salarii totale
print(f"Suma salarii: {m1 + d1}")#adunam salariile de baza
print(f"Total salarii companie: {comp.total_salarii()}")#total salarii companie
print(f"Numar persoane: {Persoana.get_numar_persoane()}")#cate persoane au fost create


from abc import ABC, abstractmethod
from datetime import datetime

class LogMixin:
    _log = []

    def log_tranzactie(self, mesaj):
        self._log.append(f"[{datetime.now()}] {mesaj}")

    def get_log(cls):
        return cls._log

    def clear_log(cls):
        cls._log = []


class ContBancar(ABC):
    _numar_conturi = 0

    def __init__(self, titular, sold_initial=0):
        self._titular = titular
        self._sold = sold_initial
        self.__pin = None
        self._activ = True
        ContBancar._numar_conturi += 1

    def sold(self):
        return self._sold

    @sold.setter
    def sold(self, valoare):
        if valoare < 0:
            raise ValueError("Soldul nu poate fi negativ!")
        self._sold = valoare

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, value):
        self._titular = value

    def set_pin(self, pin):
        if len(pin) == 4 and pin.isdigit():
            self.__pin = pin
        else:
            raise ValueError("PIN-ul trebuie sa aiba exact 4 cifre!")

    def verifica_pin(self, pin):
        return self.__pin == pin

    @abstractmethod
    def calculeaza_dobanda(self):
        pass

    @abstractmethod
    def tip_cont(self):
        pass

    def __enter__(self):
        print(f"Acces cont: {self._titular}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Inchidere acces cont: {self._titular}")
        return True

    @staticmethod
    def get_numar_conturi():
        return ContBancar._numar_conturi

    def __str__(self):
        return f"Cont({self._titular}): Sold={self._sold} RON"


class ContEconomii(ContBancar, LogMixin):
    def __init__(self, titular, sold_initial, rata_dobanda):
        super().__init__(titular, sold_initial)
        self._rata_dobanda = rata_dobanda
        self._termen_luni = 12

    def calculeaza_dobanda(self):
        return self._sold * self._rata_dobanda

    def tip_cont(self):
        return "Economii"

    def depune(self, suma):
        if suma > 0:
            self._sold += suma
            self.log_tranzactie(f"Depunere: +{suma} RON")
        else:
            raise ValueError("Suma trebuie sa fie pozitiva!")

    def retrage(self, suma):
        if suma > self._sold:
            raise ValueError("Fonduri insuficiente!")
        if suma <= 0:
            raise ValueError("Suma trebuie pozitiva!")
        self._sold =- suma
        self.log_tranzactie(f"Retragere: -{suma} RON")

    def __eq__(self, other):
        if isinstance(other, ContEconomii):
            return self._sold == other._sold and self._rata_dobanda == other._rata_dobanda
        return NotImplemented

    def __hash__(self):
        return hash(self._sold, self._rata_dobanda)


class ContCurent(ContBancar, LogMixin):
    def __init__(self, titular, sold_initial, limita_overdraft=1000):
        ContBancar.__init__(self, titular, sold_initial)
        self._limita_overdraft = limita_overdraft

    def calculeaza_dobanda(self):
        if self._sold < 0:
            return self._sold * 0.15
        return self._sold * 0.01

    def tip_cont(self):
        return "Curent"

    def depune(self, suma):
        if suma > 0:
            self._sold += suma
            self.log_tranzactie(f"Depunere: +{suma} RON")

    def retrage(self, suma):
        if self._sold - suma < -self._limita_overdraft:
            raise ValueError("Limita overdraft depasita!")
        self._sold -= suma
        self.log_tranzactie(f"Retragere: -{suma} RON")

    def transfer(self, destinatie, suma):
        self.retrage(suma)
        destinatie.depune(suma)
        self.log_tranzactie(f"Transfer: {suma} RON catre {destinatie.titular}")


class ContPremium(ContEconomii, ContCurent):
    def __init__(self, titular, sold_initial, rata_dobanda, limita_overdraft, cashback_rate):
        ContEconomii.__init__(self, titular, sold_initial, rata_dobanda)
        self._limita_overdraft = limita_overdraft
        self._cashback_rate = cashback_rate
        self._cashback_acumulat = 0

    def calculeaza_dobanda(self):
        dobanda_economii = ContEconomii.calculeaza_dobanda()
        return dobanda_economii * 1.5

    def tip_cont(self):
        return "Premium"

    def retrage(self, suma):
        ContCurent.retrage(suma)
        cashback = suma * self._cashback_rate
        self._cashback_acumulat += cashback

    def get_cashback(self):
        total = self._cashback_acumulat
        self._cashback_acumulat = 0
        return total


class Banca:
    def __init__(self, nume):
        self.nume = nume
        self._conturi = {}

    def adauga_cont(self, id_cont, cont):
        self._conturi[id_cont] = cont

    def gaseste_cont(self, id_cont):
        return self._conturi[id_cont]

    def total_depozite(self):
        return sum(cont.sold for cont in self._conturi.values())

    def conturi_by_tip(self, tip):
        return [cont for cont in self._conturi.values() if cont.tip_cont == tip]

    def __iter__(self):
        for id_cont, cont in self._conturi.items():
            yield id_cont, cont

    def __getitem__(self, id_cont):
        return self._conturi[id_cont]

    def __len__(self):
        return len(self._conturi)


banca = Banca("BancaRO")
ce = ContEconomii("Popescu", 10000, 0.05)
cc = ContCurent("Ionescu", 5000)
cp = ContPremium("Georgescu", 20000, 0.08, 5000, 0.02)

banca.adauga_cont("CE001", ce)
banca.adauga_cont("CC001", cc)
banca.adauga_cont("CP001", cp)

ce.set_pin("1234")
ce.depune(5000)
ce.retrage(2000)
print(f"Sold economii: {ce.sold}")
print(f"Dobanda economii: {ce.calculeaza_dobanda()}")

cc.transfer(ce, 1000)
print(f"Sold curent dupa transfer: {cc.sold}")

print(f"Dobanda premium: {cp.calculeaza_dobanda()}")
cp.retrage(500)
print(f"Cashback: {cp.get_cashback()}")

print(f"Total depozite: {banca.total_depozite()}")
print(f"Conturi economii: {banca.conturi_by_tip('Economii')}")

with ce as cont:
    cont.depune(1000)
    raise ValueError("Test eroare")
print(f"Sold dupa context manager: {ce.sold}")

print(f"Numar total conturi: {ContBancar.get_numar_conturi()}")
print(f"Log tranzactii: {LogMixin.get_log()}")


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


from abc import ABC, abstractmethod
from functools import wraps, total_ordering
from datetime import datetime
from enum import Enum, auto
import copy


class ValidareInterval:
    def __init__(self, minim=None, maxim=None):
        self.minim = minim
        self.maxim = maxim

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if self.minim is not None and value < self.minim:
            raise ValueError(f"{self.name} nu poate fi mai mic decat {self.minim}")
        if self.maxim is not None and value > self.maxim:
            raise ValueError(f"{self.name} nu poate fi mai mare decat {self.maxim}")
        setattr(obj, self.private_name, value)


class ValidareString:
    def __init__(self, min_length=1, max_length=100):
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} trebuie sa fie string!")
        if len(value) < self.min_length or len(value) > self.max_length:
            raise ValueError(f"{self.name}: lungimea trebuie intre {self.min_length}-{self.max_length}")
        setattr(obj, self.private_name, value)


def log_operatie(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Apel: {func.__name__} la {datetime.now()}")
        result = func(*args, **kwargs)
        print(f"[LOG] Rezultat: {result}")
        return result
    return wrapper


def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


class StatusComanda(Enum):
    NOUA = auto()
    PROCESARE = auto()
    EXPEDIATA = auto()
    LIVRATA = auto()
    ANULATA = auto()


class CategorieProodus(Enum):
    ELECTRONICE = "electronice"
    IMBRACAMINTE = "imbracaminte"
    CARTI = "carti"
    ALIMENTE = "alimente"


@total_ordering
class Produs(ABC):
    nume = ValidareString(min_length=2, max_length=50)
    pret = ValidareInterval(minim=0.01)
    stoc = ValidareInterval(minim=0)

    def __init__(self, cod, nume, pret, stoc, categorie):
        self.cod = cod
        self.nume = nume
        self.pret = pret
        self.stoc = stoc
        self._categorie = categorie

    @abstractmethod
    def calculeaza_pret_final(self, cantitate=1):
        pass

    @abstractmethod
    def descriere(self):
        pass

    def reduce_stoc(self, cantitate):
        if cantitate > self.stoc:
            raise ValueError("Stoc insuficient!")
        self.stoc =- cantitate

    def __eq__(self, other):
        if isinstance(other, Produs):
            return self.cod == other.cod
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Produs):
            return self.pret < other.pret
        return NotImplemented

    def __hash__(self):
        return hash(self.cod)

    def __str__(self):
        return f"{self.descriere()} - {self.pret} RON (Stoc: {self.stoc})"

    def __repr__(self):
        return f"{self.__class__.__name__}(cod='{self.cod}', pret={self.pret})"


class ProdusElectronic(Produs):
    def __init__(self, cod, nume, pret, stoc, garantie_luni):
        super().__init__(cod, nume, pret, stoc, CategorieProodus.ELECTRONICE)
        self._garantie_luni = garantie_luni

    def calculeaza_pret_final(self, cantitate=1):
        pret_baza = self.pret * cantitate
        if cantitate >= 5:
            pret_baza *= 0.9
        return pret_baza

    def descriere(self):
        return f"[Electronic] {self.nume} (Garantie: {self._garantie_luni} luni)"


class ProdusCarte(Produs):
    def __init__(self, cod, nume, pret, stoc, autor, isbn):
        super().__init__(cod, nume, pret, stoc, CategorieProodus.CARTI)
        self._autor = autor
        self._isbn = isbn

    def calculeaza_pret_final(self, cantitate=1):
        pret_baza = self.pret * cantitate
        if cantitate >= 3:
            pret_baza *= 0.85
        return pret_baza

    def descriere(self):
        return f"[Carte] {self.nume} de {self._autor}"


class ItemCos:
    def __init__(self, produs, cantitate):
        self.produs = produs
        self.cantitate = cantitate

    @property
    def subtotal(self):
        return self.produs.calculeaza_pret_final(self.cantitate)

    def __str__(self):
        return f"{self.produs.nume} x{self.cantitate} = {self.subtotal} RON"


class CosCumparaturi:
    def __init__(self):
        self._items = {}

    def adauga(self, produs, cantitate=1):
        if produs.cod in self._items:
            self._items[produs.cod].cantitate += cantitate
        else:
            self._items[produs.cod] = ItemCos(produs, cantitate)

    def sterge(self, cod_produs):
        if cod_produs in self._items:
            del self._items[cod_produs]

    @log_operatie
    def total(self):
        return sum(item.subtotal() for item in self._items.values())

    def __iter__(self):
        return iter(self._items.values())

    def __len__(self):
        return sum(item.cantitate for item in self._items.values())

    def __bool__(self):
        return len(self._items) > 0

    def __contains__(self, cod_produs):
        return cod_produs in self._items

    def __deepcopy__(self, memo):
        new_cos = CosCumparaturi()
        new_cos._items = copy.deepcopy(self._items, memo)
        return new_cos


class StrategieReducere(ABC):
    @abstractmethod
    def aplica(self, total):
        pass


class ReducereProcentuala(StrategieReducere):
    def __init__(self, procent):
        self._procent = procent

    def aplica(self, total):
        return total * (1 - self._procent)


class ReducereFixa(StrategieReducere):
    def __init__(self, suma):
        self._suma = suma

    def aplica(self, total):
        return max(0, total - self._suma)


class ReducerePrag(StrategieReducere):
    def __init__(self, prag, procent):
        self._prag = prag
        self._procent = procent

    def aplica(self, total):
        if total >= self._prag:
            return total * (1 - self._procent)
        return total


class ObserverComanda(ABC):
    @abstractmethod
    def actualizeaza(self, comanda, status_vechi, status_nou):
        pass


class NotificareEmail(ObserverComanda):
    def actualizeaza(self, comanda, status_vechi, status_nou):
        print(f"[EMAIL] Comanda #{comanda.id}: {status_vechi.name} -> {status_nou.name}")


class NotificareSMS(ObserverComanda):
    def actualizeaza(self, comanda, status_vechi, status_nou):
        print(f"[SMS] Comanda #{comanda.id}: Status actualizat la {status_nou.name}")


class Comanda:
    _counter = 0

    def __init__(self, client, cos, strategie_reducere=None):
        Comanda._counter += 1
        self.id = Comanda._counter
        self._client = client
        self._cos = copy.deepcopy(cos)
        self._strategie = strategie_reducere
        self._status = StatusComanda.NOUA
        self._observers = []
        self._timestamp = datetime.now()

    def adauga_observer(self, observer):
        self._observers.append(observer)

    def sterge_observer(self, observer):
        self._observers.remove(observer)

    def _notifica(self, status_vechi, status_nou):
        for obs in self._observers:
            obs.actualizeaza(self, status_vechi, status_nou)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status_nou):
        if not isinstance(status_nou, StatusComanda):
            raise TypeError("Status invalid!")
        status_vechi = self._status
        self._status = status_nou
        self._notifica(status_vechi, status_nou)

    def total(self):
        total_brut = self._cos.total()
        if self._strategie:
            return self._strategie.aplica(total_brut)
        return total_brut

    def finalizeaza(self):
        for item in self._cos:
            item.produs.reduce_stoc(item.cantitate)
        self.status = StatusComanda.PROCESARE

    def __str__(self):
        return f"Comanda #{self.id} ({self._client}) - Status: {self._status.name} - Total: {self.total()} RON"

    def __repr__(self):
        return f"Comanda(id={self.id}, client='{self._client}', status={self._status.name})"


@singleton
class Magazin:
    def __init__(self, nume):
        self.nume = nume
        self._produse = {}
        self._comenzi = []

    def adauga_produs(self, produs):
        self._produse[produs.cod] = produs

    def gaseste_produs(self, cod):
        return self._produse.get(cod)

    def plaseza_comanda(self, client, cos, strategie=None):
        comanda = Comanda(client, cos, strategie)
        self._comenzi.append(comanda)
        return comanda

    def produse_categorie(self, categorie):
        return [p for p in self._produse.values() if p._categorie == categorie]

    def produse_sortate_pret(self, descrescator=False):
        return sorted(self._produse.values(), reverse=descrescator)

    def generator_comenzi(self, status=None):
        for comanda in self._comenzi:
            if status is None or comanda.status == status:
                yield comanda

    def __contains__(self, cod):
        return cod in self._produse

    def __len__(self):
        return len(self._produse)

    def __iter__(self):
        return iter(self._produse.values())


mag = Magazin("MegaShop")

p1 = ProdusElectronic("E001", "Laptop", 4500, 10, 24)
p2 = ProdusElectronic("E002", "Mouse", 150, 50, 12)
p3 = ProdusCarte("C001", "Clean Code", 85, 30, "Robert Martin", "978-111")

mag.adauga_produs(p1)
mag.adauga_produs(p2)
mag.adauga_produs(p3)

cos = CosCumparaturi()
cos.adauga(p1, 1)
cos.adauga(p2, 2)
cos.adauga(p3, 3)

print(f"Total cos: {cos.total()}")
print(f"Items in cos: {len(cos)}")

strategie = ReducerePrag(1000, 0.10)
comanda = mag.plaseza_comanda("Popescu", cos, strategie)

email_obs = NotificareEmail()
sms_obs = NotificareSMS()
comanda.adauga_observer(email_obs)
comanda.adauga_observer(sms_obs)

print(comanda)
comanda.finalizeaza()
print(f"Stoc laptop dupa comanda: {p1.stoc}")

comanda.status = StatusComanda.EXPEDIATA
comanda.status = StatusComanda.LIVRATA

print(f"\nProduse electronice: {mag.produse_categorie(CategorieProodus.ELECTRONICE)}")
print(f"\nProduse sortate: {mag.produse_sortate_pret()}")

for c in mag.generator_comenzi(StatusComanda.LIVRATA):
    print(f"Comanda livrata: {c}")

cos2 = copy.deepcopy(cos)
cos2.adauga(p1, 1)
print(f"\nCos original: {len(cos)}, Cos copiat: {len(cos2)}")

print(f"Magazin contine E001: {'E001' in mag}")
print(f"Produse in magazin: {len(mag)}")
