"""
RuralBiz Navigator - Hyper-Local Market & Competitor GIS
Visualizes 5-10 km market catchment, competitors, customer pool, and local demand metrics.
"""
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from utils.ui_components import load_custom_css, render_sidebar, render_disclaimer_footer
from i18n.translations import t
from utils.map_utils import build_folium_map, build_fallback_plotly_map
from utils.formatting import format_inr
from database.db import get_competitors

st.set_page_config(
    page_title="RuralBiz Navigator - Hyper-Local Market",
    page_icon="📍",
    layout="wide"
)

load_custom_css()
render_sidebar()
lang = st.session_state.get("language", "en")

st.title("📍 " + t("nav_market", lang))
st.caption("Hyper-local catchment mapping, competitor analysis, and demand gap estimation in a 5–10 km rural radius.")

locality = st.session_state.get("locality")
business = st.session_state.get("business")
hl = st.session_state.get("hyperlocal_metrics")

if not locality or not business or not hl:
    st.warning("⚠️ Please start an assessment on the Home or Feasibility page first.")
    st.stop()

# 1. Locality Catchment Demographics Overview
st.subheader(f"🏘️ Catchment Profile: {locality.get('village_name', 'Village')}")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Local Population", f"{locality.get('population', 0):,}", f"{locality.get('households', 0):,} Households")
m2.metric("Mandi / Market Distance", f"{locality.get('market_distance_km', 0):.1f} km", "Nearest hub")
m3.metric("Road Connectivity", f"{locality.get('road_access_score', 0):.0f} / 100", "Paved road index")
m4.metric("Purchasing Power", f"{locality.get('purchasing_power_index', 0):.0f} / 100", "Income tier")
m5.metric("Target Customer Pool", f"{hl.get('customer_pool', 0):,} HHs", "5-10 km radius")

st.markdown("---")

# 2. GIS Map Visualization (Folium vs Plotly Fallback)
st.subheader("🗺️ 5 km & 10 km Hyper-Local Catchment Map")
st.markdown(
    """
    <div style="font-size:0.88rem; color:#4B5563; margin-bottom:10px;">
        <span style="color:#10B981; font-weight:bold;">● 5 km Circle (Inner):</span> Immediate hyper-local consumer footfall & daily delivery zone.<br/>
        <span style="color:#3B82F6; font-weight:bold;">● 10 km Circle (Outer):</span> Weekly market / Haat catchment & regional wholesale radius.<br/>
        <span style="color:#EF4444; font-weight:bold;">★ Red Pin:</span> Your proposed unit &bull;
        <span style="color:#D97706; font-weight:bold;">● Orange Pins:</span> Existing local competitors &bull;
        <span style="color:#2563EB; font-weight:bold;">◆ Blue Pin:</span> APMC Mandi / Market Center.
    </div>
    """,
    unsafe_allow_html=True
)

competitors_df = get_competitors(locality_id=locality.get("village_id"), business_type=business.get("category"))

map_mode = st.radio(
    "Select Map Mode",
    options=["Interactive Leaflet GIS Map (OpenStreetMap/Carto)", "Offline Synthetic Scatter Map (Plotly fallback)"],
    horizontal=True
)

if "Interactive Leaflet" in map_mode:
    try:
        folium_map = build_folium_map(locality, competitors_df, business.get("business_name", "Venture"))
        if folium_map:
            st_folium(folium_map, width="100%", height=500, returned_objects=[])
        else:
            st.warning("Leaflet rendering unavailable. Switching to offline synthetic map.")
            fig_fallback = build_fallback_plotly_map(locality, competitors_df, business.get("business_name", "Venture"))
            st.plotly_chart(fig_fallback, use_container_width=True)
    except Exception as e:
        st.info("External map tile connection not available. Showing synthetic offline map.")
        fig_fallback = build_fallback_plotly_map(locality, competitors_df, business.get("business_name", "Venture"))
        st.plotly_chart(fig_fallback, use_container_width=True)
else:
    fig_fallback = build_fallback_plotly_map(locality, competitors_df, business.get("business_name", "Venture"))
    st.plotly_chart(fig_fallback, use_container_width=True)

st.markdown("---")

# 3. Market Gap & Demand Insights
st.subheader("💡 Hyper-Local Demand & Market Gap")

col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.metric(
        "Estimated Unmet Market Gap",
        format_inr(hl.get("estimated_unmet_demand_rupees", 0)),
        "Monthly spending gap"
    )
with col_g2:
    st.metric(
        "Local Competition Score",
        f"{hl.get('competition_score', 0):.1f} / 100",
        f"{hl.get('num_competitors', 0)} competitor(s)"
    )
with col_g3:
    st.metric(
        "Local Opportunity Index",
        f"{hl.get('local_opportunity_score', 0):.1f} / 100",
        "Demand vs Competition"
    )

st.markdown("<br/>", unsafe_allow_html=True)

# 4. Competitor Table
st.subheader(f"👥 Existing Local Competitors ({business.get('category')})")
st.markdown("<span class='prototype-tag'>Prototype simulated competitor data — for demonstration only.</span>", unsafe_allow_html=True)

if competitors_df is not None and not competitors_df.empty:
    display_cols = ["business_name", "price_level", "customer_rating", "estimated_monthly_sales", "distance_from_center", "strength", "weakness"]
    comp_view = competitors_df[display_cols].copy()
    comp_view.rename(columns={
        "business_name": "Competitor Name",
        "price_level": "Price Level",
        "customer_rating": "Rating (⭐/5)",
        "estimated_monthly_sales": "Est. Monthly Sales (₹)",
        "distance_from_center": "Distance (km)",
        "strength": "Key Strength",
        "weakness": "Exploitable Weakness"
    }, inplace=True)
    comp_view["Est. Monthly Sales (₹)"] = comp_view["Est. Monthly Sales (₹)"].apply(lambda x: format_inr(x))
    st.dataframe(comp_view, use_container_width=True, hide_index=True)
else:
    st.success(f"🎉 No direct competitors found for '{business.get('category')}' in {locality.get('village_name')}! High first-mover opportunity.")

render_disclaimer_footer(lang)
