import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="🍏 Russian Apple Prices — Business Storytelling", layout="wide")

@st.cache_data
def load_data():
    # Try processed file first
    try:
        df = pd.read_csv("russian_apple_prices_long.csv")
    except FileNotFoundError:
        # Fallback: rebuild from raw wide CSV if present
        raw_path = "manzanas (1).csv"
        raw = pd.read_csv(raw_path)
        first_col = raw.columns[0]
        if not first_col.lower().startswith("city"):
            raw = raw.rename(columns={first_col: "city"})
        else:
            raw = raw.rename(columns={first_col: "city"})
        def parse_month_year(s):
            m, y = str(s).split(".")
            return datetime(int(y), int(m), 1)
        value_cols = [c for c in raw.columns if c != "city"]
        df = (raw.melt(id_vars=["city"], value_vars=value_cols, var_name="m_y", value_name="price")
                 .assign(date=lambda d: d["m_y"].astype(str).apply(parse_month_year))
                 .drop(columns=["m_y"])
                 .dropna(subset=["date", "price"])
                 .sort_values(["city", "date"])
                 .reset_index(drop=True))
        df.to_csv("russian_apple_prices_long.csv", index=False)

    # Ensure types / helper cols
    df["date"] = pd.to_datetime(df["date"])
    if "year" not in df.columns:
        df["year"] = df["date"].dt.year
    if "month" not in df.columns:
        df["month"] = df["date"].dt.month
    return df

df = load_data()

st.title("🍏 Russian Apple Prices — Business Storytelling")
st.markdown("""
Turn raw price data into business-grade insights: trends, regional differences, seasonality, volatility,
and Moscow's premium vs. the rest.
""")

# Sidebar controls
st.sidebar.header("Controls")
cities = sorted(df["city"].unique().tolist())
default_cities = cities[:3] if len(cities) >= 3 else cities
sel_cities = st.sidebar.multiselect("Select cities", options=cities, default=default_cities)

min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Year range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

show_seasonality = st.sidebar.checkbox("Show seasonality", value=True)
show_heatmap = st.sidebar.checkbox("Show city × year heatmap", value=True)
show_premium = st.sidebar.checkbox("Show Moscow premium", value=True)
show_volatility = st.sidebar.checkbox("Show volatility by city", value=False)

# Filtered dataset
mask = (df["year"].between(year_range[0], year_range[1])) & (df["city"].isin(sel_cities))
dff = df.loc[mask].copy()

#  KPIs 
col1, col2, col3, col4 = st.columns(4)
overall_avg = df["price"].mean()
sel_avg = dff["price"].mean() if not dff.empty else np.nan
col1.metric("Overall average price", f"{overall_avg:,.2f} rub/kg")
col2.metric("Selected scope avg", f"{sel_avg:,.2f} rub/kg" if not np.isnan(sel_avg) else "—")

mos_name = next((n for n in df["city"].unique() if n.lower().startswith("mosc")), None)
if mos_name is not None:
    mos = df.query("city == @mos_name")["price"].mean()
    rest = df.query("city != @mos_name")["price"].mean()
    premium_overall = (mos / rest - 1) * 100
    col3.metric(f"{mos_name} premium (overall)", f"{premium_overall:,.1f}%")
else:
    col3.metric("Moscow premium", "N/A")

# Peak / trough months (global)
monthly_all = df.groupby("month")["price"].mean()
peak_m = int(monthly_all.idxmax())
trough_m = int(monthly_all.idxmin())
col4.metric("Seasonal peak / trough", f"{peak_m} / {trough_m}")

st.divider()

# Trend by city 
st.subheader("Trend by city (selected)")
if dff.empty:
    st.info("No data for the current selection. Try widening the year range or selecting more cities.")
else:
    fig = plt.figure(figsize=(10,6))
    for city, g in dff.groupby("city"):
        plt.plot(g["date"], g["price"], label=city)
    plt.title("Apple prices over time by city")
    plt.xlabel("Date"); plt.ylabel("Price (rubles/kg)")
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)

# Seasonality 
if show_seasonality:
    st.subheader("Seasonality (average by calendar month)")
    dff2 = dff if not dff.empty else df
    monthly = dff2.groupby("month")["price"].mean().reset_index()
    fig2 = plt.figure(figsize=(8,5))
    plt.plot(monthly["month"], monthly["price"], marker="o")
    plt.title("Seasonality: Average price by month")
    plt.xlabel("Month"); plt.ylabel("Average price (rubles/kg)")
    plt.xticks(range(1,13))
    plt.tight_layout()
    st.pyplot(fig2)

#  Heatmap City × Year 
if show_heatmap:
    st.subheader("City × Year heatmap (average price)")
    dff3 = dff if not dff.empty else df
    annual_city = dff3.groupby(["year","city"])["price"].mean().reset_index()  # 👈 correcto
    if not annual_city.empty:
        pivot_cy = annual_city.pivot(index="city", columns="year", values="price")
        fig3 = plt.figure(figsize=(10,6))
        plt.imshow(pivot_cy, aspect="auto")
        plt.title("Heatmap: City vs Year average price")
        plt.xlabel("Year"); plt.ylabel("City")
        plt.yticks(range(len(pivot_cy.index)), pivot_cy.index)
        plt.xticks(range(len(pivot_cy.columns)), pivot_cy.columns, rotation=45)
        plt.colorbar(label="Average price")
        plt.tight_layout()
        st.pyplot(fig3)
    else:
        st.info("Not enough data to render the heatmap for the current selection.")

