import os
import subprocess


def run_prolog():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    solver_path = os.path.join(base_dir, "prolog", "solver.pl")
    swipl_path = r"C:\Program Files\swipl\bin\swipl.exe"

    cmd = [
        swipl_path,
        "-q",
        "-s",
        solver_path,
        "-g",
        "solve(Criminal, Room, Weapon), format('~w|~w|~w', [Criminal, Room, Weapon]), halt."
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_dir)

    if result.returncode != 0:
        return None, result.stderr.strip()

    output = result.stdout.strip()
    if not output:
        err = result.stderr.strip()
        return None, err if err else "Nu s-a gasit nicio solutie."

    parts = output.split("|")
    if len(parts) != 3:
        err = result.stderr.strip()
        return None, err if err else f"Output neasteptat din Prolog: {output}"

    return {
        "criminal": parts[0],
        "room": parts[1],
        "weapon": parts[2]
    }, None