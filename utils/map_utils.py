"""
RuralBiz Navigator - GIS & Hyper-Local Map Utilities
Supports Folium Leaflet interactive maps with automatic Plotly synthetic fallback.
Visualizes User Location, Competitors, Market Center, and 5 km / 10 km catchment radii.
"""
import folium
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, Optional
from config import MAP_RADIUS_INNER_KM, MAP_RADIUS_OUTER_KM

def build_folium_map(
    locality: Dict[str, Any],
    competitors_df: pd.DataFrame,
    business_name: str = "Proposed Business"
) -> Optional[folium.Map]:
    """
    Creates an interactive Folium Leaflet map with:
    - User/Business Location pin (Red)
    - 5 km Market Reach Buffer (Green dashed circle)
    - 10 km Regional Catchment Buffer (Blue dashed circle)
    - Local Competitor pins with sales & rating popups
    - Market Center pin
    """
    try:
        lat = float(locality.get("latitude", 20.5937))
        lon = float(locality.get("longitude", 78.9629))
        loc_name = locality.get("village_name", "Rural Location")
        
        # Center map
        m = folium.Map(
            location=[lat, lon],
            zoom_start=12,
            tiles="CartoDB positron",  # Clean, fast-loading, reliable vector-style tile
            control_scale=True
        )

        # 1. 10 km Outer Catchment Circle
        folium.Circle(
            location=[lat, lon],
            radius=MAP_RADIUS_OUTER_KM * 1000,
            color="#3B82F6",
            weight=2,
            dash_array="6, 6",
            fill=True,
            fill_color="#3B82F6",
            fill_opacity=0.06,
            popup="10 km Regional Market Catchment"
        ).add_to(m)

        # 2. 5 km Primary Reach Circle
        folium.Circle(
            location=[lat, lon],
            radius=MAP_RADIUS_INNER_KM * 1000,
            color="#10B981",
            weight=2.5,
            dash_array="4, 4",
            fill=True,
            fill_color="#10B981",
            fill_opacity=0.12,
            popup="5 km Hyper-Local Primary Reach"
        ).add_to(m)

        # 3. User Location Marker
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>Proposed Venture:</b> {business_name}<br><b>Location:</b> {loc_name}",
            tooltip=f"Proposed Site ({business_name})",
            icon=folium.Icon(color="red", icon="home", prefix="fa")
        ).add_to(m)

        # 4. Market Center Marker (slightly offset based on market_distance_km)
        mkt_dist = float(locality.get("market_distance_km", 4.0))
        mkt_lat = lat + (mkt_dist * 0.007)
        mkt_lon = lon + (mkt_dist * 0.007)
        folium.Marker(
            location=[mkt_lat, mkt_lon],
            popup=f"<b>Weekly Haat / APMC Mandi</b><br>Distance: ~{mkt_dist:.1f} km from village",
            tooltip="Local Mandi / Market Center",
            icon=folium.Icon(color="blue", icon="shopping-cart", prefix="fa")
        ).add_to(m)

        # 5. Local Bank / Financial Center
        bank_lat = lat - 0.008
        bank_lon = lon + 0.005
        folium.Marker(
            location=[bank_lat, bank_lon],
            popup=f"<b>Rural Bank / PACS Branch</b><br>Score: {locality.get('bank_access_score', 60)}/100",
            tooltip="Bank / Cooperative Credit Point",
            icon=folium.Icon(color="green", icon="university", prefix="fa")
        ).add_to(m)

        # 6. Competitor Markers
        if competitors_df is not None and not competitors_df.empty:
            for _, c in competitors_df.iterrows():
                c_lat = float(c["latitude"])
                c_lon = float(c["longitude"])
                sales = float(c.get("estimated_monthly_sales", 0))
                rating = float(c.get("customer_rating", 3.5))
                c_name = str(c.get("business_name", "Competitor"))
                
                popup_html = f"""
                <div style="font-family: Arial; font-size: 12px; width: 180px;">
                    <b style="color: #D97706;">{c_name}</b><br>
                    <b>Category:</b> {c.get('business_type', 'Trade')}<br>
                    <b>Est. Monthly Sales:</b> ₹{sales:,.0f}<br>
                    <b>Customer Rating:</b> ⭐ {rating:.1f}/5<br>
                    <b>Strength:</b> {c.get('strength', 'N/A')}<br>
                    <b>Weakness:</b> {c.get('weakness', 'N/A')}
                </div>
                """
                
                folium.Marker(
                    location=[c_lat, c_lon],
                    popup=folium.Popup(popup_html, max_width=220),
                    tooltip=f"Competitor: {c_name} (⭐ {rating:.1f})",
                    icon=folium.Icon(color="orange", icon="user", prefix="fa")
                ).add_to(m)

        return m
    except Exception as e:
        return None

def build_fallback_plotly_map(
    locality: Dict[str, Any],
    competitors_df: pd.DataFrame,
    business_name: str = "Proposed Business"
) -> go.Figure:
    """
    Offline/synthetic fallback map rendered with Plotly.
    Plots relative km coordinates with 5 km and 10 km concentric radius rings.
    Works 100% offline without relying on external map tiles or internet connectivity.
    """
    import numpy as np

    fig = go.Figure()

    # Draw 10 km concentric circle
    theta = np.linspace(0, 2 * np.pi, 100)
    x_10 = 10 * np.cos(theta)
    y_10 = 10 * np.sin(theta)
    fig.add_trace(go.Scatter(
        x=x_10, y=y_10,
        mode="lines",
        line=dict(color="#3B82F6", width=2, dash="dash"),
        name="10 km Regional Catchment",
        hoverinfo="name"
    ))

    # Draw 5 km concentric circle
    x_5 = 5 * np.cos(theta)
    y_5 = 5 * np.sin(theta)
    fig.add_trace(go.Scatter(
        x=x_5, y=y_5,
        mode="lines",
        line=dict(color="#10B981", width=2.5, dash="dot"),
        fill="toself",
        fillcolor="rgba(16, 185, 129, 0.08)",
        name="5 km Hyper-Local Primary Reach",
        hoverinfo="name"
    ))

    # Center: User Location (0, 0)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers+text",
        marker=dict(size=18, color="#EF4444", symbol="star"),
        text=[f"★ Proposed: {business_name}"],
        textposition="top center",
        name="Your Proposed Venture",
        hovertext=[f"Location: {locality.get('village_name', 'Village')}<br>Center (0, 0)"],
        hoverinfo="text"
    ))

    # Market Center offset
    mkt_dist = float(locality.get("market_distance_km", 4.0))
    fig.add_trace(go.Scatter(
        x=[mkt_dist * 0.7], y=[mkt_dist * 0.7],
        mode="markers+text",
        marker=dict(size=14, color="#2563EB", symbol="diamond"),
        text=["Local Mandi / Haat"],
        textposition="bottom right",
        name="Market Center",
        hovertext=[f"Mandi (~{mkt_dist:.1f} km away)"],
        hoverinfo="text"
    ))

    # Bank Branch offset
    fig.add_trace(go.Scatter(
        x=[-1.5], y=[2.0],
        mode="markers+text",
        marker=dict(size=12, color="#059669", symbol="square"),
        text=["Rural Bank Branch"],
        textposition="bottom left",
        name="Bank / PACS Branch",
        hovertext=["Local Bank Branch (~2.5 km away)"],
        hoverinfo="text"
    ))

    # Plot Competitors
    if competitors_df is not None and not competitors_df.empty:
        comp_x = []
        comp_y = []
        comp_texts = []
        comp_hover = []
        
        # Approximate relative km from lat/lon offset
        lat0 = float(locality.get("latitude", 20.0))
        lon0 = float(locality.get("longitude", 78.0))
        
        for _, c in competitors_df.iterrows():
            d_lat = (float(c["latitude"]) - lat0) * 111.0
            d_lon = (float(c["longitude"]) - lon0) * 105.0
            comp_x.append(round(d_lon, 2))
            comp_y.append(round(d_lat, 2))
            comp_texts.append(c["business_name"][:15])
            comp_hover.append(
                f"<b>{c['business_name']}</b><br>"
                f"Rating: ⭐ {c.get('customer_rating', 3.5)}<br>"
                f"Est. Monthly Sales: ₹{float(c.get('estimated_monthly_sales', 0)):,.0f}<br>"
                f"Strength: {c.get('strength', 'N/A')}<br>"
                f"Weakness: {c.get('weakness', 'N/A')}"
            )

        fig.add_trace(go.Scatter(
            x=comp_x, y=comp_y,
            mode="markers+text",
            marker=dict(size=13, color="#D97706", symbol="circle"),
            text=comp_texts,
            textposition="top right",
            name="Existing Competitors",
            hovertext=comp_hover,
            hoverinfo="text"
        ))

    fig.update_layout(
        title=f"Hyper-Local Reach & Competitor Map ({locality.get('village_name', 'Village')})",
        xaxis=dict(title="East-West Distance (km)", range=[-12, 12], zeroline=True),
        yaxis=dict(title="North-South Distance (km)", range=[-12, 12], zeroline=True, scaleanchor="x", scaleratio=1),
        template="plotly_white",
        height=520,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=50, b=50)
    )
    return fig
