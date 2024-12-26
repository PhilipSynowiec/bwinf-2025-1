def lies_eingabe(pfad: str) -> str:
    with open(pfad, 'r', encoding='utf-8') as f:
        return f.read()


def erstelle_zuordnung_von_zeichen_zu_sprungweite() -> dict[str, int]:
    return {**{chr(i+97): i+1 for i in range(26)}, 'ä': 27, 'ö': 28, 'ü': 29, 'ß': 30}


def wandle_text_in_kleinbuchstaben_um_und_filtere_relevante_zeichen(text: str, zeichen_zu_sprungweite: dict[str, int]) -> str:
    return ''.join([zeichen for zeichen in text.lower() if zeichen in zeichen_zu_sprungweite.keys()])


def berechne_zuganzahl_bis_zum_ende_aus_startposition(i: int, text: str, zeichen_zu_sprungweite: dict[str, int]) -> int:
    zuganzahl = 0
    while i < len(text):
        i += zeichen_zu_sprungweite[text[i]]
        zuganzahl += 1
    return zuganzahl


def ermittle_siegerin(text: str, sprungweiten: dict[str, int]) -> str:
    return 'Amira' if berechne_zuganzahl_bis_zum_ende_aus_startposition(0, text, sprungweiten) > berechne_zuganzahl_bis_zum_ende_aus_startposition(1, text, sprungweiten) else "Bela"


def main(pfad: str) -> str:
    text = lies_eingabe(pfad)
    zeichen_zu_sprungweite = erstelle_zuordnung_von_zeichen_zu_sprungweite()
    text = wandle_text_in_kleinbuchstaben_um_und_filtere_relevante_zeichen(text, zeichen_zu_sprungweite)
    siegerin = ermittle_siegerin(text, zeichen_zu_sprungweite)
    return f'{siegerin} gewinnt beim Texthopsen.'


if __name__ == '__main__':
    print(main(input('Pfad zur .txt Datei: ')))