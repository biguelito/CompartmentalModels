import streamlit as st

st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/7 - Criação de modelos.py", label="Desenhar Modelo")

st.markdown(f'''
        <h1>Modelos compartimentais</h1>
    ''', unsafe_allow_html=True)
