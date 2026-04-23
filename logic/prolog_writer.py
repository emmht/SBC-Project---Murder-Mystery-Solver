import os


def sanitize(text: str) -> str:
    return text.strip().lower().replace(" ", "_")


def write_facts_file(puzzle):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "prolog", "facts.pl")

    with open(file_path, "w", encoding="utf-8") as f:
        for s in puzzle["suspects"]:
            f.write(f"suspect({sanitize(s)}).\n")

        f.write("\n")

        for r in puzzle["rooms"]:
            f.write(f"room({sanitize(r)}).\n")

        f.write("\n")

        for w in puzzle["weapons"]:
            f.write(f"weapon({sanitize(w)}).\n")

        f.write("\n")

        for clue in puzzle["clues"]:
            c = clue.strip()

            if " nu era in " in c:
                person, room = c.split(" nu era in ")
                f.write(f"clue_person_not_in_room({sanitize(person)}, {sanitize(room)}).\n")

            elif " nu avea " in c:
                person, weapon = c.split(" nu avea ")
                f.write(f"clue_person_not_has_weapon({sanitize(person)}, {sanitize(weapon)}).\n")

            elif c.startswith("Persoana din ") and " avea " in c:
                temp = c.replace("Persoana din ", "", 1)
                room, weapon = temp.split(" avea ")
                f.write(f"clue_room_has_weapon({sanitize(room)}, {sanitize(weapon)}).\n")

            elif c.startswith("Crima nu a avut loc in "):
                room = c.replace("Crima nu a avut loc in ", "", 1)
                f.write(f"clue_crime_not_in_room({sanitize(room)}).\n")

            elif c.startswith("Crima nu s-a facut cu "):
                weapon = c.replace("Crima nu s-a facut cu ", "", 1)
                f.write(f"clue_crime_not_with_weapon({sanitize(weapon)}).\n")

            elif " era in " in c:
                person, room = c.split(" era in ")
                f.write(f"clue_person_in_room({sanitize(person)}, {sanitize(room)}).\n")

            elif " avea " in c:
                person, weapon = c.split(" avea ")
                f.write(f"clue_person_has_weapon({sanitize(person)}, {sanitize(weapon)}).\n")