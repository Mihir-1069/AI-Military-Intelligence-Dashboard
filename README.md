# AI-Powered Military Intelligence Dashboard

An End-to-End Academic Defensive Analytics and Strategic Threat Assessment System built with Python, Machine Learning, and Streamlit.

---

## 🛡️ Academic & Defensive Analytics Disclaimer

> **IMPORTANT**: This project is developed strictly for **academic research, statistical modeling, and defensive analytics**.  
> The system **DOES NOT** provide:
> - Tactical or operational military targeting recommendations
> - Individual person tracking or operational deployment instructions
> - Planning or assistance for real-world violence or operations
> 
> All predictive risk scores, threat maps, and analytics represent **aggregate, non-operational statistical outputs** derived from historical event records.

---

## 📌 Project Overview & Problem Statement

Modern defense analytics and strategic intelligence rely on historical pattern recognition, spatio-temporal trend analysis, and predictive machine learning models to assess macro-level threat environments. 

This project delivers a complete, modular, GitHub-ready software system designed to:
1. Process and clean historical global terrorism event datasets (135 schema attributes).
2. Perform dynamic temporal splitting by event year (`iyear`).
3. Compute statistical distributions, Year-over-Year (YoY) trend metrics, and anomaly activity spikes.
4. Engineer non-leaking domain features and formulate aggregate threat severity targets.
5. Train a robust `RandomForestClassifier` machine learning model to evaluate threat probabilities.
6. Provide an interactive multi-page **Streamlit Dashboard** for defensive decision support.

---

## 📂 Project Structure

```
AI-Military-Intelligence-Dashboard/
│
├── data/
│   ├── raw/
│   │   └── globalterrorismdb_0522dist.xlsx
│   ├── yearly/
│   │   └── .gitkeep
│   └── processed/
│       ├── cleaned_data.csv
│       ├── engineered_features.csv
│       └── predictions.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_training.ipynb
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   ├── preprocess.py
│   │   └── split_by_year.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── feature_engineering.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── statistical_analysis.py
│   │   └── trend_analysis.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   └── maps.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── assets/
│   │   │   └── style.css
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── kpi_cards.py
│   │   │   ├── insight_cards.py
│   │   │   ├── risk_card.py
│   │   │   └── chart_helpers.py
│   │   └── pages/
│   │       ├── 01_Threat_Analysis.py
│   │       ├── 02_Regional_Intelligence.py
│   │       ├── 03_Risk_Assessment.py
│   │       └── 04_Model_Performance.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── helper.py
│
├── models/
│   ├── threat_model.pkl
│   └── model_metadata.json
│
├── reports/
│   ├── figures/
│   └── screenshots/
│
├── powerbi/
├── requirements.txt
├── README.md
├── .gitignore
└── run.py
```

---

## 📊 Dataset Schema & Columns Used

The project uses the **Global Terrorism Database (GTD)** dataset (`globalterrorismdb_0522dist.xlsx`). Out of ~135 columns, a configurable list of 32 key analytical columns is extracted to optimize memory:

- **Identifiers & Time**: `eventid`, `iyear`, `imonth`, `iday`
- **Geography**: `country`, `country_txt`, `region`, `region_txt`, `provstate`, `city`, `latitude`, `longitude`, `location`
- **Incident Details**: `summary`, `multiple`, `success`, `suicide`, `ishostkid`, `property`, `propvalue`
- **Tactics & Weapons**: `attacktype1`, `attacktype1_txt`, `weaptype1`, `weaptype1_txt`
- **Targets & Perpetrators**: `targtype1`, `targtype1_txt`, `target1`, `natlty1`, `natlty1_txt`, `gname`
- **Casualties**: `nkill`, `nwound`

---

## ⚙️ Data Pipeline & Machine Learning Methodology

### 1. Data Cleaning (`src/data/preprocess.py`)
- Removes duplicates on `eventid`.
- Replaces coordinate sentinels (`-99`) with `NaN` and validates boundaries ($-90 \le \text{lat} \le 90$).
- Imputes missing casualty numbers with 0.
- Normalizes categorical string placeholders (`"Unknown"`).

### 2. Feature Engineering (`src/features/feature_engineering.py`)
- **Derived Metrics**: Calculates `total_casualties = nkill + nwound`, `has_casualties`, and `lethality_ratio`.
- **Target Variable Formulation**: Defines binary target `high_severity_event = 1` if `total_casualties >= 1` or `suicide == 1`, else `0`.
- **Encoding**: Applies frequency encoding and categorical ID encoding to high-cardinality geographic and tactical columns.

### 3. Machine Learning Model (`src/models/train.py`)
- **Classifier**: `RandomForestClassifier` with balanced class weights (`n_estimators=100`, `max_depth=15`).
- **Data Leakage Prevention**: Excludes direct casualty numbers (`nkill`, `nwound`) from input predictors $X$, relying exclusively on incident context (theater region, tactic, weapon, target type, suicide flag, location).
- **Persistence**: Exports trained model to `models/threat_model.pkl` and JSON metadata to `models/model_metadata.json`.

---

## 🚀 Installation & Setup

1. **Clone Repository**:
   ```bash
   git clone https://github.com/your-username/AI-Military-Intelligence-Dashboard.git
   cd AI-Military-Intelligence-Dashboard
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Place Dataset**:
   Ensure `globalterrorismdb_0522dist.xlsx` is placed in `data/raw/`.

---

## 💻 Pipeline Execution Commands (`run.py`)

Run individual stages or full execution via `run.py`:

```bash
# Step 1: Split raw dataset into yearly CSV files in data/yearly/
python run.py split

# Step 2: Clean and preprocess raw data -> data/processed/cleaned_data.csv
python run.py preprocess

# Step 3: Engineer domain features & target -> data/processed/engineered_features.csv
python run.py features

# Step 4: Train Random Forest Classifier model -> models/threat_model.pkl
python run.py train

# Step 5: Evaluate model performance & save plots to reports/figures/
python run.py evaluate

# Step 6: Generate predictions -> data/processed/predictions.csv
python run.py predict

# Launch Streamlit Multi-Page Dashboard
python run.py dashboard

# OR Execute full end-to-end pipeline in one step
python run.py all
```

---

## 🖥️ Streamlit Multi-Page Dashboard Features

Launch using `streamlit run src/dashboard/app.py` or `python run.py dashboard`:

- **🏠 Main Overview (`app.py`)**: Aggregate KPIs (Total Events, Total Casualties, Countries Affected, Regions Affected, Years Covered), global filters, temporal trends, region vs tactic breakdown, density heatmap, and dynamic insight cards.
- **📊 01 Threat Analysis (`pages/01_Threat_Analysis.py`)**: 3-year rolling average timeline, Year-over-Year (YoY) shift indicators (`↑ INCREASING`, `↓ DECREASING`, `→ STABLE`), activity spike anomaly detection, tactical attack/target/weapon distribution tabs, and casualty severity metrics.
- **🌍 02 Regional Intelligence (`pages/02_Regional_Intelligence.py`)**: Primary region selector, regional KPIs, ranked summary table with activity share %, interactive regional map, and multi-region temporal comparison line chart.
- **⚠️ 03 Risk Assessment (`pages/03_Risk_Assessment.py`)**: Real-time event attribute selection panel, model threat classification, risk summary card with probability score %, confidence level rating, supporting feature signals, and regional historical trend chart.
- **🤖 04 Model Performance (`pages/04_Model_Performance.py`)**: Quantitative metric cards (Accuracy, Precision, Recall, F1 Score, ROC-AUC), confusion matrix heatmap, feature importance drivers chart, and model specification metadata.

---

## 👥 Team Responsibilities & Git Workflow

Organized for modular development across 5 team members:

- **Member 1 (Data Lead)**: `src/data/` (Data loading, cleaning, year-wise splitting).
- **Member 2 (Analytics & Visualization Lead)**: `src/analysis/`, `src/visualization/` (Statistical breakdown, trends, charts, maps).
- **Member 3 (Feature Engineering Lead)**: `src/features/` (Derived metrics, categorical encoding, feature pipeline).
- **Member 4 (Documentation & QA Lead)**: `notebooks/`, `reports/`, documentation validation.
- **Project Lead**: `src/models/`, `src/dashboard/`, `run.py`, system integration.

---

## ⚠️ Limitations & Future Improvements

- **Limitations**: Historical database relies on public media reporting; missing geographic coordinates in legacy entries.
- **Future Enhancements**: Incorporate spatial-temporal graph neural networks (GNNs), multi-class attack risk categorizations, and automated quarterly ingestion pipelines.
