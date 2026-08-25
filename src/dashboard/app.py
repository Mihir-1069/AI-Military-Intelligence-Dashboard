import sys
from pathlib import Path
import streamlit as st

# Setup Root Directory Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Streamlit Multi-Page Navigation Configuration
home_page = st.Page("pages/00_Home.py", title="Home", icon="🏠", default=True)
threat_page = st.Page("pages/01_Threat_Analysis.py", title="Threat Analysis", icon="📊")
regional_page = st.Page("pages/02_Regional_Intelligence.py", title="Regional Intelligence", icon="🌍")
risk_page = st.Page("pages/03_Risk_Assessment.py", title="Risk Assessment", icon="⚠️")
model_page = st.Page("pages/04_Model_Performance.py", title="Model Performance", icon="🤖")

pg = st.navigation([home_page, threat_page, regional_page, risk_page, model_page])
pg.run()
