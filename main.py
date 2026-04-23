from logic.parser import load_all_puzzles
from logic.prolog_writer import write_facts_file
from logic.runner import run_prolog


def format_name(name: str) -> str:
    return name.replace("_", " ").title()


def main():
    puzzles = load_all_puzzles()

    print("\n=== SBC PROJECT: Murder Mystery Solver ===\n")

    print("Puzzle-uri disponibile:\n")
    for i, puzzle in enumerate(puzzles, start=1):
        print(f"{i}. {puzzle['title']}")

    choice = int(input("\nAlege un puzzle (număr): ")) - 1
    selected = puzzles[choice]

    print("\n==============================")
    print("Titlu:", selected["title"])
    print("Descriere:", selected["description"])

    print("\nSuspecți:", ", ".join(selected["suspects"]))
    print("Camere:", ", ".join(selected["rooms"]))
    print("Arme:", ", ".join(selected["weapons"]))

    print("\nIndiciile:")
    for clue in selected["clues"]:
        print("-", clue)

    print("\nSe genereaza facts.pl...")
    write_facts_file(selected)

    print("Se ruleaza solverul Prolog...")
    solution, error = run_prolog()

    if error:
        print("\nEroare:", error)
    else:
        print("\n=== SOLUTIE ===")
        print("Criminal:", format_name(solution["criminal"]))
        print("Camera crimei:", format_name(solution["room"]))
        print("Arma crimei:", format_name(solution["weapon"]))

    print("\n==============================")


if __name__ == "__main__":
    main()