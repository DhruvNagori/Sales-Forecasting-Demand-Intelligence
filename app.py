# ============================================================
# SALES FORECASTING & DEMAND INTELLIGENCE DASHBOARD
# Final Task 7 Streamlit Application
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from PIL import Image


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Forecasting & Demand Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CHARTS_DIR = BASE_DIR / "charts"
TRAIN_FILE = BASE_DIR / "train.csv"


# ============================================================
# 3. PROFESSIONAL LIGHT/DARK COMPATIBLE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       Global application
    -------------------------------------------------------- */

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* --------------------------------------------------------
       Main hero header
    -------------------------------------------------------- */

    .hero-card {
        background:
            linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.16),
                rgba(14, 165, 233, 0.10),
                rgba(139, 92, 246, 0.12)
            );
        border: 1px solid rgba(99, 102, 241, 0.28);
        border-radius: 18px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    }

    .hero-title {
        font-size: 2.15rem;
        font-weight: 800;
        line-height: 1.15;
        margin: 0;
        color: var(--text-color);
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.78;
        margin-top: 0.6rem;
        margin-bottom: 0;
        color: var(--text-color);
    }

    /* --------------------------------------------------------
       Section cards
    -------------------------------------------------------- */

    .section-card {
        background: rgba(127, 127, 127, 0.055);
        border: 1px solid rgba(127, 127, 127, 0.22);
        border-radius: 15px;
        padding: 1.15rem 1.25rem;
        margin: 0.7rem 0 1rem 0;
    }

    .insight-card {
        background:
            linear-gradient(
                135deg,
                rgba(14, 165, 233, 0.11),
                rgba(37, 99, 235, 0.07)
            );
        border-left: 5px solid #0EA5E9;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        margin: 0.8rem 0;
    }

    .success-card {
        background:
            linear-gradient(
                135deg,
                rgba(16, 185, 129, 0.12),
                rgba(5, 150, 105, 0.06)
            );
        border-left: 5px solid #10B981;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        margin: 0.8rem 0;
    }

    .warning-card {
        background:
            linear-gradient(
                135deg,
                rgba(245, 158, 11, 0.13),
                rgba(217, 119, 6, 0.06)
            );
        border-left: 5px solid #F59E0B;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        margin: 0.8rem 0;
    }

    .danger-card {
        background:
            linear-gradient(
                135deg,
                rgba(239, 68, 68, 0.12),
                rgba(220, 38, 38, 0.06)
            );
        border-left: 5px solid #EF4444;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        margin: 0.8rem 0;
    }

    /* --------------------------------------------------------
       Small labels / badges
    -------------------------------------------------------- */

    .badge {
        display: inline-block;
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }

    .badge-blue {
        background: rgba(37, 99, 235, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(37, 99, 235, 0.28);
    }

    .badge-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.28);
    }

    .badge-orange {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.28);
    }

    /* --------------------------------------------------------
       Metrics
    -------------------------------------------------------- */

    div[data-testid="stMetric"] {
        background: rgba(127, 127, 127, 0.055);
        border: 1px solid rgba(127, 127, 127, 0.20);
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        font-weight: 650;
    }

    /* --------------------------------------------------------
       Sidebar
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(127, 127, 127, 0.18);
    }

    /* --------------------------------------------------------
       Dataframe
    -------------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(127, 127, 127, 0.18);
        border-radius: 12px;
        overflow: hidden;
    }

    /* --------------------------------------------------------
       Responsive design
    -------------------------------------------------------- */

    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.65rem;
        }

        .hero-card {
            padding: 1.2rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. COLOR PALETTE
# ============================================================

COLORS = {
    "blue": "#3B82F6",
    "cyan": "#06B6D4",
    "green": "#10B981",
    "orange": "#F59E0B",
    "red": "#EF4444",
    "purple": "#8B5CF6",
    "pink": "#EC4899",
    "slate": "#64748B"
}

CATEGORY_COLORS = {
    "Furniture": "#3B82F6",
    "Technology": "#F59E0B",
    "Office Supplies": "#10B981"
}

REGION_COLORS = {
    "West": "#EF4444",
    "East": "#8B5CF6",
    "Central": "#06B6D4",
    "South": "#F59E0B"
}


# ============================================================
# 5. GENERAL HELPER FUNCTIONS
# ============================================================

def normalize_columns(df):
    """
    Remove leading/trailing spaces from column names.
    """
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def find_column(df, candidates):
    """
    Find a column using case-insensitive matching.
    """
    column_map = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for candidate in candidates:
        key = candidate.strip().lower()
        if key in column_map:
            return column_map[key]

    return None


def find_file(directory, possible_names):
    """
    Search for a file using multiple possible names.
    """
    if not directory.exists():
        return None

    existing_files = {
        file.name.lower(): file
        for file in directory.iterdir()
        if file.is_file()
    }

    for name in possible_names:
        if name.lower() in existing_files:
            return existing_files[name.lower()]

    return None


def find_image_by_keywords(keywords):
    """
    Find PNG/JPG image whose filename contains keywords.
    """
    if not CHARTS_DIR.exists():
        return None

    image_files = list(CHARTS_DIR.glob("*.png"))
    image_files += list(CHARTS_DIR.glob("*.jpg"))
    image_files += list(CHARTS_DIR.glob("*.jpeg"))

    for image_file in image_files:
        filename = image_file.name.lower()

        if all(keyword.lower() in filename for keyword in keywords):
            return image_file

    return None


def safe_read_csv(path):
    """
    Safely read a CSV file.
    """
    if path is None or not path.exists():
        return None

    try:
        df = pd.read_csv(path)
        return normalize_columns(df)
    except Exception as e:
        st.warning(f"Could not read {path.name}: {e}")
        return None


def display_saved_image(image_path, caption=None):
    """
    Display a saved chart image.
    """
    if image_path is None or not image_path.exists():
        return False

    try:
        image = Image.open(image_path)

        st.image(
            image,
            caption=caption,
            use_container_width=True
        )
        return True

    except Exception as e:
        st.warning(f"Could not display image: {e}")
        return False


def format_currency(value):
    """
    Format values as currency.
    """
    try:
        return f"${value:,.2f}"
    except Exception:
        return str(value)


def professional_layout(fig, title=None, height=500):
    """
    Apply a professional Plotly layout compatible
    with Streamlit light and dark modes.
    """
    fig.update_layout(
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(size=20)
        ) if title else None,

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=70 if title else 30,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial, sans-serif"
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            font_color="#F9FAFB",
            bordercolor="#374151"
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor="rgba(127,127,127,0.16)",
        zeroline=False
    )

    return fig


# ============================================================
# 6. DATA LOADING
# ============================================================

@st.cache_data
def load_train_data():
    """
    Load original Superstore dataset.
    """
    if not TRAIN_FILE.exists():
        return None

    df = pd.read_csv(TRAIN_FILE)
    df = normalize_columns(df)

    date_col = find_column(
        df,
        ["Order Date", "Order_Date", "Date"]
    )

    if date_col:
        df[date_col] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    return df


@st.cache_data
def load_segment_forecasts():
    path = find_file(
        CHARTS_DIR,
        [
            "segment_forecasts.csv",
            "segment_forecast.csv",
            "forecast_segments.csv"
        ]
    )
    return safe_read_csv(path)


@st.cache_data
def load_zscore_anomalies():
    path = find_file(
        CHARTS_DIR,
        [
            "z_score_anomalies.csv",
            "zscore_anomalies.csv",
            "z-score_anomalies.csv"
        ]
    )
    return safe_read_csv(path)


@st.cache_data
def load_isolation_anomalies():
    path = find_file(
        CHARTS_DIR,
        [
            "isolation_forest_anomalies.csv",
            "isolation_anomalies.csv"
        ]
    )
    return safe_read_csv(path)


@st.cache_data
def load_common_anomalies():
    path = find_file(
        CHARTS_DIR,
        [
            "common_anomalies.csv",
            "common_anomaly.csv"
        ]
    )
    return safe_read_csv(path)


@st.cache_data
def load_product_clusters():
    path = find_file(
        CHARTS_DIR,
        [
            "product_clusters.csv",
            "product_cluster.csv",
            "clustered_products.csv"
        ]
    )
    return safe_read_csv(path)


@st.cache_data
def load_product_features():
    path = find_file(
        CHARTS_DIR,
        [
            "product_demand_features.csv",
            "product_features.csv",
            "demand_features.csv"
        ]
    )
    return safe_read_csv(path)


# Load data
df = load_train_data()
segment_forecasts = load_segment_forecasts()
zscore_anomalies = load_zscore_anomalies()
isolation_anomalies = load_isolation_anomalies()
common_anomalies = load_common_anomalies()
product_clusters = load_product_clusters()
product_features = load_product_features()


# ============================================================
# 7. VALIDATE MAIN DATASET
# ============================================================

if df is None:
    st.error(
        "train.csv was not found in the project root folder. "
        "Place train.csv beside app.py."
    )
    st.stop()


DATE_COL = find_column(
    df,
    ["Order Date", "Order_Date", "Date"]
)

SALES_COL = find_column(
    df,
    ["Sales", "Total Sales", "Total_Sales"]
)

REGION_COL = find_column(
    df,
    ["Region"]
)

CATEGORY_COL = find_column(
    df,
    ["Category"]
)

SUBCATEGORY_COL = find_column(
    df,
    ["Sub-Category", "Sub_Category", "SubCategory"]
)

if DATE_COL is None or SALES_COL is None:
    st.error(
        "The dataset must contain an order-date column "
        "and a sales column."
    )
    st.stop()


# ============================================================
# 8. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown("## Sales Intelligence")

    st.caption(
        "Forecasting, anomaly detection and demand segmentation"
    )

    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "Sales Overview",
            "Forecast Explorer",
            "Anomaly Report",
            "Product Demand Segments"
        ]
    )

    st.markdown("---")

    st.markdown("### Project Scope")

    st.markdown(
        """
        <span class="badge badge-blue">Forecasting</span>
        <span class="badge badge-orange">Anomalies</span>
        <span class="badge badge-green">Clustering</span>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")

    st.caption(
        "Decision-support dashboard for retail sales "
        "and supply-chain planning."
    )


# ============================================================
# PAGE 1 — SALES OVERVIEW DASHBOARD
# ============================================================

if page == "Sales Overview":

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">
                Sales Overview Dashboard
            </div>
            <div class="hero-subtitle">
                Historical performance, monthly movement and
                interactive regional/category analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.subheader("Interactive Filters")

    filter_col1, filter_col2 = st.columns(2)

    if REGION_COL:
        region_options = sorted(
            df[REGION_COL]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_regions = filter_col1.multiselect(
            "Select Region",
            options=region_options,
            default=region_options
        )
    else:
        selected_regions = []

    if CATEGORY_COL:
        category_options = sorted(
            df[CATEGORY_COL]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_categories = filter_col2.multiselect(
            "Select Category",
            options=category_options,
            default=category_options
        )
    else:
        selected_categories = []

    filtered_df = df.copy()

    if REGION_COL and selected_regions:
        filtered_df = filtered_df[
            filtered_df[REGION_COL]
            .astype(str)
            .isin(selected_regions)
        ]

    if CATEGORY_COL and selected_categories:
        filtered_df = filtered_df[
            filtered_df[CATEGORY_COL]
            .astype(str)
            .isin(selected_categories)
        ]

    # --------------------------------------------------------
    # KPI metrics
    # --------------------------------------------------------

    total_sales = filtered_df[SALES_COL].sum()
    total_orders = len(filtered_df)
    average_sale = filtered_df[SALES_COL].mean()

    years = filtered_df[DATE_COL].dt.year.dropna()

    active_years = (
        int(years.nunique())
        if not years.empty
        else 0
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )

    metric2.metric(
        "Sales Records",
        f"{total_orders:,}"
    )

    metric3.metric(
        "Average Sale",
        f"${average_sale:,.2f}"
    )

    metric4.metric(
        "Years Covered",
        active_years
    )

    st.markdown("---")

    # --------------------------------------------------------
    # Requirement: Total sales by year — bar chart
    # --------------------------------------------------------

    st.subheader("Total Sales by Year")

    yearly_sales = (
        filtered_df
        .dropna(subset=[DATE_COL])
        .assign(
            Year=lambda x: x[DATE_COL].dt.year
        )
        .groupby("Year", as_index=False)[SALES_COL]
        .sum()
    )

    fig_year = px.bar(
        yearly_sales,
        x="Year",
        y=SALES_COL,
        text_auto=".3s",
        color="Year",
        color_continuous_scale=[
            "#2563EB",
            "#06B6D4",
            "#10B981"
        ]
    )

    fig_year.update_traces(
        hovertemplate=(
            "<b>Year %{x}</b><br>"
            "Sales: $%{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig_year.update_layout(
        coloraxis_showscale=False
    )

    professional_layout(
        fig_year,
        "Annual Sales Performance",
        470
    )

    fig_year.update_yaxes(
        title="Total Sales"
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Requirement: Monthly sales trend
    # --------------------------------------------------------

    st.subheader("Monthly Sales Trend")

    monthly_sales = (
        filtered_df
        .dropna(subset=[DATE_COL])
        .set_index(DATE_COL)
        .resample("MS")[SALES_COL]
        .sum()
        .reset_index()
    )

    fig_month = go.Figure()

    fig_month.add_trace(
        go.Scatter(
            x=monthly_sales[DATE_COL],
            y=monthly_sales[SALES_COL],
            mode="lines+markers",
            name="Monthly Sales",
            line=dict(
                color=COLORS["cyan"],
                width=3
            ),
            marker=dict(
                size=7,
                color=COLORS["blue"]
            ),
            fill="tozeroy",
            fillcolor="rgba(6,182,212,0.08)",
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Sales: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    professional_layout(
        fig_month,
        "Monthly Sales Movement",
        500
    )

    fig_month.update_yaxes(
        title="Sales"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Region and category analysis
    # --------------------------------------------------------

    st.subheader("Sales by Region and Category")

    chart_col1, chart_col2 = st.columns(2)

    if REGION_COL:

        region_sales = (
            filtered_df
            .groupby(REGION_COL, as_index=False)[SALES_COL]
            .sum()
            .sort_values(SALES_COL, ascending=False)
        )

        fig_region = px.bar(
            region_sales,
            x=REGION_COL,
            y=SALES_COL,
            color=REGION_COL,
            color_discrete_map=REGION_COLORS
        )

        professional_layout(
            fig_region,
            "Regional Sales Distribution",
            430
        )

        fig_region.update_yaxes(
            title="Sales"
        )

        chart_col1.plotly_chart(
            fig_region,
            use_container_width=True
        )

    if CATEGORY_COL:

        category_sales = (
            filtered_df
            .groupby(CATEGORY_COL, as_index=False)[SALES_COL]
            .sum()
            .sort_values(SALES_COL, ascending=False)
        )

        fig_category = px.bar(
            category_sales,
            x=CATEGORY_COL,
            y=SALES_COL,
            color=CATEGORY_COL,
            color_discrete_map=CATEGORY_COLORS
        )

        professional_layout(
            fig_category,
            "Category Sales Distribution",
            430
        )

        fig_category.update_yaxes(
            title="Sales"
        )

        chart_col2.plotly_chart(
            fig_category,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Combined interactive region-category chart
    # --------------------------------------------------------

    if REGION_COL and CATEGORY_COL:

        st.subheader(
            "Region × Category Performance"
        )

        region_category_sales = (
            filtered_df
            .groupby(
                [REGION_COL, CATEGORY_COL],
                as_index=False
            )[SALES_COL]
            .sum()
        )

        fig_combined = px.bar(
            region_category_sales,
            x=REGION_COL,
            y=SALES_COL,
            color=CATEGORY_COL,
            barmode="group",
            color_discrete_map=CATEGORY_COLORS
        )

        professional_layout(
            fig_combined,
            "Sales Comparison Across Regions and Categories",
            520
        )

        fig_combined.update_yaxes(
            title="Sales"
        )

        st.plotly_chart(
            fig_combined,
            use_container_width=True
        )

    st.markdown(
        """
        <div class="insight-card">
            <b>Business interpretation:</b>
            Use the filters above to identify whether sales growth
            is broad-based or concentrated in specific combinations
            of region and product category. This supports targeted
            inventory allocation rather than applying one stocking
            policy across the entire business.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE 2 — FORECAST EXPLORER
# ============================================================

elif page == "Forecast Explorer":

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">
                Forecast Explorer
            </div>
            <div class="hero-subtitle">
                Explore 1–3 month sales outlooks by product
                category or geographic region.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Model performance summary
    # --------------------------------------------------------

    st.subheader("Model Performance")

    st.markdown(
        """
        <div class="success-card">
            <b>Best evaluated overall model: XGBoost</b><br>
            The project compared multiple forecasting approaches.
            XGBoost produced the strongest overall holdout performance
            based on the evaluation results used in the notebook.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Values from your completed notebook results
    BEST_MODEL_NAME = "XGBoost"
    BEST_MODEL_MAE = 18710.45
    BEST_MODEL_RMSE = 20852.57

    model_col1, model_col2, model_col3 = st.columns(3)

    model_col1.metric(
        "Best Overall Model",
        BEST_MODEL_NAME
    )

    model_col2.metric(
        "MAE",
        f"${BEST_MODEL_MAE:,.2f}"
    )

    model_col3.metric(
        "RMSE",
        f"${BEST_MODEL_RMSE:,.2f}"
    )

    st.caption(
        "MAE and RMSE shown here are overall model evaluation "
        "metrics from the notebook. They should not be interpreted "
        "as separate accuracy scores for every individual segment."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # Required forecast controls
    # --------------------------------------------------------

    st.subheader("Interactive Forecast Selection")

    control1, control2, control3 = st.columns(3)

    selection_type = control1.selectbox(
        "Forecast Dimension",
        ["Category", "Region"]
    )

    horizon = control3.slider(
        "Forecast Horizon",
        min_value=1,
        max_value=3,
        value=3,
        step=1,
        help="Choose 1, 2 or 3 months ahead."
    )

    # Determine available segments
    if selection_type == "Category":
        if CATEGORY_COL:
            valid_segments = sorted(
                df[CATEGORY_COL]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        else:
            valid_segments = []

    else:
        if REGION_COL:
            valid_segments = sorted(
                df[REGION_COL]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        else:
            valid_segments = []

    selected_segment = control2.selectbox(
        f"Select {selection_type}",
        valid_segments
    )

    # --------------------------------------------------------
    # Segment forecast CSV
    # --------------------------------------------------------

    if segment_forecasts is not None:

        forecast_df = segment_forecasts.copy()

        forecast_date_col = find_column(
            forecast_df,
            ["Date", "ds", "Order Date", "Order_Date"]
        )

        if forecast_date_col:

            forecast_df[forecast_date_col] = pd.to_datetime(
                forecast_df[forecast_date_col],
                errors="coerce"
            )

            # Find matching segment column
            matching_col = None

            for col in forecast_df.columns:
                if (
                    str(col).strip().lower()
                    == str(selected_segment).strip().lower()
                ):
                    matching_col = col
                    break

            if matching_col:

                selected_forecast = (
                    forecast_df[
                        [forecast_date_col, matching_col]
                    ]
                    .dropna()
                    .sort_values(forecast_date_col)
                    .head(horizon)
                    .copy()
                )

                st.subheader(
                    f"{selected_segment}: "
                    f"{horizon}-Month Forecast"
                )

                # --------------------------------------------
                # Historical context
                # --------------------------------------------

                if selection_type == "Category":
                    historical_segment = df[
                        df[CATEGORY_COL].astype(str)
                        == str(selected_segment)
                    ].copy()
                else:
                    historical_segment = df[
                        df[REGION_COL].astype(str)
                        == str(selected_segment)
                    ].copy()

                historical_monthly = (
                    historical_segment
                    .dropna(subset=[DATE_COL])
                    .set_index(DATE_COL)
                    .resample("MS")[SALES_COL]
                    .sum()
                    .reset_index()
                )

                # Last 12 historical months
                historical_recent = (
                    historical_monthly
                    .tail(12)
                )

                fig_forecast = go.Figure()

                fig_forecast.add_trace(
                    go.Scatter(
                        x=historical_recent[DATE_COL],
                        y=historical_recent[SALES_COL],
                        mode="lines+markers",
                        name="Historical Sales",
                        line=dict(
                            color=COLORS["blue"],
                            width=3
                        ),
                        marker=dict(size=6),
                        hovertemplate=(
                            "<b>%{x|%b %Y}</b><br>"
                            "Historical: $%{y:,.2f}"
                            "<extra></extra>"
                        )
                    )
                )

                fig_forecast.add_trace(
                    go.Scatter(
                        x=selected_forecast[forecast_date_col],
                        y=selected_forecast[matching_col],
                        mode="lines+markers",
                        name="Segment Forecast",
                        line=dict(
                            color=COLORS["orange"],
                            width=4,
                            dash="dash"
                        ),
                        marker=dict(
                            size=10,
                            color=COLORS["orange"]
                        ),
                        hovertemplate=(
                            "<b>%{x|%b %Y}</b><br>"
                            "Forecast: $%{y:,.2f}"
                            "<extra></extra>"
                        )
                    )
                )

                professional_layout(
                    fig_forecast,
                    (
                        f"{selected_segment} Sales Outlook — "
                        f"{horizon} Month(s)"
                    ),
                    560
                )

                fig_forecast.update_yaxes(
                    title="Sales"
                )

                st.plotly_chart(
                    fig_forecast,
                    use_container_width=True
                )

                # --------------------------------------------
                # Forecast table
                # --------------------------------------------

                display_forecast = (
                    selected_forecast.copy()
                )

                display_forecast.columns = [
                    "Forecast Date",
                    "Forecasted Sales"
                ]

                display_forecast[
                    "Forecasted Sales"
                ] = display_forecast[
                    "Forecasted Sales"
                ].round(2)

                st.subheader("Forecast Output")

                st.dataframe(
                    display_forecast,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Forecast Date":
                            st.column_config.DateColumn(
                                "Forecast Date",
                                format="MMM YYYY"
                            ),
                        "Forecasted Sales":
                            st.column_config.NumberColumn(
                                "Forecasted Sales",
                                format="$%.2f"
                            )
                    }
                )

                # --------------------------------------------
                # Growth analysis
                # --------------------------------------------

                if len(selected_forecast) >= 2:

                    first_value = selected_forecast[
                        matching_col
                    ].iloc[0]

                    last_value = selected_forecast[
                        matching_col
                    ].iloc[-1]

                    if first_value != 0:
                        growth_rate = (
                            (last_value - first_value)
                            / abs(first_value)
                        ) * 100

                        if growth_rate >= 0:
                            growth_html = f"""
                            <div class="success-card">
                                <b>Forecast direction:</b>
                                {selected_segment} is projected to
                                increase by approximately
                                <b>{growth_rate:.2f}%</b> from the
                                first to the final selected forecast
                                month.
                            </div>
                            """
                        else:
                            growth_html = f"""
                            <div class="warning-card">
                                <b>Forecast direction:</b>
                                {selected_segment} is projected to
                                change by approximately
                                <b>{growth_rate:.2f}%</b> from the
                                first to the final selected forecast
                                month.
                            </div>
                            """

                        st.markdown(
                            growth_html,
                            unsafe_allow_html=True
                        )

            else:
                st.warning(
                    f"No forecast column was found for "
                    f"'{selected_segment}' in "
                    f"segment_forecasts.csv."
                )

        else:
            st.warning(
                "No date column was found in "
                "segment_forecasts.csv."
            )

    else:
        st.error(
            "segment_forecasts.csv was not found "
            "inside the charts folder."
        )

    # --------------------------------------------------------
    # Saved model comparison charts
    # --------------------------------------------------------

    st.markdown("---")
    st.subheader("Model Diagnostics and Saved Analysis")

    with st.expander(
        "View saved forecasting charts",
        expanded=False
    ):

        tab1, tab2, tab3 = st.tabs(
            [
                "XGBoost",
                "Prophet",
                "SARIMA"
            ]
        )

        with tab1:
            xgb_image = find_image_by_keywords(
                ["xgboost"]
            )

            if not display_saved_image(
                xgb_image,
                "XGBoost: Actual vs Predicted Sales"
            ):
                st.info(
                    "XGBoost chart image not found."
                )

        with tab2:
            prophet_image = find_image_by_keywords(
                ["prophet"]
            )

            if not display_saved_image(
                prophet_image,
                "Prophet: Actual vs Forecasted Sales"
            ):
                st.info(
                    "Prophet chart image not found."
                )

        with tab3:
            sarima_image = find_image_by_keywords(
                ["sarima"]
            )

            if not display_saved_image(
                sarima_image,
                "SARIMA: Actual vs Forecasted Sales"
            ):
                st.info(
                    "SARIMA chart image not found."
                )

    st.markdown(
        """
        <div class="warning-card">
            <b>Methodology note:</b>
            The segment-level forecast values displayed above are
            read from <code>charts/segment_forecasts.csv</code>.
            The XGBoost MAE and RMSE are overall model evaluation
            metrics. The dashboard keeps these two results separate
            to avoid overstating segment-level model accuracy.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE 3 — ANOMALY REPORT
# ============================================================

elif page == "Anomaly Report":

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">
                Anomaly Report
            </div>
            <div class="hero-subtitle">
                Detect unusual sales movements that may indicate
                promotions, demand surges, stock shortages or
                seasonal slowdowns.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Method selection
    # --------------------------------------------------------

    anomaly_method = st.selectbox(
        "Anomaly Detection Method",
        [
            "Isolation Forest",
            "Z-Score",
            "Common Anomalies"
        ]
    )

    if anomaly_method == "Isolation Forest":
        selected_anomaly_df = isolation_anomalies

    elif anomaly_method == "Z-Score":
        selected_anomaly_df = zscore_anomalies

    else:
        selected_anomaly_df = common_anomalies

    # --------------------------------------------------------
    # KPI summary
    # --------------------------------------------------------

    anomaly_count = (
        len(selected_anomaly_df)
        if selected_anomaly_df is not None
        else 0
    )

    common_count = (
        len(common_anomalies)
        if common_anomalies is not None
        else 0
    )

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        "Selected Method",
        anomaly_method
    )

    kpi2.metric(
        "Detected Anomalies",
        anomaly_count
    )

    kpi3.metric(
        "Common to Both Methods",
        common_count
    )

    st.markdown("---")

    # --------------------------------------------------------
    # Required anomaly chart
    # --------------------------------------------------------

    st.subheader("Anomaly Visualization")

    if anomaly_method == "Isolation Forest":

        anomaly_image = (
            find_image_by_keywords(
                ["isolation", "anomal"]
            )
            or find_image_by_keywords(
                ["isolation"]
            )
        )

    elif anomaly_method == "Z-Score":

        anomaly_image = (
            find_image_by_keywords(
                ["z", "score", "anomal"]
            )
            or find_image_by_keywords(
                ["z_score"]
            )
        )

    else:
        anomaly_image = None

    # For common anomalies, build an interactive chart
    if (
        anomaly_method == "Common Anomalies"
        and selected_anomaly_df is not None
    ):

        anomaly_date_col = find_column(
            selected_anomaly_df,
            ["Order Date", "Order_Date", "Date"]
        )

        anomaly_sales_col = find_column(
            selected_anomaly_df,
            ["Sales"]
        )

        if anomaly_date_col and anomaly_sales_col:

            temp_anomaly = selected_anomaly_df.copy()

            temp_anomaly[
                anomaly_date_col
            ] = pd.to_datetime(
                temp_anomaly[anomaly_date_col],
                errors="coerce"
            )

            weekly_sales = (
                df
                .dropna(subset=[DATE_COL])
                .set_index(DATE_COL)
                .resample("W")[SALES_COL]
                .sum()
                .reset_index()
            )

            fig_common = go.Figure()

            fig_common.add_trace(
                go.Scatter(
                    x=weekly_sales[DATE_COL],
                    y=weekly_sales[SALES_COL],
                    mode="lines",
                    name="Weekly Sales",
                    line=dict(
                        color=COLORS["blue"],
                        width=2
                    )
                )
            )

            fig_common.add_trace(
                go.Scatter(
                    x=temp_anomaly[anomaly_date_col],
                    y=temp_anomaly[anomaly_sales_col],
                    mode="markers",
                    name="Common Anomalies",
                    marker=dict(
                        color=COLORS["red"],
                        size=13,
                        symbol="diamond"
                    )
                )
            )

            professional_layout(
                fig_common,
                "Anomalies Confirmed by Both Methods",
                560
            )

            fig_common.update_yaxes(
                title="Weekly Sales"
            )

            st.plotly_chart(
                fig_common,
                use_container_width=True
            )

    else:

        if not display_saved_image(
            anomaly_image,
            f"Weekly Sales Anomalies using {anomaly_method}"
        ):
            st.info(
                "Matching saved anomaly image was not found. "
                "The anomaly table is still available below."
            )

    # --------------------------------------------------------
    # Required anomaly table
    # --------------------------------------------------------

    st.subheader("Detected Anomaly Dates and Sales Values")

    if (
        selected_anomaly_df is not None
        and not selected_anomaly_df.empty
    ):

        table_df = selected_anomaly_df.copy()

        table_date_col = find_column(
            table_df,
            ["Order Date", "Order_Date", "Date"]
        )

        table_sales_col = find_column(
            table_df,
            ["Sales"]
        )

        if table_date_col:
            table_df[table_date_col] = pd.to_datetime(
                table_df[table_date_col],
                errors="coerce"
            )

        preferred_columns = []

        if table_date_col:
            preferred_columns.append(table_date_col)

        if table_sales_col:
            preferred_columns.append(table_sales_col)

        explanation_col = find_column(
            table_df,
            [
                "Possible Explanation",
                "Explanation"
            ]
        )

        if explanation_col:
            preferred_columns.append(explanation_col)

        z_col = find_column(
            table_df,
            ["Z_Score", "Z Score", "Z-Score"]
        )

        if z_col:
            preferred_columns.append(z_col)

        if preferred_columns:
            table_df = table_df[
                preferred_columns
            ]

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning(
            "No anomaly CSV data is available for "
            "the selected method."
        )

    # --------------------------------------------------------
    # Comparison interpretation
    # --------------------------------------------------------

    st.markdown("---")
    st.subheader("Method Comparison")

    st.markdown(
        """
        <div class="insight-card">
            <b>What the comparison tells us:</b><br>
            Z-Score and Isolation Forest do not flag exactly the
            same observations. Z-Score focuses on values that are
            statistically far from the overall mean, while Isolation
            Forest detects observations that are unusual relative to
            the broader data pattern. The overlap between the methods
            therefore represents higher-confidence anomalies, while
            disagreements indicate method-specific sensitivity.
        </div>
        """,
        unsafe_allow_html=True
    )

    if common_anomalies is not None:

        st.markdown(
            f"""
            <div class="success-card">
                <b>High-confidence overlap:</b>
                Your analysis identified
                <b>{len(common_anomalies)}</b> anomalies that were
                flagged by both methods. These dates deserve priority
                investigation because two independent detection
                approaches agreed that the sales behaviour was unusual.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGE 4 — PRODUCT DEMAND SEGMENTS
# ============================================================

elif page == "Product Demand Segments":

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">
                Product Demand Segments
            </div>
            <div class="hero-subtitle">
                K-Means clustering groups sub-categories with similar
                sales, growth, volatility and order-value behaviour.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Cluster summary
    # --------------------------------------------------------

    st.subheader("Demand Segmentation Overview")

    if product_clusters is not None:

        cluster_col = find_column(
            product_clusters,
            ["Cluster"]
        )

        subcat_col = find_column(
            product_clusters,
            [
                "Sub-Category",
                "Sub_Category",
                "SubCategory"
            ]
        )

        if cluster_col:

            unique_clusters = (
                product_clusters[cluster_col]
                .dropna()
                .nunique()
            )

            segment_kpi1, segment_kpi2, segment_kpi3 = st.columns(3)

            segment_kpi1.metric(
                "Demand Clusters",
                unique_clusters
            )

            segment_kpi2.metric(
                "Products Segmented",
                len(product_clusters)
            )

            if subcat_col:
                segment_kpi3.metric(
                    "Sub-Categories",
                    product_clusters[
                        subcat_col
                    ].nunique()
                )
            else:
                segment_kpi3.metric(
                    "Records",
                    len(product_clusters)
                )

    # --------------------------------------------------------
    # Required cluster chart
    # --------------------------------------------------------

    st.markdown("---")
    st.subheader("K-Means Cluster Visualization")

    cluster_image = (
        find_image_by_keywords(
            ["product", "demand", "segment"]
        )
        or find_image_by_keywords(
            ["kmeans", "pca"]
        )
        or find_image_by_keywords(
            ["cluster"]
        )
    )

    if not display_saved_image(
        cluster_image,
        "Product Demand Segments using K-Means and PCA"
    ):

        # Try dynamic PCA columns from CSV
        if product_clusters is not None:

            pca1_col = find_column(
                product_clusters,
                ["PCA1", "PCA 1"]
            )

            pca2_col = find_column(
                product_clusters,
                ["PCA2", "PCA 2"]
            )

            cluster_col = find_column(
                product_clusters,
                ["Cluster"]
            )

            if pca1_col and pca2_col and cluster_col:

                dynamic_cluster_df = (
                    product_clusters.copy()
                )

                dynamic_cluster_df[
                    cluster_col
                ] = dynamic_cluster_df[
                    cluster_col
                ].astype(str)

                fig_cluster = px.scatter(
                    dynamic_cluster_df,
                    x=pca1_col,
                    y=pca2_col,
                    color=cluster_col,
                    color_discrete_sequence=[
                        COLORS["blue"],
                        COLORS["orange"],
                        COLORS["green"],
                        COLORS["red"]
                    ]
                )

                professional_layout(
                    fig_cluster,
                    "Product Demand Segments using K-Means and PCA",
                    560
                )

                st.plotly_chart(
                    fig_cluster,
                    use_container_width=True
                )

            else:
                st.warning(
                    "Cluster chart image and PCA columns "
                    "were not found."
                )

    # --------------------------------------------------------
    # Required sub-category → cluster table
    # --------------------------------------------------------

    st.subheader("Sub-Category to Demand Cluster Mapping")

    if (
        product_clusters is not None
        and not product_clusters.empty
    ):

        cluster_col = find_column(
            product_clusters,
            ["Cluster"]
        )

        subcat_col = find_column(
            product_clusters,
            [
                "Sub-Category",
                "Sub_Category",
                "SubCategory"
            ]
        )

        if subcat_col and cluster_col:

            mapping_df = (
                product_clusters[
                    [subcat_col, cluster_col]
                ]
                .drop_duplicates()
                .sort_values(
                    [cluster_col, subcat_col]
                )
                .copy()
            )

            mapping_df.columns = [
                "Sub-Category",
                "Demand Cluster"
            ]

            st.dataframe(
                mapping_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning(
                "The product cluster CSV does not contain both "
                "Sub-Category and Cluster columns."
            )

            st.dataframe(
                product_clusters,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.error(
            "product_clusters.csv was not found "
            "inside the charts folder."
        )

    # --------------------------------------------------------
    # Cluster characteristics
    # --------------------------------------------------------

    st.markdown("---")
    st.subheader("Cluster Characteristics")

    features_source = None

    if product_clusters is not None:
        required_feature_candidates = [
            "Total_Sales",
            "Growth_Rate",
            "Sales_Volatility",
            "Average_Order_Value"
        ]

        available_count = sum(
            find_column(
                product_clusters,
                [candidate]
            ) is not None
            for candidate in required_feature_candidates
        )

        if available_count >= 2:
            features_source = product_clusters

    if features_source is None and product_features is not None:
        features_source = product_features

    if features_source is not None:

        feature_cluster_col = find_column(
            features_source,
            ["Cluster"]
        )

        feature_candidates = [
            "Total_Sales",
            "Growth_Rate",
            "Sales_Volatility",
            "Average_Order_Value"
        ]

        available_features = [
            find_column(
                features_source,
                [feature]
            )
            for feature in feature_candidates
        ]

        available_features = [
            feature
            for feature in available_features
            if feature is not None
        ]

        if feature_cluster_col and available_features:

            cluster_summary = (
                features_source
                .groupby(feature_cluster_col)[
                    available_features
                ]
                .mean()
                .round(2)
            )

            st.dataframe(
                cluster_summary,
                use_container_width=True
            )

    # --------------------------------------------------------
    # Business stocking strategy
    # Based on your actual cluster summary shown earlier
    # --------------------------------------------------------

    st.subheader("Recommended Stocking Strategy")

    strategy_col1, strategy_col2 = st.columns(2)

    with strategy_col1:

        st.markdown(
            """
            <div class="success-card">
                <b>Cluster 2 — High Sales Volume</b><br>
                Highest average total sales in the cluster summary.
                Maintain strong base inventory, frequent replenishment
                and supplier continuity because stockouts could create
                significant lost revenue.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="insight-card">
                <b>Cluster 0 — Premium / High-Value Demand</b><br>
                Strong sales with the highest average order value and
                substantial volatility. Use selective safety stock,
                tighter monitoring and value-based replenishment rather
                than simply maximizing unit inventory.
            </div>
            """,
            unsafe_allow_html=True
        )

    with strategy_col2:

        st.markdown(
            """
            <div class="warning-card">
                <b>Cluster 3 — Rapid Growth Segment</b><br>
                Highest growth rate in the cluster summary. Increase
                stock progressively, shorten forecast review cycles and
                monitor whether growth persists before committing to
                excessive long-term inventory.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-card">
                <b>Cluster 1 — Lower-Intensity Stable Demand</b><br>
                Lower total sales, lower volatility and lower average
                order value. Use lean inventory, periodic replenishment
                and avoid unnecessary safety-stock accumulation.
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # Elbow method diagnostic
    # --------------------------------------------------------

    with st.expander(
        "View clustering diagnostics",
        expanded=False
    ):

        elbow_image = find_image_by_keywords(
            ["elbow"]
        )

        if not display_saved_image(
            elbow_image,
            "Elbow Method for Optimal Number of Clusters"
        ):
            st.info(
                "Elbow-method chart image not found."
            )

        st.markdown(
            """
            The elbow curve shows a substantial reduction in inertia
            up to approximately **K = 4**, after which improvements
            become smaller. This supports the four-cluster solution
            used for product demand segmentation.
            """
        )


# ============================================================
# 9. GLOBAL FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Sales Forecasting & Demand Intelligence System | "
    "Retail Decision Support | "
    "Forecasting • Anomaly Detection • Demand Segmentation"
)