import streamlit as st
from compartmentals.CompartmentalModelSolver import CompartmentalModelSolver
from models.seird import SEIRD
from models.seir import SEIR

seird = SEIRD()
seir = SEIR()

st.title("Modelos interativos")
st.markdown("Configure os parâmetros abaixo e clique em **Rodar Simulação** para visualizar o gráfico.")

days = st.number_input("Dias", value=int(seird.get_default("days")), min_value=0)

st.markdown("### População Inicial")
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2 = st.columns(2)
with row1_col1:
    S = st.number_input("Susceptíveis (S)", value=int(seird.get_default("S")), min_value=0)
with row1_col2:
    E = st.number_input("Expostos (E)", value=int(seird.get_default("E")), min_value=0)
with row1_col3:
    I = st.number_input("Infectados (I)", value=int(seird.get_default("I")), min_value=0)
with row2_col1:
    R = st.number_input("Recuperados (R)", value=int(seird.get_default("R")), min_value=0)
with row2_col2:
    D = st.number_input("Mortos (D)", value=int(seird.get_default("D")), min_value=0)

st.markdown("### Taxas do Modelos")
col1, col2, col3, col4 = st.columns(4)
with col1:
    r0 = st.number_input("R0", value=float(seird.get_default("r0")), min_value=0.0)
with col2:
    sigma = st.number_input("sigma - Incubação", value=float(seird.get_default("sigma")), min_value=0.0)
with col3:
    gamma = st.number_input("gamma - Recuperação", value=float(seird.get_default("gamma")), min_value=0.0)
with col4:
    mu = st.number_input("mu - Mortalidade", value=float(seird.get_default("mu")), min_value=0.0)

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
    
    seir_fig = seir_solver.get_figure()
    st.plotly_chart(seir_fig, use_container_width=True)
    seird_fig = seird_solver.get_figure()
    st.plotly_chart(seird_fig, use_container_width=True)
else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")
