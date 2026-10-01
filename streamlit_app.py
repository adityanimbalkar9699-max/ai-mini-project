import os
import sys

# Dynamic root path resolution for Streamlit Cloud & local execution
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from knowledge.knowledge_base import kb
from inference.forward_chaining import run_forward_chaining
from inference.backward_chaining import run_backward_chaining

# Page Configuration
st.set_page_config(
    page_title="MediMind // Clinical Decision Support & Symbolic AI Engine",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Glassmorphism UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #0F172A 100%);
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }

    .hero-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    .glass-card {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    .badge-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.5);
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .badge-urgent {
        background: rgba(245, 158, 11, 0.2);
        color: #FDE68A;
        border: 1px solid rgba(245, 158, 11, 0.5);
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .badge-moderate {
        background: rgba(59, 130, 246, 0.2);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.5);
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .trace-box {
        background: #090D16;
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 8px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #38BDF8;
        max-height: 280px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="hero-title">MEDIMIND // CLINICAL DECISION SUPPORT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Symbolic AI Medical Expert System & Production Rule Engine (Forward & Backward Chaining)</div>', unsafe_allow_html=True)

# Sidebar Preset Case & Controls
st.sidebar.markdown("### 📋 Clinical Presets")
presets = kb.get_case_presets()
preset_titles = ["None (Custom Selection)"] + [f"{p['id']}: {p['title']}" for p in presets]
selected_preset_title = st.sidebar.selectbox("Load Clinical Vignette", preset_titles)

active_preset_symptoms = []
active_preset_target = None

if selected_preset_title != "None (Custom Selection)":
    selected_id = selected_preset_title.split(":")[0]
    preset_obj = next((p for p in presets if p["id"] == selected_id), None)
    if preset_obj:
        st.sidebar.info(f"**Loaded Case**: {preset_obj['title']}\n\n**Patient**: Age {preset_obj['patient']['age']}, {preset_obj['patient']['gender']} | BP: {preset_obj['patient']['bp']} | HR: {preset_obj['patient']['hr']} bpm")
        active_preset_symptoms = preset_obj.get("symptoms", [])
        active_preset_target = preset_obj.get("target_disease")

# Main Navigation Tabs
tab_fwd, tab_bwd, tab_kb = st.tabs([
    "01 // Forward Chaining (Differential Diagnosis)",
    "02 // Backward Chaining (Hypothesis Verification)",
    "03 // Production Rules & Knowledge Base"
])

# -----------------------------------------------------------------------------
# TAB 1: Forward Chaining Engine
# -----------------------------------------------------------------------------
with tab_fwd:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-top:0;'>Data-Driven Forward Chaining Diagnostics</h3>", unsafe_allow_html=True)
    st.markdown("Select patient clinical observations to assert into Working Memory. The symbolic inference engine will execute multi-pass rule firing to derive differential diagnoses.")

    categorized = kb.get_categorized_symptoms()
    selected_symptoms = set(active_preset_symptoms)

    cols = st.columns(4)
    cat_keys = list(categorized.keys())
    for idx, cat_name in enumerate(cat_keys):
        with cols[idx % 4]:
            st.markdown(f"**{cat_name}**")
            for sym in categorized[cat_name]:
                default_checked = sym in active_preset_symptoms
                label_formatted = sym.replace("_", " ").title()
                if st.checkbox(label_formatted, value=default_checked, key=f"fwd_{sym}"):
                    selected_symptoms.add(sym)

    st.markdown("---")
    symptom_list = list(selected_symptoms)
    st.markdown(f"**Asserted Clinical Signals ({len(symptom_list)}):** `{', '.join(symptom_list) if symptom_list else 'None'}`")

    if st.button("⚡ Run Forward Chaining Inference Engine", use_container_width=True, type="primary"):
        if not symptom_list:
            st.warning("Please select at least one clinical symptom to begin inference.")
        else:
            rules = kb.get_all_rules()
            results = run_forward_chaining(rules, symptom_list)

            if results:
                st.markdown(f"### Diagnostic Results ({len(results)} Differential Matches)")
                for r in results:
                    sev = r.get("severity", "MODERATE").upper()
                    badge_class = "badge-critical" if sev in ["CRITICAL", "EMERGENCY"] else ("badge-urgent" if sev == "URGENT" else "badge-moderate")
                    match_badge = "✅ FULL MATCH" if r.get("is_full_match") else f"⚠️ PARTIAL MATCH ({r.get('match_ratio')}%)"

                    st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0; color: #F8FAFC;">{r['diagnosis']} <span style="font-size: 0.8rem; color: #94A3B8;">(ICD-10: {r['icd10']})</span></h4>
                            <div>
                                <span class="{badge_class}">{sev}</span>
                                <span style="margin-left: 8px; font-size: 0.85rem; font-weight: 600; color: #38BDF8;">{match_badge}</span>
                            </div>
                        </div>
                        <div style="font-size: 0.9rem; color: #94A3B8;">
                            <b>Category:</b> {r['category']} | <b>Rule ID:</b> {r['rule_id']} | <b>Match Ratio:</b> {r['match_count']}/{r['total_required']} symptoms
                        </div>
                        <div style="margin-top: 0.6rem; font-size: 0.88rem;">
                            <span style="color: #34D399;"><b>Satisfied Evidence:</b> {', '.join(r['satisfied_symptoms'])}</span><br>
                            <span style="color: #FCA5A5;"><b>Missing Evidence:</b> {', '.join(r['missing_symptoms']) if r['missing_symptoms'] else 'None'}</span>
                        </div>
                        <div style="margin-top: 0.8rem; background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 6px; font-size: 0.85rem;">
                            <b>🔬 Recommended Diagnostic Tests:</b> {r['tests_recommended']}<br>
                            <b>💊 Recommended Clinical Protocol:</b> {r['treatment']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with st.expander("🔍 Inspect Full Forward Reasoning Audit Trace"):
                    trace_text = "\n".join(results[0].get("reasoning_trace", []))
                    st.code(trace_text, language="text")
            else:
                st.error("No production rules triggered for the asserted symptom set.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: Backward Chaining Engine
# -----------------------------------------------------------------------------
with tab_bwd:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-top:0;'>Goal-Driven Backward Chaining Verification</h3>", unsafe_allow_html=True)
    st.markdown("Assert a diagnostic hypothesis goal to recursively prove or disprove whether available patient evidence supports the hypothesis.")

    all_diseases = kb.get_disease_names()
    default_target_idx = 0
    if active_preset_target and active_preset_target in all_diseases:
        default_target_idx = all_diseases.index(active_preset_target)

    target_hypothesis = st.selectbox("Select Hypothesis Goal to Prove", all_diseases, index=default_target_idx)

    st.markdown("#### Patient Evidence Base")
    bwd_selected_symptoms = set(active_preset_symptoms)
    categorized_bwd = kb.get_categorized_symptoms()

    b_cols = st.columns(4)
    b_cat_keys = list(categorized_bwd.keys())
    for idx, cat_name in enumerate(b_cat_keys):
        with b_cols[idx % 4]:
            st.markdown(f"**{cat_name}**")
            for sym in categorized_bwd[cat_name]:
                default_checked = sym in active_preset_symptoms
                label_formatted = sym.replace("_", " ").title()
                if st.checkbox(label_formatted, value=default_checked, key=f"bwd_{sym}"):
                    bwd_selected_symptoms.add(sym)

    st.markdown("---")
    bwd_symptom_list = list(bwd_selected_symptoms)

    if st.button("🎯 Execute Backward Chaining Prover", use_container_width=True, type="primary"):
        rules = kb.get_all_rules()
        bwd_res = run_backward_chaining(rules, target_hypothesis, bwd_symptom_list)

        if bwd_res["matched"]:
            st.success(f"✨ HYPOTHESIS PROVEN: **{bwd_res['diagnosis']}** (Rule {bwd_res['rule_id']}) is fully supported by evidence!")
        else:
            st.error(f"❌ HYPOTHESIS UNPROVEN: **{bwd_res['diagnosis']}** (Rule {bwd_res['rule_id']}) cannot be verified with current evidence.")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Hypothesis Goal", bwd_res["diagnosis"])
        with c2:
            st.metric("Satisfied Antecedents", len(bwd_res["satisfied_symptoms"]))
        with c3:
            st.metric("Unsatisfied Antecedents", len(bwd_res["missing_symptoms"]))

        st.markdown(f"**Satisfied Evidence:** `{', '.join(bwd_res['satisfied_symptoms']) if bwd_res['satisfied_symptoms'] else 'None'}`")
        st.markdown(f"**Missing Required Evidence:** `{', '.join(bwd_res['missing_symptoms']) if bwd_res['missing_symptoms'] else 'None'}`")

        if bwd_res["recommended_inquiry"]:
            st.info("**Next Step Clinical Inquiries:**\n" + "\n".join([f"- {inq}" for inq in bwd_res["recommended_inquiry"]]))

        with st.expander("🔍 Inspect Full Backward Proof Trace"):
            st.code("\n".join(bwd_res["reasoning_trace"]), language="text")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: Knowledge Base Explorer
# -----------------------------------------------------------------------------
with tab_kb:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-top:0;'>Medical Knowledge Base Production Rules</h3>", unsafe_allow_html=True)

    rules = kb.get_all_rules()
    st.markdown(f"Total Production Rules Loaded: **{len(rules)}**")

    for rule in rules:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem;">
            <b>[{rule['id']}] IF</b> { ' AND '.join(rule['symptoms']) } <b>THEN</b> <span style="color: #38BDF8;">{rule['diagnosis']}</span> (ICD-10: {rule.get('icd10', 'N/A')}, Category: {rule.get('category', 'General')})
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
