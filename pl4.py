import tkinter as tk
from tkinter import Label, Entry, Button, Checkbutton, Toplevel
import gurobipy as gp
from gurobipy import GRB
from itertools import product
import subprocess
import sys

def show_menu():
    # Close the current Tkinter window or GUI
    root.destroy()  # Assuming 'root' is your Tkinter window instance

    # Run the "main.py" script
    subprocess.run([sys.executable, 'main.py'])


def get_binary_matrix_values(entries_matrix):
    binary_matrix_values = []
    for row in entries_matrix:
        # Ensure the Entry widget is not destroyed before retrieving its value
        row_values = []
        for entry in row:
            if entry.winfo_exists():
                row_values.append(int(entry.get()))
            else:
                # Handle the case where the Entry widget is destroyed
                row_values.append(0)  # Or any default value you prefer
        binary_matrix_values.append(row_values)

    print("Binary Matrix of Neighboring Regions:")
    for row in binary_matrix_values:
        print(row)

    return binary_matrix_values

def pl_4():
    global entries_matrix, populations, B, K, D

    num_regions = len(entries_matrix)
    a_percent = 0.05
    c_percent = 0.02
    b_percent = 0.01

    A = get_binary_matrix_values(entries_matrix)

    model = gp.Model("Localisation_Agences_DAB")
    x = model.addVars(num_regions, vtype=GRB.BINARY, name="x")
    y = model.addVars(num_regions, vtype=GRB.BINARY, name="y")

    model.setObjective(gp.quicksum(a_percent * x[i] * populations[i] + c_percent * y[i] * populations[i] + b_percent * x[i] * gp.quicksum(populations[j] * A[i][j] for j in range(num_regions)) for i in range(num_regions)), sense=GRB.MAXIMIZE)

    for j in range(num_regions):
     model.addConstr(gp.quicksum(A[i][j] * x[i] for i in range(num_regions)) + y[j] >= 1, name=f"contrainte_a_{j}")

    model.addConstr(gp.quicksum((x[i] + x[j]) * A[i][j] for i, j in product(range(num_regions), repeat=2) if i != j) <= 1, name="contrainte_b")

    model.addConstr(gp.quicksum(K * x[i] + D * y[i] for i in range(num_regions)) <= B, name="contrainte_c")

    model.optimize()

    # Create a new window to display the results
    result_window = Toplevel(root)
    result_window.title("Résultats")

        # Afficher les résultats sur la fenêtre
    results_label = Label(result_window, text="\n\nRésultats:", font=('Arial', 14, 'bold'))
    results_label.pack()

    for i in range(num_regions):
        result_label = Label(result_window, text=f"Region {i + 1}: Agence={int(x[i].x)}, Serveur DAB={int(y[i].x)}", font=('Arial', 12))
        result_label.pack()

    total_clients_label = Label(result_window, text=f"\nNombre total de clients: {int(model.objVal)}", font=('Arial', 12, 'bold'))
    total_clients_label.pack()
def set_pop_values(pop_window):
    global populations, B, K, D, entry_budget, entry_cout_agence, entry_cout_dab

    B = int(entry_budget.get())
    K = int(entry_cout_agence.get())
    D = int(entry_cout_dab.get())
    populations = [float(entry.get()) for entry in populations]
    pop_window.destroy()
def population_interface():
    global populations, B, K, D, entry_budget, entry_cout_agence, entry_cout_dab

    pop_window = Toplevel(root)
    pop_window.title("Saisie des populations")

    size = int(entry_regions.get())

    # Titre
    Label(pop_window, text="Saisie des populations", font=('Arial', 14, 'bold')).grid(row=0, columnspan=2, pady=10)

    populations = []
    for i in range(size):
        Label(pop_window, text=f"Population de la région {i + 1}:", font=('Arial', 12)).grid(row=i + 1, column=0, padx=5, pady=5)
        entry = Entry(pop_window, font=('Arial', 12))
        entry.grid(row=i + 1, column=1, padx=5, pady=5)
        populations.append(entry)

    # Bouton de soumission
    btn_submit = Button(pop_window, text="Submit", command=lambda: set_pop_values(pop_window), font=('Arial', 12),bg='lightgreen')
    btn_submit.grid(row=size + 2, columnspan=2, pady=10)

def matrix_interface():
    global entries_matrix

    matrix_window = Toplevel(root)
    matrix_window.title("Matrice des régions voisines")

    size = int(entry_regions.get())

    # Étiquettes pour les lignes
    for i in range(size):
        Label(matrix_window, text=f'R{i + 1}', font=('Arial', 12)).grid(row=i + 1, column=0, padx=5, pady=5)

    # Étiquettes pour les colonnes
    for j in range(size):
        Label(matrix_window, text=f'R{j + 1}', font=('Arial', 12)).grid(row=0, column=j + 1, padx=5, pady=5)

    # Utiliser la variable globale entries_matrix
    entries_matrix = []
    for i in range(size):
        row_entries = []
        for j in range(size):
            entry = Entry(matrix_window, width=5, font=('Arial', 12))
            entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            row_entries.append(entry)
        entries_matrix.append(row_entries)

    # Bouton de soumission
    btn_submit = Button(matrix_window, text="Submit", command=lambda: matrix_window.destroy(), font=('Arial', 12),bg='lightgreen')
    btn_submit.grid(row=size + 1, columnspan=size + 1, pady=10)


def main_interface():
    global root, entry_regions, entry_budget, entry_cout_agence, entry_cout_dab
    root = tk.Tk()
    root.title("Interface de saisie")
    
    Label(root, text="Nombre des régions:", font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5)
    entry_regions = Entry(root, font=('Arial', 12))
    entry_regions.grid(row=0, column=1, padx=5, pady=5)
    
    # Séparateur
   # Label(root, text="(maximum 9 regions)*").grid(row=1, column=0)
    Label(root, text="").grid(row=2, column=0)

    Label(root, text="Budget:", font=('Arial', 12)).grid(row=3, column=0, padx=5, pady=5)
    entry_budget = Entry(root, font=('Arial', 12))
    entry_budget.grid(row=3, column=1, padx=5, pady=5)

    # Séparateur
    Label(root, text="").grid(row=4, column=0)

    Label(root, text="Coût d'une agence:", font=('Arial', 12)).grid(row=5, column=0, padx=5, pady=5)
    entry_cout_agence = Entry(root, font=('Arial', 12))
    entry_cout_agence.grid(row=5, column=1, padx=5, pady=5)

    # Séparateur
    Label(root, text="").grid(row=6, column=0)

    Label(root, text="Coût du DAB:", font=('Arial', 12)).grid(row=7, column=0, padx=5, pady=5)
    entry_cout_dab = Entry(root, font=('Arial', 12))
    entry_cout_dab.grid(row=7, column=1, padx=5, pady=5)

    # Séparateur
    Label(root, text="").grid(row=8, column=0)

    btn_pop_interface = Button(root, text="Saisie des populations", command=population_interface, font=('Arial', 12),bg='lightblue')
    btn_pop_interface.grid(row=9, columnspan=2, pady=10)

    btn_matrix_interface = Button(root, text="Matrice des régions voisines", command=matrix_interface, font=('Arial', 12),bg='lightblue')
    btn_matrix_interface.grid(row=10, columnspan=2, pady=10)

    btn_solve = Button(root, text="Solve", command=pl_4, font=('Arial', 12),bg='lightgreen')
    btn_solve.grid(row=11, columnspan=2, pady=10)
    tk.Button(root, text="Main Menu", command=show_menu).grid(row=11, column=0, padx=5, pady=5)
    root.mainloop()

# Run the main interface
main_interface()
