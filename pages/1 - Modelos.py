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

st.markdown("### Modelos a serem simulados")
col1, col2, col3, col4 = st.columns(4)
with col1:
    do_seir = st.checkbox("SEIR", value=True)
with col2:
    do_seirs = st.checkbox("SEIRS", value=True)
with col3:
    do_seird = st.checkbox("SEIRD", value=True)
with col4:
    do_seirsd = st.checkbox("SEIRSD", value=True)

if st.button("Rodar Simulação"):
    figs = []

    if do_seir:
        seir_beta = beta if use_beta else r0 * gamma
        solver = CompartmentalModelSolver(
            ode_function=seir.odes,
            initial_conditions=[S, E, I, R],
            transfer_rates=[seir_beta, sigma, gamma],
            days=days,
            compartments=seir.COMPARTMENTS,
            model_name="SEIR"
        )
        solver.solve()
        figs.append(solver.get_figure())

    if do_seirs:
        seirs_beta = beta if use_beta else r0 * gamma
        solver = CompartmentalModelSolver(
            ode_function=seirs.odes,
            initial_conditions=[S, E, I, R],
            transfer_rates=[seirs_beta, sigma, gamma, alfa],
            days=days,
            compartments=seirs.COMPARTMENTS,
            model_name="SEIRS"
        )
        solver.solve()
        figs.append(solver.get_figure())

    if do_seird:
        seird_beta = beta if use_beta else r0 * (gamma + mu)
        solver = CompartmentalModelSolver(
            ode_function=seird.odes,
            initial_conditions=[S, E, I, R, D],
            transfer_rates=[seird_beta, sigma, gamma, mu],
            days=days,
            compartments=seird.COMPARTMENTS,
            model_name="SEIRD"
        )
        solver.solve()
        figs.append(solver.get_figure())

    if do_seirsd:
        seirsd_beta = beta if use_beta else r0 * (gamma + mu)
        solver = CompartmentalModelSolver(
            ode_function=seirsd.odes,
            initial_conditions=[S, E, I, R, D],
            transfer_rates=[seirsd_beta, sigma, gamma, alfa, mu],
            days=days,
            compartments=seirsd.COMPARTMENTS,
            model_name="SEIRSD"
        )
        solver.solve()
        figs.append(solver.get_figure())

    if figs:
        for i in range(0, len(figs), 2):
            cols = st.columns(2)
            for col, fig in zip(cols, figs[i:i+2]):
                col.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecione pelo menos um modelo para rodar a simulação.")
else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")