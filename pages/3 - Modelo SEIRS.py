import streamlit as st
from compartmentals.CompartmentalModelSolver import CompartmentalModelSolver
from models.seirs import SEIRS

seirs = SEIRS()

st.title("Modelo SEIRS Interativo")
st.image("models/figures/seirs.png", caption="modelo SEIR", use_container_width=True)
with st.expander("📘 Mostrar Equações do Modelo SEIRS"):
    st.latex(r'''
    \frac{dS}{dt} = -\beta \cdot I \cdot \frac{S}{N} + \alpha \cdot R
    ''')
    st.latex(r'''
    \frac{dE}{dt} = \beta \cdot I \cdot \frac{S}{N} - \sigma \cdot E
    ''')
    st.latex(r'''
    \frac{dI}{dt} = \sigma \cdot  E - \gamma \cdot I
    ''')
    st.latex(r'''
    \frac{dR}{dt} = \gamma \cdot I - \alpha \cdot R
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
    - α - alfa: taxa de perda de imunidade
    - N = S + E + I + R: população total  
    ''')

st.markdown("Configure os parâmetros abaixo e clique em **Rodar Simulação** para visualizar o gráfico.")

days = st.number_input("Dias", value=int(seirs.get_default("days")), min_value=0)

st.markdown("### População Inicial")
col1, col2, col3, col4 = st.columns(4)
with col1:
    S = st.number_input("Susceptíveis (S)", value=int(seirs.get_default("S")), min_value=0)
with col2:
    E = st.number_input("Expostos (E)", value=int(seirs.get_default("E")), min_value=0)
with col3:
    I = st.number_input("Infectados (I)", value=int(seirs.get_default("I")), min_value=0)
with col4:
    R = st.number_input("Recuperados (R)", value=int(seirs.get_default("R")), min_value=0)

st.markdown("### Taxas do Modelo SEIRS")
col1, col2, col3, col4 = st.columns(4)
with col1:
    r0 = st.number_input("R0", value=float(seirs.get_default("r0")), min_value=0.0)
with col2:
    sigma = st.number_input("sigma - Incubação", value=float(seirs.get_default("sigma")), min_value=0.0)
with col3:
    gamma = st.number_input("gamma - Recuperação", value=float(seirs.get_default("gamma")), min_value=0.0)
with col4:
    alfa = st.number_input("alfa - Perda de imunidade", value=float(seirs.get_default("alfa")), min_value=0.0)

if st.button("Rodar Simulação"):
    beta = r0 * gamma
    initial_conditions = [S, E, I, R]
    transfer_rates = [beta, sigma, gamma, alfa]
    compartments = seirs.COMPARTMENTS

    solver = CompartmentalModelSolver(
        ode_function=seirs.odes,
        initial_conditions=initial_conditions,
        transfer_rates=transfer_rates,
        days=days,
        compartments=compartments,
        model_name="SEIRS"
    )
    solver.solve()
    fig = solver.get_figure()
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Configure os parâmetros e clique em **Rodar Simulação**.")
