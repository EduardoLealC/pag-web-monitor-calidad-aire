import streamlit as st
from data.influx import get_latest_values
from component.kpi_card import render_kpi_cards, _show_detail
from config import PARAMS


@st.fragment(run_every=300)
def _data_fragment():
    with st.spinner("Consultando sensores..."):
        data = get_latest_values()
    render_kpi_cards(data, PARAMS)


def render():
    st.title("Monitor de Calidad de Aire")
    st.caption("Laboratorio Mancera — actualización cada 5 min")

    # Modal fuera del fragment — sobrevive los reruns de 5 min
    if st.session_state.get("__kpi_open"):
        field    = st.session_state.pop("__kpi_open")
        snapshot = st.session_state.pop("__kpi_snapshot", {})
        _show_detail(field, PARAMS, snapshot)

    _data_fragment()

    st.divider()
    st.subheader("Visualización completa")
    grafana_url = "http://146.83.216.213:3000/public-dashboards/debf9db62ab945d8a29128105b3a45bc"
    st.components.v1.iframe(grafana_url, height=800)