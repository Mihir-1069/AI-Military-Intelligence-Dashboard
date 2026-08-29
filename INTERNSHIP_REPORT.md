# BSERC ONLINE INTERNSHIP PROJECT COMPLETION REPORT

---

<div align="center">

# 🎓 BHARAT SPACE EDUCATION RESEARCH CENTRE (BSERC)
### REGIONAL OFFICE: C-32, RAM NAGAR, SECTOR 14, KAUSHAMBI, GHAZIABAD, DELHI NCR, UTTAR PRADESH - 201010, INDIA

<br>

## A FORMAL COMPREHENSIVE ONLINE INTERNSHIP TRAINING & PROJECT REPORT ON
# 🛡️ AI-POWERED MILITARY INTELLIGENCE DASHBOARD
***Defensive Analytics, Temporal Trend Modeling, and Machine Learning Threat Severity Assessment***

<br>

**Submitted in Partial Fulfillment for the Completion of Remote/Online Internship Program at BSERC**

<br>

---

### 👨‍💻 **STUDENT INTERN TEAM & OFFICIAL BSERC IDs**

| Intern Name | Official BSERC Intern ID | Assigned Project Role | Core Ownership Scope |
|---|---|---|---|
| **Mihir Kumar** *(Project Lead)* | **BSERC-08200** | **Lead Architect & Primary Developer** | Engineered full data pipeline, preprocessing engine, feature matrix, ML model, Streamlit multipage application (`app.py`, `00` to `04`), dark theme CSS (`style.css`), CLI runner (`run.py`), and Streamlit Cloud deployment |
| **Rasleen Kaur** | **BSERC-14865** | **Data Operations & Quality Assurance** | Assisted in raw dataset field validation, coordinate verification, and schema checks |
| **Khushi** | **BSERC-07895** | **Feature Analysis & Encodings** | Collaborated on categorical feature mapping and attack tactic value counts |
| **Hitesh Khutela** | **BSERC-02818** | **Machine Learning Experimentation** | Collaborated on model parameter testing and validation split scripts |
| **Saloni Bhimrao Rangari** | **BSERC-02699** | **Statistical Metrics & Trend Analysis** | Collaborated on regional metric calculations and annual trend aggregates |

---

### 🏫 **MENTORSHIP & MANAGEMENT DETAILS**
- **Faculty / Project Mentor**: **Dr. Smita Agrawal** (Designation: Mentor \| Contact: +91 9928023107)
- **Program Coordinator**: **Rahul Singh** (Designation: Outreach Director \| Email: `Director@bserc.org` \| Mobile: +91 7303048634)
- **Host Institution**: **Bharat Space Education Research Centre (BSERC)**
- **Official Data Source**: **Global Terrorism Database (GTD)** — National Consortium for the Study of Terrorism and Responses to Terrorism (START), University of Maryland ([`https://www.start.umd.edu/data-tools/GTD`](https://www.start.umd.edu/data-tools/GTD))
- **Live Deployed Web Application**: [`https://ai-military-intelligence-dashboard-azou6rjqnalb6pttxubte9.streamlit.app/`](https://ai-military-intelligence-dashboard-azou6rjqnalb6pttxubte9.streamlit.app/)
- **GitHub Repository**: [`https://github.com/Mihir-1069/AI-Military-Intelligence-Dashboard`](https://github.com/Mihir-1069/AI-Military-Intelligence-Dashboard)

---

</div>

<br>

> [!IMPORTANT]
> **ACADEMIC & DEFENSIVE RESEARCH DISCLAIMER**  
> This internship project report and the associated software application were developed strictly for **academic research, statistical data analysis, and defensive analytics**. The system provides macro-level historical threat trend analysis, aggregate spatial risk heatmaps, and probabilistic threat severity classification. **No tactical military targeting, operational attack recommendations, or individual tracking capabilities are included or implied.**

---

## 📄 CERTIFICATE OF ONLINE INTERNSHIP COMPLETION

<div align="center">

### **BHARAT SPACE EDUCATION RESEARCH CENTRE (BSERC)**
*Regional Office: C-32, Ram Nagar, Sector 14, Kaushambi, Ghaziabad, Delhi NCR, Uttar Pradesh - 201010, India*

</div>

<br>

This is to certify that **Mihir Kumar** (Project Lead & System Architect, ID: BSERC-08200), **Rasleen Kaur** (ID: BSERC-14865), **Khushi** (ID: BSERC-07895), **Hitesh Khutela** (ID: BSERC-02818), and **Saloni Bhimrao Rangari** (ID: BSERC-02699) have successfully completed their online research internship program at **Bharat Space Education Research Centre (BSERC)**.

During the virtual internship period, the intern team developed an end-to-end data science project titled **"AI-Powered Military Intelligence Dashboard"** utilizing historical data from the START University of Maryland Global Terrorism Database (GTD). **Mihir Kumar** conceptualized and engineered the primary core application pipeline, machine learning modeling, and Streamlit web dashboard.

<br>

<table width="100%">
<tr>
<td width="50%" valign="top">

**Dr. Smita Agrawal**  
*Designation: Mentor*  
Bharat Space Education Research Centre (BSERC)  
Contact: +91 9928023107  
*Virtual Verification: APPROVED & VERIFIED (ONLINE)*

</td>
<td width="50%" valign="top">

**Rahul Singh**  
*Designation: Outreach Director*  
Bharat Space Education Research Centre (BSERC)  
Email: `Director@bserc.org` \| Mobile: +91 7303048634  
*Virtual Verification: APPROVED & VERIFIED (ONLINE)*

</td>
</tr>
</table>

---

## 🙏 ACKNOWLEDGEMENTS

We express our sincere gratitude and appreciation to **Bharat Space Education Research Centre (BSERC)** for offering us this online research internship opportunity.

We extend our deepest gratitude to our Project Mentor, **Dr. Smita Agrawal**, for her guidance, technical insights, and valuable feedback throughout the virtual internship. Her mentorship enabled us to adhere to rigorous data science standards and defensive analytics principles.

We also express our sincere thanks to **Rahul Singh** (Outreach Director) for his administrative coordination, mentorship support, and encouragement throughout the program.

Finally, we acknowledge the collective efforts and contributions of all student interns—**Mihir Kumar** (Project Lead & Core Developer), **Rasleen Kaur**, **Khushi**, **Hitesh Khutela**, and **Saloni Bhimrao Rangari**.

---

## 📑 TABLE OF CONTENTS

1. [Executive Summary & Abstract](#-executive-summary--abstract)
2. [Chapter 1: Introduction, Background & Objectives](#-chapter-1-introduction-background--objectives)
3. [Chapter 2: Team Roles & System Architecture](#-chapter-2-team-roles--system-architecture)
4. [Chapter 3: Data Ingestion & Preprocessing Engine](#-chapter-3-data-ingestion--preprocessing-engine)
5. [Chapter 4: Feature Engineering & Data Leakage Prevention](#-chapter-4-feature-engineering--data-leakage-prevention)
6. [Chapter 5: Machine Learning Model Development & Performance](#-chapter-5-machine-learning-model-development--performance)
7. [Chapter 6: Statistical Trend Engine & Anomaly Detection](#-chapter-6-statistical-trend-engine--anomaly-detection)
8. [Chapter 7: Interactive Dashboard UI & User Experience](#-chapter-7-interactive-dashboard-ui--user-experience)
9. [Chapter 8: System Tools, Installation & CLI Interface](#-chapter-8-system-tools-installation--cli-interface)
10. [Chapter 9: Discussion, Future Work & Conclusion](#-chapter-9-discussion-future-work--conclusion)
11. [Official Virtual Verification & Verification Log](#-official-virtual-verification--verification-log)

---

## 📌 EXECUTIVE SUMMARY & ABSTRACT

Modern security and defense research increasingly relies on data science, spatio-temporal modeling, and machine learning to analyze global threat environments. Historical event repositories contain rich information regarding tactical shifts, regional vulnerability hotspots, and casualty profiles.

During this online internship at **Bharat Space Education Research Centre (BSERC)**, an end-to-end data science application was developed: **AI-Powered Military Intelligence Dashboard**. The system processes **209,706 historical event records** spanning 50 years (1970–2020) from the Global Terrorism Database (GTD) published by the National Consortium for the Study of Terrorism and Responses to Terrorism (START), University of Maryland ([`https://www.start.umd.edu/data-tools/GTD`](https://www.start.umd.edu/data-tools/GTD)).

The platform carries out end-to-end data processing: raw data ingestion, cleaning, year-wise dataset partitioning, categorical encoding, machine learning threat severity classification (`RandomForestClassifier`), and interactive visualization via a dark-navy Streamlit Community Cloud web application deployed at [`https://ai-military-intelligence-dashboard-azou6rjqnalb6pttxubte9.streamlit.app/`](https://ai-military-intelligence-dashboard-azou6rjqnalb6pttxubte9.streamlit.app/). The trained classifier achieves an **Accuracy of 84.57%**, **Precision of 89.49%**, **Recall of 84.33%**, **F1-Score of 86.83%**, and an **ROC-AUC score of 92.73%** on 41,942 test incidents.

---

## 🏢 CHAPTER 1: INTRODUCTION, BACKGROUND & OBJECTIVES

### 1.1 Host Organization Profile
- **Organization Name**: Bharat Space Education Research Centre (BSERC)
- **Regional Office Address**: C-32, Ram Nagar, Sector 14, Kaushambi, Ghaziabad, Delhi NCR, Uttar Pradesh - 201010, India
- **Mentorship Team**: Dr. Smita Agrawal (Mentor), Rahul Singh (Outreach Director)
- **Mode of Internship**: Online / Virtual Remote Research Internship Program

### 1.2 Data Source Attribution & Scope
- **Dataset Title**: Global Terrorism Database (GTD)
- **Provider Institution**: National Consortium for the Study of Terrorism and Responses to Terrorism (START), University of Maryland
- **Official Portal**: `https://www.start.umd.edu/data-tools/GTD`
- **Scope**: 209,706 recorded global incidents from 1970 through 2020 across 135 raw attribute dimensions.

### 1.3 Defensive Analytics Principles
In accordance with ethical academic research guidelines, this project strictly focuses on **defensive analytics**:
- Macro-level historical temporal trend analysis
- Aggregate regional activity distribution heatmaps
- Non-leaking predictive event severity classification
- **Exclusion of operational military targeting, tactical strike planning, or individual tracking capabilities.**

---

## 👥 CHAPTER 2: TEAM ROLES & SYSTEM ARCHITECTURE

### 2.1 Codebase Package Architecture
The project was architected following modular software design principles. **Mihir Kumar** served as the Project Lead and primary developer, engineering the overall codebase, machine learning pipeline, data cleaning algorithms, and Streamlit dashboard interface. Team members collaborated on specific sub-module scripts:

```
AI-Military-Intelligence-Dashboard/
│
├── .streamlit/                       # Dark theme Streamlit configuration
├── data/
│   ├── raw/                          # Raw Excel GTD dataset (START UMD)
│   ├── yearly/                       # 50 Yearly split CSV files (1970 - 2020)
│   └── processed/                    # Cleaned & engineered datasets
│
├── models/                           # Machine Learning artifacts (threat_model.pkl)
├── reports/                          # Evaluation figures & JSON metric summaries
│
├── src/                              # Core Python Package Source Code
│   ├── data/                         # Data Ingestion & Preprocessing (Led by Mihir Kumar & Rasleen Kaur)
│   ├── features/                     # Feature Matrix Engineering (Led by Mihir Kumar & Khushi)
│   ├── analysis/                     # Statistical & Anomaly Engine (Led by Mihir Kumar & Saloni Bhimrao Rangari)
│   ├── models/                       # ML Training & Inference Engine (Led by Mihir Kumar & Hitesh Khutela)
│   ├── dashboard/                    # Multipage Streamlit UI (Led by Mihir Kumar)
│   └── utils/                        # Logging & Path Config
│
└── run.py                            # Central CLI Execution Interface
```

### 2.2 End-to-End Data Pipeline Flowchart

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

## ⚙️ CHAPTER 3: DATA INGESTION & PREPROCESSING ENGINE

### 3.1 Attribute Selection & Filtering
From the raw 135 GTD fields, 32 core attributes were extracted representing event identifiers, temporal parameters, spatial coordinates, tactical classifications, target categories, weapon types, and casualty metrics:

| Attribute Category | Selected Field Names |
|---|---|
| **Event Identification** | `eventid` |
| **Temporal Parameters** | `iyear`, `imonth`, `iday` |
| **Geographic Location** | `country`, `country_txt`, `region`, `region_txt`, `provstate`, `city`, `latitude`, `longitude` |
| **Tactical Context** | `attacktype1`, `attacktype1_txt`, `targtype1`, `targtype1_txt`, `weaptype1`, `weaptype1_txt`, `gname` |
| **Operational Flags** | `suicide`, `success`, `multiple`, `property`, `ishostkid` |
| **Casualty Measures** | `nkill`, `nwound` |

### 3.2 Cleaning & Sentinel Value Sanitization
1. **Sentinel Replacement**: Field values equal to `-99` or `-9` (representing missing/unknown GTD records) were programmatically converted to `NaN`.
2. **Coordinate Boundaries**: Latitude and longitude values were validated strictly within $[-90^\circ, +90^\circ]$ and $[-180^\circ, +180^\circ]$ respectively.
3. **Casualty Defaults**: Missing `nkill` and `nwound` records were imputed to `0` for aggregate casualty summation.

---

## 📊 CHAPTER 4: FEATURE ENGINEERING & DATA LEAKAGE PREVENTION

### 4.1 Mathematical Formulas & Derivations

#### 1. Total Casualties Metric Formula:
```math
\text{total\_casualties} = \text{nkill} + \text{nwound}
```
> **Plain Text Definition**:  
> `total_casualties = nkill (Total Fatalities) + nwound (Total Wounded)`

<br>

#### 2. Lethality Ratio Metric Formula:
```math
\text{lethality\_ratio} = \begin{cases} \frac{\text{nkill}}{\text{total\_casualties}} & \text{if } \text{total\_casualties} > 0 \\ 0 & \text{if } \text{total\_casualties} = 0 \end{cases}
```
> **Plain Text Definition**:  
> `lethality_ratio = nkill / total_casualties` (evaluated when `total_casualties > 0`; defaults to `0.0` otherwise)

---

### 4.2 Target Variable Classification Formula (`high_severity_event`)

```math
\text{high\_severity\_event} = \begin{cases} 1 & \text{if } (\text{total\_casualties} \ge 1 \lor \text{suicide} = 1) \\ 0 & \text{otherwise} \end{cases}
```
> **Plain Text Definition**:  
> `high_severity_event = 1` if `total_casualties >= 1` OR `suicide == 1`; otherwise `0`

<br>

**Class Distribution across 209,706 GTD Incident Records:**
- **High Severity Class (`1`)**: **60.35%** (126,557 incidents)
- **Moderate/Low Severity Class (`0`)**: **39.65%** (83,149 incidents)

---

### 4.3 Data Leakage Safeguard Implementation

Direct casualty metrics (`nkill`, `nwound`, `total_casualties`, and `lethality_ratio`) are strictly **excluded** from the input predictor feature matrix `X`. 

Because the target variable `high_severity_event` is derived directly from casualty thresholds (`total_casualties >= 1` or `suicide == 1`), including casualty counts as input predictors would cause **artificial target leakage**, artificially inflating model performance during training while failing on real-world unobserved incidents.

To ensure true predictive generalization, the machine learning classifier predicts event severity using **only contextual incident features**:
- **Temporal Attributes**: Event Year (`iyear`), Event Month (`imonth`), Event Day (`iday`)
- **Geographic Location**: Region Code (`region_txt_code`), Country Code (`country_txt_code`), Spatial Coordinates (`latitude`, `longitude`)
- **Tactical Event Context**: Attack Type Code (`attacktype1_txt_code`), Target Category Code (`targtype1_txt_code`), Weapon Category Code (`weaptype1_txt_code`)
- **Tactical Operational Flags**: Suicide Flag (`suicide`), Attack Execution Success Flag (`success`), Property Damage Flag (`property`), Hostage/Kidnapping Flag (`ishostkid`)

---

## 🤖 CHAPTER 5: MACHINE LEARNING MODEL DEVELOPMENT & EVALUATION

### 5.1 Model Specifications & Training Config
- **Algorithm**: `RandomForestClassifier`
- **Number of Estimators (`n_estimators`)**: 100
- **Max Tree Depth (`max_depth`)**: 15
- **Class Weights**: `balanced`
- **Train/Test Split**: 80% Train (167,764 samples) / 20% Test (41,942 samples) Stratified

### 5.2 Quantitative Performance Metrics Table

| Evaluation Metric | Test Score | Significance |
|---|---|---|
| **Accuracy** | **84.57%** | High overall classification reliability |
| **Precision** | **89.49%** | Minimal false positive high-severity alerts |
| **Recall** | **84.33%** | Strong sensitivity in identifying threat incidents |
| **F1 Score** | **86.83%** | Optimal balance between Precision and Recall |
| **ROC-AUC** | **92.73%** | Superior discrimination capability across thresholds |

---

## 📈 CHAPTER 6: STATISTICAL TREND ENGINE & ANOMALY DETECTION

### 6.1 Year-over-Year (YoY) Percentage Change
$$\text{YoY\_Change}_t = \left( \frac{\text{Event\_Count}_t - \text{Event\_Count}_{t-1}}{\text{Event\_Count}_{t-1}} \right) \times 100$$

### 6.2 Z-Score Spike Anomaly Detection Algorithm
$$\mu = \frac{1}{N} \sum_{i=1}^{N} x_i, \quad \sigma = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2}$$
$$Z_t = \frac{x_t - \mu}{\sigma}$$
An anomaly spike year is declared when $Z_t > 1.5$.

---

## 🖥️ CHAPTER 7: INTERACTIVE DASHBOARD UI & USER EXPERIENCE

The application interface is deployed live at [`https://ai-military-intelligence-dashboard-azou6rjqnalb6pttxubte9.streamlit.app/`](https://ai-military-intelligence-dashboard-azou6rjqnalb6pttxubte9.streamlit.app/) and structured into 5 dedicated multipage views:

1. **🏠 Home Overview** (`pages/00_Home.py`): Global filters sidebar, KPI metrics grid, main trend timeline, regional & tactical breakdown, Carto Darkmatter density heatmap, dynamic automated insights.
2. **📊 Threat Analysis** (`pages/01_Threat_Analysis.py`): 3-year rolling average line, YoY shift badges (`↑ INCREASING`, `↓ DECREASING`, `→ STABLE`), Z-score activity spikes table (>1.5 std dev), tactical category distributions.
3. **🌍 Regional Intelligence** (`pages/02_Regional_Intelligence.py`): Theater region selector, ranked regional summary table with color gradients, aggregate regional density map, multi-region temporal comparison line chart.
4. **⚠️ Risk Assessment** (`pages/03_Risk_Assessment.py`): Real-time event attribute selectors, model inference engine, structured risk card (HIGH / MODERATE / LOW), supporting feature signals.
5. **🤖 Model Performance** (`pages/04_Model_Performance.py`): Quantitative metric cards, confusion matrix heatmap figure, feature importance drivers chart, model specifications.

---

## 🛠️ CHAPTER 8: SYSTEM TOOLS, INSTALLATION & CLI INTERFACE

### 8.1 Technology Stack
- **Python 3.10+**
- **Data Engineering**: Pandas (≥2.0.0), NumPy (≥1.24.0), OpenPyXL
- **Machine Learning**: Scikit-Learn (≥1.2.0), Joblib
- **Data Visualization**: Plotly (≥5.14.0), Matplotlib, Seaborn
- **Web Dashboard**: Streamlit (≥1.36.0)

### 8.2 CLI Commands
```bash
# Execute end-to-end pipeline
python run.py all

# Launch Streamlit Dashboard
python run.py dashboard
```

---

## 🎓 CHAPTER 9: DISCUSSION, FUTURE WORK & CONCLUSION

### 9.1 Conclusion
The online research internship at **Bharat Space Education Research Centre (BSERC)** successfully produced an academic-grade data science application. The **AI-Powered Military Intelligence Dashboard** processes 50 years of START UMD GTD event data, enforces data leakage safeguards, achieves an 84.57% classification accuracy (92.73% ROC-AUC), and delivers an interactive cloud dashboard.

### 9.2 Future Research Scope
1. **Spatial-Temporal Graph Neural Networks (GNNs)**: Model cross-border group connectivity.
2. **Multi-Class Threat Tiering**: Classify threat severity into 4 discrete risk tiers (Critical, Severe, Moderate, Low).

---

## 🌐 OFFICIAL VIRTUAL VERIFICATION & VERIFICATION LOG

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
