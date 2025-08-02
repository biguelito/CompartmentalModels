import plotly.graph_objects as go
import os
import numpy as np
from math import ceil

class CompartmentalGraph:
    def __init__(self, days, s, e, i, r):
        self.days = days
        self.S = s
        self.E = e
        self.I = i
        self.R = r
        self.figure = None

    def create_figure(self):
        tspan = np.arange(0, self.days, 1)
        steps = ceil(self.days / 5)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tspan, y=self.S, mode='lines+markers', name='Susceptíveis'))
        fig.add_trace(go.Scatter(x=tspan, y=self.E, mode='lines+markers', name='Expostos'))
        fig.add_trace(go.Scatter(x=tspan, y=self.I, mode='lines+markers', name='Infectados'))
        fig.add_trace(go.Scatter(x=tspan, y=self.R, mode='lines+markers', name='Recuperados'))

        fig.update_layout(
            title='Simulation of SEIR Model',
            xaxis_title='Day',
            yaxis_title='Counts',
            title_x=0.5,
            width=900,
            height=600
        )
        fig.update_xaxes(
            tickangle=-90,
            tickformat=None,
            tickmode='array',
            tickvals=np.arange(0, self.days + 1, steps)
        )

        self.figure = fig
        return

    def get_fig(self):
        if (self.figure is None):
            self.create_figure()
        return self.figure

    def save(self, name):
        if not os.path.exists("images"):
            os.mkdir("images")
        self.figure.write_image(f"images/plotly_{name}.png")
