import tkinter as tk

window = tk.Tk()
window.title("Operational Research Group Project")

title_label = tk.Label(window, text="Operational Research Group Project", font=("Arial", 18, "bold"))
title_label.pack(pady=20)  

presenter_label = tk.Label(window, text="Presented By:", font=("Arial", 14, "bold"))
presenter_label.pack(pady=10)  

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

separator = tk.Frame(window, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(pady=20)  


label = tk.Label(window, text="Choose a problem to solve", font=("Arial", 14, "bold"))
label.pack(pady=10)  

problem_frame = tk.Frame(window)
problem_frame.pack(pady=3)  
problem_label = tk.Label(problem_frame, text="PL1 : Agricultural Area Optimization")
problem_label.pack(side=tk.LEFT)
button = tk.Button(problem_frame, text="Resolution", command=None)
button.pack(side=tk.RIGHT)

problem_frame = tk.Frame(window)
problem_frame.pack(pady=3)  
problem_label = tk.Label(problem_frame, text="PL2 : ChausseTous Entreprise Production Optimization")
problem_label.pack(side=tk.LEFT)
button = tk.Button(problem_frame, text="Resolution", command=None)
button.pack(side=tk.RIGHT)

problem_frame = tk.Frame(window)
problem_frame.pack(pady=3)  
problem_label = tk.Label(problem_frame, text="PL3 : Human Resources Needs Optimization")
problem_label.pack(side=tk.LEFT)
button = tk.Button(problem_frame, text="Resolution", command=None)
button.pack(side=tk.RIGHT)

problem_frame = tk.Frame(window)
problem_frame.pack(pady=3)  
problem_label = tk.Label(problem_frame, text="PL4 : Bank Branches Optimization")
problem_label.pack(side=tk.LEFT)
button = tk.Button(problem_frame, text="Resolution", command=None)
button.pack(side=tk.RIGHT)

problem_frame = tk.Frame(window)
problem_frame.pack(pady=3)  
problem_label = tk.Label(problem_frame, text="PL5 : Positioning of Transmitting Antennas")
problem_label.pack(side=tk.LEFT)
button = tk.Button(problem_frame, text="Resolution", command=None)
button.pack(side=tk.RIGHT)

problem_frame = tk.Frame(window)
problem_frame.pack(pady=3)  
problem_label = tk.Label(problem_frame, text="PL6 : Network Optimization")
problem_label.pack(side=tk.LEFT)
button = tk.Button(problem_frame, text="Resolution", command=None)
button.pack(side=tk.RIGHT)


# Define a placeholder function for the "solve_problem" function
def solve_problem(problem_id):
    print(f"Solving problem PL{problem_id}")
    # TODO: Implement the actual problem solving logic here

# Start the main loop
window.mainloop()
