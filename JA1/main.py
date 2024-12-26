from math import floor, ceil


def lies_eingabe(pfad: str) -> tuple[int, int, int]:
    with open(pfad, 'r') as f:
        interessenten, hoehe, breite = map(int, [f.readline() for _ in range(3)])
        return interessenten, hoehe, breite


def berechne_groessere_durch_kleinere_seite_der_kleingaerten(hoehe: int, breite: int, spaltenanzahl: int, zeilenanzahl: int) -> float:
    horizontale_seite = breite/spaltenanzahl
    vertikale_seite = hoehe/zeilenanzahl
    return max(horizontale_seite, vertikale_seite) / min(horizontale_seite, vertikale_seite)


def berechne_moegliche_spalten_und_zeilenanzahlen(interessenten: int):
    for spaltenanzahl in range(1, floor(1.1 * interessenten) + 1):
        for zeilenanzahl in range(ceil(interessenten / spaltenanzahl), floor(1.1 * interessenten / spaltenanzahl) + 1):
            yield spaltenanzahl, zeilenanzahl


def berechne_optimale_spalten_und_zeilenanzahl(interessenten: int, hoehe: int, breite: int) -> tuple[int, int]:
    return min(berechne_moegliche_spalten_und_zeilenanzahlen(interessenten), key = lambda dim: berechne_groessere_durch_kleinere_seite_der_kleingaerten(hoehe, breite, dim[0], dim[1]))


def main(pfad: str) -> str:
    interessenten, hoehe, breite = lies_eingabe(pfad)
    spaltenanzahl, zeilenanzahl = berechne_optimale_spalten_und_zeilenanzahl(interessenten, hoehe, breite)
    return f'Das Feld sollte gleichmäßig in {spaltenanzahl} Spalten und {zeilenanzahl} Zeilen aufgeteilt werden.'


if __name__ == '__main__':
    print(main(input('Pfad zur .txt Datei: ')))