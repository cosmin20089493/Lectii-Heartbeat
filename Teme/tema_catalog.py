# tema_catalog.py
# Program pentru gestionarea notelor elevilor
# Exerseaza: if / elif / else, lista, set, tuple, dictionar

# Catalogul este de tip dictionar
catalog = {
    "Alex": [8, 9],
    "Radu": [5, 6],
    "Ion": [7, 8],
}

# Tuple: elevi initiali
elevi_initiali = ("Alex", "Radu", "Ion")

# Daca un elev din tuple nu exista in catalog, il adaugam cu lista goala
for e in elevi_initiali:
    if e not in catalog:
        catalog[e] = []

# Set: materii
materii = {"mate", "romana", "info"}


def media_note(lista_note: list[int]) -> float:
    """Calculeaza media notelor. Daca nu exista note, media este 0."""
    if len(lista_note) == 0:
        return 0.0
    return sum(lista_note) / len(lista_note)


def afiseaza_meniu() -> None:
    print("\n1) Adauga nota")
    print("2) Afiseaza situatia unui elev")
    print("3) Afiseaza elevii promovati/corigenti")
    print("4) Verifica materia")
    print("0) Iesire")


while True:
    afiseaza_meniu()
    optiune = input("Alege: ").strip()   #.strip() curata spatiile inutile de la capetele unui text

    if optiune == "1":
        # 1) Adauga nota
        nume = input("Nume elev: ").strip()

        # daca elevul nu exista in catalog, il adaugam cu lista goala
        if nume not in catalog:
            catalog[nume] = []

        nota_text = input("Adauga nota (int): ").strip()

        # validare ca numar intreg
        if not nota_text.isdigit():
            print("Nota invalida (trebuie int intre 1 si 10).")
        else:
            nota = int(nota_text)

            # validare interval 1..10 (if/elif/else)
            if nota < 1 or nota > 10:
                print("Nota invalida")
            else:
                catalog[nume].append(nota)
                print("Nota adaugata.")

    elif optiune == "2":
        # 2) Afiseaza situatia unui elev
        nume = input("Nume elev: ").strip()

        if nume not in catalog:
            print("Elev inexistent")
        else:
            note = catalog[nume]

            if len(note) == 0:
                print("Nu are note")
                print("Media: 0.0")
            else:
                print("Note:", note)
                print("Media:", round(media_note(note), 2))

    elif optiune == "3":
        # 3) Afiseaza elevii promovati / corigenti
        promovati = []
        corigenti = []

        for nume, note in catalog.items():
            media = media_note(note)

            if media >= 5:
                promovati.append(nume)
            else:
                corigenti.append(nume)

        print("Promovati:", promovati)
        print("Corigenti:", corigenti)

    elif optiune == "4":
        # 4) Verifica materia (set)
        materie = input("Materie: ").strip().lower()

        if materie in materii:
            print("Materie valida")
        else:
            print("Materie invalida")

    elif optiune == "0":
        # 0) Iesire
        print("La revedere!")
        break

    else:
        print("Optiune invalida. Alege 1, 2, 3, 4 sau 0.")
