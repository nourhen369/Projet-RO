import tkinter as tk
from tkinter import messagebox
import gurobipy as gp
from gurobipy import GRB
import ttkbootstrap as tkb

def pl2():
    def create_heures_sup_entries(nb_mois):
        heures_sup_entries = []
        for i in range(nb_mois):
            heures_sup_entries_label = tk.Label(root, text=f"Maximum d'heures supplémentaires par mois{i+1}:")
            heures_sup_entries_label.grid(row=2+i, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["heures_sup"]) 
            entry.grid(row=2+i, column=1)
            heures_sup_entries.append(entry)
        return heures_sup_entries    
    def create_nb_chaussures_entries(nb_mois):
        nb_chaussures_entries = []
        for i in range(nb_mois):
            nb_chaussures_entries_label = tk.Label(root, text=f"Nombre de paires de chaussures fabriquées à la fin du mois{i+1}:")
            nb_chaussures_entries_label.grid(row=2+nb_mois+i, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["nb_chaussures"]) 
            entry.grid(row=2+nb_mois+i, column=1)
            nb_chaussures_entries.append(entry)
        return nb_chaussures_entries 
    def create_nb_ouv_rec_entries(nb_mois):
        nb_ouv_rec_entries = []
        for i in range(nb_mois):
            nb_ouv_rec_entries_label = tk.Label(root, text=f"Nombre de recrutés en début de mois {i+1}:")
            nb_ouv_rec_entries_label.grid(row=2+2*nb_mois+i, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["nb_ouv_rec"]) 
            entry.grid(row=2+i+2*nb_mois, column=1)
            nb_ouv_rec_entries.append(entry)
        return nb_ouv_rec_entries  
    def create_nb_ouv_lic_entries(nb_mois):
        nb_ouv_lic_entries = []
        for i in range(nb_mois):
            nb_ouv_lic_entries_label = tk.Label(root, text=f"Nombre de licenciés en début de mois {i+1}:")
            nb_ouv_lic_entries_label.grid(row=2+3*nb_mois+i, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["nb_ouv_lic"]) 
            entry.grid(row=2+i+3*nb_mois, column=1)
            nb_ouv_lic_entries.append(entry)
        return nb_ouv_lic_entries  
    def create_stock_entries(nb_mois):
        stock_entries = []
        for i in range(nb_mois):
            stock_par_mois_label = tk.Label(root, text=f"Stock au mois {i+1}:")
            stock_par_mois_label.grid(row=2+i+4*nb_mois, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["stock_par_mois"]) 
            entry.grid(row=2+i+4*nb_mois, column=1)
            stock_entries.append(entry)
        return stock_entries   
    def create_nb_ouvriers_init_entries(nb_mois):
        nb_ouvriers_init_entries = []
        for i in range(nb_mois):
            nb_ouvriers_init_label = tk.Label(root, text=f"Ouvriers disponibles au mois {i+1}:")
            nb_ouvriers_init_label.grid(row=2+i+5*nb_mois, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["nb_ouv_init"]) 
            entry.grid(row=2+i+5*nb_mois, column=1)
            nb_ouvriers_init_entries.append(entry)
        return nb_ouvriers_init_entries 
############################# 2eme colonne #############################
    def create_demand_entries(nb_mois):
        demand_entries = []
        for i in range(nb_mois):
            demande_par_mois_label = tk.Label(root, text=f"Demande au mois {i+1}:")
            demande_par_mois_label.grid(row=2+i+6*nb_mois, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["demande_par_mois"]) 
            entry.grid(row=2+i+6*nb_mois, column=1)
            demand_entries.append(entry)
        return demand_entries   
    def create_cout_stockage_paire_chaussure_entries(nb_mois):
        cout_stockage_paire_chaussure_entries = []
        for i in range(nb_mois):
            cout_stockage_paire_chaussure_label = tk.Label(root, text=f"Cout de stockage d'une paire de chaussures au mois {i+1}:")
            cout_stockage_paire_chaussure_label.grid(row=3+i, column=4, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["cout_stockage_paire_chaussure"]) 
            entry.grid(row=3+i, column=5)
            cout_stockage_paire_chaussure_entries.append(entry)
        return cout_stockage_paire_chaussure_entries     
    def create_salaires_entries(nb_mois):
        salaires_entries = []
        for i in range(nb_mois):
            salaires_entries_label = tk.Label(root, text=f"Salaire de chaque employé au mois {i+1}:")
            salaires_entries_label.grid(row=3+nb+i, column=4, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["salaires"]) 
            entry.grid(row=3+nb+i, column=5)
            salaires_entries.append(entry)
        return salaires_entries  
    def create_cout_mat_paire_chaussure_entries(nb_mois):
        cout_mat_paire_chaussure_entries = []
        for i in range(nb_mois):
            cout_mat_paire_chaussure_label = tk.Label(root, text=f"Cout de matières premières au mois {i+1}:")
            cout_mat_paire_chaussure_label.grid(row=8+nb+i, column=0, sticky="w")
            entry = tk.Entry(root)
            entry.insert(tk.END, default_values["cout_mat_paire_chaussure"]) 
            entry.grid(row=8+nb+i, column=1)
            cout_mat_paire_chaussure_entries.append(entry)
        return cout_mat_paire_chaussure_entries      
    
    def solve_optimization():
        try: 
            # Create a new optimization model
            model = gp.Model("ProductionOptimization")

            # Decision Variables
            NHS = create_heures_sup_entries(nb)
            NCH = create_nb_chaussures_entries(nb)
            NOR = create_nb_ouv_rec_entries(nb)
            NOL = create_nb_ouv_lic_entries(nb)

            # Variables auxilieres
            S = create_stock_entries(nb)
            NO = create_nb_ouvriers_init_entries(nb)

            # Parameters
            cout_stock_chaussures = create_cout_stockage_paire_chaussure_entries(nb)
            salaires = create_salaires_entries(nb)
            prix_heure_supp = float(demande_par_mois_entry.get())
            cout_recrutement_ouvrier = float(recrutement_par_mois_entry.get())
            cout_licenciement_ouvrier = float(licenciement_par_mois_entry.get())
            cout_mat_paire_chaussure = create_cout_mat_paire_chaussure_entries(nb)
            demande = create_demand_entries(nb)
            nb_heures_travail = int(working_hours_par_mois_entry.get())

            c = []
            for i in range(nb):
                c.append(float(NHS[i].get()) * prix_heure_supp + float(salaires[i].get()) * float(NO[i].get()) + float(cout_stock_chaussures[i].get()) * float(S[i].get()) + float(cout_mat_paire_chaussure[i].get()) * float(NCH[i].get()) + float(cout_recrutement_ouvrier) * float(NOR[i].get()) + float(cout_licenciement_ouvrier) * float(NOL[i].get()))
            ct = sum(c)

            # Objective Function
            model.setObjective(ct, gp.GRB.MINIMIZE)
            
            # Constraints
            for i in range(nb):
                # les heures supplémentaires
                model.addConstr(float(NHS[i].get()) <= prix_heure_supp * float(NO[i].get()))
                # la production et la demande
                model.addConstr(int(S[i].get()) + int(NCH[i].get()) >= int(demande[i].get()))
                # la production et les heures supp
                model.addConstr(int(NCH[i].get()) <= 1/(nb*(float(NHS[i].get()) + float(NO[i].get())*nb_heures_travail)))
                if(i>0):
                    # effectif
                    model.addConstr(float(NO[i].get()) == float(NO[i-1].get()) + float(NOR[i].get()) - float(NOL[i].get()))
                    # stock
                    model.addConstr(int(S[i].get()) == int(S[i-1].get()) + int(NCH[i].get()) - int(demande[i].get()))

            # Solve the model
            model.optimize()

            # Display the optimal solution or relevant information
            if model.status == GRB.OPTIMAL:
                # Display optimal total cost
                print(f"Cout total Optimal: {model.objVal:.2f}")

                # Display optimal production plan for each month
                for i in range(nb):
                    print(f"Mois {i+1}:")
                    print(f"\tNombre de chaussures produites: {NCH[i].x:.0f}")
                    print(f"\tNombre d'heures supplémentaires: {NHS[i].x:.2f}")
                    print(f"\tNombre des recrutés: {NOR[i].x:.0f}")
                    print(f"\tNombre des licencés: {NOL[i].x:.0f}")
                    print(f"\tStock vers la fin du mois: {S[i].x:.2f}")

                # Display additional relevant information
                print(f"Cout total des heures supplémentaires: {sum(c) - sum(salaires)}")
                print(f"Cout de recrutement: {sum([float(cout_recrutement_ouvrier) * float(NOR[i].x) for i in range(nb)])}")
                print(f"Cout de licenciement: {sum([float(cout_licenciement_ouvrier) * float(NOL[i].x) for i in range(nb)])}")

            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "L'optimisation n'a pas convergé")
                messagebox.showwarning("Warning", "Le modèle n’a pas pu être résolu de manière optimale.")
        except ValueError:
            messagebox.showerror("Error", "Veuillez saisir des valeurs numériques valides.")


    # Create a Tkinter window
    root = tk.Tk()
    root.title("Optimisation de la Production de l'Entreprise ChausseTous")

    nb = nombre_mois()
    
    # Default values for parameters
    default_values = {
        "nb_mois": 1,
        "heures_sup": 20,
        "nb_chaussures": 3000,
        "nb_ouv_rec": 100,
        "nb_ouv_lic": 100,
        "stock_par_mois": 500,
        "nb_ouv_init": 100,
        "create_demand_entries": 3000,
        "salaires": 1500,
        "cout_recrutement_ouvrier": 1600,
        "cout_licenciement_ouvrier": 2000,
        "nb_heures_travail_par_ouvrier": 160,
        "nb_heures_max_supplementaires": 20, 
        "cout_stockage_paire_chaussure": 3,
        "cout_heure_supplementaire_ouvrier": 13,
        "cout_mat_paire_chaussure": 15,
        "heures_travail_paire_chaussure": 4,
        "demande_par_mois": 3000,
    }

    # GUI elements to input parameters
    nb_mois_label = tk.Label(root, text=f"Nombre de mois:  {nombre_mois()}")
    nb_mois_label.grid(row=0, columnspan=5)

    create_heures_sup_entries(nb)
    create_nb_chaussures_entries(nb)
    create_nb_ouv_rec_entries(nb)
    create_nb_ouv_lic_entries(nb)
    create_stock_entries(nb)
    create_nb_ouvriers_init_entries(nb)
    create_demand_entries(nb)
########################
    # create the entry of the cost of an additional hour
    demande_par_mois_label = tk.Label(root, text="Cout d'une heure supplémentaire:")
    demande_par_mois_label.grid(row=2, column=4, sticky="w")
    demande_par_mois_entry = tk.Entry(root)
    demande_par_mois_entry.insert(tk.END, default_values["cout_recrutement_ouvrier"]) 
    demande_par_mois_entry.grid(row=2, column=5)
    create_cout_stockage_paire_chaussure_entries(nb)
    create_salaires_entries(nb)
    # create the entry of "frais de recrutement"
    recrutement_par_mois_label = tk.Label(root, text="Couts de recruitment:")
    recrutement_par_mois_label.grid(row=3+2*nb, column=4, sticky="w")
    recrutement_par_mois_entry = tk.Entry(root)
    recrutement_par_mois_entry.insert(tk.END, default_values["cout_recrutement_ouvrier"]) 
    recrutement_par_mois_entry.grid(row=3+2*nb, column=5)
    # create the entry of  "frais de licenciement"
    licenciement_par_mois_label = tk.Label(root, text="Couts de licenciement:")
    licenciement_par_mois_label.grid(row=4+2*nb, column=4, sticky="w")
    licenciement_par_mois_entry = tk.Entry(root)
    licenciement_par_mois_entry.insert(tk.END, default_values["demande_par_mois"]) 
    licenciement_par_mois_entry.grid(row=4+2*nb, column=5)
    # create the entry of total working hours per month
    working_hours_par_mois_label = tk.Label(root, text="Nombre d'heures de travail pour chaque employé:")
    working_hours_par_mois_label.grid(row=5+2*nb, column=4, sticky="w")
    working_hours_par_mois_entry = tk.Entry(root)
    working_hours_par_mois_entry.insert(tk.END, default_values["nb_heures_travail_par_ouvrier"]) 
    working_hours_par_mois_entry.grid(row=5+2*nb, column=5)

    solve_button = tk.Button(root, text="Résoudre", command=solve_optimization)
    solve_button.grid(row=7+2*nb, column=4)

    result_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)
    result_text.grid(row=7+2*nb, column=5)

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

root = tkb.Window(themename="darkly")

root.title("Optimisation de la Production de l'Entreprise ChausseTous")
root.geometry("400x200+800+200")

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
solve_button = tk.Button(root, text="Continuer", command=pl2)
solve_button.pack(pady=20)
solve_button.pack(side=tk.TOP, anchor=tk.CENTER)

root.mainloop()

