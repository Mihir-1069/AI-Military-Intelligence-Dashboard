import sys
from pathlib import Path
import streamlit as st

# Setup Root Directory Path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Streamlit Multi-Page Navigation Configuration
PAGES_DIR = CURRENT_DIR / "pages"

home_page = st.Page(str(PAGES_DIR / "00_Home.py"), title="Home", icon="🏠", default=True)
threat_page = st.Page(str(PAGES_DIR / "01_Threat_Analysis.py"), title="Threat Analysis", icon="📊")
regional_page = st.Page(str(PAGES_DIR / "02_Regional_Intelligence.py"), title="Regional Intelligence", icon="🌍")
risk_page = st.Page(str(PAGES_DIR / "03_Risk_Assessment.py"), title="Risk Assessment", icon="⚠️")
model_page = st.Page(str(PAGES_DIR / "04_Model_Performance.py"), title="Model Performance", icon="🤖")

pg = st.navigation([home_page, threat_page, regional_page, risk_page, model_page])
pg.run()
