import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Parameters
length = 20.0
width = 10.0
num_points_x = 100
num_points_y = 50
dx = length / num_points_x
dy = width / num_points_y
velocity = 1.0
diffusion_coefficient = 0.1
time_step = 0.01
num_frames = 2000


fluid_density = np.zeros((num_points_y, num_points_x))
fluid_density[num_points_y // 4:num_points_y // 2,
              num_points_x // 4:num_points_x // 2] = 1.0  # Fluid density initially nonzero in a portion of the pipe


def euler_method_advection_diffusion(u_initial, velocity, diffusion_coefficient, dt, dx, dy):
    u = u_initial.copy()
    num_points_y, num_points_x = u.shape

    u_new = np.zeros((num_points_y, num_points_x))
    for i in range(1, num_points_y - 1):
        for j in range(1, num_points_x - 1):
            # Advection term
            advective_flux_x = velocity * (u[i, j] - u[i, j - 1]) / dx
            advective_flux_y = velocity * (u[i, j] - u[i - 1, j]) / dy

            # Diffusion term
            diffusive_flux_x = diffusion_coefficient * (u[i, j + 1] - 2 * u[i, j] + u[i, j - 1]) / (dx ** 2)
            diffusive_flux_y = diffusion_coefficient * (u[i + 1, j] - 2 * u[i, j] + u[i - 1, j]) / (dy ** 2)

            # Update using Euler's method
            u_new[i, j] = u[i, j] + dt * (-advective_flux_x - advective_flux_y + diffusive_flux_x + diffusive_flux_y)

    # Boundary conditions (no flux)
    u_new[:, 0] = u_new[:, 1]
    u_new[:, -1] = u_new[:, -2]
    u_new[0, :] = u_new[1, :]
    u_new[-1, :] = u_new[-2, :]

    return u_new


# Predictor-Corrector method to improve accuracy
def predictor_corrector_method(u_initial, velocity, diffusion_coefficient, dt, dx, dy):
    # Predict using Euler's method
    u_predicted = euler_method_advection_diffusion(u_initial, velocity, diffusion_coefficient, dt, dx, dy)

    # Correct using Euler's method with the predicted value
    u_corrected = euler_method_advection_diffusion(u_predicted, velocity, diffusion_coefficient, dt, dx, dy)

    return u_corrected


# Function to update plot for animation
def update(frame):
    global fluid_density
    fluid_density = predictor_corrector_method(fluid_density, velocity, diffusion_coefficient, time_step, dx, dy)
    im.set_array(fluid_density)
    return im,


# Set up the root Tkinter window
root = tk.Tk()
root.title("2D Fluid Flow Simulation")

# Set window size
root.geometry("700x800")

# Create initial plot
fig, ax = plt.subplots()
ax.set_xlim(0, length)
ax.set_ylim(0, width)
ax.set_xlabel('Position (x)')
ax.set_ylabel('Position (y)')
ax.set_title('2D Fluid Flow in a Pipe (Advection-Diffusion Equation)')
im = ax.imshow(fluid_density, extent=[0, length, 0, width], origin='lower', cmap='jet', interpolation='nearest')
plt.close(fig)  # Close the initial plot window

# Embed the plot in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=3)

# Animator object for animation
ani = FuncAnimation(fig, update, frames=num_frames, interval=70, blit=True)

# Function to update velocity
def update_velocity(val):
    global velocity
    velocity = float(val)

# Function to update diffusion coefficient
def update_diffusion_coefficient(val):
    global diffusion_coefficient
    diffusion_coefficient = float(val)

# Slider for velocity
vel_slider = tk.Scale(root, from_=0.1, to=2.0, resolution=0.2, orient=tk.HORIZONTAL, label="Velocity", command=update_velocity)
vel_slider.grid(row=1, column=0)

# Slider for diffusion coefficient
diff_slider = tk.Scale(root, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Diffusion Coefficient", command=update_diffusion_coefficient)
diff_slider.grid(row=1, column=1)

# Start button
def start_animation():
    ani.event_source.start()

start_button = tk.Button(root, text="Start", command=start_animation)
start_button.grid(row=1, column=2)

# Pause button
def pause_animation():
    ani.event_source.stop()

pause_button = tk.Button(root, text="Pause", command=pause_animation)
pause_button.grid(row=2, column=0)

# Reset button
def reset_animation():
    global velocity, diffusion_coefficient, fluid_density
    velocity = 1.0
    diffusion_coefficient = 0.1
    fluid_density = np.zeros((num_points_y, num_points_x))
    fluid_density[num_points_y // 4:num_points_y // 2,
    num_points_x // 4:num_points_x // 2] = 1.0
    vel_slider.set(velocity)
    diff_slider.set(diffusion_coefficient)
    ani.event_source.stop()
    im.set_array(fluid_density)
    canvas.draw()

reset_button = tk.Button(root, text="Reset", command=reset_animation)
reset_button.grid(row=2, column=1)

# Function to close the Tkinter window
def close_window():
    root.quit()
    root.destroy()

# Close button
close_button = tk.Button(root, text="Close", command=close_window)
close_button.grid(row=2, column=2)

# Run the Tkinter event loop
root.mainloop()
