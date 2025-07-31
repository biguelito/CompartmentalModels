from scipy.integrate import odeint
import numpy as np
from CompartmentalGraph import CompartmentalGraph
from CompartmentalModel import CompartmentalModel
from time import time

class CompartmentalModelSolver:
    model:CompartmentalModel = None
    solved_odes = None

    def __init__(self, initial_conditions, transfer_rates, days):
        self.model = CompartmentalModel(initial_conditions, transfer_rates, days)

    def solve(self):
        tspan = np.arange(0, self.model.days, 1)
        solved_odes = odeint(self.model.get_odes, self.model.initialValues, tspan, args=tuple([self.model.transfer_rates]))
        self.solved_odes = solved_odes[:, 0], solved_odes[:, 1], solved_odes[:, 2], solved_odes[:, 3]

    def _create_figure(self, lib):
        fig = CompartmentalGraph(self.model.days, self.solved_odes[0], self.solved_odes[1], self.solved_odes[2], self.solved_odes[3])
        fig.create_figure(lib)
        return fig

    def get_matplotlib_figure(self):
        return self._create_figure("matplotlib")

    def save(self, lib, name=f"simulation_{time()}"):
        fig = self._create_figure(lib)
        fig.save(lib, name)
