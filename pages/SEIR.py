import streamlit as st
from CompartmentalModelSolver import CompartmentalModelSolver

def seir_odes(initialValues, time, transfer_rates):
    S, E, I, R = initialValues
    beta, sigma, gamma = transfer_rates
    N = S + E + I + R

    dSdt = -beta * I * (S / N)
    dEdt = beta * I * (S / N) - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I

    return [dSdt, dEdt, dIdt, dRdt]

initS = 1000000
initE = 1
initI = 1
initR = 0
initSigma = 1/3
initGamma = 1/2
initR0 = 4.0
beta = initR0 * initGamma
initDays = 100

st.title("Modelo SEIR Interativo")

st.markdown("Configure os parâmetros abaixo e clique em **Rodar Simulação** para visualizar o gráfico.")

st.subheader("Parâmetros do Modelo")

days = st.slider("Dias de simulação", min_value=1, max_value=365, value=initDays)
st.markdown("**População Inicial**")
S = st.number_input("Susceptíveis (S)", value=initS, min_value=0)
E = st.number_input("Expostos (E)", value=initE, min_value=0)
I = st.number_input("Infectados (I)", value=initI, min_value=0)
R = st.number_input("Recuperados (R)", value=initR, min_value=0)

st.markdown("### Taxas do Modelo SEIR")

R0Col1, SigmaCol2, GammaCol3 = st.columns(3)
with R0Col1:
    r0 = st.number_input("R0", value=initR0, min_value=0.0, max_value=100000.0)
with SigmaCol2:
    sigma = st.number_input("sigma - Incubação", value=initSigma, min_value=0.0, max_value=100000.0)
with GammaCol3:
    gamma = st.number_input("gamma - Recuperação", value=initGamma, min_value=0.0, max_value=100000.0)

if st.button("▶️ Rodar Simulação"):
    beta = r0 * gamma
    initial_conditions = [S, E, I, R]
    transfer_rates = [beta, sigma, gamma]

    solver = CompartmentalModelSolver(seir_odes, initial_conditions, transfer_rates, days)
    solver.solve()

    fig = solver.get_figure()
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")
