import numpy as np
import sympy as sp
from abc import ABC, abstractmethod
from dataclasses import dataclass

G = 1
c = 1

@dataclass
class StateVector:
    x: float
    y: float
    v_x: float
    v_y: float

class MetricStrategy(ABC):

    @abstractmethod
    def get_accelerations(self, state: StateVector) -> np.ndarray:
        pass

class GeneralMetric(MetricStrategy):
    def __init__(self, symbols: list, metric: sp.Matrix):
        self.symbols = symbols
        self.metric = metric
        self.inverse_metric = metric.inv()
        self.n = len(self.symbols)
        self.christoffels = [[[0 for _ in range(self.n)] for _ in range(self.n)] for _ in range(self.n)]    
        self.calculate_christoffels()

    def calculate_christoffels(self):
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    summ = 0
                    for l in range(self.n):                            
                        summ += (self.inverse_metric[i,l])*(sp.diff(self.metric[j,l], self.symbols[k])+sp.diff(self.metric[k,l], self.symbols[j])-sp.diff(self.metric[j,k], self.symbols[l]))
                    self.christoffels[i][j][k] = sp.simplify(0.5*summ)
        self.f_christoffels = sp.lambdify(self.symbols, self.christoffels, 'numpy')
        self.f_metric = sp.lambdify(self.symbols, self.metric, 'numpy')

    def get_accelerations(self, state: StateVector) -> np.ndarray:
        r = np.sqrt((state.x)**2+(state.y)**2)
        phi = np.arctan2(state.y, state.x)
        v_r = (state.x*state.v_x + state.y*state.v_y)/r
        v_phi = (state.x*state.v_x - state.y*state.v_y)/r**2
        g = self.f_metric(0, r, phi)
        g_tt = g[0,0]
        g_rr = g[1,1]
        g_phiphi = g[2,2]
        u_t = 1/np.sqrt(g_tt+g_rr*(v_r)**2+g_phiphi*(v_phi)**2)
        u = np.array([u_t, v_r*u_t, v_phi*u_t])

        chris = self.f_christoffels(0, r, phi)
        a_spherical = -np.einsum('ijk,j,k->i', chris, u, u)
        a_t_sph = a_spherical[0]
        a_r_sph = a_spherical[1]
        a_phi_sph = a_spherical[2]

        a_x = (a_r_sph - r*u[2]**2)*np.cos(phi)-(r*a_phi_sph+2*u[1]*u[2])*np.sin(phi)
        a_y = (a_r_sph - r*u[2]**2)*np.sin(phi)+(r*a_phi_sph+2*u[1]*u[2])*np.cos(phi)
        return np.array([state.v_x, state.v_y, a_x, a_y])

