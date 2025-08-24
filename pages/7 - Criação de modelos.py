import uuid
import streamlit as st
from typing import List
from streamlit_flow import streamlit_flow as st_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState  # se não existir, use: from streamlit_flow import StreamlitFlowState

st.set_page_config(layout="wide")

if "flow_state" not in st.session_state:
    nodes: List[StreamlitFlowNode] = []
    edges: List[StreamlitFlowEdge] = []
    st.session_state.flow_state = StreamlitFlowState(nodes=nodes, edges=edges)

left, right = st.columns([2, 1])

with left:
    st.subheader("Canvas do modelo")

    # ✅ SEMPRE capture o estado retornado
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
    )

with right:
    st.subheader("Adicionar itens")

    with st.form("form_new_compartment", clear_on_submit=True):
        new_id = st.text_input("Id do compartimento", max_chars=8)
        new_label = st.text_input("Nome do compartimento", max_chars=50)
        pos_x = value=0
        pos_y = 200 + 60*len(st.session_state.flow_state.nodes)

        if st.form_submit_button("➕ Adicionar compartimento"):
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
        if st.form_submit_button("➡️ Adicionar aresta"):
            if src == tgt:
                st.warning("Origem e destino devem ser diferentes.")
            else:
                eid = f"{src}-{tgt}-{uuid.uuid4().hex[:4]}"
                st.session_state.flow_state = StreamlitFlowState(
                    nodes=list(st.session_state.flow_state.nodes),
                    edges=list(st.session_state.flow_state.edges) + [
                        StreamlitFlowEdge(id=eid, source=src, target=tgt, animated=True, label=elabel)
                    ],
                )
                st.rerun()
