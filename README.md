#  Russian Apple Prices Analysis (2013–2020)

## Overview
This project takes raw apple price data from Russian cities (2013–2020) and transforms it into **business-grade storytelling**.  
Instead of just running models, the focus is on explaining **why the numbers matter** for retailers, consumers, and strategic planning.

The analysis covers:
- Data wrangling (wide → long format for time-series analysis)
- Exploratory Data Analysis (EDA) with a **business-first narrative**
- Seasonality, regional price differences, and volatility
- A lightweight **baseline forecast** to establish a planning benchmark
- An interactive **Streamlit dashboard** to explore the data dynamically

---

## Key Highlights
- **Data wrangling:** reshaped messy wide-format data into a clean long-format dataset.
- **Business insights:** Moscow consistently shows a **15–16% premium** over other cities.
- **Macro event:** prices jumped ~**28% YoY** in Moscow between 2014 and 2015, reflecting the ruble crisis.
- **Seasonality:** peak in **July (~100 rub/kg)**, trough in **November (~80 rub/kg)**.
- **Regional opportunities:** Krasnodar and Kaliningrad remain structurally cheaper than Moscow/Ekaterimburgo.
- **Volatility:** Saint Petersburg has the highest price volatility, signaling riskier margins.

---

## Visual Storytelling
The notebook includes visualizations such as:
-  Trends over time by city  
-  Seasonality patterns across months  
-  Heatmap of city × year average prices  
-  Moscow premium vs. other cities (annual %)  
-  Each chart is paired with a **business interpretation**, simulating how an analyst would present results to non-technical stakeholders.

---

## Forecasting
A **seasonal naïve forecast** was built as a baseline:  
- Each month of 2020 is predicted using the same month from 2019.  
- Provides a quick planning benchmark before introducing more complex models.  
- Sets the stage for ARIMA/Prophet/ML models to demonstrate added value.

---

## Business Impact
- Price premiums and seasonality directly affect retailer margins and consumer pricing.  
- Recommendations:  
  - **Tailored pricing in Moscow** to reflect the persistent premium.  
  - **Contract negotiations around July peaks** to hedge seasonal cost increases.  
  - **Flexible replenishment in high-volatility cities** (e.g., Saint Petersburg).  
  - **Sourcing from structurally cheaper regions** like Krasnodar to improve margins.  

---

## Interactive Dashboard
An interactive version of the analysis is available via **Streamlit**.  
Recruiters and stakeholders can explore the data themselves: filter cities, select year ranges, and view KPIs.

### Run the app locally
```bash
pip install -r requirements.txt
streamlit run app.py
