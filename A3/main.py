from itertools import combinations


def lies_eingabe(pfad: str) -> tuple[int, list[tuple[int, ...]]]:
    with open(pfad, "r") as f:
        mitgliederanzahl = int(f.readline())
        teilnahme_intervalle = [tuple(map(int, f.readline().split())) for _ in range(mitgliederanzahl)]
    return mitgliederanzahl, teilnahme_intervalle


def formatiere_ausgabe(teilnehmer_pro_strecke: dict[int, list[int]], teilnehmer_anzahl: int) -> str:
    return f"Es würden {teilnehmer_anzahl} Mitglieder teilnehmen. Die möglichen Teilnehmer jeder Streckenlänge sind:\n" + "\n".join([f"Streckenlänge {strecke}m: " + ", ".join(str(mitglied) for mitglied in teilnehmer_pro_strecke[strecke]) for strecke in teilnehmer_pro_strecke.keys()])


def erzeuge_teilnahme_bitmasken_fuer_strecken(relevante_strecken: list[int], teilnahme_intervalle: list[tuple[int, ...]]):
    bitmasken_liste = []
    for strecke in relevante_strecken:
        bitmaske = 0
        for i, (min_len, max_len) in enumerate(teilnahme_intervalle):
            if min_len <= strecke <= max_len:
                bitmaske |= (1 << i)
        bitmasken_liste.append(bitmaske)

    return bitmasken_liste


def ermittle_beste_auswahl_und_teilnehmeranzahl(relevante_strecken: list[int], bitmasken: list[int], mitgliederanzahl: int) -> tuple[tuple[int, int, int], int]:
    beste_auswahl = ()
    max_teilnehmer = 0
    for strecken_auswahl in combinations(range(len(relevante_strecken)), 3):
        vereinigte_strecken_bitmaske = bitmasken[strecken_auswahl[0]] | bitmasken[strecken_auswahl[1]] | bitmasken[
            strecken_auswahl[2]]
        teilnehmer_anzahl = vereinigte_strecken_bitmaske.bit_count()
        if teilnehmer_anzahl > max_teilnehmer:
            max_teilnehmer = teilnehmer_anzahl
            beste_auswahl = (relevante_strecken[strecken_auswahl[0]], relevante_strecken[strecken_auswahl[1]],
                             relevante_strecken[strecken_auswahl[2]])
            if max_teilnehmer == mitgliederanzahl:
                break

    return beste_auswahl, max_teilnehmer


def ermittle_moegliche_teilnehmer_pro_strecke(strecken: tuple[int, int, int], teilnahme_intervalle: list[tuple[int, ...]], bitmasken: list[int], relevante_strecken: list[int]) -> dict[int, list[int]]:
    strecken_mitglieder = {}
    for strecke in strecken:
        bitmaske = bitmasken[relevante_strecken.index(strecke)]
        strecken_mitglieder[strecke] = [i + 1 for i in range(len(teilnahme_intervalle)) if (bitmaske >> i) & 1]

    return strecken_mitglieder


def main(pfad: str) -> str:
    mitgliederanzahl, teilnahme_intervalle = lies_eingabe(pfad)
    relevante_strecken = sorted(set(max_len for _, max_len in teilnahme_intervalle))
    bitmasken = erzeuge_teilnahme_bitmasken_fuer_strecken(relevante_strecken, teilnahme_intervalle)
    strecken, teilnehmer_anzahl = ermittle_beste_auswahl_und_teilnehmeranzahl(relevante_strecken, bitmasken, mitgliederanzahl)
    teilnehmer_pro_strecke = ermittle_moegliche_teilnehmer_pro_strecke(strecken, teilnahme_intervalle, bitmasken, relevante_strecken)
    return formatiere_ausgabe(teilnehmer_pro_strecke, teilnehmer_anzahl)


if __name__ == "__main__":
    print(main(input("Pfad zur .txt Datei: ")))
