import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
import numpy as np
from math import ceil

class CompartmentalGraph:
    plotly_figure = None
    matplotlib_figure = None
    days = None
    S = None
    E = None
    I = None
    R = None

    def __init__(self, days, s, e, i, r):
        self.days = days
        self.S = s
        self.E = e
        self.I = i
        self.R = r

        return

    def _create_plotly_figure(self):
        tspan = np.arange(0, self.days, 1)
        steps = ceil(self.days/5)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tspan, y=self.S, mode='lines+markers', name='Susceptible'))
        fig.add_trace(go.Scatter(x=tspan, y=self.E, mode='lines+markers', name='Exposed'))
        fig.add_trace(go.Scatter(x=tspan, y=self.I, mode='lines+markers', name='Infected'))
        fig.add_trace(go.Scatter(x=tspan, y=self.R, mode='lines+markers',name='Recovered'))
        
        fig.update_layout(title='Simulation of SEIR Model',
            xaxis_title='Day',
            yaxis_title='Counts',
            title_x=0.5,
            width=900, height=600
        )
        fig.update_xaxes(tickangle=-90, tickformat = None, tickmode='array', tickvals=np.arange(0, self.days + 1, steps))
        self.figure = fig
        self.plotly_figure = fig

        return

    def _create_matplotlib_figure(self):
        tspan = np.arange(0, self.days, 1)
        steps = ceil(self.days / 5)

        fig, self.ax = plt.subplots(figsize=(9, 6))  # tamanho equivalente ao width=900, height=600 do plotly

        self.ax.plot(tspan, self.S, marker='o', label='Susceptible')
        self.ax.plot(tspan, self.E, marker='o', label='Exposed')
        self.ax.plot(tspan, self.I, marker='o', label='Infected')
        self.ax.plot(tspan, self.R, marker='o', label='Recovered')

        self.ax.set_title('Simulation of SEIR Model', fontsize=14, loc='center')
        self.ax.set_xlabel('Day')
        self.ax.set_ylabel('Counts')
        self.ax.set_xticks(np.arange(0, self.days + 1, steps))
        self.ax.tick_params(axis='x', rotation=90)
        self.ax.legend()
        fig.tight_layout()
        self.matplotlib_figure = fig

        return 

    def create_figure(self, lib):
        if (lib == "plotly"):
            self._create_plotly_figure()
            return

        if (lib == "matplotlib"):
            self._create_matplotlib_figure()
            return

        return

    def save(self, lib, name):
        if not os.path.exists("images"):
            os.mkdir("images")

        if lib == "plotly":
            self.plotly_figure.write_image(f"images/plotly_{name}.png")

        if lib == "matplotlib":
            self.matplotlib_figure.savefig(f"images/matplotlib_{name}.png")
        
        return