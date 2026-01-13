#  Orbital Pathfinder

**A Real-Time General Relativity Geodesic Simulator**

Orbital Pathfinder is a Python-based physics engine that visualizes the motion of test particles in curved spacetime. Unlike simple gravity simulators, this project does not use hardcoded force laws. Instead, it takes a **metric tensor** defined by the user, symbolically derives the **Christoffel symbols** using `sympy`, and solves the **Geodesic Equations** numerically in real-time.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)
![Physics](https://img.shields.io/badge/physics-General%20Relativity-purple)

##  Key Features

* **Universal Solver:** Works with any static, spherically symmetric metric (Schwarzschild, Wormholes, Minkowski, etc.).
* **Symbolic Computation:** Uses `sympy` to calculate equations of motion on the fly. No pre-baked formulas!
* **Automatic Geometry Analysis:** Automatically detects and visualizes Event Horizons or Throat geometries (singularities in $g_{rr}$).
* **Real-Time Visualization:** Animated trajectories with history trails using `matplotlib`.
* **Robust Physics:** Implements Semi-Implicit Euler integration for stable orbital mechanics.

##  Installation

1.  **Clone the repository** (or download files):
    ```bash
    git clone [https://github.com/your-username/orbital-pathfinder.git](https://github.com/your-username/orbital-pathfinder.git)
    cd orbital-pathfinder
    ```

2.  **Install dependencies:**
    This project requires Python 3 and the following libraries:
    ```bash
    pip install numpy matplotlib sympy
    ```
##  Example Scenarios

Here are tested parameters you can input to simulate different spacetimes. Assume starting radius $x = 10.0$.

### 1. Schwarzschild Black Hole ⚫
The classic non-rotating black hole.
* **g_tt:** `(1-2/r)`
* **g_rr:** `-1/(1-2/r)`
* **g_phi:** `-r**2`

| Velocity ($v_y$) | Outcome | Description |
| :--- | :--- | :--- |
| `0.316` | **Circular Orbit** | The particle stays on a stable path. |
| `0.31` | **Rosette Orbit** | Displays perihelion precession (a key proof of GR). |
| `0.2` | **Crash** | The particle falls into the Event Horizon. |

### 2. Morris-Thorne Wormhole 🌀
A traversable wormhole with no event horizon. The "throat" is located at $r=2$.
* **g_tt:** `(1-1/r)`
* **g_rr:** `-1/(1-(2/r)**2)`
* **g_phi:** `-r**2`

| Velocity ($v_y$) | Outcome | Description |
| :--- | :--- | :--- |
| `0.223` | **Stable Orbit** | A complex, precessing orbit around the throat. |
| `0.35` | **Escape** | The gravity is weaker than a Black Hole; the particle escapes to infinity. |

### 3. Minkowski Space (Flat Spacetime) 📏
Standard space with no gravity.
* **g_tt:** `1`
* **g_rr:** `-1`
* **g_phi:** `-r**2`

| Velocity ($v_y$) | Outcome | Description |
| :--- | :--- | :--- |
| `0.5` | **Straight Line** | The particle moves in a straight line (Newton's 1st Law). |

##  How It Works

1.  **Metric Definition:** The user inputs the diagonal elements of the metric tensor:
    $$g_{\mu\nu} = \text{diag}(g_{tt}, g_{rr}, g_{\phi\phi})$$
2.  **Symbolic Differentiation:** The engine calculates the **Christoffel Symbols** of the second kind:
    $$\Gamma^\lambda_{\mu\nu} = \frac{1}{2} g^{\lambda\sigma} (\partial_\mu g_{\sigma\nu} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu})$$
3.  **Geodesic Equation:** The program solves the differential equation for the four-velocity $u^\mu$:
    $$\frac{d^2x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta} u^\alpha u^\beta = 0$$
4.  **Integration:** The state vector $[x, y, v_x, v_y]$ is updated every time step using numerical integration.

##  Project Structure

* `main.py`: The entry point. Handles user input, the simulation loop, and visualization.
* `src/physics.py`: Contains the `GeneralMetric` class (symbolic math core) and `StateVector` data structure.

##  Contributing

Feel free to fork this project and submit pull requests. Ideas for future features:
* Kerr Metric support (rotating black holes).
* 3D Visualization.
* Adaptive time-stepping (Runge-Kutta 4).

## 📜 License

This project is open-source and available under the MIT License.

## Usage

Run the main simulation script:

```bash
python main.py

