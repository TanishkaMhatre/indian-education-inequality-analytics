import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ----------------------
# App Config
# ----------------------
st.set_page_config(
    page_title="Indian Education Inequality Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------
# Load data
# ----------------------
ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "outputs" / "master_state_education_inequality.csv"

if not MASTER.exists():
    st.error(f"Master CSV not found: {MASTER}")
    st.stop()

df = pd.read_csv(MASTER)

# ----------------------
# Clean + ensure numeric
# ----------------------
num_cols = [
    "Education_Inequality_Index",
    "Gender_Gap_Literacy",
    "Transition_Loss_1_8_to_9_10",
    "Infra_Index",
    "Pct_Internet_AllMgmt",
    "Pct_Electricity_AllMgmt",
    "Pct_Library_AllMgmt",
    "Pct_Handwash_AllMgmt",
    "Rural_Urban_Enrol_Divide",
    "Pct_SecHS_With_Voc",
]

for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

for c in num_cols:
    if c in df.columns and df[c].isna().any():
        df[c] = df[c].fillna(df[c].median())

df["Education_Inequality_Index"] = df["Education_Inequality_Index"].clip(lower=0.1)

# ----------------------
# Theme (CSS)
# ----------------------
st.markdown(
    """
    <style>
    .main {background-color: #f6f7fb;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    .small-note {color:#6b7280; font-size: 0.9rem;}
    .metric-card {background:white; padding:12px; border-radius:14px; border:1px solid #e5e7eb;}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Header
# ----------------------
st.title("📊 Indian Education Inequality Analytics")
st.markdown(
    "A state-wise analytics dashboard built on UDISE-style education indicators. "
    "Explore inequality through **ranking, drivers, clustering (AI), trends, and tables**."
)

# ----------------------
# Sidebar (Controls)
# ----------------------
st.sidebar.header("Controls")
top_n = st.sidebar.slider("Number of states to display", 5, 25, 10)

metric = st.sidebar.selectbox(
    "Ranking Metric",
    [
        "Education_Inequality_Index",
        "Gender_Gap_Literacy",
        "Transition_Loss_1_8_to_9_10",
        "Infra_Index",
        "Pct_Internet_AllMgmt",
        "Pct_Electricity_AllMgmt",
        "Pct_Library_AllMgmt",
        "Pct_Handwash_AllMgmt",
        "Rural_Urban_Enrol_Divide",
        "Pct_SecHS_With_Voc",
    ],
)

order = st.sidebar.radio("Sort", ["Highest First", "Lowest First"])
ascending = True if order == "Lowest First" else False

filtered = df.sort_values(metric, ascending=ascending).head(top_n)

# ----------------------
# KPI Cards (Top-level)
# ----------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("States/UTs", int(df["State"].nunique()))
c2.metric("Highest Inequality", df.sort_values("Education_Inequality_Index", ascending=False).iloc[0]["State"])
c3.metric("Lowest Inequality", df.sort_values("Education_Inequality_Index", ascending=True).iloc[0]["State"])
c4.metric("Avg Infrastructure Index", f"{df['Infra_Index'].mean():.2f}")

st.divider()

# ----------------------
# Tabs
# ----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1) Inequality Ranking",
    "2) Key Drivers",
    "3) State Clusters (AI)",
    "4) Infrastructure Trends",
    "5) Tables & Downloads"
])

# ----------------------
# TAB 1: Ranking
# ----------------------
with tab1:
    st.subheader("Education Inequality Ranking")
    st.markdown(
        "<span class='small-note'>This view ranks states using the selected metric. "
        "Switch metrics in the sidebar to explore different inequality dimensions.</span>",
        unsafe_allow_html=True
    )

    # Key highlight
    worst = df.sort_values(metric, ascending=False).iloc[0]["State"]
    best = df.sort_values(metric, ascending=True).iloc[0]["State"]
    st.info(f"**Highlight:** Highest = **{worst}**, Lowest = **{best}** for **{metric}**.")

    fig = px.bar(
        filtered,
        x=metric,
        y="State",
        orientation="h",
        color=metric,
        color_continuous_scale="Blues",
        height=540,
        title=f"Top {top_n} States by {metric} ({order})"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# TAB 2: Drivers
# ----------------------
with tab2:
    st.subheader("Key Drivers & Relationships")
    st.markdown(
        "<span class='small-note'>These relationships help explain *why* inequality is high in certain states.</span>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 Gender Gap vs Infrastructure")
        st.write("Do better school facilities correlate with lower literacy gender gaps?")

        fig2 = px.scatter(
            df,
            x="Infra_Index",
            y="Gender_Gap_Literacy",
            size="Education_Inequality_Index",
            size_max=42,
            hover_name="State",
            color="Education_Inequality_Index",
            color_continuous_scale="RdYlBu_r",
            height=520,
        )
        fig2.update_layout(xaxis_title="Infrastructure Index (Higher = Better)",
                           yaxis_title="Literacy Gender Gap (Male - Female)")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("### 📌 Transition Loss vs Rural–Urban Divide")
        st.write("Do states with higher rural-urban divide show greater transition loss?")

        fig3 = px.scatter(
            df,
            x="Rural_Urban_Enrol_Divide",
            y="Transition_Loss_1_8_to_9_10",
            hover_name="State",
            color="Education_Inequality_Index",
            color_continuous_scale="Viridis",
            height=520,
        )
        fig3.update_layout(xaxis_title="Rural–Urban Enrol Divide",
                           yaxis_title="Transition Loss (Proxy Dropout)")
        st.plotly_chart(fig3, use_container_width=True)

# ----------------------
# TAB 3: Clustering
# ----------------------
with tab3:
    st.subheader("State Clusters (AI Grouping)")
    st.markdown(
        "<span class='small-note'>KMeans groups states based on similar patterns across drivers.</span>",
        unsafe_allow_html=True
    )

    k = st.slider("Clusters (k)", 2, 8, 4)

    features = df[[
        "Gender_Gap_Literacy",
        "Transition_Loss_1_8_to_9_10",
        "Infra_Index",
        "Rural_Urban_Enrol_Divide"
    ]].copy()

    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    temp = df.copy()
    temp["Cluster"] = km.fit_predict(X).astype(str)

    st.info("**How to read:** Each color = a group of states with similar inequality patterns.")

    figc = px.scatter(
        temp,
        x="Infra_Index",
        y="Transition_Loss_1_8_to_9_10",
        color="Cluster",
        hover_name="State",
        size="Education_Inequality_Index",
        size_max=38,
        height=560,
        title="Clusters: Infrastructure vs Transition Loss"
    )
    figc.update_layout(xaxis_title="Infrastructure Index (Higher = Better)",
                       yaxis_title="Transition Loss (Proxy Dropout)")
    st.plotly_chart(figc, use_container_width=True)

    st.markdown("### Cluster Summary (mean values)")
    st.dataframe(
        temp.groupby("Cluster")[[
            "Education_Inequality_Index",
            "Gender_Gap_Literacy",
            "Transition_Loss_1_8_to_9_10",
            "Infra_Index",
            "Rural_Urban_Enrol_Divide"
        ]].mean().round(2),
        use_container_width=True
    )

# ----------------------
# TAB 4: Trends
# ----------------------
with tab4:
    st.subheader("Infrastructure Trends (2013–2016)")
    st.markdown(
        "<span class='small-note'>Trend charts are based on year-wise infrastructure datasets (if available in your data folder).</span>",
        unsafe_allow_html=True
    )

    trend_choice = st.selectbox("Choose trend dataset", [
        "Electricity (2013–2016)",
        "Water (2013–2016)"
    ])

    if trend_choice.startswith("Electricity"):
        trend_path = ROOT / "data" / "percentage-of-schools-with-electricity-2013-2016.csv"
        state_col = "State_UT"
        year_col = "year"
    else:
        trend_path = ROOT / "data" / "percentage-of-schools-with-water-facility-2013-2016.csv"
        state_col = "State/UT"
        year_col = "Year"

    if not trend_path.exists():
        st.warning(f"Trend dataset not found: {trend_path.name}")
    else:
        tdf = pd.read_csv(trend_path)
        tdf.columns = [c.strip() for c in tdf.columns]

        # normalize state col
        if state_col in tdf.columns:
            tdf = tdf.rename(columns={state_col: "State"})
        if year_col in tdf.columns:
            tdf = tdf.rename(columns={year_col: "Year"})

        if "All Schools" not in tdf.columns:
            st.warning("Column 'All Schools' not found in selected dataset.")
        else:
            state_selected = st.selectbox("Select state for trend", sorted(tdf["State"].astype(str).unique()))
            sdata = tdf[tdf["State"].astype(str) == str(state_selected)].sort_values("Year")

            figl = px.line(
                sdata,
                x="Year",
                y="All Schools",
                markers=True,
                height=520,
                title=f"{trend_choice}: % Schools (All Schools) — {state_selected}"
            )
            figl.update_layout(yaxis_title="% Schools", xaxis_title="Year")
            st.plotly_chart(figl, use_container_width=True)

# ----------------------
# TAB 5: Tables + Downloads
# ----------------------
with tab5:
    st.subheader("Tables & Downloads")
    st.markdown(
        "<span class='small-note'>Use these tables for documentation. You can also download filtered outputs.</span>",
        unsafe_allow_html=True
    )

    # Table for selected metric
    table = df.sort_values(metric, ascending=ascending).head(top_n)[[
        "State",
        "Education_Inequality_Index",
        "Gender_Gap_Literacy",
        "Transition_Loss_1_8_to_9_10",
        "Infra_Index",
        "Pct_Internet_AllMgmt",
        "Pct_Electricity_AllMgmt",
        "Pct_Library_AllMgmt",
        "Pct_Handwash_AllMgmt",
        "Pct_SecHS_With_Voc",
        "Rural_Urban_Enrol_Divide"
    ]].copy()

    st.markdown("### Ranked Table (current metric)")
    st.dataframe(table, use_container_width=True, height=520)

    colA, colB = st.columns(2)
    with colA:
        st.download_button(
            "⬇️ Download this table (CSV)",
            data=table.to_csv(index=False).encode("utf-8"),
            file_name="ranked_table.csv",
            mime="text/csv"
        )
    with colB:
        st.download_button(
            "⬇️ Download full master dataset (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="master_state_education_inequality.csv",
            mime="text/csv"
        )

# ----------------------
# Footer
# ----------------------
st.markdown("---")
st.caption(
    "📊 Indian Education Inequality Analytics Dashboard | "
    "Data Source: UDISE (2015–16) & Infrastructure Trends (2013–2016) | "
    "Developed by Tanishka Dnyaneshwar Mhatre"
)