def read_input() -> tuple[list[list[str]], set[str]]:
    with open("schwierigkeiten0.txt") as f:
        n, m, k = map(int, f.readline().split())
        exams = [[c.strip() for c in f.readline().split(" < ")] for _ in range(n)]
        exercises = set(c.strip() for c in f.readline().split())
    return exams, exercises


def find_minimum(exams: list[list[str]]):
    # Bei Konflikten iterativ ältere Daten weglassen
    options = []
    while not options:
        options = {exam[0] for exam in exams if not any([exam[0] in e[1:] for e in exams])}
        exams = exams[1:]
    print(options)
    return options.pop()


def run():
    exams, exercises = read_input()
    ordering = []
    while exercises:
        print(exams)
        print(exercises)
        minimum = find_minimum(exams)
        if minimum in exercises:
            ordering.append(minimum)
            exercises.remove(minimum)
        exams = [[e for e in exam if e != minimum] for exam in exams]
        exams = [exam for exam in exams if exam]
        print(ordering)


run()