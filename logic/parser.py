import os
import json
import re


def extract_number(filename):
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else 0


def load_puzzle(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_puzzles(folder="puzzles"):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder_path = os.path.join(base_dir, folder)

    puzzles = []

    filenames = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".json")],
        key=extract_number
    )

    for filename in filenames:
        path = os.path.join(folder_path, filename)
        puzzle = load_puzzle(path)
        puzzle["filename"] = filename
        puzzles.append(puzzle)

    return puzzles
