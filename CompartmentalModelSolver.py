from scipy.integrate import odeint
import numpy as np
from CompartmentalGraph import CompartmentalGraph
from CompartmentalModel import CompartmentalModel
from time import time

class CompartmentalModelSolver:
    def __init__(self, ode_function, initial_conditions, transfer_rates, days):
        self.model = CompartmentalModel(initial_conditions, transfer_rates, days)
        self.ode_function = ode_function
        self.solved_odes = None

    def solve(self):
        tspan = np.arange(0, self.model.days, 1)
        solved_odes = odeint(
            self.ode_function,
            self.model.initialValues,
            tspan,
            args=(self.model.transfer_rates,)
        )
        self.solved_odes = solved_odes[:, 0], solved_odes[:, 1], solved_odes[:, 2], solved_odes[:, 3]

    def get_figure(self):
        fig = CompartmentalGraph(
            self.model.days,
            self.solved_odes[0],
            self.solved_odes[1],
            self.solved_odes[2],
            self.solved_odes[3]
        )
        return fig.get_fig() 

    def save(self, name=f"simulation_{time()}"):
        fig = self.get_figure()
        fig.save(name)
