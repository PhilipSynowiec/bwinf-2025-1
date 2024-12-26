def read_input() -> tuple[list[list[str]], set[str]]:
    with open("schwierigkeiten1.txt") as f:
        n, m, k = map(int, f.readline().split())
        exams = [[c.strip() for c in f.readline().split(" < ")] for _ in range(n)]
        exercises = set(c.strip() for c in f.readline().split())
    return exams, exercises


def find_minimum(exams: list[list[str]], exercises: set[str]):
    # Ansatz: Greedy Konfliktminimierung. Wenn es nicht optimal ist, dann nicht greedy machen.
    min_conflicts = float("inf")
    choice = None
    for e in exercises:
        conflicts = 0
        for exam in exams:
            if e in exam:
                i = 0
                while exam[i] not in exercises:
                    i += 1
                if e != exam[i]:
                    conflicts += 1
        if conflicts < min_conflicts:
            min_conflicts = conflicts
            choice = e
    print(choice, min_conflicts)
    return choice


def run():
    exams, exercises = read_input()
    ordering = []
    while exercises:
        minimum = find_minimum(exams, exercises)
        ordering.append(minimum)
        exercises.remove(minimum)
        exams = [[e for e in exam if e != minimum] for exam in exams]
        exams = [exam for exam in exams if exam]
    print(ordering)

run()