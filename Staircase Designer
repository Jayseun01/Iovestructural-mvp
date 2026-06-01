"""
iLoveStructural - Staircase Designer Tool
Parametric staircase design with reinforcement scheduling
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from config import INPUT_PARAMETERS_BY_FAMILY, REINFORCEMENT_STANDARDS
from calculator import (
    calculate_derived_parameters,
    validate_design,
    generate_stair_design,
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="iLoveStructural - Staircase Designer",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .main {
        padding: 2rem 1rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    h1 {
        text-align: center;
        color: #667eea;
        font-size: 2.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .step-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
    }
    
    .step-section h3 {
        color: white;
        margin-top: 0;
    }
    
    .metric-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<h1>🏗️ Staircase Designer</h1>
<p class="subtitle">Parametric design with automatic reinforcement scheduling</p>
""", unsafe_allow_html=True)

# ============================================================================
# STEP 1: SELECT STAIRCASE TYPE
# ============================================================================

st.markdown("""
<div class="step-section">
<h3>1️⃣ Select Staircase Type</h3>
</div>
""", unsafe_allow_html=True)

families = list(INPUT_PARAMETERS_BY_FAMILY.keys())
selected_family = st.selectbox(
    "Staircase Type",
    families,
    format_func=lambda x: INPUT_PARAMETERS_BY_FAMILY[x]["display_name"],
    label_visibility="collapsed",
)

family_config = INPUT_PARAMETERS_BY_FAMILY.get(selected_family, {})
st.info(family_config.get("description", ""))

# ============================================================================
# STEP 2: INPUT PARAMETERS
# ============================================================================

st.markdown("""
<div class="step-section">
<h3>2️⃣ Enter Dimensions</h3>
</div>
""", unsafe_allow_html=True)

core_inputs = family_config.get("core_inputs", {})
user_inputs = {}

cols = st.columns(len(core_inputs))

for col, (param_id, param) in zip(cols, core_inputs.items()):
    with col:
        st.markdown(f"**{param['display']}**")
        value = st.number_input(
            label=param["display"],
            value=param.get("typical", 3000),
            min_value=param.get("min", 0),
            max_value=param.get("max", 10000),
            step=param.get("step", 50),
            label_visibility="collapsed",
            key=f"input_{param_id}"
        )
        st.caption(f"{param.get('unit', '')}")
        user_inputs[param_id] = value

# ============================================================================
# STEP 3: CALCULATE & VALIDATE
# ============================================================================

if user_inputs:
    derived = calculate_derived_parameters(user_inputs, selected_family)
    validation = validate_design(user_inputs, derived, selected_family)
    
    st.markdown("""
    <div class="step-section">
    <h3>3️⃣ Calculated Dimensions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Show derived parameters
    derived_config = family_config.get("derived_outputs", {})
    derived_cols = st.columns(min(3, len(derived_config)))
    
    for col, (param_id, param) in zip(derived_cols, list(derived_config.items())[:3]):
        with col:
            value = derived.get(param_id, 0)
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{value:.0f}</div>
                <div class="metric-label">{param['display']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Validation feedback
    st.markdown("---")
    
    if validation["is_valid"]:
        st.success(f"✅ {validation['message']}")
    else:
        st.error("❌ Design Issues:")
        for issue in validation.get("issues", []):
            st.error(f"  • {issue}")
    
    if validation.get("warnings"):
        st.warning("⚠️ Warnings:")
        for warning in validation["warnings"]:
            st.warning(f"  • {warning}")
    
    # ===== GENERATE OUTPUT =====
    
    if validation["is_valid"]:
        st.markdown("---")
        
        if st.button("🎨 Generate Design", type="primary", use_container_width=True):
            # Generate design
            output = generate_stair_design(user_inputs, derived)
            st.session_state.design_output = output
            st.rerun()

# ============================================================================
# OUTPUT SECTION
# ============================================================================

if "design_output" in st.session_state:
    output = st.session_state.design_output
    
    st.markdown("""
    <div class="step-section">
    <h3>📊 Results</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary
    st.success(f"✅ {output['rebar_summary']}")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Weight", f"{output['total_weight']:.1f}kg")
    col2.metric("Rebar Patterns", len(output['rebars']))
    col3.metric("Riser Height", f"{output['geometry']['riser_height']:.0f}mm")
    col4.metric("Riser Count", f"{output['geometry']['riser_count']:.0f}")
    
    # Schedule
    st.subheader("Reinforcement Schedule")
    st.dataframe(
        output["rebar_schedule"],
        use_container_width=True,
        hide_index=True,
    )
    
    # Download as CSV
    csv = output["rebar_schedule"].to_csv(index=False)
    st.download_button(
        "📥 Download Schedule (CSV)",
        data=csv,
        file_name=f"stair_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    
    # New design button
    if st.button("🔄 New Design", use_container_width=True):
        st.session_state.design_output = None
        st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; margin-top: 3rem;">
<p>iLoveStructural © 2024 | Staircase Designer Tool</p>
<p style="font-size: 0.9rem;">Professional Engineering Design Platform</p>
</div>
""", unsafe_allow_html=True)
