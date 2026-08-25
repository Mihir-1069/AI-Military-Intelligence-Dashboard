import streamlit as st

def render_risk_assessment_card(
    risk_category: str,
    probability: float,
    confidence_level: str,
    supporting_signals: dict,
    model_name: str = "RandomForestClassifier"
) -> None:
    """
    Renders structured risk assessment card with semantic color badges and valid HTML DOM hierarchy.
    """
    cat_upper = risk_category.upper()
    if "HIGH" in cat_upper:
        card_class = "risk-card-high"
        badge_class = "badge-high"
        badge_text = "HIGH RISK CLASSIFICATION"
    elif "MODERATE" in cat_upper:
        card_class = "risk-card-moderate"
        badge_class = "badge-moderate"
        badge_text = "MODERATE RISK CLASSIFICATION"
    else:
        card_class = "risk-card-low"
        badge_class = "badge-low"
        badge_text = "LOW RISK CLASSIFICATION"

    html_code = (
        f'<div class="risk-card {card_class}">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">'
        f'<span class="risk-badge {badge_class}">{badge_text}</span>'
        f'<span style="font-size: 0.85rem; opacity: 0.8;">Model: <strong>{model_name}</strong></span>'
        f'</div>'
        f'<div style="font-size: 2.2rem; font-weight: 700; font-family: monospace; margin: 8px 0;">'
        f'{probability * 100:.1f}% <span style="font-size: 1rem; font-weight: 400; opacity: 0.8;">Threat Severity Probability</span>'
        f'</div>'
        f'<div style="font-size: 0.9rem;">'
        f'Model Confidence Rating: <strong>{confidence_level.upper()}</strong>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_code, unsafe_allow_html=True)

    if supporting_signals:
        st.markdown("##### 📌 Key Analytical Feature Signals")
        cols = st.columns(len(supporting_signals))
        for col, (feat_name, feat_val) in zip(cols, supporting_signals.items()):
            with col:
                st.metric(label=feat_name, value=str(feat_val))
