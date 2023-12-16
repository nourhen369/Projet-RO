import tkinter as tk
from tkinter import messagebox, ttk
import gurobipy as gp
from gurobipy import *
import ttkbootstrap as tkb
from ttkbootstrap import ttk

# fct bch tekhou el nb de mois mel premiere fenetre le deusieme
def nombre_mois():
    try:
        nb_mois = int(nb_mois_entry.get())
        # Validate input value
        if nb_mois <= 0 or nb_mois > 12:
            raise ValueError("Le nombre de mois doit être compris entre 1 et 12.")
        return nb_mois
    except ValueError as error:
        messagebox.showerror("Error", str(error))
        return None

# second window elli bch noptimisiw feha
def pl2():  
    nb = nombre_mois()
    def solve():
        try: 
            model = gp.Model(name="Production Optimization")
            
            NHS, NCH, NOR, NOL, S, NO, C, Cs, demande, Sal, Hsup, R, L, h , Vol, Hmax= [], [], [], [], [], [], [], [], [], [], [], [], [], [],[], []
            valeurs = [NHS, NCH, NOR, NOL, S, NO, C, Cs, demande, Sal, Hsup, R, L, h , Vol, Hmax] # feha les valeurs elli bch yaatihom el user
            
            for i, row_entries in enumerate(entries):
                for j, entry in enumerate(row_entries):
                    # print(entry)
                    try:
                        valeurs[i].append(float(entry.get()))
                    except ValueError:
                        messagebox.showerror("Error", "Prière de remplir tous les champs avec des valeurs numériques valides!")
                        return None
            
            # Ajoutez les variables de décision au modèle, CONTINUOUS allows the variable to take any real number value within a specified range.
            heures_sup = {t: model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"heures_sup_{i+1}") for t in range(nb)}
            paires_chaussures = {t: model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"paires_chaussures_{i+1}") for t in range(nb)}
            ouvriers_rec = {t: model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"ouvriers_rec_{i+1}") for t in range(nb)}
            ouvriers_lic = {t: model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"ouvriers_lic_{i+1}") for t in range(nb)}
            
            # les vars auxilieres [nehsbouhom des variables de decision]
            ouvriers_dispo = {t: model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"ouvriers_dispo_{t}") for t in range(nb)}
            stock = {t: model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"stock_{t}") for t in range(nb)}

            # Update the model to integrate new variables
            model.update()

            for i in range(nb): 
                if i > 0:
                    model.addConstr(stock[i-1] + paires_chaussures[i] >= demande[i])
                    model.addConstr(ouvriers_dispo[i]==ouvriers_dispo[i-1]+ouvriers_rec[i]-ouvriers_lic[i])
                    model.addConstr(stock[i]==stock[i-1]+paires_chaussures[i-1]-demande[i-1])
                model.addConstr(heures_sup[i] <= Hmax[i]*ouvriers_dispo[i])
                # les contraintes de signe 
            model.addConstrs(stock[i] >= 0 for i in range(nb))
            model.addConstrs(ouvriers_dispo[i] >= 0 for i in range(nb))
            model.addConstrs(ouvriers_rec[i] >= 0 for i in range(nb))
            model.addConstrs(ouvriers_lic[i] >= 0 for i in range(nb))
            model.addConstrs(heures_sup[i] >= 0 for i in range(nb))

            # Objective Function
            model.setObjective(
                gp.quicksum(
                    ouvriers_rec[t] * R[t] +
                    ouvriers_lic[t] * L[t] +
                    heures_sup[t] * Hsup[t] +
                    paires_chaussures[t] * C[t] +
                    NO[t] * Sal[t]
                    for t in range(nb)
                ),
                gp.GRB.MINIMIZE)
            
            # Solve the model
            model.optimize()

            # Display the optimal solution or relevant information
            if model.status == gp.GRB.OPTIMAL:
                result_window = tk.Toplevel(root)
                result_window.title("Results")
                result_window.geometry("+500+250")

                text_widget = tk.Label(result_window, width=40, height=10, text=f"Planning optimal de production: {model.objVal:.2f}")
                text_widget.pack()
            else:
                messagebox.showwarning("Warning", "L'optimisation n'a pas convergé! Le modèle n'a pas pu être résolu de manière optimale.")
        except ValueError:
            messagebox.showerror("Error", "Resaisir vos données!")

    table_frame = tk.PanedWindow(root)
    table_frame.pack(side="top", fill="both", expand=True)
    
    parametres = ["Nombre d'heures supplémentaires",
                    "Nombre de paires de chaussures fabriqués",
                    "Nombre d'ouvriers recrutés",
                    "Nombre d'ouvriers licencés",
                    "Stock",
                    "Nombre d'ouvriers disponible",
                    "Cout de production d'une paire de chaussure",
                    "Cout de stockage d'une paire de chaussure",
                    "Demande",
                    "Salaire d'un ouvrier", 
                    "Coût d'une heure supplémentaire par ouvrier", 
                    "Frais de recrutement,", 
                    "Frais de licenciement", 
                    ": Nombre d'heure nécessaire pour fabriquer une paire de chaussure", 
                    "Volume horaire mensuel de travail par ouvrier", 
                    "Nombre d'heures sup max par ouvrier",
                    "Résoudre le problème d'optimisation"]
    mois = []
    for i in range(nb):
        mois.append(f"Mois {i+1}")

    for j, label_text in enumerate(mois):
        label = tk.Label(table_frame, text=label_text, bg='#2E2E2E', fg='white')
        label.grid(row=0, column=j+1, padx=2, pady=2, sticky='nsew', rowspan=2)

    for i, label_text in enumerate(parametres):
        label = tk.Label(table_frame, text=label_text, bg='#2E2E2E', fg='white')
        label.grid(row=i+2, column=0, padx=2, pady=2, sticky='nsew')
    
    entries = [[ttk.Entry(table_frame, width=8) for _ in range(nb)] for _ in range(16)]
    for i in range(16):
        for j in range(nb):
            entry = entries[i][j]
            entry.grid(row=i+2, column=j+1, padx=2, pady=2, sticky='nsew')
            entry_style = ttk.Style()
            entry_style.configure('Black.TEntry', foreground='white')
            entry.configure(style='Black.TEntry')

    button = tk.Button(table_frame, text="Résoudre",bg='Black', command=solve)
    button.grid(row=18, column=1, padx=2, pady=2, sticky='nsew')
    
    table_frame.mainloop()


# awwel fenetre elli bch naatiw feha le nombre de mois
root = tkb.Window(themename="darkly")

root.title("Optimisation de la Production de l'Entreprise ChausseTous")
root.geometry("+0+0")

title_label = tk.Label(root, text="")
title_label.pack(pady=5)

nb_mois = 1
nb_mois_label = tk.Label(root, text="Nombre de mois:")
nb_mois_entry = tk.Entry(root)
nb_mois_entry.insert(tk.END, nb_mois)  

# Center label and entry horizontally
nb_mois_label.pack(side=tk.TOP, anchor=tk.CENTER)
nb_mois_entry.pack(side=tk.TOP, anchor=tk.CENTER)

# Center button horizontally and vertically
continue_button = tk.Button(root, text="Continuer", command=pl2)
continue_button.pack(pady=20)
continue_button.pack(side=tk.TOP, anchor=tk.CENTER)

root.mainloop()
    
