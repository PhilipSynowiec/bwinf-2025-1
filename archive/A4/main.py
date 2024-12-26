# Annahmen: offenheit, Tore als abgeschlossene Strecken haben keine gemeinsamen Punkte
from itertools import combinations

from tools import track


def lies_eingabe(pfad: str):
    with open(pfad, "r") as f:
        n, r = map(int, f.readline().split(" "))
        goals = [tuple(map(int, f.readline().strip().split(" "))) for _ in range(n)]
    return n, r, goals


def transformiere(tore, r):
    # Transformiert die Tore, sodass die Pfosten um den Radius zueinander verschoben sind und deshalb im weiteren Radius 0 genommen werden kann, und die Pfosten jedes Tors lexikografisch geordnet sind (v1 < v2). Gibt None zurück, wenn der Ball nicht durch die Tore passt.
    trafo = []
    for x1, y1, x2, y2 in tore:
        if x1 == x2:
            x1, y1, x2, y2 = (x1, min(y1, y2) + r, x2, max(y1, y2) - r)
            if y1 >= y2:
                return None
        else:
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            m = (y2-y1)/(x2-x1)
            c = r/(1+m**2)**0.5
            x1, y1, x2, y2 = (x1 + c, y1 + m*c, x2 - c, y2 - m*c)
            if x1 >= x2:
                return None

        trafo.append((x1, y1, x2, y2))

    return trafo


def waehle_m(tore):
    # Stelle Ungleichungen der Form ... für jedes Tor auf, anhand der Schussgerade y = mx+t
    # t liegt zwischen den Zahlen der Form y-xm mit (x, y) in {(x1, y1), (x2, y2)} für jedes Tor
    # Ziel: Finden von m, das in der Vereinigung dieser Mengen liegt
    # Idee: Alle Intervalle zwischen nebeneinanderliegenden Schnittpunkten zweier solcher Geraden t(m) = y-xm betrachten
    # zwischen diesen ändern sich obere und untere Schranke nicht

    # Schnittpunkte bestimmen (wenn sie nicht existieren, i.e. x1=x2, ändern sie die Schranken auch nicht)
    geraden = {(x1, y1) for x1, y1, x2, y2 in tore}.union({(x2, y2) for x1, y1, x2, y2 in tore})

    schnittpunkte = sorted({(y2 - y1) / (x2 - x1) for (x1, y1), (x2, y2) in combinations(geraden, 2) if  x1 != x2})
    # TODO das hier muss effizienter gemacht werden, eventuell kann man manche Schnittpunkte ignorieren. Eventuell kann man die Ordnung schon davor behalten und nur Geraden benachbarter Tore schneiden oder so, aber keine Ahnung jetzt.


    intervalle = {(schnittpunkte[0] - 1, schnittpunkte[0]), (schnittpunkte[-1], schnittpunkte[-1] + 1)}.union(
        {(schnittpunkte[i], schnittpunkte[i + 1]) for i in range(1, len(schnittpunkte) - 1)})

    # Nun finde Intervalle, in denen die untere unter der oberen Grenze liegt (da sich die Geraden auf den Intervallen nicht schneiden, reichen die Mittelpunkte der Schranken bzw. zum Finden der Schranken der Geraden)
    m_intervalle = set()
    for a, b in intervalle:
        m = (a + b) / 2
        untere = max(min(y1-x1*m, y2-x2*m) for x1, y1, x2, y2 in tore)
        obere = min(max(y1-x1*m, y2-x2*m) for x1, y1, x2, y2 in tore)
        if untere < obere:
            m_intervalle.add((a, b))

    # Kann durch beliebige andere Auswahl eines Elements aus der Vereinigung der offenen Intervalle ersetzt werden
    if m_intervalle:
        a, b = list(m_intervalle)[0]
        return (a + b) / 2
    return None


def waehle_t(m, tore):
    # t liegt zwischen den Zahlen der Form y-xm mit (x, y) in {(x1, y1), (x2, y2)} für jedes Tor
    untere = max(min(y1-x1*m, y2-x2*m) for x1, y1, x2, y2 in tore)
    obere = min(max(y1-x1*m, y2-x2*m) for x1, y1, x2, y2 in tore)
    return (untere + obere)/2 # Kann durch beliebige andere Auswahl eines Elements aus dem offenen Intervall ersetzt werden


def waehle_startpunkt(m, t, tore):
    # Liste der x-Koordinaten der Schnittpunkte der Gerade mit den Toren in der Reihenfolge
    xcoors = [(x1*(y2-y1)+t*(x2-x1)-y1*(x2-x1))/(y2-y1-m*(x2-x1)) for x1, y1, x2, y2 in tore]

    if xcoors == sorted(xcoors):
        x = xcoors[0]-1
    elif xcoors == sorted(xcoors)[::-1]:
        x = xcoors[-1]+1
    else:
        return None
    return x, m * x + t


def main(pfad):
    n, r, tore = lies_eingabe(pfad)
    tore = transformiere(tore, r)
    if tore is None:
        return "Es ist unmöglich, da der Ball nicht durch alle Tore passt."
    m = waehle_m(tore)
    if m is None:
        return "Es ist unmöglich."
    t = waehle_t(m, tore)
    start = waehle_startpunkt(m, t, tore)
    if start is None:
        return "Es ist in dieser Reihenfolge nicht möglich."
    return f"Es ist möglich, z.B. wenn man aus dem Punkt ({start[0]}, {start[1]}) entlang der durch y = {m}x+{t} gegebenen Geraden schießt."


if __name__ == "__main__":
    print(track(main)("krocket5.txt"))
