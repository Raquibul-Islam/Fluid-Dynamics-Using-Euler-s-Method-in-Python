import tkinter as tk
from tkinter import ttk
from tabulate import tabulate
import subprocess

def f(x, y, equation):
    return eval(equation)


# Euler method
def euler(x0, y0, xn, n, equation):
    # Calculating step size
    h = (xn - x0) / n

    results = []

    for i in range(n):
        slope = f(x0, y0, equation)
        yn = y0 + h * slope
        results.append([x0, y0, slope, yn])
        y0 = yn
        x0 = x0 + h

    slope = f(xn, yn, equation)
    results.append([xn, yn, slope, yn])

    return results



def calculate():
    # Get input values from entry widgets
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        xn = float(entry_xn.get())
        step = float(entry_step.get())
    except ValueError:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error: Invalid input. Please enter valid numerical values.")
        result_text.config(state=tk.DISABLED)
        return

    equation = entry_equation.get()

    n = int((xn - x0) / step)

    # Call Euler method
    result = euler(x0, y0, xn, n, equation)

    # Display the results in tabular format
    table = tabulate(result, headers=['x', 'y', 'Slope', 'yn'], tablefmt='grid')
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, table)
    result_text.config(state=tk.DISABLED)


# Function to open fluid_dynamics.py
def open_fluid_dynamics():
    subprocess.Popen(['python', 'fluid_dynamics.py'])


def open_graph():
    subprocess.Popen(['python', 'graph.py'])


# Create the main Tkinter window
root = tk.Tk()
root.title("Numeric Project")

# Increase the window size
root.geometry("700x800")

# Header Label
header_label = ttk.Label(root, text="Numeric Project", font=("Arial", 16, "bold"))
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create input labels and entry widgets
label_equation = ttk.Label(root, text="Differential equation (dy/dx):")
label_equation.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entry_equation = ttk.Entry(root)
entry_equation.grid(row=1, column=1, padx=10, pady=5)

label_x0 = ttk.Label(root, text="Give the initial value of x (x0):")
label_x0.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
entry_x0 = ttk.Entry(root)
entry_x0.grid(row=2, column=1, padx=10, pady=5)

label_y0 = ttk.Label(root, text="Give the initial value of y (y0):")
label_y0.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
entry_y0 = ttk.Entry(root)
entry_y0.grid(row=3, column=1, padx=10, pady=5)

label_xn = ttk.Label(root, text="Calculation point (xn) :")
label_xn.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
entry_xn = ttk.Entry(root)
entry_xn.grid(row=4, column=1, padx=10, pady=5)

label_step = ttk.Label(root, text="Step size (h) :")
label_step.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
entry_step = ttk.Entry(root)
entry_step.grid(row=5, column=1, padx=10, pady=5)

# Button to calculate
btn_calculate = ttk.Button(root, text="Calculate Euler Predicted and Corrector Value", command=calculate)
btn_calculate.grid(row=6, column=0, columnspan=2, pady=10)

# Text widget to display the results
result_text = tk.Text(root, height=30, width=80)
result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
result_text.config(state=tk.DISABLED)

# Button to open fluid_dynamics.py
btn_fluid_dynamics = ttk.Button(root, text="See Fluid Dynamics", command=open_fluid_dynamics)
btn_fluid_dynamics.grid(row=8, column=0, pady=10)

btn_fluid_dynamics = ttk.Button(root, text="See The graph", command=open_graph)
btn_fluid_dynamics.grid(row=8, column=1, pady=10)

# Run the Tkinter event loop
root.mainloop()
