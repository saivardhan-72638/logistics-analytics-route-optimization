# Logistics Analytics & Route Optimization

A complete academic Python project for **Strategic Planning and Data Exploration in Logistics**.

## What the project does

The system uses e-commerce order data to:

1. Clean and integrate order, item, customer and review data.
2. Measure logistics KPIs.
3. Explore delivery patterns with charts.
4. Predict delivery duration with regression.
5. Predict late-delivery risk with classification.
6. Group operational regions using K-Means clustering.
7. Demonstrate vehicle-route optimization.
8. Save reproducible outputs for the project report and presentation.

## Dataset

The project follows the schema of the **Brazilian E-Commerce Public Dataset by Olist**. For immediate demonstration, `scripts/generate_sample_data.py` creates synthetic data using the same core column names. This is deliberately labeled synthetic so the results are not presented as real Olist findings.

For the real dataset, place these files in `data/raw/`:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_reviews_dataset.csv`

Additional Olist tables can be added later for seller/product/geolocation analysis.

## Run on Windows

```powershell
cd logistics_analytics_project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m scripts.generate_sample_data
python -m scripts.run_pipeline
```

For real Olist data:

```powershell
python -m scripts.run_pipeline --real-data
```

The current pipeline accepts the same input files for both modes; `--real-data` is kept as an explicit presentation flag.

## Outputs

After a successful run:

- `outputs/reports/kpis.csv`
- `outputs/reports/model_results.json`
- `outputs/reports/state_clusters.csv`
- `outputs/reports/route_optimization.json`
- `outputs/reports/project_summary.json`
- `outputs/figures/*.png`
- `outputs/models/*.joblib`
- `data/processed/delivered_orders.csv`

## Project architecture

```text
Raw CSV data
    ↓
Validation + integration
    ↓
Feature engineering
    ↓
KPI baseline ──→ EDA charts
    ↓
Predictive analytics
 ┌───────────────┬─────────────────┐
 │ Regression    │ Classification  │
 │ delivery days │ late risk       │
 └───────────────┴─────────────────┘
    ↓
Regional clustering
    ↓
Route optimization prototype
    ↓
Business recommendations
```

## Important limitation

The Olist dataset is historical. The route module is a demonstration using geographic distance, not live road traffic. A production system would require road-network travel times, vehicle capacity, delivery windows, live order status and dispatch constraints.

## Academic presentation line

> “Our project converts historical e-commerce logistics data into operational decisions by measuring delivery KPIs, discovering patterns, predicting delivery and late-risk outcomes, segmenting regions, and demonstrating route optimization.”
