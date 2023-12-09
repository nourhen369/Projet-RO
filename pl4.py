import tkinter as tk
from tkinter import messagebox
import gurobipy as gp
from gurobipy import GRB
import main
import os

result_text = None 
def create_main_interface(num_regions):   
 def solve_optimization():
    try:
        
        budget = float(budget_entry.get())
        agency_cost = float(agency_cost_entry.get())
        dab_cost = float(dab_cost_entry.get())
        coeff_a = float(coeff_a_entry.get())
        coeff_b = float(coeff_b_entry.get())
        coeff_c = float(coeff_c_entry.get())

        # Retrieve population data from the Entry widgets and parse them into a list
        population_list = []
        for i in range(num_regions):
            region_population = float(population_entries[i].get())
            population_list.append(region_population)

        # Retrieve adjacency matrix values from the Entry widgets
        adjacency_matrix_values = []
        for i in range(num_regions):
            row_values = []
            for j in range(num_regions):
                value = int(adjacency_entries[i][j].get())
                row_values.append(value)
            adjacency_matrix_values.append(row_values)

        # Create a new optimization model
        model = gp.Model("BankBranchesOptimization")

        # Decision Variables
        x = model.addVars(num_regions, vtype=GRB.BINARY, name="x")  # Binary decision variables for agencies

        # Objective Function
        obj = gp.LinExpr()
        for i in range(num_regions):
            sum_neighboring_population = sum(adjacency_matrix_values[i][j] * population_list[j] for j in range(num_regions))
            obj += x[i] * (coeff_a * population_list[i] + coeff_b * sum_neighboring_population) + coeff_c * population_list[i]

        model.setObjective(obj, sense=GRB.MAXIMIZE)

        # Constraints
        model.addConstr(sum(agency_cost * x[i] for i in range(num_regions)) + sum(dab_cost * x[i] for i in range(num_regions)) <= budget, "BudgetConstraint")

        # Solve the model
        model.optimize()

        # Display the optimal solution or relevant information
        if model.status == GRB.OPTIMAL:
            optimal_solution = "Optimal solution found:\n"
            for i in range(num_regions):
                if x[i].x > 0.5:
                    optimal_solution += f"Open agency in region {i + 1}\n"
            optimal_solution += f"Total number of clients served: {model.objVal}"
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, optimal_solution)
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Optimization did not converge")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# Create a Tkinter window
 root = tk.Tk()
 root.title("Bank Branches Optimization")



# Default values for parameters
 default_values = {
    "B": 2000000,
    "K": 500000,
    "D": 20000,
    "a": 5,
    "b": 1,
    "c": 2
 }

# GUI elements to input parameters
 budget_label = tk.Label(root, text="Budget:")
 budget_label.grid(row=0, column=0)
 budget_entry = tk.Entry(root)
 budget_entry.insert(tk.END, default_values["B"])  # Set default value for Budget
 budget_entry.grid(row=0, column=1)

 agency_cost_label = tk.Label(root, text="Agency Cost:")
 agency_cost_label.grid(row=1, column=0)
 agency_cost_entry = tk.Entry(root)
 agency_cost_entry.insert(tk.END, default_values["K"])  # Set default value for Agency Cost
 agency_cost_entry.grid(row=1, column=1)

 dab_cost_label = tk.Label(root, text="DAB Cost:")
 dab_cost_label.grid(row=2, column=0)
 dab_cost_entry = tk.Entry(root)
 dab_cost_entry.insert(tk.END, default_values["D"])  # Set default value for DAB Cost
 dab_cost_entry.grid(row=2, column=1)

 coeff_a_label = tk.Label(root, text="Coefficient a (%):")
 coeff_a_label.grid(row=3, column=0)
 coeff_a_entry = tk.Entry(root)
 coeff_a_entry.insert(tk.END, default_values["a"])  # Set default value for Coefficient a
 coeff_a_entry.grid(row=3, column=1)

 coeff_b_label = tk.Label(root, text="Coefficient b (%):")
 coeff_b_label.grid(row=4, column=0)
 coeff_b_entry = tk.Entry(root)
 coeff_b_entry.insert(tk.END, default_values["b"])  # Set default value for Coefficient b
 coeff_b_entry.grid(row=4, column=1)

 coeff_c_label = tk.Label(root, text="Coefficient c (%):")
 coeff_c_label.grid(row=5, column=0)
 coeff_c_entry = tk.Entry(root)
 coeff_c_entry.insert(tk.END, default_values["c"])  # Set default value for Coefficient c
 coeff_c_entry.grid(row=5, column=1)

 population_label = tk.Label(root, text="Population for each region:")
 population_label.grid(row=6, column=0)



# Create Entry widgets for population input for each region with default values
 population_entries = []
 for i in range(num_regions):
    label = tk.Label(root, text=f"Region {i+1}:")
    label.grid(row=6 + i, column=0)
    entry = tk.Entry(root)
    entry.grid(row=6 + i, column=1)
    population_entries.append(entry)

 adjacency_label = tk.Label(root, text="Adjacency Matrix (0 or 1):")
 adjacency_label.grid(row=6, column=2)

# Default adjacency matrix

# Create Entry widgets for adjacency matrix with default values
 adjacency_entries = []
 for i in range(num_regions):
    row_entries = []
    for j in range(num_regions):
        value = tk.StringVar()
        entry = tk.Entry(root, width=3, textvariable=value)
        entry.grid(row=6 + i, column=3 + j)
        row_entries.append(entry)
    adjacency_entries.append(row_entries)

 solve_button = tk.Button(root, text="Solve", command=solve_optimization)
 solve_button.grid(row=6 + num_regions, columnspan=2)

 result_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)
 result_text.grid(row=7 + num_regions, columnspan=4)


 root.mainloop()

# Your existing code to create the Tkinter window to input the number of regions...
def get_num_regions():
    global num_regions_entry

    try:
        num_regions = int(num_regions_entry.get())
        if num_regions <= 0:
            messagebox.showerror("Error", "Please enter a valid positive number of regions.")
        else:
            root.destroy()  # Close the current window
            create_main_interface(num_regions)  # Pass the Entry widget to the function

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric value for the number of regions.")

# Create a Tkinter window to input the number of regions
root = tk.Tk()
root.title("Enter Number of Regions")

num_regions_label = tk.Label(root, text="Enter the number of regions:")
num_regions_label.pack()

num_regions_entry = tk.Entry(root)
num_regions_entry.pack()

proceed_button = tk.Button(root, text="Proceed", command=get_num_regions)
proceed_button.pack()
def go_to_homepage():
    os.system("Projet-ro/main.py")

home_button = tk.Button(root, text="Go to Home Page", command=go_to_homepage)
home_button.pack()

root.mainloop()