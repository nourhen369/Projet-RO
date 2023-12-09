import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import gurobipy as gp

class Exo1:
    def __init__(self, root):
        self.root = root
        self.root.title("PL 1")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.geometry("+350+100")

        self.setup_styles()
        self.create_table_frame()
        self.create_constraints_constants_frame()
        self.create_buttons_frame()
        self.create_result_label()

    def setup_styles(self):
        style = ttk.Style(theme='darkly')

    def create_table_frame(self):
        self.table_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.table_frame.pack(padx=10, pady=10)
        self.create_table_labels()
        self.create_entry_widgets()

    def create_table_labels(self):
        self.row_labels = ["Rendement", "Prix de vente", "Nombre ouvriers", "Temps machine", "Eau", "Salaire annuel/ouvrier", "Frais fixe de gestion"]
        self.column_labels = ["Blé", "Orge", "Mais", "Bet-sucre", "Tournesol"]

        for j, label_text in enumerate(self.column_labels):
            label = tk.Label(self.table_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=0, column=j+1, padx=2, pady=2, sticky='nsew', rowspan=2)

        for i, label_text in enumerate(self.row_labels):
            label = tk.Label(self.table_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=i+2, column=0, padx=2, pady=2, sticky='nsew')

    def create_entry_widgets(self):
        self.entries = [[ttk.Entry(self.table_frame, width=8) for _ in range(5)] for _ in range(7)]
        for i in range(7):
            for j in range(5):
                entry = self.entries[i][j]
                entry.grid(row=i+2, column=j+1, padx=2, pady=2, sticky='nsew')
                entry_style = ttk.Style()
                entry_style.configure('Black.TEntry', foreground='white')
                entry.configure(style='Black.TEntry')

    def create_constraints_constants_frame(self):
        constraints_constants_frame = tk.Frame(self.root, bg='#2E2E2E')
        constraints_constants_frame.pack(padx=10, pady=(0, 20))  # Add more space at the bottom

        self.create_constraints_frame(constraints_constants_frame)
        
        # Add vertical separator
        ttk.Separator(constraints_constants_frame, orient=tk.VERTICAL).grid(row=1, column=2, rowspan=6, sticky='ns', padx=(20,20))

        self.create_constants_frame(constraints_constants_frame)

    def create_constraints_frame(self, parent_frame):
        label = tk.Label(parent_frame, text='Les contraintes', bg='#2E2E2E', fg='white')
        label.grid(row=0, column=0, padx=2, pady=20, sticky='nsew', columnspan=2)

        constraint_labels = ["Main d'oeuvre <", "Eau d'irrigation <", "Temps machines <"]
        self.constraint_entries = []

        for i, label_text in enumerate(constraint_labels):
            label = tk.Label(parent_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=i + 1, column=0, padx=2, pady=2, sticky='nsew')

            entry = ttk.Entry(parent_frame, width=8, style='Dark.TEntry')
            entry.grid(row=i + 1, column=1, padx=2, pady=2, sticky='nsew')
            self.constraint_entries.append(entry)

    def create_constants_frame(self, parent_frame):
        label = tk.Label(parent_frame, text='Les constantes', bg='#2E2E2E', fg='white')
        label.grid(row=0, column=3, padx=2, pady=20, sticky='nsew', columnspan=2)

        constant_labels = ["Zone Agricole", "Cout heure machine", "Cout metre cube eau"]
        self.constant_entries = []

        for i, label_text in enumerate(constant_labels):
            label = tk.Label(parent_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=i + 1, column=3, padx=2, pady=2, sticky='nsew')

            entry = ttk.Entry(parent_frame, width=8, style='Dark.TEntry')
            entry.grid(row=i + 1, column=4, padx=2, pady=2, sticky='nsew')

            self.constant_entries.append(entry)

    def create_buttons_frame(self):
        button_frame = tk.Frame(self.root, bg='#2E2E2E')
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Menu Principale", command=self.show_menu, style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Valeurs par défauts", command=self.default_values, style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_values, style='TButton').pack(side=tk.LEFT, padx=5)

        # Create a new frame for the "Calculate" button and pack it separately
        calculate_frame = tk.Frame(self.root, bg='#2E2E2E')
        calculate_frame.pack(pady=5)
        ttk.Button(calculate_frame, text="Calculate", command=self.run, style='TButton').pack(side=tk.LEFT, padx=5)



    def create_result_label(self):
        self.result_label = tk.Label(self.root, text="", bg='#2E2E2E', fg='white')
        self.result_label.pack()

    def calculate_sum(self):
        total_sum = sum([float(entry.get()) for row in self.entries for entry in row if entry.get().replace('.', '').isdigit()])
        self.result_label.config(text=f"Total Sum: {total_sum}")

    def reset_values(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.result_label.config(text="")

    def show_menu(self):
        self.result_label.config(text="Menu Principale clicked")

    def default_values(self):
        default_table_values_list = [
            [70, 60, 55, 50, 60],
            [60, 50, 66, 110, 60],
            [2, 1, 2, 3, 2],
            [30, 24, 20, 28, 25],
            [3000, 2000, 2500, 3800, 3200],
            [500, 500, 600, 700, 550],
            [250, 180, 190, 310, 320]
        ]

        default_constraints_values_list = [3000, 25000000, 24000]
        default_constants_values_list = [1000, 30, 0.1]

        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                value = default_table_values_list[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, str(value))

        for i, constraint_entry in enumerate(self.constraint_entries):
            value = default_constraints_values_list[i]
            constraint_entry.delete(0, tk.END)
            constraint_entry.insert(0, str(value))

        for i, constant_entry in enumerate(self.constant_entries):
            value = default_constants_values_list[i]
            constant_entry.delete(0, tk.END)
            constant_entry.insert(0, str(value))

    def run(self):
        try:
            model = gp.Model("Exo1")

            self.Rendement, self.Prix_vente, self.main_doeuvre, self.Temps_machine, self.Eau, self.Salaire_annuel, self.Frais_gestion= [], [], [], [], [], [], []
            Attributs = [self.Rendement, self.Prix_vente, self.main_doeuvre, self.Temps_machine, self.Eau, self.Salaire_annuel, self.Frais_gestion]
            Constantes=[]
            Contraintes=[]

            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    Attributs[i].append(float(entry.get()))

            for i, entry in enumerate(self.constraint_entries):
                Contraintes.append(float(entry.get()))

            
            for i, entry in enumerate(self.constant_entries):
                Constantes.append(float(entry.get())) 

            zoneAgricole=Constantes[0]
            coutHeureMachine=Constantes[1]
            coutEau=Constantes[2]

            mainOeuvre=Contraintes[0]
            quantiteEau=Contraintes[1]
            tempsMachine=Contraintes[2]

            x = model.addVars(range(5), vtype=gp.GRB.INTEGER, name="x")

            model.setObjective(gp.quicksum(x[i] * (
                    (self.Rendement[i] * self.Prix_vente[i])
                    - (self.main_doeuvre[i] * self.Salaire_annuel[i])
                    - (self.Temps_machine[i] * coutHeureMachine)
                    - (self.Eau[i] * coutEau)
            ) - self.Frais_gestion[i]
                for i in range(5)), gp.GRB.MAXIMIZE)

            model.addConstr(gp.quicksum((self.main_doeuvre[i] * x[i]) for i in range(5)) <= mainOeuvre)
            model.addConstr(gp.quicksum((self.Temps_machine[i] * x[i]) for i in range(5)) <= tempsMachine)
            model.addConstr(gp.quicksum((self.Eau[i] * x[i]) for i in range(5)) <= quantiteEau)
            for i in range(5):
                model.addConstr(x[i] >= 0)
            model.addConstr(gp.quicksum(x[i] for i in range(5)) <= zoneAgricole)

            model.optimize()

            result_window = tk.Toplevel(self.root)
            result_window.title("Results")
            result_window.geometry("+500+250")

            text_widget = tk.Text(result_window, wrap=tk.WORD, width=40, height=10)
            text_widget.pack(padx=10, pady=10)

            for i, v in enumerate(model.getVars()):
                text_widget.insert(tk.END, f"{self.column_labels[i]}: {abs(int(v.x))} Hectares\n-------------\n")

            text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
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


        #print(coutHeureMachine)


if __name__ == "__main__":
    root = tk.Tk()
    app = Exo1(root)
    root.mainloop()
