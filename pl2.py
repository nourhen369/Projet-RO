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

    table_frame = tk.PanedWindow(root)
    table_frame.pack(side="top", fill="both", expand=True)
    
    row_labels = ["Nombre d'heures supplémentaires",
                    "Nombre de paires de chaussures fabriqués",
                    "Nombre d'ouvriers recrutés",
                    "Nombre d'ouvriers licencés",
                    "Stock",
                    "Nombre d'ouvriers disponible",
                    "Cout de production d'une paire de chaussure",
                    "Cout de stockage d'une paire de chaussure",
                    "Demande",
                    "#Salaire d'un ouvrier", 
                    "#Coût d'une heure supplémentaire par ouvrier", 
                    "#Frais de recrutement,", 
                    "#Frais de licenciement", 
                    "#: Nombre d'heure nécessaire pour fabriquer une paire de chaussure", 
                    "#Volume horaire mensuel de travail par ouvrier", 
                    "#Nombre d'heures sup max par ouvrier"]
    column_labels = []
    for i in range(nb):
        column_labels.append(f"Mois {i+1}")

    for j, label_text in enumerate(column_labels):
        label = tk.Label(table_frame, text=label_text, bg='#2E2E2E', fg='white')
        label.grid(row=0, column=j+1, padx=2, pady=2, sticky='nsew', rowspan=2)

    for i, label_text in enumerate(row_labels):
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
    table_frame.mainloop()

    def solve_optimization():
        try: 
            # Create a new optimization model
            model = gp.Model(name = "ProductionOptimization")
            
            # Ajoutez les variables de décision au modèle
            for i in range(nb):
                heures_sup = model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"heures_sup_{i+1}")
                paires_chaussures = model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"paires_chaussures_{i+1}")
                ouvriers_rec = model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"ouvriers_rec_{i+1}")
                ouvriers_lic = model.addVar(lb = 0, vtype=gp.GRB.CONTINUOUS, name=f"ouvriers_lic_{i+1}")
            
            # les vars auxilieres
            ouvriers_dispo = {t: model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"ouvriers_dispo_{t}") for t in range(nb)}
            stock = {t: model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"stock_{t}") for t in range(nb)}

            # Update the model to integrate new variables
            model.update

            # mes parametres
            demande = create_demand_entries(nb)
            Hmax = create_nb_max_heures_supp()
            H = int(create_nb_heures_travail_par_ouvrier().get())

            for i in range(nb): 
                if i > 0:
                    model.addConstr(stock[i-1] + paires_chaussures[i] >= int(demande[i].get()))
                    model.addConstr(ouvriers_dispo[i]==ouvriers_dispo[i-1]+ouvriers_rec[i]-ouvriers_lic[i])
                    model.addConstr(stock[i]==stock[i-1]+paires_chaussures[i-1]-demande[i-1])
                model.addConstr(heures_sup[i] <= Hmax*ouvriers_dispo[i])
                model.addConstr(paires_chaussures[i]<=(1/nb)*(1/(heures_sup[i]+ouvriers_dispo[i]*H)))
                # les contraintes de signe 
                model.addConstrs(stock[i] >= 0)
                model.addConstrs(ouvriers_dispo[i] >= 0)
                model.addConstrs(ouvriers_rec[i] >= 0)
                model.addConstrs(ouvriers_lic[i] >= 0)
                model.addConstrs(heures_sup[i] >= 0)

            # Objective Function
            model.setObjective(
                gp.quicksum(
                    ouvriers_rec[t] * float(cout_recrutement_ouvrier) +
                    ouvriers_lic[t] * float(cout_licenciement_ouvrier) +
                    heures_sup[t] * float(prix_heure_supp) +
                    paires_chaussures[t] * float(cout_mat_paire_chaussure[i].get()) +
                    ouvriers_lic[t] * float(salaires[i].get())
                    for t in range(nb)
                ),
                gp.GRB.MINIMIZE)
            
            # Solve the model
            model.optimize()

            # Display the optimal solution or relevant information
            if model.status == GRB.OPTIMAL:
                # Display optimal total cost
                print(f"Cout total Optimal: {model.objVal:.2f}")
                result_text.insert(tk.END, f"Cout total Optimal: {model.objVal:.2f}\n")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "L'optimisation n'a pas convergé")
                messagebox.showwarning("Warning", "Le modèle n’a pas pu être résolu de manière optimale.")
        except ValueError:
            messagebox.showerror("Error", "Veuillez saisir des valeurs numériques valides.")

# awwel fenetre elli bch naatiw feha le nombre de mois
root = tkb.Window(themename="darkly")

root.title("Optimisation de la Production de l'Entreprise ChausseTous")
root.geometry("+0+0")

title_label = tk.Label(root, text="")
title_label.pack(pady=20)

nb_mois = 1
nb_mois_label = tk.Label(root, text="Nombre de mois:")
nb_mois_entry = tk.Entry(root)
nb_mois_entry.insert(tk.END, nb_mois)  

# Center label and entry horizontally
nb_mois_label.pack(side=tk.TOP, anchor=tk.CENTER)
nb_mois_entry.pack(side=tk.TOP, anchor=tk.CENTER)

# Center button horizontally and vertically
continue_button = tk.Button(root, text="Continuer", command=pl2)
continue_button.pack(pady=4)
continue_button.pack(side=tk.TOP, anchor=tk.CENTER)

solve_button = tk.Button(root, text="Résoudre", command=None)
solve_button.pack(pady=2)
solve_button.pack(side=tk.TOP, anchor=tk.CENTER)

title_label = tk.Label(root, text="")
title_label.pack(pady=20)

root.mainloop()
    
