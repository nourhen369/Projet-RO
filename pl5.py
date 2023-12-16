import tkinter as tk
from tkinter import ttk
import ctypes
import random

def mark_cell(event):
    row = event.widget.grid_info()["row"]
    col = event.widget.grid_info()["column"]
    cell_value = selected_value.get()

    if not cell_value:
        return

    labels[row][col].config(text=cell_value)
    combine_zones(row, col, cell_value)



def combine_zones(row, col, cell_value):
    def get_adjacent_cells(r, c):
        return [
            (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)
        ]

    def find_connected_cells(row, col, cell_value, connected):
        queue = [(row, col)]

        while queue:
            current_row, current_col = queue.pop(0)

            if (current_row, current_col) not in connected:
                connected.add((current_row, current_col))
                for nr, nc in get_adjacent_cells(current_row, current_col):
                    if (
                        0 <= nr < len(labels) and 0 <= nc < len(labels[0])
                        and labels[nr][nc].cget("text") == cell_value
                        and (nr, nc) not in connected
                    ):
                        queue.append((nr, nc))

    current_zone = set()
    find_connected_cells(row, col, cell_value, current_zone)

    if len(current_zone) > 1:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        # Collect all unique combinations of letters in the current zone
        unique_combinations = set(''.join(labels[r][c].cget('text') for r, c in current_zone))

        for r, c in current_zone:
            labels[r][c].config(bg=color)
            labels[r][c].config(text=cell_value)

        middle_row, middle_col = find_middle(list(current_zone))
        labels[middle_row][middle_col].config(text=cell_value, bg=color)

        label_frontier(current_zone, cell_value)

# ... (rest of the code remains the same)



def find_middle(cells):
    if not cells:
        return 0, 0

    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    return sum(rows) // len(cells), sum(cols) // len(cells)

def label_frontier(current_zone, cell_value):
    frontier = set()
    for r, c in current_zone:
        neighbors = [
            (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)
        ]
        for nr, nc in neighbors:
            if 0 <= nr < len(labels) and 0 <= nc < len(labels[0]) and (nr, nc) not in current_zone:
                frontier.add((nr, nc))

    marked_frontiers = set()
    for r, c in frontier:
        if labels[r][c].cget("text") != cell_value and labels[r][c].cget("text") != "":
            # Create a unique key for the frontier using sorted letter combination
            frontier_key = tuple(sorted(set(cell_value.lower() + labels[r][c].cget('text').lower())))
            if len(frontier_key) <= 2:  # Ensure there are at most 2 distinct letters
                labels[r][c].config(text=''.join(frontier_key))
                marked_frontiers.add(frontier_key)




root = tk.Tk()
root.title("Grid Interface")

user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
popup_width = screen_width // 2
popup_height = screen_height // 2
x_offset = (screen_width - popup_width) // 2
y_offset = (screen_height - popup_height) // 2

root.geometry(f"{popup_width}x{popup_height}+{x_offset}+{y_offset}")

input_frame = tk.Frame(root)
input_frame.pack()

tk.Label(input_frame, text="Rows (Max 12):").grid(row=0, column=0)
entry_rows = tk.Entry(input_frame)
entry_rows.grid(row=0, column=1)

tk.Label(input_frame, text="Columns (Max 12):").grid(row=1, column=0)
entry_columns = tk.Entry(input_frame)
entry_columns.grid(row=1, column=1)

tk.Label(input_frame, text="Select Letter:").grid(row=2, column=0)
selected_value = ttk.Combobox(input_frame, values=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
selected_value.grid(row=2, column=1)

create_button = tk.Button(input_frame, text="Create Grid", command=lambda: create_grid())
create_button.grid(row=3, columnspan=2)

grid_frame = tk.Frame(root)
grid_frame.pack()

labels = []

def create_grid():
    global labels
    try:
        rows = min(12, int(entry_rows.get()))
        columns = min(12, int(entry_columns.get()))

        for widget in grid_frame.winfo_children():
            widget.destroy()

        labels = []
        for i in range(rows):
            row_labels = []
            for j in range(columns):
                label = tk.Label(grid_frame, text="", width=5, height=2, borderwidth=1, relief="solid")
                label.grid(row=i, column=j)
                label.bind("<Button-1>", mark_cell)
                row_labels.append(label)
            labels.append(row_labels)
    except ValueError:
        pass


root.mainloop()
