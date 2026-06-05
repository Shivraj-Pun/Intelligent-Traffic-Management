# 🚦 Intelligent Traffic Management

A smart traffic congestion prediction and route planning system built with **R (XGBoost)** for machine learning and **Python (Streamlit)** for the interactive web interface, complemented by an HTML/CSS dashboard.

## Overview

Traffic congestion is one of the major challenges in urban transportation systems. This project leverages Machine Learning techniques to forecast traffic congestion using historical traffic data and presents predictions through an interactive dashboard.

The system uses XGBoost for congestion prediction, an R Plumber REST API for serving forecasts, and a Streamlit dashboard with Folium maps for visualization.

## Features

- **Congestion Prediction** — XGBoost regression model trained on traffic data with engineered features (rush hour flags, cyclic hour encoding, weekend indicators)
- **Smart Route Planning** — Interactive map with real-time route rendering via OSRM, geocoding via Geopy, and congestion-aware travel time estimates
- **Traffic Dashboard** — Standalone HTML/CSS dashboard for traffic data visualization
- **REST API** — R Plumber API exposing prediction and EDA endpoints for the Streamlit frontend
- **Scalable Architecture** — Designed for future smart-city integration

## Tech Stack

| Layer | Technology |
|---|---|
| ML Model | R, XGBoost, caret, dplyr |
| API | R Plumber |
| Frontend | Python, Streamlit, Folium, Geopy |
| Dashboard | HTML, CSS |
| Routing | OSRM (Open Source Routing Machine) |
| Data Processing | Pandas, NumPy |

## Project Structure

```
├── Traffic.R               # Main R script — data prep, model training, evaluation, interactive CLI
├── traffic_model.R          # R model training module (used by the API)
├── traffic_model_api.R      # R Plumber API — /predict and /eda endpoints
├── streamlit_app.py         # Streamlit UI — route mapping + congestion display
├── traffic_route.py         # Extended Streamlit UI — OSRM routing + EDA charts
└── dashboard/
    ├── index.html           # Standalone traffic dashboard
    └── index.css            # Dashboard styles
```

## Machine Learning Pipeline

### Feature Engineering

Traffic-related features were generated to improve predictive performance:
- Cyclic hour transformations (sin/cos encoding)
- Rush hour indicators (8–10 AM, 5–7 PM)
- Weekend flags
- Day-of-week numeric encoding

### Model Training

The congestion forecasting model was trained using XGBoost, a gradient boosting framework known for high predictive performance on structured datasets. The model is trained on 80% of the data with early stopping.

### Evaluation

Performance was evaluated using regression metrics:
- **R² Score > 0.85**
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

## Getting Started

### Prerequisites

- **R** (≥ 4.0) with packages: `dplyr`, `caret`, `xgboost`, `plumber`
- **Python** (≥ 3.10) with packages: `streamlit`, `pandas`, `requests`, `folium`, `geopy`, `streamlit-folium`, `polyline`, `seaborn`, `matplotlib`

### Clone Repository

```bash
git clone https://github.com/Shivraj-Pun/Intelligent-Traffic-Management.git
cd Intelligent-Traffic-Management
```

### Run the R Prediction API

```bash
Rscript -e "library(plumber); pr('traffic_model_api.R') %>% pr_run(port=8000)"
```

### Run the Streamlit App

```bash
streamlit run streamlit_app.py
# or
streamlit run traffic_route.py
```

### View the Dashboard

Open `dashboard/index.html` in your browser.

## How It Works

1. **Data Preparation** — Traffic data is loaded from CSV and enriched with features: day-of-week encoding, rush hour flag, weekend flag, and cyclic hour transformations (sin/cos)
2. **Model Training** — An XGBoost gradient boosting model is trained on 80% of the data with early stopping, predicting congestion percentage
3. **API Layer** — The trained model is served via a Plumber REST API at `localhost:8000`
4. **Frontend** — Streamlit apps consume the API, display routes on Folium maps, and show congestion predictions with color-coded status indicators

## Future Improvements

- Deep Learning based forecasting models
- Live traffic sensor integration
- Real-time streaming pipelines
- Smart signal optimization
- Reinforcement Learning based traffic control
- Cloud deployment using AWS

## Applications

- Smart City Infrastructure
- Urban Traffic Planning
- Congestion Monitoring
- Route Optimization
- Transportation Analytics

## Author

**Shivraj Pun**

- LinkedIn: https://www.linkedin.com/in/shivraj-pun
- GitHub: https://github.com/Shivraj-Pun

## License

This project is for educational purposes.
