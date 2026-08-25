import streamlit as st

def render_kpi_card(label: str, value: str, subtext: str = "", color: str = "#38bdf8") -> None:
    """Renders a styled dark-navy KPI card with dynamic font scaling for large numbers like '1,064,954'."""
    val_len = len(str(value))
    if val_len > 10:
        font_style = "font-size: clamp(1.0rem, 1.4vw, 1.3rem);"
    elif val_len > 7:
        font_style = "font-size: clamp(1.1rem, 1.6vw, 1.45rem);"
    else:
        font_style = "font-size: clamp(1.3rem, 1.8vw, 1.7rem);"

    subtext_html = f'<div class="kpi-subtext">{subtext}</div>' if subtext else ""
    html_code = (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value" style="color: {color}; {font_style}">{value}</div>'
        f'{subtext_html}'
        f'</div>'
    )
    st.markdown(html_code, unsafe_allow_html=True)

def render_kpi_grid(kpis: list) -> None:
    """
    Renders a responsive row of KPI cards using Streamlit columns.
    kpis format: list of dicts with keys 'label', 'value', 'subtext', 'color'
    """
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            render_kpi_card(
                label=kpi.get("label", ""),
                value=kpi.get("value", "0"),
                subtext=kpi.get("subtext", ""),
                color=kpi.get("color", "#38bdf8")
            )
