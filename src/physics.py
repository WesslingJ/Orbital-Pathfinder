import numpy as numpy
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

    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.v_x, self.v_y])

    @staticmethod
    def from_array(arr: np.ndarray):
        return StateVector(x=arr[0], y=arr[1], v_x=arr[2], v_y=[3])

class MetricStrategy(ABC):

    @abstractmethod
    def get_accelerations(self, state: StateVector) -> np.ndarray:
        pass

class SchwarzschildMetric(MetricStrategy):
    """
    Rozwiązanie dla sferycznie symetrycznej, nierotującej czarnej dziury.
    Używamy jednostek naturalnych: G=1, c=1.
    """
    
    def __init__(self, mass: float):
        self.M = mass
        self.rs = 2.0 * mass # Promień Schwarzschilda (2GM/c^2 przy G=c=1)

    def get_accelerations(self, state: StateVector) -> np.ndarray:
        # Tu jutro wpiszemy pełne równania geodezyjnych
        # Na razie placeholder (zwracamy zera)
        return np.array([0.0, 0.0])

class PhysicsEngine:

    def __innit__(self, metric: MetricStrategy):
        self.metric = metric

    def evolve(self, initial_state: StateVector, t_span: tuple):
        pass