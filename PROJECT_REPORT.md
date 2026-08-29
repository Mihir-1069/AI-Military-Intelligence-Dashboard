# ACADEMIC ONLINE INTERNSHIP PROJECT TECHNICAL REPORT

---

<div align="center">

# 🛡️ AI-POWERED MILITARY INTELLIGENCE DASHBOARD
### Defensive Analytics, Temporal Trend Modeling, and Machine Learning Threat Severity Assessment

**Bharat Space Education Research Centre (BSERC) Online Internship Program**  
*Academic Research & Software Development Project Report*

---

</div>

> [!IMPORTANT]
> **ACADEMIC & DEFENSIVE RESEARCH DISCLAIMER**  
> This technical report and the underlying software system were developed exclusively for **academic research, statistical modeling, and defensive analytics**. The system provides macro-level historical terrorism trend analysis, aggregate spatial risk heatmaps, and probabilistic threat classification. **No tactical military targeting, operational attack planning, or individual tracking capabilities are included or implied.**

---

## 📋 1. INSTITUTIONAL & MENTORSHIP DETAILS

| Parameter | Official Record Details |
|---|---|
| **Host Organization** | **Bharat Space Education Research Centre (BSERC)** |
| **Regional Office Address** | C-32, Ram Nagar, Sector 14, Kaushambi, Ghaziabad, Delhi NCR, Uttar Pradesh - 201010, India |
| **Faculty / Project Mentor** | **Dr. Smita Agrawal** (Designation: Mentor \| Contact: +91 9928023107) |
| **Program Coordinator** | **Rahul Singh** (Designation: Outreach Director \| Email: `Director@bserc.org` \| Mobile: +91 7303048634) |
| **Official Data Source** | **Global Terrorism Database (GTD)** — START, University of Maryland ([`https://www.start.umd.edu/data-tools/GTD`](https://www.start.umd.edu/data-tools/GTD)) |
| **Project Repository** | `https://github.com/Mihir-1069/AI-Military-Intelligence-Dashboard` |
| **Live Web Application** | `https://ai-military-intelligence-dashboard.streamlit.app` |

---

## 👥 2. TEAM CONTRIBUTORS & OFFICIAL BSERC INTERN IDS

The project architecture was developed with clear modular division. **Mihir Kumar** served as the Project Lead and primary developer, engineering the overall codebase, machine learning pipeline, data cleaning algorithms, and Streamlit dashboard interface. Team members collaborated on specific sub-module scripts:

| Intern Name | Official BSERC Intern ID | Role & Contribution Scope | Codebase Module |
|---|---|---|---|
| **Mihir Kumar** *(Project Lead)* | **BSERC-08200** | **Lead Architect & Primary Developer** (Engineered full pipeline, preprocess engine, feature matrix, ML model, Streamlit multipage app, `run.py`, and Streamlit Cloud deployment) | `src/dashboard/`, `run.py`, `.streamlit/` |
| **Rasleen Kaur** | **BSERC-14865** | **Data Operations & Quality Assurance** (Assisted in dataset validation & schema verification) | `src/data/` |
| **Khushi** | **BSERC-07895** | **Feature Analysis & Encodings** (Collaborated on categorical feature mapping) | `src/features/` |
| **Hitesh Khutela** | **BSERC-02818** | **Machine Learning Experimentation** (Collaborated on model training validation scripts) | `src/models/` |
| **Saloni Bhimrao Rangari** | **BSERC-02699** | **Statistical Metrics & Trend Analysis** (Collaborated on statistical metrics helpers) | `src/analysis/` |

---

## 🎯 3. EXECUTIVE SUMMARY & PROBLEM STATEMENT

### 3.1 Problem Statement
Modern defense research relies heavily on data science, spatio-temporal pattern recognition, and predictive machine learning to evaluate macro-threat environments. Historical event datasets contain valuable indicators regarding tactical shifts, regional hotspots, and severity profiles. However, raw historical records often suffer from high dimensionality, missing geographic coordinates, inconsistent field encodings, and complex multi-year distributions.

### 3.2 System Solution
This project delivers a complete, modular, Python-based academic analytics system named **AI-Military-Intelligence-Dashboard**. The platform processes **209,706 historical event records** spanning 50 years (1970–2020) from the Global Terrorism Database (GTD) published by the National Consortium for the Study of Terrorism and Responses to Terrorism (START), University of Maryland ([`https://www.start.umd.edu/data-tools/GTD`](https://www.start.umd.edu/data-tools/GTD)). The system executes data ingestion, preprocessing, year-wise dataset partitioning, domain feature engineering, machine learning threat classification (`RandomForestClassifier`), and presents the outputs through an interactive Streamlit Community Cloud dashboard.

---

## ⚙️ 4. SYSTEM ARCHITECTURE & DATA PIPELINE

```
+---------------------------------------------------------------------------------+
|                         START UMD GTD RAW DATASET                               |
|                 (https://www.start.umd.edu/data-tools/GTD)                      |
|                           209,706 rows x 135 columns                            |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                       STAGE 1 & 2: DATA CLEANING & SPLITTING                    |
|                (src/data/load_data.py, preprocess.py, split_by_year.py)          |
|    * Selects 32 key columns         * Replaces -99 sentinels with NaN           |
|    * Removes duplicates             * Splits into 50 yearly CSV files           |
|    * Exports cleaned_data.csv (209,706 rows x 32 columns)                      |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                         STAGE 3: FEATURE ENGINEERING                            |
|                  (src/features/feature_engineering.py)                          |
|    * Computes total_casualties = nkill + nwound                                 |
|    * Formulates target high_severity_event (60.35% positive ratio)              |
|    * Frequency & Ordinal Categorical Encoding                                   |
|    * Exports engineered_features.csv (209,706 rows x 46 features)               |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                     STAGE 4 & 5: MACHINE LEARNING & EVALUATION                  |
|                 (src/models/train.py, evaluate.py, predict.py)                  |
|    * Trains RandomForestClassifier (100 trees, max depth 15, balanced weights)  |
|    * Prevents data leakage (Excludes direct casualty counts from X predictors)  |
|    * Achieves 84.57% Accuracy, 89.49% Precision, 92.73% ROC-AUC                 |
|    * Exports threat_model.pkl and predictions.csv                               |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                    STAGE 6: MULTIPAGE STREAMLIT DASHBOARD                       |
|               (src/dashboard/app.py & pages/00_Home to 04_Model)                |
|    * Home / Overview Page           * Regional Intelligence                     |
|    * Threat Analysis & YoY Spikes   * ML Risk Assessment & Performance          |
+---------------------------------------------------------------------------------+
```

---

## 📊 5. FEATURE ENGINEERING & TARGET FORMULATION

To ensure statistical rigor and prevent artificial target leakage, feature engineering was implemented as follows:

### 5.1 Derived Metrics
1. **Total Casualties**:
   $$\text{total\_casualties} = \text{nkill} + \text{nwound}$$
2. **Casualty Flag**:
   $$\text{has\_casualties} = \begin{cases} 1 & \text{if } \text{total\_casualties} > 0 \\ 0 & \text{otherwise} \end{cases}$$
3. **Lethality Ratio**:
   $$\text{lethality\_ratio} = \begin{cases} \frac{\text{nkill}}{\text{total\_casualties}} & \text{if } \text{total\_casualties} > 0 \\ 0 & \text{otherwise} \end{cases}$$

### 5.2 Target Variable Formulation (`high_severity_event`)
The target variable is formulated as a binary classification label indicating high-severity aggregate threat incidents:
$$\text{high\_severity\_event} = \begin{cases} 1 & \text{if } \text{total\_casualties} \ge 1 \lor \text{suicide} = 1 \\ 0 & \text{otherwise} \end{cases}$$
Across the 209,706 cleaned historical records, this produces a balanced class distribution:
- **Positive Target Ratio (`1`)**: **60.35%** (High Severity Incidents)
- **Negative Target Ratio (`0`)**: **39.65%** (Low/Moderate Severity Incidents)

### 5.3 Data Leakage Prevention Strategy
To prevent data leakage during model training, direct casualty measures ($\text{nkill}, \text{nwound}, \text{total\_casualties}, \text{lethality\_ratio}$) are **strictly excluded** from the input predictor matrix $X$. The classifier predicts threat severity using only contextual incident attributes (event year, month, region code, country code, attack tactic code, target category code, weapon category code, suicide flag, success flag, property damage flag, and geographic coordinates).

---

## 🤖 6. MACHINE LEARNING MODEL PERFORMANCE EVALUATION

### 6.1 Model Architecture & Hyperparameters
- **Classifier**: `RandomForestClassifier`
- **Number of Estimators**: 100 decision trees
- **Maximum Depth**: 15
- **Class Weighting**: Balanced (`class_weight="balanced"`)
- **Train/Test Split**: 80% Train (167,764 samples) / 20% Test (41,942 samples) stratified

### 6.2 Quantitative Metrics Summary

| Metric | Score | Metric Description |
|---|---|---|
| **Accuracy** | **84.57%** | Overall correct severity classification ratio |
| **Precision** | **89.49%** | Positive predictive value (Low false positive rate) |
| **Recall** | **84.33%** | Detection sensitivity for high-severity events |
| **F1-Score** | **86.83%** | Harmonic mean of Precision and Recall |
| **ROC-AUC** | **92.73%** | Superior discrimination capability across thresholds |

### 6.3 Top Feature Importance Drivers (Gini Impurity Reduction)
1. **`attacktype1_txt_code`** (Tactical Attack Type Code)
2. **`weaptype1_txt_code`** (Weapon Category Code)
3. **`targtype1_txt_code`** (Target Category Code)
4. **`region_txt_code`** (Geographic Region Code)
5. **`suicide`** (Suicide Tactical Flag)
6. **`success`** (Attack Execution Success Flag)
7. **`latitude` & `longitude`** (Spatial Location Coordinates)

*(Note: Feature importances reflect statistical model reliance during decision splitting and do not imply direct causation).*

---

## 🖥️ 7. STREAMLIT DASHBOARD USER INTERFACE

The Streamlit dashboard interface (`src/dashboard/`) is structured into 5 dedicated multipage views with custom dark charcoal/navy styling (`style.css`):

```
src/dashboard/
├── app.py                            # Streamlit Navigation Config (st.navigation)
├── assets/style.css                  # Global Dark Navy Theme & Responsive Card Styles
├── components/                       # Modular UI Components
│   ├── kpi_cards.py                  # HTML Responsive KPI Grid
│   ├── insight_cards.py              # Automated Dynamic Insights Engine
│   ├── risk_card.py                  # Structured Risk Assessment Card & Semantic Badges
│   └── chart_helpers.py              # Plotly Dark Visualizer Helpers
└── pages/
    ├── 00_Home.py                    # Main Overview Landing View & Global Sidebar Filters
    ├── 01_Threat_Analysis.py         # Temporal Trends, YoY Shift Badges, Anomaly Spikes
    ├── 02_Regional_Intelligence.py   # Theater Region Breakdown, Ranked Table, Comparison
    ├── 03_Risk_Assessment.py         # Real-time Attribute Selection & ML Severity Card
    └── 04_Model_Performance.py       # Metrics Cards, Confusion Matrix & Feature Drivers
```

### 7.1 Semantic Color System
- 🔴 **RED (`#ef4444`)**: High risk / severe warning / fatalities
- 🟡 **AMBER (`#f59e0b`)**: Moderate risk / attention / wounded
- 🟢 **GREEN (`#10b981`)**: Low risk / stable trend
- 🔵 **BLUE (`#38bdf8`)**: Neutral analytical metrics / highlights

---

## 🛠️ 8. PIPELINE EXECUTION & REPOSITORY CONTROL

All pipeline stages can be executed via the central CLI runner `run.py`:

```bash
# Stage 1: Split raw dataset into yearly CSV files in data/yearly/
python run.py split

# Stage 2: Preprocess raw data -> data/processed/cleaned_data.csv
python run.py preprocess

# Stage 3: Engineer domain features & target -> data/processed/engineered_features.csv
python run.py features

# Stage 4: Train Machine Learning threat model -> models/threat_model.pkl
python run.py train

# Stage 5: Evaluate model performance & save figures -> reports/figures/
python run.py evaluate

# Stage 6: Generate predictions CSV -> data/processed/predictions.csv
python run.py predict

# Launch Multi-Page Streamlit Dashboard
python run.py dashboard

# OR Execute full end-to-end pipeline in one step
python run.py all
```

---

## 🎓 9. CONCLUSION & FUTURE ENHANCEMENTS

### 9.1 Academic & Technical Summary
During the online internship program at **Bharat Space Education Research Centre (BSERC)**, an academic-grade data science application was engineered. The project addresses data cleaning across 209,706 historical incidents from START UMD GTD, implements data leakage safeguards, achieves strong machine learning classification accuracy (**84.57%** / **92.73% ROC-AUC**), and delivers an interactive dashboard deployed on Streamlit Cloud.

### 9.2 Future Scope & Enhancements
1. **Spatial-Temporal Graph Neural Networks (GNNs)**: Model regional group connections and cross-border threat transfers.
2. **Multi-Class Severity Classification**: Expand binary classification into 4 discrete risk tiers (Critical, Severe, Elevated, Low).
3. **Automated Data Ingestion Pipelines**: Integrate quarterly GTD dataset updates automatically via Cloud DTS workflows.

---

## 🌐 10. OFFICIAL VIRTUAL VERIFICATION LOG

*This report was completed as part of the official online remote internship program organized by Bharat Space Education Research Centre (BSERC). Digital verification records for all participating interns are logged below:*

<br>

| Intern Name | BSERC Intern ID | Role Scope | Verification Status |
|---|---|---|---|
| **Mihir Kumar** *(Project Lead)* | **BSERC-08200** | **Lead Architect & Primary Developer** | **VERIFIED & COMPLETED** |
| **Rasleen Kaur** | **BSERC-14865** | **Data Operations & QA** | **VERIFIED & COMPLETED** |
| **Khushi** | **BSERC-07895** | **Feature Analysis & Encodings** | **VERIFIED & COMPLETED** |
| **Hitesh Khutela** | **BSERC-02818** | **Machine Learning Experimentation** | **VERIFIED & COMPLETED** |
| **Saloni Bhimrao Rangari** | **BSERC-02699** | **Statistical Metrics & Trend Analysis** | **VERIFIED & COMPLETED** |

<br><br>

---

### 🛡️ INSTITUTIONAL APPROVAL RECORD

<table width="100%">
<tr>
<td width="50%" valign="top">

**Faculty / Project Mentor:**  
**Dr. Smita Agrawal**  
Designation: Mentor  
Bharat Space Education Research Centre (BSERC)  
Contact: +91 9928023107  
*Status: Approved via BSERC Virtual Evaluation*

</td>
<td width="50%" valign="top">

**Program Coordinator:**  
**Rahul Singh**  
Designation: Outreach Director  
Bharat Space Education Research Centre (BSERC)  
Email: `Director@bserc.org` \| Mobile: +91 7303048634  
*Status: Approved via BSERC Outreach Management*

</td>
</tr>
</table>

---
*Official Office Address: Bharat Space Education Research Centre / Regional Office: C-32, Ram Nagar, Sector 14, Kaushambi, Ghaziabad, Delhi NCR, Uttar Pradesh - 201010, India*
