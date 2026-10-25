"""
Food Verse AI - System Architecture & Food Science Engine
Provides technical documentation, mathematical models, HACCP auditing principles,
and multimodal vision pipeline specifications.
"""

import streamlit as st

def render_architecture_tab():
    """Renders the Food Science & Technical Architecture documentation."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin:0; font-weight:800; color:#F8FAFC;">🔬 Food Science & System Architecture</h2>
        <p style="color:#94A3B8; font-size:0.95rem; margin-top:4px;">
            Underlying clinical nutrition formulas, computer vision pipeline, microbiological diagnostic principles, and cloud deployment topology.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="fv-card">
            <h3 class="fv-card-title">🧮 Nutritional & Metabolic Mathematics</h3>
            
            <p style="font-size:0.9rem; color:#CBD5E1; margin-top:10px;">
                <b>1. Basal Metabolic Rate (BMR) - Mifflin-St Jeor Equation:</b><br>
                Recognized by the Academy of Nutrition and Dietetics as the most accurate clinical BMR predictor:
            </p>
            <div style="background:rgba(15,23,42,0.8); padding:10px 14px; border-radius:8px; font-family:'JetBrains Mono', monospace; font-size:0.82rem; color:#34D399; margin:8px 0;">
                BMR_men = 10·weight(kg) + 6.25·height(cm) - 5·age(y) + 5<br>
                BMR_women = 10·weight(kg) + 6.25·height(cm) - 5·age(y) - 161
            </div>

            <p style="font-size:0.9rem; color:#CBD5E1; margin-top:14px;">
                <b>2. Total Daily Energy Expenditure (TDEE):</b>
            </p>
            <div style="background:rgba(15,23,42,0.8); padding:10px 14px; border-radius:8px; font-family:'JetBrains Mono', monospace; font-size:0.82rem; color:#38BDF8; margin:8px 0;">
                TDEE = BMR × PAL (Physical Activity Level: 1.2 to 1.9)
            </div>

            <p style="font-size:0.9rem; color:#CBD5E1; margin-top:14px;">
                <b>3. FoodVerse Health Score Formula (1-100):</b>
            </p>
            <div style="background:rgba(15,23,42,0.8); padding:10px 14px; border-radius:8px; font-family:'JetBrains Mono', monospace; font-size:0.82rem; color:#F59E0B; margin:8px 0;">
                Score = 100 - (Sodium_mg / 40) - (Sugar_g × 1.2) + (Fiber_g × 2.5) + (Protein_ratio × 15) - UltraProcessingPenalty
            </div>
        </div>
        
        <div class="fv-card">
            <h3 class="fv-card-title">🛡️ Food Spoilage & Pathogen Diagnostic Matrix</h3>
            <p style="font-size:0.88rem; color:#CBD5E1; line-height:1.6;">
                The diagnostic engine evaluates 4 distinct optical biomarkers:
            </p>
            <ul style="font-size:0.85rem; color:#94A3B8; padding-left:20px; line-height:1.6;">
                <li><b>Cellular Turgor & Wrinkling:</b> Measures dehydration of epidermal cell walls indicating storage senescence.</li>
                <li><b>Enzymatic Browning Index:</b> Polyphenol oxidase (PPO) reaction catalyzed by mechanical trauma and oxygen.</li>
                <li><b>Mycelium & Sporulation:</b> Detection of fungal filaments (<i>Botrytis cinerea</i>, <i>Penicillium digitatum</i>, <i>Rhizopus</i>) producing mycotoxins (e.g. patulin).</li>
                <li><b>Slime & Bacterial Biofilms:</b> Surface specular reflection changes indicative of psychrotrophic bacterial colonies (<i>Pseudomonas</i>).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="fv-card">
            <h3 class="fv-card-title">🏛️ Multimodal AI Inference Pipeline</h3>
            <p style="font-size:0.88rem; color:#CBD5E1; line-height:1.6;">
                The platform utilizes a dual-path multimodal inference architecture with high-availability fallback:
            </p>
            
            <div style="background:rgba(15,23,42,0.8); padding:14px; border-radius:10px; margin:12px 0; border:1px solid rgba(255,255,255,0.06);">
                <div style="display:flex; align-items:center; gap:8px; color:#10B981; font-weight:700; font-size:0.9rem;">
                    <span>🟢 Primary Engine: Google Gemini 2.5 Flash</span>
                </div>
                <p style="font-size:0.82rem; color:#94A3B8; margin:4px 0 0 0;">
                    Native multimodal tokenization processing raw image tensors with spatial awareness, detecting micro-textures and boundary overlaps.
                </p>
            </div>

            <div style="background:rgba(15,23,42,0.8); padding:14px; border-radius:10px; margin:12px 0; border:1px solid rgba(255,255,255,0.06);">
                <div style="display:flex; align-items:center; gap:8px; color:#F59E0B; font-weight:700; font-size:0.9rem;">
                    <span>⚡ Secondary Engine: Groq Llama 3.2 Vision / Llama 3.3 70B</span>
                </div>
                <p style="font-size:0.82rem; color:#94A3B8; margin:4px 0 0 0;">
                    Sub-second LPUs delivering ultra-low-latency structured JSON generation and culinary reasoning.
                </p>
            </div>

            <div style="background:rgba(15,23,42,0.8); padding:14px; border-radius:10px; margin:12px 0; border:1px solid rgba(255,255,255,0.06);">
                <div style="display:flex; align-items:center; gap:8px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                    <span>📦 Standalone Simulation Mode: Zero External Database</span>
                </div>
                <p style="font-size:0.82rem; color:#94A3B8; margin:4px 0 0 0;">
                    Complete deterministic fallback engine with pre-baked high fidelity food science datasets, allowing instantaneous zero-configuration deployment on Streamlit Community Cloud.
                </p>
            </div>
        </div>

        <div class="fv-card">
            <h3 class="fv-card-title">📜 Commercial HACCP & FDA Compliance Standards</h3>
            <p style="font-size:0.88rem; color:#CBD5E1; line-height:1.6;">
                Adheres to FDA 2022 Food Code (§2-402.11 Hair Restraints, §3-301.11 Bare Hand Contact, §3-302.11 Cross-Contamination Separation) and HACCP Critical Control Points (CCPs).
            </p>
            <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:10px;">
                <span class="fv-tag">HACCP Principle 1-7</span>
                <span class="fv-tag">FDA 2022 Food Code</span>
                <span class="fv-tag">USDA FSIS Guidelines</span>
                <span class="fv-tag">Codex Alimentarius</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
