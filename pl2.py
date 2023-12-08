import tkinter as tk
from tkinter import messagebox
import gurobipy as gp
from gurobipy import GRB

def pl2():
    def solve_optimization():
        try:
            # Retrieve parameter values from the GUI entries
            nb_ouvriers_initiaux = int(nb_ouvriers_initiaux_entry.get())
            nb_heures_travail_par_ouvrier = int(nb_heures_travail_par_ouvrier_entry.get())
            nb_heures_max_supplementaires = int(nb_heures_max_supplementaires_entry.get())
            cout_recrutement_ouvrier = float(cout_recrutement_ouvrier_entry.get())
            cout_licenciement_ouvrier = float(cout_licenciement_ouvrier_entry.get())
            cout_stockage_paire_chaussure = float(cout_stockage_paire_chaussure_entry.get()) # depend de nb_mois
            cout_heure_supplementaire_ouvrier = float(cout_heure_supplementaire_ouvrier_entry.get())
            cout_mat_paire_chaussure = float(cout_mat_paire_chaussure_entry.get()) # depend de nb_mois
            heures_travail_paire_chaussure = float(heures_travail_paire_chaussure_entry.get())
            demande_par_mois = float(demande_par_mois_entry.get()) # depend de nb_mois
            stock_init = float(stock_init_entry.get())

            # Create a new optimization model
            model = gp.Model("ProductionOptimization")

            # Decision Variables
            x = {}
            y = {}
            for t in range(nb_mois):
                x[t] = model.addVar(vtype=gp.GRB.INTEGER, name="production_%s" % t) #number of shoes produced in each month
                y[t] = model.addVar(vtype=gp.GRB.INTEGER, name="ouvriers_%s" % t) #number of workers hired in each month
                model.addConstr(x[t] >= demande_par_mois[t])

            # Objective Function
            model.setObjective(
                gp.quicksum(y[t] * cout_recrutement_ouvrier for t in range(nb_mois) if y[t] > 0)
                + gp.quicksum(y[t] * cout_licenciement_ouvrier for t in range(nb_mois) if y[t] < 0)
                + gp.quicksum(
                    x[t] * cout_mat_paire_chaussure + y[t] * nb_heures_travail_par_ouvrier * 1500
                    + (x[t] * heures_travail_paire_chaussure - y[t] * nb_heures_travail_par_ouvrier,
                    nb_heures_max_supplementaires) * cout_heure_supplementaire_ouvrier
                    + (stock_init * cout_stockage_paire_chaussure)
                    for t in range(nb_mois)
                ),
                gp.GRB.MINIMIZE,
            )
            
            # Constraints
            model.addConstr(y[0] == nb_ouvriers_initiaux)
            for t in range(1, nb_mois):
                model.addConstr(y[t] >= y[t - 1] - gp.ceil((nb_ouvriers_initiaux - y[0]) / 5))
                model.addConstr(y[t] <= y[t - 1] + gp.floor((y[0] - nb_ouvriers_initiaux) / 5))
            for t in range(nb_mois):
                model.addConstr(x[t] * heures_travail_paire_chaussure <= y[t] * nb_heures_travail_par_ouvrier + nb_heures_max_supplementaires)
            
            # Solve the model
            model.optimize()

            # Display the optimal solution or relevant information
            if model.status == GRB.OPTIMAL:
                optimal_solution = "Optimal solution found:\n"

                optimal_solution += f"Optimal total cost: {model.objVal:.2f}\nNumber of shoes produced:"
                for t in range(nb_mois):
                    optimal_solution += f"\tMonth {t + 1}: {x[t].x:.0f}"

                optimal_solution += "\nNumber of workers employed:"
                for t in range(nb_mois):
                    optimal_solution += f"\tMonth {t + 1}: {y[t].x:.0f}"

                total_hiring_cost = sum(y[t].x * cout_recrutement_ouvrier for t in range(nb_mois) if y[t].x > 0)
                total_firing_cost = sum(y[t].x * cout_licenciement_ouvrier for t in range(nb_mois) if y[t].x < 0)
                optimal_solution += f"Total cost of hiring: {total_hiring_cost:.2f}"
                optimal_solution += f"Total cost of firing: {total_firing_cost:.2f}"

                # Total cost of overtime
                total_overtime_cost = sum((x[t].x * heures_travail_paire_chaussure - y[t].x * nb_heures_travail_par_ouvrier) * cout_heure_supplementaire_ouvrier for t in range(nb_mois))
                optimal_solution += f"Total cost of overtime: {total_overtime_cost:.2f}"

                # Inventory level at the end of each month
                inventory = [stock_init]
                for t in range(1, nb_mois):
                    inventory.append(inventory[t - 1] + x[t - 1].x - demande_par_mois[t])
                optimal_solution += "Inventory level at the end of each month:"
                for t in range(nb_mois):
                    optimal_solution += f"\tMonth {t + 1}: {inventory[t]:.2f}"

                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, optimal_solution)

            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Optimization did not converge")
                messagebox.showwarning("Warning", "Model could not be solved to optimality.")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

    # Create a Tkinter window
    root = tk.Tk()
    root.title("ChausseTous Entreprise Production Optimization")

    # Default values for parameters
    default_values = {
        "nb_mois": 1,
        "nb_ouvriers_initiaux": 100,
        "nb_heures_travail_par_ouvrier": 160,
        "nb_heures_max_supplementaires": 20, 
        "cout_recrutement_ouvrier": 1600,
        "cout_licenciement_ouvrier": 2000,
        "cout_stockage_paire_chaussure": 3,
        "cout_heure_supplementaire_ouvrier": 13,
        "cout_mat_paire_chaussure": 15,
        "heures_travail_paire_chaussure": 4,
        "demande_par_mois": 3000,
        "stock_init": 500,
    }

    # GUI elements to input parameters
    nb_mois_label = tk.Label(root, text=f"Number of months:  {nombre_mois()}")
    nb_mois_label.grid(row=0, column=0)

    nb_ouvriers_initiaux_label = tk.Label(root, text="Number of initial workers:")
    nb_ouvriers_initiaux_label.grid(row=1, column=0)
    nb_ouvriers_initiaux_entry = tk.Entry(root)
    nb_ouvriers_initiaux_entry.insert(tk.END, default_values["nb_ouvriers_initiaux"])  
    nb_ouvriers_initiaux_entry.grid(row=1, column=1)

    nb_heures_travail_par_ouvrier_label = tk.Label(root, text="Maximum number of working hours per worker:")
    nb_heures_travail_par_ouvrier_label.grid(row=2, column=0)
    nb_heures_travail_par_ouvrier_entry = tk.Entry(root)
    nb_heures_travail_par_ouvrier_entry.insert(tk.END, default_values["nb_heures_travail_par_ouvrier"]) 
    nb_heures_travail_par_ouvrier_entry.grid(row=2, column=1)

    nb_heures_max_supplementaires_label = tk.Label(root, text="Maximum number of overtime hours:")
    nb_heures_max_supplementaires_label.grid(row=3, column=0)
    nb_heures_max_supplementaires_entry = tk.Entry(root)
    nb_heures_max_supplementaires_entry.insert(tk.END, default_values["nb_heures_max_supplementaires"])  
    nb_heures_max_supplementaires_entry.grid(row=3, column=1)

    cout_recrutement_ouvrier_label = tk.Label(root, text="Cost of hiring a worker:")
    cout_recrutement_ouvrier_label.grid(row=4, column=0)
    cout_recrutement_ouvrier_entry = tk.Entry(root)
    cout_recrutement_ouvrier_entry.insert(tk.END, default_values["cout_recrutement_ouvrier"])  
    cout_recrutement_ouvrier_entry.grid(row=4, column=1)

    cout_licenciement_ouvrier_label = tk.Label(root, text="Cost of firing a worker:")
    cout_licenciement_ouvrier_label.grid(row=5, column=0)
    cout_licenciement_ouvrier_entry = tk.Entry(root)
    cout_licenciement_ouvrier_entry.insert(tk.END, default_values["cout_licenciement_ouvrier"]) 
    cout_licenciement_ouvrier_entry.grid(row=5, column=1)

    cout_stockage_paire_chaussure_label = tk.Label(root, text="Cost of storing a pair of shoes:")
    cout_stockage_paire_chaussure_label.grid(row=6, column=0)
    cout_stockage_paire_chaussure_entry = tk.Entry(root)
    cout_stockage_paire_chaussure_entry.insert(tk.END, default_values["cout_stockage_paire_chaussure"]) 
    cout_stockage_paire_chaussure_entry.grid(row=6, column=1)

    cout_heure_supplementaire_ouvrier_label = tk.Label(root, text="Cost of overtime per hour:")
    cout_heure_supplementaire_ouvrier_label.grid(row=7, column=0)
    cout_heure_supplementaire_ouvrier_entry = tk.Entry(root)
    cout_heure_supplementaire_ouvrier_entry.insert(tk.END, default_values["cout_heure_supplementaire_ouvrier"]) 
    cout_heure_supplementaire_ouvrier_entry.grid(row=7, column=1)

    cout_mat_paire_chaussure_label = tk.Label(root, text="Cost of material per pair of shoes:")
    cout_mat_paire_chaussure_label.grid(row=8, column=0)
    cout_mat_paire_chaussure_entry = tk.Entry(root)
    cout_mat_paire_chaussure_entry.insert(tk.END, default_values["cout_mat_paire_chaussure"]) 
    cout_mat_paire_chaussure_entry.grid(row=8, column=1)

    heures_travail_paire_chaussure_label = tk.Label(root, text="Number of hours of work per pair of shoes:")
    heures_travail_paire_chaussure_label.grid(row=9, column=0)
    heures_travail_paire_chaussure_entry = tk.Entry(root)
    heures_travail_paire_chaussure_entry.insert(tk.END, default_values["heures_travail_paire_chaussure"]) 
    heures_travail_paire_chaussure_entry.grid(row=9, column=1)

    demande_par_mois_label = tk.Label(root, text="Demand per month:")
    demande_par_mois_label.grid(row=10, column=0)
    demande_par_mois_entry = tk.Entry(root)
    demande_par_mois_entry.insert(tk.END, default_values["demande_par_mois"]) 
    demande_par_mois_entry.grid(row=10, column=1)

    stock_init_label = tk.Label(root, text="Initial stock:")
    stock_init_label.grid(row=11, column=0)
    stock_init_entry = tk.Entry(root)
    stock_init_entry.insert(tk.END, default_values["stock_init"]) 
    stock_init_entry.grid(row=11, column=1)

    solve_button = tk.Button(root, text="Solve", command=solve_optimization)
    solve_button.grid(row=14, columnspan=2)

    result_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)
    result_text.grid(row=15, columnspan=4)

def nombre_mois():
    try:
        nb_mois = int(nb_mois_entry.get())

        # Validate input value
        if nb_mois <= 0 or nb_mois > 12:
            raise ValueError("Number of months must be between 1 and 12.")

        return nb_mois
    except ValueError as error:
        messagebox.showerror("Error", str(error))
        return None

root = tk.Tk()
root.title("ChausseTous Entreprise Production Optimization")
nb_mois = 1
nb_mois_label = tk.Label(root, text="Number of months:")
nb_mois_label.grid(row=0, column=0)
nb_mois_entry = tk.Entry(root)
nb_mois_entry.insert(tk.END, nb_mois)  
nb_mois_entry.grid(row=0, column=1)

solve_button = tk.Button(root, text="Continue Solving", command=pl2)
solve_button.grid(row=14, columnspan=2)

root.mainloop()

