# 🥗 Food Verse AI — Multimodal Food Intelligence Agent
### *Skill Wallet Capstone Project 3: Multimodal Food Science & AI Systems Engineering*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8502)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-10B981.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-3B82F6.svg)](LICENSE)
[![AI Architecture: Multimodal](https://img.shields.io/badge/Vision_Engine-Gemini_2.5_Flash_%7C_Groq-F59E0B.svg)](#system-architecture)

---

## 📌 Executive Overview

**Food Verse AI** is an advanced, production-ready multimodal artificial intelligence platform designed at the intersection of clinical nutrition science, optical computer vision diagnostics, commercial food safety compliance (HACCP / FDA Food Code), and adaptive metabolic energy expenditure modeling.

The application requires **zero external database dependencies** and features an automatic **Standalone Showcase / Simulation Mode**, enabling seamless 1-click evaluation and deployment on **Streamlit Community Cloud** with or without live API keys.

---

## 🏛️ Core Intelligence Pillars & Modules

### 1. 🍽️ Tab 1: Food Recognition & Nutrition Audit (Epic 2)
- **Computer Vision Extraction**: Identifies dish nomenclature, culinary style/cuisine, ingredient components, and portion weight (grams).
- **Nutritional Audit**: Computes total Calories (kcal), Protein (g), Carbohydrates (g), Total Fats (g), Dietary Fiber (g), Sugar (g), and Sodium (mg).
- **Composite Health Score (1–100)**: Evaluates nutrient density, fiber-to-carb balance, sodium moderation, and ultra-processing indices.
- **Interactive Data Visualizations**: Interactive Plotly Caloric Macro Distribution Donut Chart and Daily Reference Intake (DRI % based on 2000 kcal standard) horizontal bar chart.
- **Allergen Detection**: Flags FDA major allergens (Gluten, Dairy, Shellfish, Tree Nuts, Peanuts, Soy, Eggs, Fish, Sesame) with severity gradings.

### 2. 🥑 Tab 2: Food Freshness & Spoilage Diagnostic (Epic 3)
- **Multi-Factor Spoilage Inspection**: Evaluates 4 biomorphometric decay vectors:
  1. *Surface Texture & Firmness*: Softening, collapse of parenchyma cell walls, or slime formation.
  2. *Discoloration & Oxidation*: Enzymatic browning (PPO) percentages and necrotic spotting.
  3. *Wrinkling & Turgor Pressure Loss*: Dehydration index and skin elasticity.
  4. *Mold & Microbial Detection*: Mycelium fungal filament identification (*Botrytis*, *Penicillium*, *Rhizopus*).
- **Classification Stage**: `[Fresh 🟢 | Moderately Fresh 🟡 | Spoiled 🔴]` with an interactive Freshness Gauge (0–100%).
- **Actionable Food Safety Guidance**: Immediate directives (`SAFE TO CONSUME`, `CONSUME WITHIN 24–48H`, `DISCARD IMMEDIATELY`) and empirical shelf-life estimates.
- **Scientific Preservation Protocols**: Optimal temperature (°C/°F), relative humidity controls, and ethylene gas isolation guidance.

### 3. 🧼 Tab 3: Commercial Kitchen Hygiene & Food Safety Compliance (Epic 4)
- **Computer Vision Inspection**: Processes commercial kitchen photographs and video frames according to FDA 2022 Food Code and HACCP standards.
- **Audited Hygiene Indicators**:
  - *Hair Restraint Compliance* (§2-402.11): Chef hats, bouffant hairnets, and beard nets.
  - *Glove Protocol* (§3-301.11): Disposable food-safe glove usage vs bare-hand contact.
  - *Sanitization & Cleanliness*: Stainless steel prep cleanliness and chemical wiping cloth buckets.
  - *Cross-Contamination Hazards* (§3-302.11): Raw poultry/meat proximity to ready-to-eat garnishes and color-coded board separation.
- **Compliance Scoring & Grade**: Computes an overall Kitchen Hygiene Compliance Score (0–100%) and Grade (Grade A, B, C, F).
- **Itemized Violation Logs**: Logs HACCP/FDA code references, severity levels (Critical, Major, Minor, Pass), detailed observations, and immediate corrective action protocols.
- **Audit Export**: 1-click downloadable HACCP Audit Report in formatted Markdown.

### 4. 🍳 Tab 4: Smart Kitchen Recipe Assistant (Epic 4)
- **Pantry Inventory Manager**: Dynamic multi-select tags and custom ingredient addition with 1-click presets (*Mediterranean*, *High-Protein*, *Student Budget*, *Plant-Powered Vegan*).
- **Nutritional Recipe Synthesis**: Generates chef-crafted recipes with prep time, cook time, difficulty rating, servings, and complete macronutrient profiles.
- **Smart Ingredient Substitutions**: Provides intelligent ingredient swaps for allergies, dietary constraints, or missing items.
- **Zero-Waste Food Science**: Integrates culinary scrap reduction tips (peels, stems, bones).

### 5. 📊 Tab 5: Personalized 7-Day Meal Planner & TDEE Engine (Epic 5)
- **Biometric Profile Form**: Captures age, gender, height (cm), weight (kg), activity level, dietary constraints (Vegan, Keto, Diabetic-Friendly, etc.), and fitness goals.
- **Clinical Metabolic Formulation**:
  - **Mifflin-St Jeor Equation** for Basal Metabolic Rate (BMR):
    $$\text{BMR}_{\text{male}} = 10 \cdot W + 6.25 \cdot H - 5 \cdot A + 5$$
    $$\text{BMR}_{\text{female}} = 10 \cdot W + 6.25 \cdot H - 5 \cdot A - 161$$
  - **TDEE Calculation**: Calibrated via Physical Activity Level (PAL) multipliers (1.2 to 1.9).
- **Adaptive 7-Day Nutritional Schedule**: Generates tailored breakfast, lunch, dinner, and snack targets for Monday through Sunday.
- **Automated Supermarket Aisle Checklist**: Organizes required groceries into departments (Produce, Lean Proteins, Whole Grains, Dairy & Alternatives, Pantry & Oils).
- **Export Options**: 1-click download of the complete 7-day blueprint as Markdown or CSV.

### 6. 🔬 Tab 6: Food Science & System Architecture
- Mathematical documentation, optical biomarker breakdown, and dual-inference pipeline topology.

---

## 🛠️ Project Structure

```
Food Verse AI - Multimodal Food Intelligence Agent/
│
├── app.py                     # Main Streamlit orchestration application
├── requirements.txt           # Production dependencies for Streamlit Cloud
├── README.md                  # Comprehensive documentation and manual
│
├── .streamlit/
│   └── config.toml            # Modern dark slate theme configuration
│
├── assets/
│   ├── style.css              # Custom CSS design system (glassmorphism & tokens)
│   └── samples/               # Bundled high-resolution sample datasets
│       ├── salmon_bowl.jpg    # Sample culinary dish for Tab 1
│       ├── spoiled_fruit.jpg  # Sample surface spoilage for Tab 2
│       └── kitchen_hygiene.jpg# Sample commercial kitchen line for Tab 3
│
├── modules/
│   ├── __init__.py
│   ├── ai_engine.py           # Unified Multimodal AI Engine (Gemini / Groq / Demo)
│   ├── sample_data.py         # Curated presets, benchmarks, and data schemas
│   ├── nutrition_audit.py     # Tab 1: Food recognition, macros, Plotly charts
│   ├── freshness_diagnostic.py# Tab 2: Spoilage index, mold detection, safety advice
│   ├── hygiene_compliance.py  # Tab 3: HACCP kitchen compliance & violation logs
│   ├── recipe_assistant.py    # Tab 4: Pantry manager & recipe generator
│   ├── meal_planner.py        # Tab 5: Mifflin-St Jeor BMR/TDEE & 7-day planner
│   └── system_architecture.py # Tab 6: Mathematical formulas & system specs
│
└── tests/
    └── test_modules.py        # Automated test suite (Mifflin-St Jeor, AI schemas, etc.)
```

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10 or higher
- Optional: Google Gemini API key ([Google AI Studio](https://aistudio.google.com/)) or Groq Cloud API key ([Groq Console](https://console.groq.com/))

### 1. Clone & Enter Directory
```bash
git clone <repository_url>
cd "Food Verse AI - Multimodal Food Intelligence Agent"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
python -m unittest tests/test_modules.py
```
*(All 5 test suites will pass in <0.1 seconds).*

### 4. Launch Application
```bash
python -m streamlit run app.py
```
Open your browser to `http://localhost:8501` (or the terminal-assigned port).

---

## ☁️ 1-Click Streamlit Community Cloud Deployment

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Select your repository, set the main file path to `app.py`, and click **Deploy**.
4. *(Optional)* Add `GEMINI_API_KEY` or `GROQ_API_KEY` in Streamlit App Secrets (`Settings > Secrets`). If omitted, the app will smoothly run in the high-fidelity **Standalone Showcase Mode**!

---

## 🔒 Security & Privacy
- **Client-Side Key Ephemerality**: API keys entered into the sidebar are stored strictly in temporary browser session state (`st.session_state`) and are never written to disk or transmitted to third-party loggers.
- **Zero Database Footprint**: No SQL or NoSQL database dependencies; self-contained in-memory execution guarantees zero cross-tenant data leakage.

---

## 👨‍🔬 Authors & Acknowledgments
- **Project**: Skill Wallet Capstone Project 3
- **Specialization**: Food Science, Nutritional Biochemistry & Multimodal AI Agent Engineering
- **Frameworks**: Streamlit, Plotly, Google GenAI SDK, Groq LPU Cloud
