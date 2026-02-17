""""
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

"""

from abc import ABC, abstractmethod
from datetime import datetime

class LogMixin:
    _log = []

    def log_tranzactie(self, mesaj):
        self._log.append(f"[{datetime.now()}] {mesaj}")

    # GRESIT: lipseste decoratorul, altfel metoda primeste self, nu cls
    # def get_log(cls):
    @classmethod
    def get_log(cls):  # CORECT: classmethod primeste cls (clasa)
        return cls._log

    # GRESIT: la fel ca mai sus
    # def clear_log(cls):
    @classmethod
    def clear_log(cls):  # CORECT
        cls._log = []


class ContBancar(ABC):
    # GRESIT: ai scris numar_conturi, dar mai jos folosesti _numar_conturi
    # numar_conturi = 0
    _numar_conturi = 0  # CORECT: numele trebuie sa fie acelasi peste tot

    def __init__(self, titular, sold_initial=0):
        self._titular = titular
        self._sold = sold_initial
        self.__pin = None
        self._activ = True
        ContBancar._numar_conturi += 1  # CORECT: exista acum

    # GRESIT: asa nu poti folosi @sold.setter (sold e functie, nu property)
    # def sold(self):
    @property
    def sold(self):  # CORECT: facem sold property, ca sa mearga cont.sold
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
        # GRESIT: return True ascunde erorile din with (nu mai vezi ValueError)
        return False  # CORECT: lasa eroarea sa se vada

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
        # GRESIT: self._sold =- suma (inseamna "seteaza soldul la -suma")
        self._sold -= suma  # CORECT: scadem suma din sold
        self.log_tranzactie(f"Retragere: -{suma} RON")

    def __eq__(self, other):
        if isinstance(other, ContEconomii):
            return self._sold == other._sold and self._rata_dobanda == other._rata_dobanda
        return NotImplemented

    def __hash__(self):
        # GRESIT: hash(self._sold, self._rata_dobanda) -> hash primeste un singur argument
        return hash((self._sold, self._rata_dobanda))  # CORECT: hash pe tuple


class ContCurent(ContBancar, LogMixin):
    def __init__(self, titular, sold_initial, limita_overdraft=1000):
        # merge si asa, dar mai curat e super()
        # ContBancar.__init__(self, titular, sold_initial)
        super().__init__(titular, sold_initial)  # CORECT, simplu
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
        else:
            raise ValueError("Suma trebuie sa fie pozitiva!")  # CORECT: lipsise altfel validarea

    def retrage(self, suma):
        if suma <= 0:
            raise ValueError("Suma trebuie pozitiva!")  # CORECT: validare
        if self._sold - suma < -self._limita_overdraft:
            raise ValueError("Limita overdraft depasita!")
        self._sold -= suma
        self.log_tranzactie(f"Retragere: -{suma} RON")

    def transfer(self, destinatie, suma):
        self.retrage(suma)
        destinatie.depune(suma)
        self.log_tranzactie(f"Transfer: {suma} RON catre {destinatie.titular}")


class ContPremium(ContEconomii):
    # ATENTIE: mostenirea multipla (ContEconomii, ContCurent) e prea complicata aici.
    # Ca sa mearga simplu, facem Premium ca un ContEconomii cu overdraft + cashback.
    def __init__(self, titular, sold_initial, rata_dobanda, limita_overdraft, cashback_rate):
        super().__init__(titular, sold_initial, rata_dobanda)
        self._limita_overdraft = limita_overdraft
        self._cashback_rate = cashback_rate
        self._cashback_acumulat = 0

    def calculeaza_dobanda(self):
        # GRESIT: ContEconomii.calculeaza_dobanda() fara self
        dobanda_economii = ContEconomii.calculeaza_dobanda(self)  # CORECT: trimitem self
        return dobanda_economii * 1.5

    def tip_cont(self):
        return "Premium"

    def retrage(self, suma):
        if suma <= 0:
            raise ValueError("Suma trebuie pozitiva!")
        if self._sold - suma < -self._limita_overdraft:
            raise ValueError("Limita overdraft depasita!")
        self._sold -= suma
        cashback = suma * self._cashback_rate
        self._cashback_acumulat += cashback
        self.log_tranzactie(f"Retragere: -{suma} RON (cashback +{cashback} RON)")

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
        # CORECT: cont.sold e property acum
        return sum(cont.sold for cont in self._conturi.values())

    def conturi_by_tip(self, tip):
        # GRESIT: cont.tip_cont == tip (tip_cont e metoda, trebuie apelata)
        return [cont for cont in self._conturi.values() if cont.tip_cont() == tip]  # CORECT

    def __iter__(self):
        for id_cont, cont in self._conturi.items():
            yield id_cont, cont

    def __getitem__(self, id_cont):
        return self._conturi[id_cont]

    def __len__(self):
        return len(self._conturi)


# TESTARE
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

# GRESIT in varianta ta: with ascundea eroarea (return True in __exit__)
# Acum o prindem ca sa nu opreasca tot programul
try:
    with ce as cont:
        cont.depune(1000)
        raise ValueError("Test eroare")
except ValueError as e:
    print("Eroare prinsa:", e)

print(f"Sold dupa context manager: {ce.sold}")

print(f"Numar total conturi: {ContBancar.get_numar_conturi()}")
print(f"Log tranzactii: {LogMixin.get_log()}")
