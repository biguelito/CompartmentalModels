import streamlit as st
import matplotlib.pyplot as plt
from CompartmentalModelSolver import CompartmentalModelSolver
from CompartmentalGraph import CompartmentalGraph

def seir_odes(initialValues, time, transfer_rates):
    S, E, I, R = initialValues
    beta, sigma, gamma = transfer_rates
    N = S + E + I + R

    dSdt = -beta * I * (S / N)
    dEdt = beta * I * (S / N) - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I

    return [dSdt, dEdt, dIdt, dRdt]

st.set_page_config(layout="centered", page_title="SEIR Simulation")
st.title("Simulação SEIR Interativa")

st.subheader(" Parâmetros do Modelo")

days = st.slider("Dias de simulação", min_value=10, max_value=365, value=100)
st.markdown("**População Inicial**")
S = st.number_input("Susceptíveis (S)", value=999, min_value=0)
E = st.number_input("Expostos (E)", value=1, min_value=0)
I = st.number_input("Infectados (I)", value=0, min_value=0)
R = st.number_input("Recuperados (R)", value=0, min_value=0)

st.markdown("### Taxas do Modelo SEIR")

R0Col1, SigmaCol2, GammaCol3 = st.columns(3)
with R0Col1:
    r0 = st.slider("R0", 0.0, 10.0, 0.3)
with SigmaCol2:
    sigma = st.slider("sigma - Incubação", 0.0, 10.0, 0.2)
with GammaCol3:
    gamma = st.slider("gamma - Recuperação", 0.0, 10.0, 0.1)

run_simulation = st.button("▶️ Rodar Simulação")

# --- Executa simulação ---
if run_simulation:
    st.success("Simulando o modelo...")
    
    beta = r0 * gamma
    initial_conditions = [S, E, I, R]
    transfer_rates = [beta, sigma, gamma]

    solver = CompartmentalModelSolver(seir_odes, initial_conditions, transfer_rates, days)
    solver.solve()

    fig = solver.get_figure()
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Configure os parâmetros acima e clique em **Rodar Simulação**.")
