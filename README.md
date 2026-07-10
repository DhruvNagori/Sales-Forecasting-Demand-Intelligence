# Sales Forecasting & Demand Intelligence System

An end-to-end data science project for analyzing retail sales, forecasting short-term demand, detecting unusual sales patterns, and segmenting products based on demand behavior.

The project uses the **Superstore Sales dataset** and combines time series forecasting, machine learning, anomaly detection, clustering, and an interactive Streamlit dashboard to support inventory and supply-chain planning.

## Project Objectives

- Analyze historical sales trends and seasonality
- Forecast future sales using multiple approaches
- Compare models using MAE, RMSE, and MAPE
- Detect unusual weekly sales spikes and drops
- Forecast demand by product category and region
- Segment products based on demand behavior
- Present results through an interactive dashboard

## Forecasting Models

Three different forecasting approaches were implemented:

- **SARIMA** — Statistical time series forecasting
- **Prophet** — Trend and seasonality-based forecasting
- **XGBoost** — Machine learning using lag and rolling features

### Model Performance

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| **XGBoost** | **18,710.45** | **20,852.57** | **19.12%** |
| Prophet | 20,296.01 | 22,487.47 | 21.89% |
| SARIMA | 21,060.32 | 22,019.99 | 22.38% |

**XGBoost achieved the lowest error on the selected holdout period and was used as the best-performing model for short-term forecasting analysis.**

## Additional Analysis

### Anomaly Detection
Weekly sales anomalies were identified using:
- Isolation Forest
- Rolling Z-Score detection

The results from both methods were compared to identify higher-confidence unusual sales events.

### Product Demand Segmentation
Product sub-categories were grouped using:
- Total Sales
- Year-over-Year Growth Rate
- Sales Volatility
- Average Order Value

The segmentation workflow uses **K-Means Clustering**, the **Elbow Method**, and **PCA visualization** to support different stocking strategies across demand groups.

## Streamlit Dashboard

The interactive dashboard contains four pages:

1. **Sales Overview** — yearly sales, monthly trends, region and category filters
2. **Forecast Explorer** — 1 to 3 month forecasts by category or region
3. **Anomaly Report** — detected anomaly dates and sales values
4. **Product Demand Segments** — cluster visualization and stocking strategies

## Project Structure

```text
SalesForecasting_DhruvNagori/
├── analysis.ipynb
├── app.py
├── train.csv
├── requirements.txt
├── Summary.pdf
├── README.md
└── charts/
```

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

## Technologies Used

`Python` `Pandas` `NumPy` `Matplotlib` `Plotly` `Scikit-learn` `Statsmodels` `Prophet` `XGBoost` `Streamlit`

## Key Limitation

The forecasts are based mainly on historical sales patterns and do not directly include external factors such as promotions, pricing changes, holidays, stockouts, competitor activity, or economic conditions. Forecasts should therefore be treated as decision-support estimates rather than guaranteed outcomes.

## Author

**Dhruv Nagori**  
Data Science  
Dr. B. R. Ambedkar National Institute of Technology, Jalandhar