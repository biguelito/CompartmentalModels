import streamlit as st
from compartmentals.CompartmentalModelSolver import CompartmentalModelSolver
from models.seir import SEIR

seir = SEIR()

st.title("Modelo SEIR Interativo")
st.image("models/figures/seir.png", caption="modelo SEIR", use_container_width=True)
with st.expander("📘 Mostrar Equações do Modelo SEIR"):
    st.latex(r'''
    \frac{dS}{dt} = -\beta \cdot I \cdot \frac{S}{N}
    ''')
    st.latex(r'''
    \frac{dE}{dt} = \beta \cdot I \cdot \frac{S}{N} - \sigma \cdot E
    ''')
    st.latex(r'''
    \frac{dI}{dt} = \sigma \cdot  E - \gamma \cdot I
    ''')
    st.latex(r'''
    \frac{dR}{dt} = \gamma \cdot I
    ''')
    st.markdown(r'''
    **Onde:**
    - S: suscetíveis  
    - E: expostos  
    - I: infectados  
    - R: recuperados  
    - β - beta: taxa de infecção  
    - σ - sigma: taxa de incubação  
    - γ - gamma: taxa de recuperação  
    - N = S + E + I + R: população total  
    ''')

st.markdown("Configure os parâmetros abaixo e clique em **Rodar Simulação** para visualizar o gráfico.")

days = st.number_input("Dias", value=int(seir.get_default("days")), min_value=0)

st.markdown("### População Inicial")
col1, col2, col3, col4 = st.columns(4)
with col1:
    S = st.number_input("Susceptíveis (S)", value=int(seir.get_default("S")), min_value=0)
with col2:
    E = st.number_input("Expostos (E)", value=int(seir.get_default("E")), min_value=0)
with col3:
    I = st.number_input("Infectados (I)", value=int(seir.get_default("I")), min_value=0)
with col4:
    R = st.number_input("Recuperados (R)", value=int(seir.get_default("R")), min_value=0)

st.markdown("### Taxas do Modelo SEIR")

R0Col1, SigmaCol2, GammaCol3 = st.columns(3)
with R0Col1:
    r0 = st.number_input("R0", value=float(seir.get_default("r0")), min_value=0.0)
with SigmaCol2:
    sigma = st.number_input("sigma - Incubação", value=float(seir.get_default("sigma")), min_value=0.0)
with GammaCol3:
    gamma = st.number_input("gamma - Recuperação", value=float(seir.get_default("gamma")), min_value=0.0)

if st.button("Rodar Simulação"):
    beta = r0 * gamma
    initial_conditions = [S, E, I, R]
    transfer_rates = [beta, sigma, gamma]
    compartments = seir.COMPARTMENTS

    solver = CompartmentalModelSolver(
        ode_function=seir.odes,
        initial_conditions=initial_conditions,
        transfer_rates=transfer_rates,
        days=days,
        compartments=compartments,
        model_name="SEIR"
    )
    solver.solve()
    fig = solver.get_figure()
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")