import streamlit as st
from compartmentals.CompartmentalModelSolver import CompartmentalModelSolver
from models.seird import SEIRD
from models.seir import SEIR
from models.seirs import SEIRS

DEFAULTS = {
    "S": 1_000_000,
    "E": 1,
    "I": 1,
    "R": 0,
    "D": 0,
    "sigma": 0.2,
    "gamma": 0.14,
    "alfa": 0.03,
    "mu": 0.03,
    "r0": 2.2,
    "days": 365
}

seird = SEIRD()
seir = SEIR()
seirs = SEIRS()

st.title("Modelos interativos")
st.markdown("Configure os parâmetros abaixo e clique em **Rodar Simulação** para visualizar o gráfico.")

days = st.number_input("Dias", value=int(DEFAULTS["days"]), min_value=0)

st.markdown("### População Inicial")
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2 = st.columns(2)
with row1_col1:
    S = st.number_input("Susceptíveis (S)", value=int(DEFAULTS["S"]), min_value=0)
with row1_col2:
    E = st.number_input("Expostos (E)", value=int(DEFAULTS["E"]), min_value=0)
with row1_col3:
    I = st.number_input("Infectados (I)", value=int(DEFAULTS["I"]), min_value=0)
with row2_col1:
    R = st.number_input("Recuperados (R)", value=int(DEFAULTS["R"]), min_value=0)
with row2_col2:
    D = st.number_input("Mortos (D)", value=int(DEFAULTS["D"]), min_value=0)

st.markdown("### Taxas do Modelos")
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2 = st.columns(2)
with row1_col1:
    r0 = st.number_input("R0", value=float(DEFAULTS["r0"]), min_value=0.0)
with row1_col2:
    sigma = st.number_input("sigma - Incubação", value=float(DEFAULTS["sigma"]), min_value=0.0)
with row1_col3:
    gamma = st.number_input("gamma - Recuperação", value=float(DEFAULTS["gamma"]), min_value=0.0)
with row2_col1:
    mu = st.number_input("mu - Mortalidade", value=float(DEFAULTS["mu"]), min_value=0.0)
with row2_col2:
    alfa = st.number_input("alfa - Imunidade", value=float(DEFAULTS["alfa"]), min_value=0.0)

if st.button("Rodar Simulação"):
    beta = r0 * gamma

    seir_initial_conditions = [S, E, I, R]
    seir_transfer_rates = [beta, sigma, gamma]
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
        
    seirs_initial_conditions = [S, E, I, R]
    seirs_transfer_rates = [beta, sigma, gamma, alfa]
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

    seird_initial_conditions = [S, E, I, R, D]
    seird_transfer_rates = [beta, sigma, gamma, mu]
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

    st.plotly_chart(seir_fig, use_container_width=True)
    st.plotly_chart(seirs_fig, use_container_width=True)
    st.plotly_chart(seird_fig, use_container_width=True)
else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")
