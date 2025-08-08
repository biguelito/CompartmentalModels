import streamlit as st
from compartmentals.CompartmentalModelSolver import CompartmentalModelSolver
from models.seird import SEIRD
from models.seir import SEIR
from models.seirs import SEIRS
from models.seirsd import SEIRSD

COVID_DEFAULTS = {
    "S": 1_000_000,
    "E": 1,
    "I": 1,
    "R": 0,
    "D": 0,
    "beta": 0.4332,
    "sigma": 0.192,
    "gamma": 0.143,
    "alfa": 0.0056,
    "mu": 0.0014,
    "r0": 3,
    "days": 365
}

seird = SEIRD()
seir = SEIR()
seirs = SEIRS()
seirsd = SEIRSD()

st.title("Modelos interativos")
st.markdown("Configure os parâmetros abaixo e clique em **Rodar Simulação** para visualizar o gráfico.")

days = st.number_input("Dias", value=int(COVID_DEFAULTS["days"]), min_value=0)

st.markdown("### População Inicial")
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2 = st.columns(2)
with row1_col1:
    S = st.number_input("Susceptíveis (S)", value=int(COVID_DEFAULTS["S"]), min_value=0)
with row1_col2:
    E = st.number_input("Expostos (E)", value=int(COVID_DEFAULTS["E"]), min_value=0)
with row1_col3:
    I = st.number_input("Infectados (I)", value=int(COVID_DEFAULTS["I"]), min_value=0)
with row2_col1:
    R = st.number_input("Recuperados (R)", value=int(COVID_DEFAULTS["R"]), min_value=0)
with row2_col2:
    D = st.number_input("Mortos (D)", value=int(COVID_DEFAULTS["D"]), min_value=0)

st.markdown("### Taxas do Modelos")

use_beta = st.toggle("Inserir β (desligue para inserir R₀)", value=True)

row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2 = st.columns(2)
with row1_col1:
    if use_beta:
        beta = st.number_input("β (beta) - Transmissão", value=float(COVID_DEFAULTS["beta"]), min_value=0.0, step=0.0001, format="%.4f")
    else:   
        r0 = st.number_input("R0", value=float(COVID_DEFAULTS["r0"]), min_value=0.0, step=0.0001, format="%.4f")
with row1_col2:
    sigma = st.number_input("σ (sigma) - Incubação", value=float(COVID_DEFAULTS["sigma"]), min_value=0.0, step=0.0001, format="%.4f")
with row1_col3:
    gamma = st.number_input("γ (gamma) - Recuperação", value=float(COVID_DEFAULTS["gamma"]), min_value=0.0, step=0.0001, format="%.4f")
with row2_col1:
    mu = st.number_input("μ (mu) - Mortalidade", value=float(COVID_DEFAULTS["mu"]), min_value=0.0, step=0.0001, format="%.4f")
with row2_col2:
    alfa = st.number_input("α (alfa) - Perda de imunidade", value=float(COVID_DEFAULTS["alfa"]), min_value=0.0, step=0.0001, format="%.4f")

if st.button("Rodar Simulação"):

    seir_beta = beta if use_beta else r0 * gamma
    seir_initial_conditions = [S, E, I, R]
    seir_transfer_rates = [seir_beta, sigma, gamma]
    seir_compartments = seir.COMPARTMENTS
    seir_solver = CompartmentalModelSolver(
        ode_function=seir.odes,
        initial_conditions=seir_initial_conditions,
        transfer_rates=seir_transfer_rates,
        days=days,
        compartments=seir_compartments,
        model_name="SEIR"
    )
    seir_solver.solve()
    seir_fig = seir_solver.get_figure()
        
    seirs_beta = beta if use_beta else r0 * gamma
    seirs_initial_conditions = [S, E, I, R]
    seirs_transfer_rates = [seirs_beta, sigma, gamma, alfa]
    seirs_compartments = seirs.COMPARTMENTS
    solver = CompartmentalModelSolver(
        ode_function=seirs.odes,
        initial_conditions=seirs_initial_conditions,
        transfer_rates=seirs_transfer_rates,
        days=days,
        compartments=seirs_compartments,
        model_name="SEIRS"
    )
    solver.solve()
    seirs_fig = solver.get_figure()

    seird_beta = beta if use_beta else r0 * (gamma + mu)
    seird_initial_conditions = [S, E, I, R, D]
    seird_transfer_rates = [seird_beta, sigma, gamma, mu]
    seird_compartments = seird.COMPARTMENTS
    seird_solver = CompartmentalModelSolver(
        ode_function=seird.odes,
        initial_conditions=seird_initial_conditions,
        transfer_rates=seird_transfer_rates,
        days=days,
        compartments=seird_compartments,
        model_name="SEIRD"
    )
    seird_solver.solve()
    seird_fig = seird_solver.get_figure()
    
    seirsd_beta = beta if use_beta else r0 * (gamma + mu)
    seirsd_initial_conditions = [S, E, I, R, D]
    seirsd_transfer_rates = [seirsd_beta, sigma, gamma, alfa, mu]
    seirsd_compartments = seirsd.COMPARTMENTS
    seirsd_solver = CompartmentalModelSolver(
        ode_function=seirsd.odes,
        initial_conditions=seirsd_initial_conditions,
        transfer_rates=seirsd_transfer_rates,
        days=days,
        compartments=seirsd_compartments,
        model_name="SEIRSD"
    )
    seirsd_solver.solve()
    seirsd_fig = seirsd_solver.get_figure()

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    with row1_col1:
        st.plotly_chart(seir_fig, use_container_width=True)
    with row1_col2:
        st.plotly_chart(seirs_fig, use_container_width=True)
    with row2_col1:
        st.plotly_chart(seird_fig, use_container_width=True)
    with row2_col2:
        st.plotly_chart(seirsd_fig, use_container_width=True)
else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")
