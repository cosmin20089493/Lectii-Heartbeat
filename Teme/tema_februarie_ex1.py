# De rezolvat erorile si comentat fiecare linie de cod
from abc import ABC, abstractmethod  #import pentru calse abstracte si metode abstracte


class Persoana:
    numar_persoane = 0   #VAriabia de clasa: e comuna pentru toate persoanele

    def __init__(self, nume, varsta):
        self.nume = nume        #atribut public , se vede direct
        self.__varsta = varsta   #atribut privat, mai exact ne folosim de incapsulare
       # GRESIT !!!  numar_persoane += 1
        Persoana.numar_persoane += 1  # CORECT: modificam variabila de CLASA, nu una locala

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
        # GRESIT!!!numar_persoane -= 1
        Persoana.numar_persoane -= 1  # CORECT: scadem contorul din variabila de clasa


class Angajat(Persoana, ABC):
    def __init__(self, nume, varsta, salariu, departament):
        #Gresit,lipseste self !!! Persoana.__init__(nume, varsta)
        Persoana.__init__(self, nume, varsta)  # CORECT: trimitem si self

        self._salariu = salariu  #Atribut protejat, se foloseste in clasa "copil"
        self._departament = departament #departamentul angajatului
        self._bonus = 0  # CORECT: trebuie sa fie _bonus, nu __bonus (altfel nu e accesibil in clasele copil)

    @abstractmethod
    def calculeaza_salariu_total(self):
        pass   #metoda obligatoriein clasele copil

    def aplica_bonus(self, procent):
        self._bonus = self._salariu * procent / 100 #calculam bonsul in bani

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
        #Gresit !!!return f"{self.__class__(self.nume)}: Salariu={self._salariu}"
        return f"{self.__class__.__name__}(nume='{self.nume}', salariu={self._salariu})"


class Manager(Angajat): #am creeat o noua classa Manager
    def __init__(self, nume, varsta, salariu, departament, echipa):
        # GRESIT: lipsea departament in super()
        super().__init__(nume, varsta, salariu, departament)  # CORECT: trimitem toate argumentele
        self.echipa = echipa #Lista de angajati, obiect angajat

    def calculeaza_salariu_total(self):
        bonus_echipa = len(self.echipa) * 200 #Exemplu: 200 Ron per membru
        #!!!gresit: __bonus nu exista aici (privat in Angajat)
        return self._salariu + self._bonus + bonus_echipa  # CORECT: folosim _bonus

    def adauga_membru(self, angajat):
        self.echipa.append(angajat)  #Adaugam un obiect (developer/Angajat) in echipa

    def __str__(self):
        # GRESIT: join nu merge pe obiecte
        membri = ", ".join(membru.nume for membru in self.echipa)  # CORECT: luam doar numele
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
        # daca nivelul e gresit, folosim 1.0 ca fallback
        multiplier = Developer.NIVEL_MULTIPLIER.get(self.nivel, 1.0)
        return self._salariu * multiplier + self._bonus  # CORECT: folosim _bonus

    def adauga_proiect(self, proiect):
        # GRESIT: self._proiecte = proiect (suprascria lista)
        self._proiecte.append(proiect)  # CORECT: adaugam in lista

    def __str__(self):
        return f"Developer: {self.nume}, Limbaj: {self.limbaj}, Nivel: {self.nivel}"

    def __iter__(self):
        return iter(self._proiecte) #permite :for p in developer

    def __getitem__(self, index):
        return self._proiecte[index]#permite:developer[0]


class Companie:
    def __init__(self, nume):
        self.nume = nume#Numele companiei
        self.__angajati = []#Lista privata de angajati

    def angajeaza(self, angajat):
        # GRESIT: self.__angajati = angajat (inlocuia lista)
        self.__angajati.append(angajat)  # CORECT: adaugam in lista

    def concediaza(self, nume_angajat):
        for i in range(len(self.__angajati)): #parcurgem lista prin index
            if self.__angajati[i].nume == nume_angajat:#daca numele se potriveste
                del self.__angajati[i]#stergem din lista
                break

    def total_salarii(self):
        total = 0
        for ang in self.__angajati:
            total += ang.calculeaza_salariu_total()  # CORECT: total real (include bonus)
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

# optional: aplicam bonus ca sa vedem diferenta
m1.aplica_bonus(10)
d1.aplica_bonus(5)

print(f"Salariu total manager: {m1.calculeaza_salariu_total()}")
print(f"Salariu total developer: {d1.calculeaza_salariu_total()}")
print(f"Comparatie: {m1 > d1}")
print(f"Suma salarii: {m1 + d1}")
print(f"Total salarii companie: {comp.total_salarii()}")
print(f"Numar persoane: {Persoana.get_numar_persoane()}")
