import uuid
import streamlit as st
from typing import List
from streamlit_flow import streamlit_flow as st_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState 

st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/7 - Criação de modelos.py", label="Desenhar Modelo")

if "flow_state" not in st.session_state:
    nodes: List[StreamlitFlowNode] = []
    edges: List[StreamlitFlowEdge] = []
    st.session_state.flow_state = StreamlitFlowState(nodes=nodes, edges=edges)

left, right = st.columns([2, 1])

with left:
    st.subheader("Canvas do modelo")

    flow = st_flow(
        "flow",
        st.session_state.flow_state,
        fit_view=True,
        show_controls=True,
        show_minimap=True,
        get_node_on_click=True,
        get_edge_on_click=True,
        allow_new_edges=True,
        height=520,
        enable_edge_menu=True,
        enable_node_menu=True,
        enable_pane_menu=True
    )

with right:
    st.subheader("Adicionar itens")

    with st.form("form_new_compartment", clear_on_submit=True):
        new_id = st.text_input("Id do compartimento", max_chars=8)
        new_label = st.text_input("Nome do compartimento", max_chars=50)
        pos_x = value=0
        pos_y = 220 + 60*len(st.session_state.flow_state.nodes)

        if st.form_submit_button("Adicionar compartimento"):
            node_id = (new_id.strip().upper() if new_id else uuid.uuid4().hex[:6].upper())
            if any(n.id == node_id for n in st.session_state.flow_state.nodes):
                st.warning(f"ID '{node_id}' já existe.")
            else:
                new_nodes = list(st.session_state.flow_state.nodes) + [
                    StreamlitFlowNode(
                        id=node_id,
                        pos=(int(pos_x), int(pos_y)),
                        data={"content": new_label or node_id},
                        connectable=True, draggable=True, deletable=True
                    )
                ]
                st.session_state.flow_state = StreamlitFlowState(
                    nodes=new_nodes,
                    edges=list(st.session_state.flow_state.edges),
                )
                st.rerun()

    with st.form("add_edge_form", clear_on_submit=True):
        node_ids = [n.id for n in st.session_state.flow_state.nodes]
        src = st.selectbox("Origem", node_ids, key="src_sel")
        tgt = st.selectbox("Destino", node_ids, key="tgt_sel")
        elabel = st.text_input("Rótulo (opcional)")
        if st.form_submit_button("Adicionar conexao"):
            if src == tgt:
                st.warning("Origem e destino devem ser diferentes.")
            else:
                eid = f"{src}-{tgt}-{uuid.uuid4().hex[:4]}"
                new_edges = list(st.session_state.flow_state.edges) + [
                        StreamlitFlowEdge(id=eid, source=src, target=tgt, animated=True, label=elabel, marker_end={'type': 'arrowclosed'}, label_show_bg=True)]
                
                st.session_state.flow_state = StreamlitFlowState(
                    nodes=list(st.session_state.flow_state.nodes),
                    edges=new_edges
                )
                st.rerun()

selected_entity = next((x for x in st.session_state.flow_state.nodes if x.id == flow.selected_id), None)
is_compartment = selected_entity is not None
is_connection = False
if (not is_compartment):
    selected_entity = next((x for x in st.session_state.flow_state.edges if x.id == flow.selected_id), None)
    is_connection = selected_entity is not None

if is_compartment:
    st.markdown(f"Compartimento {selected_entity.data["content"]}")

    with st.form("edit_node_form"):
        new_label = st.text_input("Rótulo do nó", value=selected_entity.data.get("label", selected_entity.id))
        colA, colB = st.columns(2)
        save = colA.form_submit_button("💾 Salvar nó")
        delete = colB.form_submit_button("🗑️ Remover nó")
        if save:
            selected_entity.data["label"] = new_label
            st.rerun()
        if delete:
            new_nodes = [x for x in st.session_state.flow_state.nodes if x.id != selected_entity.id]
            new_edges = [e for e in st.session_state.flow_state.edges if e.source != selected_entity.id and e.target != selected_entity.id]
            
            st.session_state.flow_state = StreamlitFlowState(
                nodes=new_nodes,
                edges=new_edges
            )
            st.rerun()

if is_connection: 
    st.markdown(f"Conexao {selected_entity.label}")

    with st.form("edit_edge_form"):
        selected_entity.label = st.text_input("Rótulo da aresta", value=selected_entity.label or "")
        colA, colB = st.columns(2)
        delete = colB.form_submit_button("🗑️ Remover aresta")
        if delete:
            new_edges = [x for x in st.session_state.flow_state.edges if x.id != selected_entity.id]

            st.session_state.flow_state = StreamlitFlowState(
                nodes=st.session_state.flow_state.nodes,
                edges=new_edges
            )
            st.rerun()