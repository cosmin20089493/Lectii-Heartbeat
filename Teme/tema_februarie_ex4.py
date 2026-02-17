"""
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

"""

from abc import ABC, abstractmethod                      # import pentru clase abstracte si metode abstracte
from functools import wraps, total_ordering              # wraps pentru decorator corect, total_ordering pentru comparatii
from datetime import datetime                            # datetime pentru log cu data/ora
from enum import Enum, auto                              # Enum + auto pentru statusuri
import copy                                              # copy pentru deepcopy (copiere cos, fara referinte comune)


class ValidareInterval:                                  # descriptor: valideaza numere intre minim/maxim
    def __init__(self, minim=None, maxim=None):          # constructor descriptor
        self.minim = minim                               # prag minim (sau None)
        self.maxim = maxim                               # prag maxim (sau None)

    def __set_name__(self, owner, name):                 # python apeleaza cand descriptorul e pus pe clasa
        self.name = name                                 # numele campului (ex: "pret")
        self.private_name = f"_{name}"                   # numele real unde tinem valoarea in obiect

    def __get__(self, obj, objtype=None):                # citire valoare (ex: produs.pret)
        if obj is None:                                  # daca accesam pe clasa, nu pe instanta
            return self                                  # returnam descriptorul
        return getattr(obj, self.private_name, None)     # luam valoarea din atributul privat

    def __set__(self, obj, value):                       # setare valoare (ex: produs.pret = 10)
        if self.minim is not None and value < self.minim:  # verificare minim
            raise ValueError(f"{self.name} nu poate fi mai mic decat {self.minim}")  # eroare
        if self.maxim is not None and value > self.maxim:  # verificare maxim
            raise ValueError(f"{self.name} nu poate fi mai mare decat {self.maxim}")  # eroare
        setattr(obj, self.private_name, value)           # setam valoarea in atributul privat


class ValidareString:                                    # descriptor: valideaza string cu lungime minima/maxima
    def __init__(self, min_length=1, max_length=100):    # constructor descriptor
        self.min_length = min_length                     # lungime minima
        self.max_length = max_length                     # lungime maxima

    def __set_name__(self, owner, name):                 # python apeleaza cand descriptorul e pus pe clasa
        self.name = name                                 # numele campului (ex: "nume")
        self.private_name = f"_{name}"                   # numele real unde tinem valoarea in obiect

    def __get__(self, obj, objtype=None):                # citire valoare
        if obj is None:                                  # acces pe clasa
            return self                                  # returnam descriptor
        return getattr(obj, self.private_name, None)     # returnam valoarea

    def __set__(self, obj, value):                       # setare valoare
        if not isinstance(value, str):                   # validare tip
            raise TypeError(f"{self.name} trebuie sa fie string!")  # eroare tip
        if len(value) < self.min_length or len(value) > self.max_length:  # validare lungime
            raise ValueError(f"{self.name}: lungimea trebuie intre {self.min_length}-{self.max_length}")  # eroare
        setattr(obj, self.private_name, value)           # setam valoarea


def log_operatie(func):                                  # decorator: printeaza log cand e apelata o functie
    @wraps(func)                                         # CORECT: pastram numele/descrierea functiei originale
    def wrapper(*args, **kwargs):                         # wrapper primeste orice argumente
        print(f"[LOG] Apel: {func.__name__} la {datetime.now()}")  # log apel cu timestamp
        result = func(*args, **kwargs)                    # apelam functia originala
        print(f"[LOG] Rezultat: {result}")                # log rezultat
        return result                                     # returnam rezultatul mai departe
    return wrapper                                        # returnam wrapper-ul


def singleton(cls):                                      # decorator: transforma clasa in singleton (o singura instanta)
    instances = {}                                       # dict: cls -> instanta
    def get_instance(*args, **kwargs):                   # functie care returneaza instanta unica
        if cls not in instances:                         # daca nu avem instanta creata
            instances[cls] = cls(*args, **kwargs)        # o cream si o salvam
        return instances[cls]                            # returnam instanta existenta
    return get_instance                                   # returnam functia care inlocuieste clasa


class StatusComanda(Enum):                               # enum pentru status comanda
    NOUA = auto()                                        # comanda noua
    PROCESARE = auto()                                   # in procesare
    EXPEDIATA = auto()                                   # expediata
    LIVRATA = auto()                                     # livrata
    ANULATA = auto()                                     # anulata


class CategorieProdus(Enum):                             # GRESIT la tine: CategorieProodus (typo) -> CORECT: CategorieProdus
    ELECTRONICE = "electronice"                          # categorie electronice
    IMBRACAMINTE = "imbracaminte"                        # categorie imbracaminte
    CARTI = "carti"                                      # categorie carti
    ALIMENTE = "alimente"                                # categorie alimente


@total_ordering                                          # daca avem __eq__ + __lt__, python genereaza restul comparatiilor
class Produs(ABC):                                       # clasa abstracta pentru produse
    nume = ValidareString(min_length=2, max_length=50)   # descriptor: nume minim 2 caractere
    pret = ValidareInterval(minim=0.01)                  # descriptor: pret minim 0.01
    stoc = ValidareInterval(minim=0)                     # descriptor: stoc minim 0

    def __init__(self, cod, nume, pret, stoc, categorie):  # constructor produs
        self.cod = cod                                   # cod produs (string)
        self.nume = nume                                 # nume produs (validat de descriptor)
        self.pret = pret                                 # pret produs (validat)
        self.stoc = stoc                                 # stoc produs (validat)
        self._categorie = categorie                       # categorie produs (Enum)

    @abstractmethod                                      # metoda abstracta: fiecare produs calculeaza pret final diferit
    def calculeaza_pret_final(self, cantitate=1):        # pret final pentru o cantitate
        pass                                             # implementat in clase copil

    @abstractmethod                                      # metoda abstracta: descriere produs
    def descriere(self):                                 # descriere pentru afisare
        pass                                             # implementat in clase copil

    def reduce_stoc(self, cantitate):                    # scade stocul dupa o comanda
        if cantitate <= 0:                               # validare cantitate
            raise ValueError("Cantitatea trebuie sa fie pozitiva!")  # eroare
        if cantitate > self.stoc:                        # daca nu avem destul stoc
            raise ValueError("Stoc insuficient!")        # eroare
        # GRESIT la tine: self.stoc =- cantitate (seteaza stocul la -cantitate)
        self.stoc -= cantitate                           # CORECT: scadem cantitatea din stoc

    def __eq__(self, other):                             # egalitate produse
        if isinstance(other, Produs):                    # doar daca other e Produs
            return self.cod == other.cod                 # egale daca au acelasi cod
        return NotImplemented                              # altfel nu comparam

    def __lt__(self, other):                             # comparatie pentru sortare
        if isinstance(other, Produs):                    # doar daca other e Produs
            return self.pret < other.pret                # sortam dupa pret
        return NotImplemented                              # altfel nu comparam

    def __hash__(self):                                  # hash pentru a fi folosit in set/dict
        return hash(self.cod)                            # hash dupa cod

    def __str__(self):                                   # afisare produs
        return f"{self.descriere()} - {self.pret} RON (Stoc: {self.stoc})"  # string clar

    def __repr__(self):                                  # repr pentru debug
        return f"{self.__class__.__name__}(cod='{self.cod}', pret={self.pret})"  # repr scurt


class ProdusElectronic(Produs):                          # produs electronic
    def __init__(self, cod, nume, pret, stoc, garantie_luni):  # constructor electronice
        super().__init__(cod, nume, pret, stoc, CategorieProdus.ELECTRONICE)  # CORECT: folosim enum corect
        self._garantie_luni = garantie_luni              # garantie in luni

    def calculeaza_pret_final(self, cantitate=1):        # pret final electronice
        pret_baza = self.pret * cantitate                # pret baza
        if cantitate >= 5:                               # discount la cantitate mare
            pret_baza *= 0.9                             # 10% reducere
        return pret_baza                                 # returnam pretul

    def descriere(self):                                 # descriere electronice
        return f"[Electronic] {self.nume} (Garantie: {self._garantie_luni} luni)"  # text


class ProdusCarte(Produs):                               # produs carte
    def __init__(self, cod, nume, pret, stoc, autor, isbn):  # constructor carte
        super().__init__(cod, nume, pret, stoc, CategorieProdus.CARTI)  # CORECT: enum corect
        self._autor = autor                               # autor carte
        self._isbn = isbn                                 # isbn carte

    def calculeaza_pret_final(self, cantitate=1):        # pret final carti
        pret_baza = self.pret * cantitate                # pret baza
        if cantitate >= 3:                               # discount la 3+ carti
            pret_baza *= 0.85                            # 15% reducere
        return pret_baza                                 # returnam pretul

    def descriere(self):                                 # descriere carte
        return f"[Carte] {self.nume} de {self._autor}"    # text


class ItemCos:                                           # un element in cos (produs + cantitate)
    def __init__(self, produs, cantitate):               # constructor item
        self.produs = produs                             # produsul
        self.cantitate = cantitate                       # cantitatea

    @property                                            # property: item.subtotal (fara paranteze)
    def subtotal(self):                                  # subtotal = pret final pentru cantitatea itemului
        return self.produs.calculeaza_pret_final(self.cantitate)  # calcul subtotal

    def __str__(self):                                   # afisare item
        return f"{self.produs.nume} x{self.cantitate} = {self.subtotal} RON"  # text


class CosCumparaturi:                                    # cos de cumparaturi
    def __init__(self):                                  # constructor cos
        self._items = {}                                 # dict cod_produs -> ItemCos

    def adauga(self, produs, cantitate=1):               # adauga produs in cos
        if cantitate <= 0:                               # validare cantitate
            raise ValueError("Cantitatea trebuie sa fie pozitiva!")  # eroare
        if produs.cod in self._items:                    # daca produsul exista deja
            self._items[produs.cod].cantitate += cantitate  # crestem cantitatea
        else:                                            # daca nu exista
            self._items[produs.cod] = ItemCos(produs, cantitate)  # adaugam item nou

    def sterge(self, cod_produs):                        # sterge produs din cos dupa cod
        if cod_produs in self._items:                    # daca exista codul
            del self._items[cod_produs]                  # il stergem

    @log_operatie                                        # decoram cu log
    def total(self):                                     # totalul cosului
        # GRESIT la tine: item.subtotal() (subtotal e property, nu functie)
        return sum(item.subtotal for item in self._items.values())  # CORECT: folosim item.subtotal

    def __iter__(self):                                  # permite: for item in cos
        return iter(self._items.values())                # iterator peste valori

    def __len__(self):                                   # permite len(cos)
        return sum(item.cantitate for item in self._items.values())  # numar total bucati

    def __bool__(self):                                  # permite: if cos:
        return len(self._items) > 0                      # True daca avem cel putin un produs distinct

    def __contains__(self, cod_produs):                  # "cod in cos"
        return cod_produs in self._items                 # verificam in dict

    def __deepcopy__(self, memo):                        # definim cum se copiaza cosul
        new_cos = CosCumparaturi()                       # cream cos nou
        new_cos._items = copy.deepcopy(self._items, memo)  # copiem itemele in profunzime
        return new_cos                                   # returnam cosul nou


class StrategieReducere(ABC):                            # interfata pentru strategii de reducere
    @abstractmethod                                      # obligam clasele copil sa implementeze
    def aplica(self, total):                             # aplica reducerea pe total
        pass                                             # implementat in copii


class ReducereProcentuala(StrategieReducere):            # reducere procentuala
    def __init__(self, procent):                         # constructor reducere
        self._procent = procent                          # procent (ex: 0.10 pentru 10%)

    def aplica(self, total):                             # aplica reducerea
        return total * (1 - self._procent)               # total minus procent


class ReducereFixa(StrategieReducere):                   # reducere fixa in bani
    def __init__(self, suma):                            # constructor
        self._suma = suma                                # suma de scazut

    def aplica(self, total):                             # aplica reducerea
        return max(0, total - self._suma)                # nu coboram sub 0


class ReducerePrag(StrategieReducere):                   # reducere doar daca treci un prag
    def __init__(self, prag, procent):                   # constructor
        self._prag = prag                                # prag minim
        self._procent = procent                          # procent reducere (ex 0.10)

    def aplica(self, total):                             # aplica reducerea
        if total >= self._prag:                          # daca totalul trece pragul
            return total * (1 - self._procent)           # aplicam reducerea
        return total                                     # altfel fara reducere


class ObserverComanda(ABC):                              # interfata observer (observatori)
    @abstractmethod                                      # obligam implementarea
    def actualizeaza(self, comanda, status_vechi, status_nou):  # metoda apelata cand se schimba statusul
        pass                                             # implementat in observatori


class NotificareEmail(ObserverComanda):                  # observer email
    def actualizeaza(self, comanda, status_vechi, status_nou):  # implementare
        print(f"[EMAIL] Comanda #{comanda.id}: {status_vechi.name} -> {status_nou.name}")  # afisare


class NotificareSMS(ObserverComanda):                    # observer sms
    def actualizeaza(self, comanda, status_vechi, status_nou):  # implementare
        print(f"[SMS] Comanda #{comanda.id}: Status actualizat la {status_nou.name}")  # afisare


class Comanda:                                           # clasa comanda
    _counter = 0                                         # contor de comenzi (id unic)

    def __init__(self, client, cos, strategie_reducere=None):  # constructor comanda
        Comanda._counter += 1                            # crestem contorul
        self.id = Comanda._counter                       # setam id comanda
        self._client = client                            # numele clientului
        self._cos = copy.deepcopy(cos)                   # copiem cosul ca sa nu se schimbe din exterior
        self._strategie = strategie_reducere             # strategia de reducere (sau None)
        self._status = StatusComanda.NOUA                # status initial
        self._observers = []                             # lista de observatori
        self._timestamp = datetime.now()                 # momentul crearii

    def adauga_observer(self, observer):                 # adaugam observer
        self._observers.append(observer)                 # punem in lista

    def sterge_observer(self, observer):                 # stergem observer
        self._observers.remove(observer)                 # scoatem din lista

    def _notifica(self, status_vechi, status_nou):       # notificam toti observerii
        for obs in self._observers:                      # parcurgem lista
            obs.actualizeaza(self, status_vechi, status_nou)  # apelam metoda observerului

    @property                                            # property status
    def status(self):                                    # getter status
        return self._status                               # returnam statusul

    @status.setter                                       # setter status
    def status(self, status_nou):                        # setam status nou
        if not isinstance(status_nou, StatusComanda):    # validare tip
            raise TypeError("Status invalid!")           # eroare
        status_vechi = self._status                      # salvam statusul vechi
        self._status = status_nou                        # setam statusul nou
        self._notifica(status_vechi, status_nou)         # notificam observatorii

    def total(self):                                     # total comanda (cu reducere daca exista)
        total_brut = self._cos.total()                   # total cos (apeleaza metoda total)
        if self._strategie:                              # daca avem strategie
            return self._strategie.aplica(total_brut)    # aplicam reducerea
        return total_brut                                # altfel total brut

    def finalizeaza(self):                               # finalizeaza comanda (scade stoc)
        for item in self._cos:                           # iteram itemele din cos
            item.produs.reduce_stoc(item.cantitate)      # scadem stocul produsului
        self.status = StatusComanda.PROCESARE            # schimbam statusul (declanseaza notify)

    def __str__(self):                                   # afisare comanda
        return f"Comanda #{self.id} ({self._client}) - Status: {self._status.name} - Total: {self.total()} RON"

    def __repr__(self):                                  # repr comanda
        return f"Comanda(id={self.id}, client='{self._client}', status={self._status.name})"


@singleton                                              # facem Magazin singleton
class Magazin:                                          # clasa magazin
    def __init__(self, nume):                            # constructor
        self.nume = nume                                 # numele magazinului
        self._produse = {}                               # dict cod -> produs
        self._comenzi = []                               # lista comenzi

    def adauga_produs(self, produs):                     # adauga produs in magazin
        self._produse[produs.cod] = produs               # salvam dupa cod

    def gaseste_produs(self, cod):                       # cauta produs dupa cod
        return self._produse.get(cod)                    # return produs sau None

    def plaseaza_comanda(self, client, cos, strategie=None):  # GRESIT la tine: plaseza_comanda -> CORECT: plaseaza_comanda
        comanda = Comanda(client, cos, strategie)        # cream comanda
        self._comenzi.append(comanda)                    # o salvam
        return comanda                                   # o returnam

    def produse_categorie(self, categorie):              # filtreaza produse dupa categorie
        return [p for p in self._produse.values() if p._categorie == categorie]  # lista filtrata

    def produse_sortate_pret(self, descrescator=False):  # returneaza produse sortate dupa pret
        return sorted(self._produse.values(), reverse=descrescator)  # sortare (foloseste __lt__)

    def generator_comenzi(self, status=None):            # generator: comenzi filtrate optional dupa status
        for comanda in self._comenzi:                    # parcurgem toate comenzile
            if status is None or comanda.status == status:  # verificam filtrul
                yield comanda                            # dam comanda inapoi (yield)

    def __contains__(self, cod):                         # "cod in magazin"
        return cod in self._produse                      # verificam in dict

    def __len__(self):                                   # len(magazin)
        return len(self._produse)                        # cate produse avem

    def __iter__(self):                                  # for produs in magazin
        return iter(self._produse.values())              # iterator peste produse


# TESTARE
mag = Magazin("MegaShop")                                # cream magazin (singleton, aceeasi instanta mereu)

p1 = ProdusElectronic("E001", "Laptop", 4500, 10, 24)    # produs electronic 1
p2 = ProdusElectronic("E002", "Mouse", 150, 50, 12)      # produs electronic 2
p3 = ProdusCarte("C001", "Clean Code", 85, 30, "Robert Martin", "978-111")  # produs carte

mag.adauga_produs(p1)                                    # adaugam laptop in magazin
mag.adauga_produs(p2)                                    # adaugam mouse
mag.adauga_produs(p3)                                    # adaugam carte

cos = CosCumparaturi()                                   # cream cos
cos.adauga(p1, 1)                                        # adaugam 1 laptop
cos.adauga(p2, 2)                                        # adaugam 2 mouse-uri
cos.adauga(p3, 3)                                        # adaugam 3 carti

print(f"Total cos: {cos.total()}")                       # afisam total cos (cu log)
print(f"Items in cos: {len(cos)}")                       # afisam total bucati (nu produse distincte)

strategie = ReducerePrag(1000, 0.10)                     # reducere 10% daca totalul >= 1000
comanda = mag.plaseaza_comanda("Popescu", cos, strategie)  # CORECT: numele metodei plaseaza_comanda

email_obs = NotificareEmail()                            # observer email
sms_obs = NotificareSMS()                                # observer sms
comanda.adauga_observer(email_obs)                       # adaugam email observer
comanda.adauga_observer(sms_obs)                         # adaugam sms observer

print(comanda)                                           # afisam comanda (total cu reducere)
comanda.finalizeaza()                                    # finalizam comanda (scade stoc + status PROCESARE)
print(f"Stoc laptop dupa comanda: {p1.stoc}")            # verificam stocul dupa scadere

comanda.status = StatusComanda.EXPEDIATA                 # schimbam status (notifica)
comanda.status = StatusComanda.LIVRATA                   # schimbam status (notifica)

print(f"\nProduse electronice: {mag.produse_categorie(CategorieProdus.ELECTRONICE)}")  # filtrare electronice
print(f"\nProduse sortate: {mag.produse_sortate_pret()}")  # sortare dupa pret crescator

for c in mag.generator_comenzi(StatusComanda.LIVRATA):   # iteram doar comenzile livrate
    print(f"Comanda livrata: {c}")                       # afisam comanda livrata

cos2 = copy.deepcopy(cos)                                # copiem cosul
cos2.adauga(p1, 1)                                       # mai adaugam 1 laptop in cosul copiat
print(f"\nCos original: {len(cos)}, Cos copiat: {len(cos2)}")  # comparam marimea cosurilor

print(f"Magazin contine E001: {'E001' in mag}")          # test __contains__
print(f"Produse in magazin: {len(mag)}")                 # test __len__
