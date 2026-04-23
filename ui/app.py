import tkinter as tk
from tkinter import messagebox

from logic.parser import load_all_puzzles
from logic.prolog_writer import write_facts_file
from logic.runner import run_prolog


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SBC Project - Murder Mystery Solver")
        self.root.geometry("1250x820")
        self.root.configure(bg="#111111")

        self.puzzles = load_all_puzzles()
        self.selected_puzzle = None

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="SBC Project - Murder Mystery Solver",
            font=("Segoe UI", 22, "bold"),
            bg="#111111",
            fg="#ff4d4d",
            pady=12
        )
        title_label.pack()

        main_frame = tk.Frame(self.root, bg="#111111")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        left_frame = tk.Frame(main_frame, bg="#1a1a1a", bd=2, relief="solid")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        tk.Label(
            left_frame,
            text="Puzzle-uri",
            font=("Segoe UI", 16, "bold"),
            bg="#1a1a1a",
            fg="#ff4d4d",
            pady=12
        ).pack()

        self.listbox = tk.Listbox(
            left_frame,
            width=30,
            height=35,
            font=("Segoe UI", 14),
            bg="#262626",
            fg="white",
            selectbackground="#b30000",
            selectforeground="white",
            activestyle="none",
            bd=0,
            highlightthickness=0
        )
        self.listbox.pack(fill=tk.Y, expand=True, padx=10, pady=10)

        for i, puzzle in enumerate(self.puzzles):
            self.listbox.insert(tk.END, f"{i + 1}. {puzzle['title']}")

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        right_frame = tk.Frame(main_frame, bg="#111111")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        details_frame = tk.Frame(right_frame, bg="#1a1a1a", bd=2, relief="solid")
        details_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            details_frame,
            text="Detalii puzzle",
            font=("Segoe UI", 16, "bold"),
            bg="#1a1a1a",
            fg="#ff4d4d",
            anchor="w",
            padx=12,
            pady=8
        ).pack(fill=tk.X)

        self.details_text = tk.Text(
            details_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg="#262626",
            fg="white",
            insertbackground="white",
            bd=0,
            padx=12,
            pady=10,
            height=16
        )
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        button_frame = tk.Frame(right_frame, bg="#111111")
        button_frame.pack(fill=tk.X, pady=10)

        solve_button = tk.Button(
            button_frame,
            text="Afișează soluția",
            command=self.solve_puzzle,
            font=("Segoe UI", 13, "bold"),
            bg="#b30000",
            fg="white",
            activebackground="#ff1a1a",
            activeforeground="white",
            padx=18,
            pady=8,
            bd=0,
            cursor="hand2"
        )
        solve_button.pack()

        solution_frame = tk.Frame(right_frame, bg="#1a1a1a", bd=2, relief="solid")
        solution_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            solution_frame,
            text="Soluție",
            font=("Segoe UI", 16, "bold"),
            bg="#1a1a1a",
            fg="#ff4d4d",
            anchor="w",
            padx=12,
            pady=8
        ).pack(fill=tk.X)

        self.solution_text = tk.Text(
            solution_frame,
            wrap=tk.WORD,
            font=("Consolas", 12, "bold"),
            bg="#330000",
            fg="#ffffff",
            insertbackground="white",
            bd=0,
            padx=12,
            pady=10,
            height=12
        )
        self.solution_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def format_name(self, text):
        return text.replace("_", " ").title()

    def on_select(self, event):
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            return

        puzzle = self.puzzles[index]
        self.selected_puzzle = puzzle

        self.details_text.delete("1.0", tk.END)
        self.solution_text.delete("1.0", tk.END)

        text = f"Titlu: {puzzle['title']}\n\n"
        text += f"Descriere: {puzzle['description']}\n\n"

        text += "Suspecți:\n"
        for s in puzzle["suspects"]:
            text += f"  • {s}\n"

        text += "\nCamere:\n"
        for r in puzzle["rooms"]:
            text += f"  • {r}\n"

        text += "\nArme:\n"
        for w in puzzle["weapons"]:
            text += f"  • {w}\n"

        text += "\nIndiciile:\n"
        for c in puzzle["clues"]:
            text += f"  • {c}\n"

        self.details_text.insert(tk.END, text)

    def generate_explanation_steps(self, puzzle, solution):
        criminal = self.format_name(solution["criminal"])
        room = self.format_name(solution["room"])
        weapon = self.format_name(solution["weapon"])

        steps = []
        steps.append("Pași de rezolvare:")
        steps.append("1. Sistemul a citit suspecții, camerele, armele și toate indiciile din puzzle.")
        steps.append("2. Informațiile au fost transformate în fapte Prolog.")
        steps.append("3. Solverul a generat și verificat combinațiile posibile dintre suspecți, camere și arme.")
        steps.append("4. Au fost eliminate toate combinațiile care contrazic indiciile.")

        step_index = 5
        for clue in puzzle["clues"]:
            if room.lower() in clue.lower() or weapon.lower() in clue.lower() or criminal.lower() in clue.lower():
                steps.append(f"{step_index}. Indiciul „{clue}” a contribuit direct la restrângerea soluției.")
                step_index += 1

        steps.append(f"{step_index}. După filtrarea tuturor variantelor invalide, a rămas o singură soluție corectă.")
        step_index += 1
        steps.append(f"{step_index}. Rezultatul final este: {criminal} a comis crima în {room} folosind {weapon}.")

        return "\n".join(steps)

    def solve_puzzle(self):
        if not self.selected_puzzle:
            messagebox.showerror("Eroare", "Selectează un puzzle!")
            return

        write_facts_file(self.selected_puzzle)
        solution, error = run_prolog()

        self.solution_text.delete("1.0", tk.END)

        if error:
            self.solution_text.configure(bg="#4d0000", fg="#ffffff")
            self.solution_text.insert(tk.END, f"Eroare:\n{error}")
            return

        self.solution_text.configure(bg="#330000", fg="#ffffff")
        self.solution_text.insert(tk.END, f"Criminal: {self.format_name(solution['criminal'])}\n")
        self.solution_text.insert(tk.END, f"Camera: {self.format_name(solution['room'])}\n")
        self.solution_text.insert(tk.END, f"Arma: {self.format_name(solution['weapon'])}\n\n")

        explanation = self.generate_explanation_steps(self.selected_puzzle, solution)
        self.solution_text.insert(tk.END, explanation)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()