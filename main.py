import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import sympy as sp
from src.physics import StateVector, GeneralMetric

# --- Configuration ---
dt = 0.05 
animation_speed = 1
symbols = sp.symbols('t r phi')
t, r, phi = symbols

user_gtt = input("Define g_tt: ")
user_gr = input("Define g_r: ")
user_gphi = input("Define g_phi: ")

user_vy = input("Define v_y:")

g_tt = sp.sympify(user_gtt)
g_r = sp.sympify(user_gr)
g_phi = sp.sympify(user_gphi)

v_y_val = float(user_vy)

user_metric = sp.diag(g_tt, g_r, g_phi)
metric = GeneralMetric(symbols, user_metric) 

horizon_radius = 0.0
has_horizon = False

try:
    singularities = sp.solve(1/g_r, r)
    
    valid_radii = []
    for sol in singularities:
        if sol.is_real and sol > 0:
            valid_radii.append(float(sol))
            
    if valid_radii:
        horizon_radius = max(valid_radii)
        has_horizon = True
    else:
        print("No horizons, spacetime is flat")

except Exception as e:
    print(f"No analytical solutions: {e}")


# --- Initial state ---
state = StateVector(x=10.0, y=0.0, v_x=0.0, v_y=v_y_val)

x_history = [state.x]
y_history = [state.y]

# --- Simulation loop ---

def update(frame):

    if has_horizon:
        current_r = np.sqrt(state.x**2 + state.y**2)
        if current_r <= horizon_radius + 0.1: 
            print(f"Particle hit the barrier (r < {horizon_radius:.2f}).")
            ani.event_source.stop()
            return point, trail

    results = metric.get_accelerations(state)
    
    ax_acc = results[2] 
    ay_acc = results[3] 
    
    state.v_x = state.v_x + ax_acc*dt
    state.v_y = state.v_y + ay_acc*dt
    state.x = state.x + state.v_x*dt
    state.y = state.y + state.v_y*dt

    x_history.append(state.x)
    y_history.append(state.y)
    trail.set_data(x_history, y_history)
    point.set_data([state.x], [state.y])
    
    return point, trail

# --- Drawing ---
fig = plt.figure(figsize=(8, 8))
ax = plt.gca()

if has_horizon:
    event_horizon = Circle((0, 0), horizon_radius, color='black', alpha=0.3, label=f'Horyzont (r={horizon_radius:.1f})')
    ax.add_patch(event_horizon)
else:
    ax.plot(0, 0, 'k+', alpha=0.3, label='Centrum (r=0)')

point, = plt.plot([], [], 'ro', label='Statek')
trail, = ax.plot([],[],'-')

plt.axis('equal')
plt.grid(True)
plt.title("Trajectory of particle in chosen spacetime")
plt.legend()

ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ani = FuncAnimation(fig, update, frames=1000, interval=animation_speed, blit=True)
plt.show()
