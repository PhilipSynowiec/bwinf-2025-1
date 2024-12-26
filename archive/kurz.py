def berechne_zuganzahl_aus_position(i, text, s):
    return berechne_zuganzahl_aus_position(i+s[text[i]], text, s) + 1 if i < len(text) else 0

def main(pfad):
    sprungweiten = {**{chr(i+97): i+1 for i in range(26)}, 'ä': 27, 'ö': 28, 'ü': 29, 'ß': 30}
    text = ''.join(z for z in open(pfad, 'r', encoding='utf-8').read().lower() if z in sprungweiten)
    return f'{"Amira" if berechne_zuganzahl_aus_position(0, text, sprungweiten) > berechne_zuganzahl_aus_position(1, text, sprungweiten) else "Bela"} gewinnt beim Texthopsen.'

print(main(input('Pfad zur .txt Datei: ')))