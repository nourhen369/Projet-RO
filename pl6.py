import tkinter as tk
from tkinter import ttk
import heapq
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Exo6:
    def __init__(self, root):
        self.root = root
        self.root.title("PL 6")
        self.root.geometry("800x600")     
        self.root.resizable(False, False)
        self.root.geometry("+350+100")
        self.links = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['B', 'E', 'F'],
            'D': ['E'],
            'E': ['G'],
            'F': ['E'],
            'G': []
        }
        self.setup_styles()
        self.create_title()
        self.create_resolution()
        self.create_table_frame()
        self.create_result_frame()
        self.create_buttons_frame()

        self.cost_entries = {}
        
        self.create_result_label()
    def setup_styles(self):
        style = ttk.Style(theme='darkly')

    def create_resolution(self):
     ttk.Label(self.root, text="Définir les coûts de transmission dans un réseau IP, où chaque chemin permet le transfert unidirectionnel d'un paquet IP à travers ce réseau.:", foreground='white', background='#000000').pack()
    def create_title(self):
        title_label = tk.Label(self.root, text="Problème de Routage", font=('Arial', 20, 'bold'), bg='#000000', fg='#0000FF')
        title_label.pack(pady=20)


    def create_table_frame(self):
        self.table_frame = tk.Frame(self.root, bg="#000000")
        self.table_frame.pack(padx=10, pady=10)
        self.create_table_labels()
        self.create_entry_widgets()

    def create_table_labels(self):
        self.row_labels = ["Les noueds :   ", "Cout :    "]
        self.noueds = ["A->B", "A->C", "B->D", "B->E", "C->B", "C->E", "C->F", "D->E", "E->G", "F->E"]

        for j, label_text in enumerate(self.noueds):
            label = tk.Label(self.table_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=0, column=j + 1, padx=2, pady=2, sticky='nsew', rowspan=2)

        for i, label_text in enumerate(self.row_labels):
            label = tk.Label(self.table_frame, text=label_text, bg='#2E2E2E', fg='white')
            label.grid(row=i + 1, column=0, padx=2, pady=2, sticky='nsew')

    def create_entry_widgets(self):
        self.entries = [[ttk.Entry(self.table_frame, width=8) for _ in range(10)] for _ in range(1)]
        for i in range(1):
            for j in range(10):
                entry = self.entries[i][j]
                entry.grid(row=i + 2, column=j + 1, padx=2, pady=2, sticky='nsew')
                entry_style = ttk.Style()
                entry_style.configure('Black.TEntry', foreground='Black')
                entry.configure(style='Black.TEntry')

    def create_buttons_frame(self):
        button_frame = tk.Frame(self.root, bg='#2E2E2E')
        button_frame.pack(pady=10)
 
        ttk.Button(button_frame, text="Valeurs par défauts", command=self.default_values, style='TButton').pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_values, style='TButton').pack(side=tk.LEFT, padx=5)

        calculate_frame = tk.Frame(self.root, bg='#2E2E2E')
        calculate_frame.pack(pady=5)
        ttk.Button(calculate_frame, text="Trouver le chemin le plus court", command=self.run_dijkstra, style='TButton').pack(side=tk.LEFT, padx=5)

    def create_result_frame(self):
        self.result_frame = ttk.LabelFrame(self.root, text="     ")
        self.result_frame.pack(padx=10, pady=10)

        ttk.Label(self.result_frame, text="Nœud de départ :").pack()
        self.start_entry = ttk.Entry(self.result_frame, width=8)
        self.start_entry.pack()

        ttk.Label(self.result_frame, text="Nœud d'arrivée :").pack()
        self.end_entry = ttk.Entry(self.result_frame, width=8)
        self.end_entry.pack()


    def create_result_label(self):
        self.result_label = tk.Label(self.root, text="", bg='#2E2E2E', fg='white')
        self.result_label.pack()

    def reset_values(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

    def show_menu(self):
        self.result_label.config(text="Menu Principale clicked")

    def default_values(self):
        default_table_values_list = [
            [4, 3, 3, 6, 5, 4, 6, 6, 5, 5, 2, 1, 3, 6],
        ]

        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                value = default_table_values_list[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, str(value))
    def dijkstra_algorithm(self, costs, start_node, end_node):
        queue = [(0, start_node, [])]
        visited = set()

        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node not in visited:
                visited.add(node)
                path = path + [node]
                if node == end_node:
                    return cost, path
                for next_node in self.links.get(node, []):
                    if next_node not in visited:
                        heapq.heappush(queue, (cost + costs.get((node, next_node), float('inf')), next_node, path))
        return float('inf'), None


    def run_dijkstra(self):
        costs = {}
        for (node_from, node_to), entry in self.cost_entries.items():
            cost = int(entry.get()) if entry.get().isdigit() else 0
            if cost != 0:
                costs[(node_from, node_to)] = cost

        start_node = self.start_entry.get().upper()
        end_node = self.end_entry.get().upper()

        min_cost, shortest_path = self.dijkstra_algorithm(costs, start_node, end_node)
            
        result_label = ttk.Label(self.root, text="", wraplength=250, foreground='red', borderwidth=2, relief='solid')
        result_label.pack(padx=10, pady=10)

        if shortest_path:
         result_label.config(text=f"Chemin le plus court de {start_node} à {end_node} : {' -> '.join(shortest_path)}")
        else:
         result_label.config(text=f"Aucun chemin possible de {start_node} à {end_node}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Exo6(root)
    root.mainloop()