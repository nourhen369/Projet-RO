import tkinter as tk
from tkinter import *
import ttkbootstrap as tkb

def home():
    def toggle_theme():
        return

    # Define a function to create and pack a problem frame
    def create_problem_frame(window, problem_text, problem_id):
        problem_frame = tk.Frame(window)
        problem_frame.pack(pady=3)

        problem_label = tk.Label(problem_frame, text=problem_text)
        problem_label.pack(side=tk.LEFT)

        button = tk.Button(problem_frame, text="Resolution", command=lambda x=problem_id: solve_problem(x))
        button.pack(side=tk.RIGHT)

        return problem_frame

    # Define a function for the "solve_problem" action
    def solve_problem(problem_id):
        print(f"Solving problem PL{problem_id}")

    # Initialize the main window
    window = tkb.Window(themename="morph")
    global theme
    theme = "morph"
    window.title("Operational Research Group Project")
    window.geometry("800x700")

    # Add title and presenter labels
    title_label = tk.Label(window, text="Operational Research Group Project", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    presenter_label = tk.Label(window, text="Presented By:", font=("Arial", 14, "bold"))
    presenter_label.pack(pady=10)

    # Display presenter names using a loop
    presenter_names = [
        "Ferjani Oussama",
        "Bchini Mohamed Aziz",
        "Khechine Nourhen",
        "Charfeddine Elyes",
        "Ben Youssef Eya",
    ]

    for name in presenter_names:
        presenter_name_label = tk.Label(window, text=name, font=("Arial", 12))
        presenter_name_label.pack(pady=3)

    # Add separator
    separator = tk.Frame(window, height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(pady=20)

    # Add problem selection label
    label = tk.Label(window, text="Choose a problem to solve", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    # Create and pack problem frames using a loop
    problems = [
        ("PL1: Agricultural Area Optimization", 1),
        ("PL2: ChausseTous Entreprise Production Optimization", 2),
        ("PL3: Human Resources Needs Optimization", 3),
        ("PL4: Bank Branches Optimization", 4),
        ("PL5: Positioning of Transmitting Antennas", 5),
        ("PL6: Network Optimization", 6),
    ]

    for text, problem_id in problems:
        create_problem_frame(window, text, problem_id)

    dark_mode_button = tkb.Button(window, text="Dark Mode", command=toggle_theme)
    dark_mode_button.pack(side=tk.LEFT, padx=15, pady=10)

    # Add exit button
    exit_button = tk.Button(window,
    text="Exit", command=window.destroy)
    exit_button.pack(side=tk.RIGHT, padx=15, pady=10)


    # Start the main loop
    window.mainloop()
