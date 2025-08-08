import streamlit as st
from compartmentals.CompartmentalModelSolver import CompartmentalModelSolver
from models.seird import SEIRD

seird = SEIRD()

st.title("Modelo SEIRD Interativo")
st.image("models/figures/seird.png", caption="modelo SEIRD", use_container_width=True)
with st.expander("📘 Mostrar Equações do Modelo SEIRD"):
    st.latex(r'''
    \frac{dS}{dt} = -\beta \cdot I \cdot \frac{S}{N}
    ''')
    st.latex(r'''
    \frac{dE}{dt} = \beta \cdot I \cdot \frac{S}{N} - \sigma \cdot E
    ''')
    st.latex(r'''
    \frac{dI}{dt} = \sigma \cdot  E - \gamma \cdot I - \mu \cdot I
    ''')
    st.latex(r'''
    \frac{dR}{dt} = \gamma \cdot I
    ''')
    st.latex(r'''
    \frac{dD}{dt} = \mu \cdot I
    ''')
    st.markdown(r'''
    **Onde:**
    - S: suscetíveis  
    - E: expostos  
    - I: infectados  
    - R: recuperados
    - D: mortos  
    - β - beta: taxa de infecção  
    - σ - sigma: taxa de incubação  
    - γ - gamma: taxa de recuperação  
    - μ - mu: taxa de mortalidade
    - N = S + E + I + R + D: população total  
    ''')

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

st.markdown("### Taxas do Modelo SEIRD")

use_beta = st.toggle("Inserir β (desligue para inserir R₀)", value=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if use_beta:
        beta = st.number_input("β (beta) - Transmissão", value=float(seird.get_default("beta")), min_value=0.0, step=0.0001, format="%.4f")
    else:   
        r0 = st.number_input("R0", value=float(seird.get_default("r0")), min_value=0.0, step=0.0001, format="%.4f")
with col2:
    sigma = st.number_input("σ (sigma) - Incubação", value=float(seird.get_default("sigma")), min_value=0.0, step=0.0001, format="%.4f")
with col3:
    gamma = st.number_input("γ (gamma) - Recuperação", value=float(seird.get_default("gamma")), min_value=0.0, step=0.0001, format="%.4f")
with col4:
    mu = st.number_input("μ (mu) - Mortalidade", value=float(seird.get_default("mu")), min_value=0.0, step=0.0001, format="%.4f")

if st.button("Rodar Simulação"):
    beta = beta if use_beta else r0 * (gamma + mu)
    initial_conditions = [S, E, I, R, D]
    transfer_rates = [beta, sigma, gamma, mu]
    compartments = seird.COMPARTMENTS

    solver = CompartmentalModelSolver(
        ode_function=seird.odes,
        initial_conditions=initial_conditions,
        transfer_rates=transfer_rates,
        days=days,
        compartments=compartments,
        model_name="SEIRD"
    )
    solver.solve()
    fig = solver.get_figure()
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")
