# kpi_card.py

import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# Modal
# ─────────────────────────────────────────────────────────────────────────────

@st.dialog(" ", width="large")
def _show_detail(field: str, params: dict, data: dict) -> None:
    p     = params[field]
    value = data.get(field)

    lo, hi = p.get("alert_low"), p.get("alert_high")
    if value is None:
        status, badge_text = "nodata", "Sin dato"
    elif (lo is not None and value < lo) or (hi is not None and value > hi):
        status, badge_text = "alert", "⚠ ALERTA"
    else:
        status, badge_text = "ok", "✓ OK"

    accent    = {"ok": "#1D9E75", "alert": "#E24B4A", "nodata": "#666"}[status]
    badge_bg  = {"ok": "#0e2418", "alert": "#2a1111", "nodata": "#222"}[status]
    badge_clr = {"ok": "#5cc98a", "alert": "#e87878", "nodata": "#666"}[status]
    header_bg = {"ok": "#0d1f17", "alert": "#1f0d0d", "nodata": "#1a1a1a"}[status]

    if lo is not None and hi is not None:
        alert_range = f"{lo} – {hi} {p['unit']}"
    elif hi is not None:
        alert_range = f"< {hi} {p['unit']}"
    elif lo is not None:
        alert_range = f"> {lo} {p['unit']}"
    else:
        alert_range = "—"

    val_str = (
        f"{value:.1f}" if isinstance(value, (int, float))
        else (str(value) if value is not None else "—")
    )

    # Ocultar X nativa
    st.markdown("""
    <style>
    [data-testid="stDialog"] [data-testid="stBaseButton-headerNoPadding"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="border-left:5px solid {accent}; background:{header_bg};
                padding:16px 20px; border-radius:10px; margin-bottom:12px;
                display:flex; align-items:center; justify-content:space-between;">
        <div>
            <div style="font-size:11px;color:#888;text-transform:uppercase;
                        letter-spacing:.07em;margin-bottom:6px;">{p['label']}</div>
            <div style="font-size:38px;font-weight:800;color:#fff;line-height:1;">
                {val_str} <span style="font-size:17px;font-weight:400;color:#aaa;">{p['unit']}</span>
            </div>
        </div>
        <span style="background:{badge_bg};color:{badge_clr};padding:6px 16px;
                     border-radius:999px;font-size:12px;font-weight:600;
                     border:1px solid {accent}55;">{badge_text}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#111;border:1px solid #2a2a2a;border-radius:10px;
                padding:14px 16px;margin-bottom:12px;font-size:14px;color:#bbb;line-height:1.6;">
        ℹ️ &nbsp;{p['description']}
    </div>
    """, unsafe_allow_html=True)

    oms = p.get('oms', '—')
    epa = p.get('epa', '—')
    st.markdown(f"""
    <div style="display:flex;gap:10px;margin-bottom:12px;">
        <div style="flex:1;background:#111;border:1px solid #2a2a2a;border-radius:10px;padding:12px 14px;">
            <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">Umbral OMS</div>
            <div style="font-size:16px;font-weight:600;color:#ddd;">{oms}</div>
        </div>
        <div style="flex:1;background:#111;border:1px solid #2a2a2a;border-radius:10px;padding:12px 14px;">
            <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">Umbral EPA</div>
            <div style="font-size:16px;font-weight:600;color:#ddd;">{epa}</div>
        </div>
        <div style="flex:1;background:#111;border:1px solid {accent}55;border-radius:10px;padding:12px 14px;">
            <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">Alerta configurada</div>
            <div style="font-size:16px;font-weight:600;color:{accent};">{alert_range}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tips = p.get("tips", [])
    if tips:
        items = "".join(
            f'<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #1e1e1e;">'
            f'<span style="color:{accent};flex-shrink:0;">→</span>'
            f'<span style="font-size:13px;color:#bbb;line-height:1.5;">{t}</span></div>'
            for t in tips
        )
        st.markdown(f"""
        <div style="background:#111;border:1px solid #2a2a2a;border-radius:10px;padding:14px 16px;">
            <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px;">
                Recomendaciones para mejorar</div>
            {items}
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Tarjetas
# ─────────────────────────────────────────────────────────────────────────────

def _inject_card_css():
    st.markdown("""
    <style>

    /* ── Botón "Ver detalle" estilizado ─────────────────────────────── */
    /* Aplica a todos los botones dentro de columnas de tarjetas KPI    */
    div[data-testid="stButton"]:has(button[kind="tertiary"]) button {
        width: 100%;
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 8px !important;
        color: rgba(255,255,255,0.35) !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        padding: 6px 0 !important;
        cursor: pointer !important;
        transition: border-color .2s, color .2s, background .2s !important;
        box-shadow: none !important;
    }
    div[data-testid="stButton"]:has(button[kind="tertiary"]) button:hover {
        border-color: rgba(255,255,255,0.28) !important;
        color: rgba(255,255,255,0.75) !important;
        background: rgba(255,255,255,0.04) !important;
    }
    div[data-testid="stButton"]:has(button[kind="tertiary"]) button:disabled {
        opacity: 0.2 !important;
        cursor: default !important;
    }

    /* ── Tarjeta ─────────────────────────────────────────────────────── */
    .kpi-card {
        border-radius: 12px;
        padding: 16px 16px 14px;
        border-left: 4px solid transparent;
        position: relative;
        transition: filter .15s, transform .12s;
        min-height: 115px;
        margin-bottom: 6px;
    }
    .kpi-card.ok     { background: #111c16; border-left-color: #1D9E75; }
    .kpi-card.alert  { background: #1c1010; border-left-color: #E24B4A; }
    .kpi-card.nodata { background: #1a1a1a; border-left-color: #333; opacity: .5; }

    .kpi-label {
        font-size: 11px; color: #888;
        text-transform: uppercase; letter-spacing: .07em;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 24px; font-weight: 700; color: #fff;
        margin-bottom: 10px; line-height: 1.1;
    }
    .kpi-unit { font-size: 12px; font-weight: 400; color: #666; }

    .kpi-badge {
        display: inline-block; font-size: 11px; font-weight: 600;
        padding: 3px 10px; border-radius: 999px;
    }
    .kpi-badge.ok     { background: #0e2418; color: #5cc98a; border: 1px solid #1D9E7544; }
    .kpi-badge.alert  { background: #2a1111; color: #e87878; border: 1px solid #E24B4A44; }
    .kpi-badge.nodata { background: #222;    color: #666;    border: 1px solid #333; }

    .kpi-arrow {
        position: absolute; bottom: 12px; right: 14px;
        font-size: 14px; color: #ffffff18; transition: color .15s;
    }
    </style>
    """, unsafe_allow_html=True)


def _card_html(p: dict, value, status: str) -> str:
    badge_label = {"ok": "✓ OK", "alert": "⚠ ALERTA", "nodata": "Sin dato"}[status]
    arrow = '<span class="kpi-arrow">↗</span>' if status != "nodata" else ""

    if value is None:
        val_str, unit_str = "—", ""
    elif isinstance(value, float):
        val_str  = f"{value:.1f}"
        unit_str = f'<span class="kpi-unit"> {p["unit"]}</span>'
    else:
        val_str  = str(value)
        unit_str = f'<span class="kpi-unit"> {p["unit"]}</span>'

    return (
        f'<div class="kpi-card {status}">'
        f'  <div class="kpi-label">{p["label"]}</div>'
        f'  <div class="kpi-value">{val_str}{unit_str}</div>'
        f'  <span class="kpi-badge {status}">{badge_label}</span>'
        f'  {arrow}'
        f'</div>'
    )


def render_kpi_cards(data: dict, params: dict, n_cols: int = 4) -> None:
    _inject_card_css()
    fields = list(params.keys())

    for row_start in range(0, len(fields), n_cols):
        row_fields = fields[row_start : row_start + n_cols]
        cols = st.columns(n_cols)

        for col, field in zip(cols, row_fields):
            p      = params[field]
            value  = data.get(field)
            lo, hi = p.get("alert_low"), p.get("alert_high")

            if value is None:
                status = "nodata"
            elif (lo is not None and value < lo) or (hi is not None and value > hi):
                status = "alert"
            else:
                status = "ok"

            with col:
                st.markdown(_card_html(p, value, status), unsafe_allow_html=True)
                clicked = st.button(
                    "Ver detalle",
                    key=f"kpi_btn_{field}",
                    disabled=(status == "nodata"),
                    use_container_width=True,
                    type="tertiary",
                )
                if clicked:
                    st.session_state["__kpi_open"]     = field
                    st.session_state["__kpi_snapshot"] = data.copy()
                    st.rerun()