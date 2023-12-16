import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap import *
from ttkbootstrap.constants import *
import gurobipy as gp
import numpy as np

class Exo3:
    def __init__(self, root):
        self.root = root
        self.root.title("PL 1")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.geometry("+350+100")

        self.setup_styles()
        self.create_table_frame()
        self.create_constraints_frame()
        self.create_buttons_frame()
        self.create_result_frame()
        self.create_result_label()

    def setup_styles(self):
        style = Style(theme='darkly')

    def create_table_frame(self):
        self.table_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.table_frame.pack(padx=10, pady=10)
        self.create_table_labels()
        self.create_entry_widgets()

    def create_table_labels(self):
        self.row_labels = ["Jour :   ","Minimum requis :    "]
        self.jourDeLaSemaine = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

        for j, label_text in enumerate(self.jourDeLaSemaine):
            label = tk.Label(self.table_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=0, column=j+1, padx=2, pady=2, sticky='nsew', rowspan=2)

        for i, label_text in enumerate(self.row_labels):
            label = tk.Label(self.table_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=i+1, column=0, padx=2, pady=2, sticky='nsew')

    def create_entry_widgets(self):
        self.entries = [[ttk.Entry(self.table_frame, width=8) for _ in range(7)] for _ in range(1)]
        for i in range(1):
            for j in range(7):
                entry = self.entries[i][j]
                entry.grid(row=i+2, column=j+1, padx=2, pady=2, sticky='nsew')
                entry_style = ttk.Style()
                entry_style.configure('Black.TEntry', foreground='white')
                entry.configure(style='Black.TEntry')
                entry.bind('<FocusOut>', lambda event, i=i, entry=entry: self.validate_entry(event, i, entry))

    def create_constraints_frame(self):
        # Create a frame for constraints
        constraints_frame = ttk.Frame(self.root)
        constraints_frame.pack(pady=10)

        # Create input labels and entries for constraints
        ttk.Label(constraints_frame, text="La seule contrainte est: ").grid(row=0, column=0, sticky='w')

        ttk.Label(constraints_frame, text="Chaque employé doit travailler pendant ").grid(row=1, column=0, sticky='w')
        self.ct1 = tk.StringVar()
        self.ct1.trace_add("write", self.update_ct2)
        ttk.Entry(constraints_frame, textvariable=self.ct1, width=3).grid(row=1, column=1)

        ttk.Label(constraints_frame, text=" jours consécutifs avant de prendre ").grid(row=1, column=2, sticky='w')
        self.ct2 = ttk.Entry(constraints_frame, width=3)
        self.ct2.grid(row=1, column=3)

        ttk.Label(constraints_frame, text=" jours de congé.").grid(row=1, column=4, sticky='w')

        # Initial update of ct2 based on the default value of ct1 (if any)
        self.ct2.bind('<Key>', lambda e: 'break')
        self.update_ct2()

    def update_ct2(self, *args):
        # Update the value of self.ct2 based on the formula: 7 - int(self.ct1.get())
        try:
            ct1_value = int(self.ct1.get())
            ct2_value = 7 - ct1_value
            self.ct2.delete(0, tk.END)
            self.ct2.insert(0, str(ct2_value))
        except ValueError:
            # Handle the case when the user enters a non-integer value in self.ct1
            pass


    
    def create_buttons_frame(self):
        button_frame = tk.Frame(self.root, bg='#2E2E2E')
        button_frame.pack(pady=10)

        self.resoudre_button = ttk.Button(button_frame, text="Résoudre", command=self.resoudre, style='TButton')
        self.resoudre_button.pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Valeurs par défauts", command=self.default_values, style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Reset", command=self.reset_values, style='TButton').pack(side=tk.LEFT, padx=10)

    def create_result_frame(self):
        # Create a LabelFrame with the 'info' style
        result_frame = ttk.Frame(self.root)
        result_frame.pack(padx=10, pady=10)

        # Create a ttk.Treeview widget
        self.table = ttk.Treeview(result_frame, columns=('Column1', 'Column2'), show='headings')

        # Define column headings
        self.table.heading('Column1', text='Jour de la semaine')
        self.table.heading('Column2', text="Nombre optimal d'employés")

        # Insert data into the table
        for day in self.jourDeLaSemaine:
            # Add an empty string as a placeholder for the second column
            self.table.insert('', 'end', values=[day, ''])

        # Pack the table
        self.table.pack(expand=True, fill='both')

    def create_result_label(self):
        self.result_label = tk.Label(self.root, text="", bg='#2E2E2E', fg='white')
        self.result_label.pack()

    def reset_values(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.result_label.config(text="")

        for item in self.table.get_children():
            self.table.delete(item)
        for day in self.jourDeLaSemaine:
            # Add an empty string as a placeholder for the second column
            self.table.insert('', 'end', values=[day, ''])
        
        self.ct1.delete(0, tk.END)
        self.ct2.delete(0, tk.END)

    def default_values(self):
        default_table_values_list = [
            [17, 13, 15, 19, 14, 16, 11],
        ]

        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                value = default_table_values_list[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, str(value))

        # Reset the values of StringVar objects
        self.ct1.set(str(5))

        self.ct2.delete(0, tk.END)
        self.ct2.insert(0, str(2))
        

    def resoudre(self):
        try:
            # Creation du modele
            model = gp.Model("Exo3")

            nb_jrs_travail = int(self.ct1.get())  # nombre de jours de travail consecutifs avant congé
            nb_jrs_semaine = 7
            jours_de_conges = np.zeros((nb_jrs_semaine, nb_jrs_semaine), dtype=int)

            for i in range(nb_jrs_semaine):
                for j in range(nb_jrs_travail):
                    jours_de_conges[i, (i+j+nb_jrs_semaine-nb_jrs_travail) % nb_jrs_semaine] = 1

            print("Jour de congès: \n", jours_de_conges)

            self.jours=[]
            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    self.jours.append(int(entry.get()))

            # les variables de décision représentant les employés prenant Y jours de congés à partir du jour i
            x=[]
            for i in range(7):
                x.append(model.addVar(lb = 0 ,vtype = gp.GRB.INTEGER, name='x'+str(i))) # model.add -> ajouter les var de decision

            # la fonction objectif
            model.setObjective(gp.quicksum(x), gp.GRB.MINIMIZE) #gb.quicksum -> faire un calcul lineaire rapide; gb.GRB.MINIMIZE -> minimiser la fct obj

            # Contraintes : le nombre d'employé doit être >= au minimum requis pour un tel jour
            for j in range(7):
                model.addConstr(gp.quicksum(jours_de_conges[:,j] * x) >= self.jours[j]) # jours_de_conges[:, j] retrieves all the elements in the j-th column of the jours_de_conges matrix

            # Optimiser le modèle
            model.optimize()

            # Une liste qui contient le nb des employes qui sont en congés pendant chaque jour
            nb = []
            for i,v in enumerate(model.getVars()):
                nb.append(int(v.x)) # v.x retrieves the solution value of the variable v after the optimization has been performed

            result=[]
            for i in range(7):
                val = model.objVal - ( nb[i] + nb[i-1] ) #mode.objVal -> represents the optimal value of the objective function after solving an optimization model
                result.append(int(val))

            # Clear existing items in the table
            for item in self.table.get_children():
                self.table.delete(item)

            # Insert values ( resultats ) into the table
            for day, nombre in zip(self.jourDeLaSemaine, result):
                self.table.insert('', 'end', values=[day, nombre])

            self.result_label.config(text=f"Nombre total des employés : {str(int(model.objVal))}")

        except Exception as e:
            # Display a separate warning window for the exception
            warning_window = tk.Toplevel(self.root)
            warning_window.title("Warning")
            warning_window.geometry("+500+250")
            warning_window.configure(bg='red')  # Set the background color to red
            warning_window.attributes("-alpha", 1)  # Set the alpha channel for transparency
            
            label_text = "ERROR OCCURRED!"
            label = tk.Label(warning_window, text=label_text, fg='white', bg='red', font=("Helvetica", 14, "bold"))
            label.pack(padx=50, pady=50)
            
            # Set label background to transparent
            label.configure(bg=warning_window.cget('bg'))

            print(e)

    def validate_entry(self, event, index, entry):
        try:
            value = int(entry.get())
            if value < 0:
                raise ValueError("Please enter a positive number.")
            if not value.is_integer():
                raise ValueError("Please enter a whole number.")
            else:
                entry.delete(0, tk.END)
                entry.insert(0, str(int(value)))
            self.resoudre_button.config(state=tk.NORMAL)
        except ValueError:
            self.resoudre_button.config(state=tk.DISABLED)
            warning_window = tk.Toplevel(self.root)
            warning_window.title("Warning")
            warning_window.geometry("+500+250")
            warning_window.configure(bg='red')
            warning_window.attributes("-alpha", 1)

            label_text = "PLEASE ENTER A POSITIVE WHOLE NUMBER!"
            label = tk.Label(warning_window, text=label_text, fg='white', bg='red', font=("Helvetica", 14, "bold"))
            label.pack(padx=50, pady=50)
            label.configure(bg=warning_window.cget('bg'))

            entry.delete(0, tk.END)
            entry.insert(0, "0")


if __name__ == "__main__":
    root = tk.Tk()
    app = Exo3(root)
    root.mainloop()

    

