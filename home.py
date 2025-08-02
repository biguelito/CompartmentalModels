import streamlit as st

# --- Configuração da página principal ---
st.set_page_config(page_title="Modelos Compartimentais", layout="centered")

st.markdown(f'''
        <h1>Modelos compartimentais</h1>
    ''', unsafe_allow_html=True)

# # --- Menu lateral de seleção de modelos ---
# st.sidebar.title("📊 Escolha o Modelo")
# model_option = st.sidebar.selectbox(
#     "Modelo Compartimental",
#     ["SEIR"]  # Adicione mais aqui no futuro, como "SIR", "SEIRS", etc.
# )

# # --- Renderização conforme modelo escolhido ---
# if model_option == "SEIR":
#     render_seir()
# else:
#     st.error("Modelo ainda não implementado.")
