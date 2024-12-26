def lese_eingabe(pfad: str) -> list[int]:
    with open(pfad, "r") as f:
        return [int(f.readline()) for _ in range(int(f.readline()))]


def formatiere_ausgabe(daten: list[tuple]) -> str:
    return '.\n'.join([f"Warte {daten[i][0] - daten[i-1][0]} Minuten, laufe " + ("zum Grabmal." if i == len(daten)-1 else f"in Abschnitt {daten[i][1]+1}") for i in range(1, len(daten))])


def wurde_abschnitt_veraendert(abschnitt: int, zeit: int, naechste_aenderungszeiten: list[int]) -> bool:
    return naechste_aenderungszeiten[abschnitt] == zeit


def wurde_abschnitt_geschlossen(abschnitt: int, zeit: int, perioden: list[int]) -> bool:
    return zeit % (2 * perioden[abschnitt]) == 0


def main(pfad: str) -> str:
    perioden = lese_eingabe(pfad)
    naechste_aenderungszeiten = perioden.copy()
    moegliche_abschnitte = {-1}
    offene_aber_unmoegliche_abschnitte = {len(perioden)}
    abschnitt_zu_weg = [[] for _ in range(len(perioden)+1)] + [[(0, -1)]]

    while len(perioden) not in moegliche_abschnitte:
        zeit = min(naechste_aenderungszeiten)

        for abschnitt in range(len(perioden)):
            if wurde_abschnitt_veraendert(abschnitt, zeit, naechste_aenderungszeiten):
                naechste_aenderungszeiten[abschnitt] += perioden[abschnitt]

                if wurde_abschnitt_geschlossen(abschnitt, zeit, perioden):
                    offene_aber_unmoegliche_abschnitte.discard(abschnitt)
                    moegliche_abschnitte.discard(abschnitt)
                    abschnitt_zu_weg[abschnitt] = []
                else:
                    offene_aber_unmoegliche_abschnitte.add(abschnitt)

        for abschnitt in list(moegliche_abschnitte):
            for richtung in [-1, 1]:
                neuer_abschnitt = abschnitt + richtung
                while neuer_abschnitt in offene_aber_unmoegliche_abschnitte:
                    moegliche_abschnitte.add(neuer_abschnitt)
                    offene_aber_unmoegliche_abschnitte.remove(neuer_abschnitt)
                    abschnitt_zu_weg[neuer_abschnitt] = abschnitt_zu_weg[abschnitt] + [(zeit, neuer_abschnitt)]
                    neuer_abschnitt += richtung

    return formatiere_ausgabe(abschnitt_zu_weg[len(perioden)])


if __name__ == "__main__":
    print(main(input("Pfad zur .txt Datei: ")))