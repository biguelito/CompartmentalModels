import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, List
import uuid

from streamlit_flow import streamlit_flow as st_flow, StreamlitFlowState
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge

st.set_page_config(page_title="Construtor de Modelos Compartimentais", layout="wide")

# ---------- Estado ----------
if "nodes" not in st.session_state:
    st.session_state.nodes: List[StreamlitFlowNode] = [
        # StreamlitFlowNode(id="S", pos=(0, 0),   data={"label": "S: Suscetíveis", "init": 1000}),
        # StreamlitFlowNode(id="E", pos=(200, 0), data={"label": "E: Expostos",     "init": 1}),
        # StreamlitFlowNode(id="I", pos=(400, 0), data={"label": "I: Infectados",   "init": 1}),
        # StreamlitFlowNode(id="R", pos=(600, 0), data={"label": "R: Recuperados",  "init": 0}),
    ]

if "edges" not in st.session_state:
    st.session_state.edges: List[StreamlitFlowEdge] = []

initial_state = StreamlitFlowState(
    nodes=st.session_state.nodes,
    edges=st.session_state.edges
)

# Propriedades extras de arestas (fórmula, nome de taxa, etc.)
if "edge_props" not in st.session_state:
    st.session_state.edge_props: Dict[str, Dict] = {}

# Parâmetros globais (variáveis de taxa)
if "globals" not in st.session_state:
    st.session_state.globals: Dict[str, float] = {
        "beta": 0.3,
        "sigma": 0.2,
        "gamma": 0.1,
        "mu": 0.0,
        "alpha": 0.0,
    }

# ---------- UI ----------
st.title("Construtor de Modelos Compartimentais (no-code)")

left, right = st.columns([2, 1])

with left:
    st.subheader("Canvas do modelo")
    element = st_flow(
        fit_view=True,
        show_controls=True,
        show_minimap=True,
        get_node_on_click=True,
        get_edge_on_click=True,
        height=520,
        key="flow",
        state=initial_state
    )
    st.caption("Dica: arraste nós para reposicioná-los; conecte nós arrastando das “alças” (handles).")

with right:
    st.subheader("Adicionar itens")

    with st.form("add_node_form", clear_on_submit=True):
        nid = st.text_input("ID do nó (ex.: S, E, I, R)")
        nlabel = st.text_input("Rótulo", value="")
        ninit = st.number_input("Valor inicial", min_value=0, value=0)
        submitted_node = st.form_submit_button("Adicionar nó")
        if submitted_node:
            if not nid:
                nid = str(uuid.uuid4())[:6]
            st.session_state.nodes.append(
                StreamlitFlowNode(
                    id=nid,
                    pos=(100 * len(st.session_state.nodes), 0),
                    data={"label": nlabel if nlabel else nid, "init": ninit},
                    selectable=True,
                )
            )
            st.rerun()

    with st.form("add_edge_form", clear_on_submit=True):
        node_ids = [n.id for n in st.session_state.nodes]
        if not node_ids:
            st.info("Crie nós primeiro para poder criar arestas.")
        src = st.selectbox("Origem", node_ids, key="src_sel")
        tgt = st.selectbox("Destino", node_ids, key="tgt_sel")
        elabel = st.text_input("Rótulo da aresta (opcional)", value="")
        submitted_edge = st.form_submit_button("➡️ Adicionar aresta")
        if submitted_edge:
            eid = f"{src}-{tgt}-{uuid.uuid4().hex[:4]}"
            st.session_state.edges.append(
                StreamlitFlowEdge(
                    id=eid, source=src, target=tgt, animated=True, label=elabel
                )
            )
            # props default da aresta
            st.session_state.edge_props[eid] = {
                "formula": "",     # ex.: beta * S * I / N
                "rate_name": "",   # ex.: beta
            }
            st.rerun()

    # st.divider()
    # st.subheader("Parâmetros globais")
    # with st.form("globals_form"):
    #     cols = st.columns(2)
    #     items = list(st.session_state.globals.items())
    #     for i, (k, v) in enumerate(items):
    #         with cols[i % 2]:
    #             st.session_state.globals[k] = st.number_input(k, value=float(v), step=0.0001, format="%.6f")
    #     st.form_submit_button("Salvar parâmetros")

st.divider()

# ---------- Edição do elemento selecionado ----------

node = next((x for x in st.session_state.nodes if x.id == element.selected_id), None)
is_node = node is not None
st.markdown(f"**Selecionado:** `{"No" if is_node else "Aresta"}` • id `{element.selected_id}`")

# etype = element["elementType"]
# eid = element["id"]

# if etype == "node":
#     # localizar nó
#     n = next((x for x in st.session_state.nodes if x.id == eid), None)
#     if n:
#         with st.form("edit_node_form"):
#             new_label = st.text_input("Rótulo do nó", value=n.data.get("label", n.id))
#             new_init = st.number_input("Valor inicial", value=float(n.data.get("init", 0.0)))
#             colA, colB = st.columns(2)
#             save = colA.form_submit_button("💾 Salvar nó")
#             delete = colB.form_submit_button("🗑️ Remover nó")
#             if save:
#                 n.data["label"] = new_label
#                 n.data["init"] = new_init
#                 st.rerun()
#             if delete:
#                 # remover nós e arestas conectadas
#                 st.session_state.nodes = [x for x in st.session_state.nodes if x.id != eid]
#                 st.session_state.edges = [e for e in st.session_state.edges if e.source != eid and e.target != eid]
#                 st.rerun()

# elif etype == "edge":
#     e = next((x for x in st.session_state.edges if x.id == eid), None)
#     if e:
#         props = st.session_state.edge_props.get(eid, {"formula": "", "rate_name": ""})
#         with st.form("edit_edge_form"):
#             e.label = st.text_input("Rótulo da aresta", value=e.label or "")
#             props["rate_name"] = st.text_input("Nome da taxa (opcional, ex.: beta)", value=props.get("rate_name",""))
#             props["formula"] = st.text_input(
#                 "Fórmula do fluxo (ex.: beta * S * I / N)",
#                 value=props.get("formula", "")
#             )
#             colA, colB = st.columns(2)
#             save = colA.form_submit_button("💾 Salvar aresta")
#             delete = colB.form_submit_button("🗑️ Remover aresta")
#             if save:
#                 st.session_state.edge_props[eid] = props
#                 st.rerun()
#             if delete:
#                 st.session_state.edges = [x for x in st.session_state.edges if x.id != eid]
#                 st.session_state.edge_props.pop(eid, None)
#                 st.rerun()

# ---------- Geração das EDOs a partir do grafo ----------
# st.divider()
# st.subheader("Gerar EDOs a partir do grafo")

# def build_odes_text():
#     # Mapear ID -> símbolo (usa rótulo até ":", se houver)
#     ids = [n.id for n in st.session_state.nodes]
#     labels = []
#     initials = []
#     for n in st.session_state.nodes:
#         # símbolo curto antes de ":" ou o próprio id
#         sym = (n.data.get("label") or n.id).split(":")[0].strip()
#         labels.append(sym)
#         initials.append(n.data.get("init", 0.0))

#     idx_by_id = {n.id: i for i, n in enumerate(st.session_state.nodes)}
#     inflow = {i: [] for i in ids}
#     outflow = {i: [] for i in ids}

#     # Distribuir termos das arestas
#     for e in st.session_state.edges:
#         frm, to = e.source, e.target
#         props = st.session_state.edge_props.get(e.id, {})
#         f = props.get("formula", "").strip()
#         term = f if f else (e.label or f"flow_{e.id}")
#         outflow[frm].append(term)
#         inflow[to].append(term)

#     # Construir texto Python e LaTeX
#     lines_py = []
#     lines_tex = []
#     lines_py.append("def odes(values, t, params):")
#     lines_py.append(f"    # ordem dos compartimentos: {', '.join(labels)}")
#     lines_py.append(f"    {', '.join(labels)} = values")
#     lines_py.append(f"    N = " + " + ".join(labels))  # população simbólica
#     if st.session_state.globals:
#         lines_py.append("    " + ", ".join(st.session_state.globals.keys()) + " = " +
#                         ", ".join([f"params['{k}']" for k in st.session_state.globals.keys()]))

#     for nid, n in zip(ids, st.session_state.nodes):
#         sym = (n.data.get("label") or n.id).split(":")[0].strip()
#         rhs_terms = []
#         rhs_terms += [f"(+ {expr})" for expr in inflow[nid]]
#         rhs_terms += [f"(- {expr})" for expr in outflow[nid]]
#         rhs = " ".join(rhs_terms) if rhs_terms else "0.0"
#         lines_py.append(f"    d{sym}dt = {rhs}")

#         # LaTeX
#         rhs_tex = []
#         rhs_tex += [f"+\\,({expr})" for expr in inflow[nid]]
#         rhs_tex += [f"-\\,({expr})" for expr in outflow[nid]]
#         rhs_tex = " ".join(rhs_tex) if rhs_tex else "0"
#         lines_tex.append(f"$$\\frac{{d{sym}}}{{dt}} = {rhs_tex}$$")

#     lines_py.append("    return [" + ", ".join([f"d{(n.data.get('label') or n.id).split(':')[0].strip()}dt" for n in st.session_state.nodes]) + "]")

#     return "\n".join(lines_py), "\n".join(lines_tex), labels, initials

# col1, col2 = st.columns([3, 2], vertical_alignment="top")
# with col1:
#     if st.button("🧮 Gerar EDOs"):
#         py_txt, tex_txt, labels, initials = build_odes_text()
#         st.code(py_txt, language="python")
#         st.markdown("**LaTeX das EDOs:**")
#         st.markdown(tex_txt)

# with col2:
#     st.markdown("**Parâmetros (dict) sugerido para o solver:**")
#     st.code(
#         "{\n" + ",\n".join([f"  '{k}': {v}" for k, v in st.session_state.globals.items()]) + "\n}",
#         language="python"
#     )
#     st.markdown("**Valores iniciais (na mesma ordem dos compartimentos):**")
#     _, _, labels, initials = build_odes_text()
#     st.code(f"{initials}  # ordem: {labels}", language="python")
