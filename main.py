import tkinter as tk
from tkinter import *
import ttkbootstrap as tkb
import pl1, pl3
from pl1 import Exo1
from pl3 import Exo3


# Define a function to create and pack a problem frame
def create_problem_frame(window, problem_text, problem_id):
    problem_frame = tk.Frame(window)
    problem_frame.pack(pady=3)

    problem_label = tk.Label(problem_frame, text=problem_text)
    problem_label.pack(side=tk.LEFT)

    button = tk.Button(problem_frame, text="Résoudre", command=lambda x=problem_id: solve_problem(x))
    button.pack(side=tk.RIGHT)

    return problem_frame

# Define a function for the "solve_problem" action
def solve_problem(problem_id):
    if problem_id == 1:
        exo1 = Exo1(tk.Toplevel())
        exo1.root.mainloop()
    if problem_id == 2:
        import pl2 
    if problem_id == 3:
        exo3 = Exo3(tk.Toplevel())
        exo3.root.mainloop()
    if problem_id == 4:
        import pl4 
    if problem_id == 5:
        import pl5
    if problem_id == 6:
        import pl6  

# Initialize the main window
window = tkb.Window(themename="darkly")
window.title("Projet de recherche opérationnelle")
window.geometry("800x700")

# Add title and presenter labels
title_label = tk.Label(window, text="Projet de recherche opérationnelle", font=("Arial", 18, "bold"))
title_label.pack(pady=20)

presenter_label = tk.Label(window, text="Presenté Par:", font=("Arial", 14, "bold"))
presenter_label.pack(pady=10)

# Display presenter names using a loop
presenter_names = [
    "Ferjani Oussama",
    "Bchini Mohamed Aziz",
    "Khechine Nourhen",
    "Charfeddine Elyes",
    "Ben Youssef Eya",
]

for name in presenter_names:
    presenter_name_label = tk.Label(window, text=name, font=("Arial", 12))
    presenter_name_label.pack(pady=3)

# Add separator
separator = tk.Frame(window, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(pady=20)

# Add problem selection label
label = tk.Label(window, text="Choisissez un problème à résoudre", font=("Arial", 14, "bold"))
label.pack(pady=10)

# Create and pack problem frames using a loop
problems = [
    ("PL1: Optimisation des surfaces agricoles", 1),
    ("PL2: Optimisation de la Production de l'Entreprise ChausseTous", 2),
    ("PL3: Optimisation des besoins en Ressources Humaines", 3),
    ("PL4: Optimisation des agences bancaires", 4),
    ("PL5: Optimisation de Positionnement des antennes", 5),
    ("PL6: Optimisation d'un réseau", 6),
]

for text, problem_id in problems:
    create_problem_frame(window, text, problem_id)

# Add exit button
exit_button = tk.Button(window,
text="Annuler", command=window.destroy)
exit_button.pack(side=tk.RIGHT, padx=15, pady=10)

# Start the main loop
window.mainloop()
