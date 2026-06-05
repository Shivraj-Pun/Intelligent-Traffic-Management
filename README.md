# Intelligent-Traffic-Management
# Intelligent Traffic Management

An end-to-end Machine Learning based traffic congestion forecasting system that predicts traffic conditions and provides interactive visualization for traffic analysis.

## Overview

Traffic congestion is one of the major challenges in urban transportation systems. This project leverages Machine Learning techniques to forecast traffic congestion using historical traffic data and presents predictions through an interactive dashboard.

The system uses XGBoost for congestion prediction, an R Plumber REST API for serving forecasts, and a Streamlit dashboard with Folium maps for visualization.

## Features

- Traffic congestion prediction using XGBoost
- Real-time forecasting through REST APIs
- Interactive Streamlit dashboard
- Geospatial visualization using Folium
- Historical traffic trend analysis
- Scalable architecture for future smart-city integration

## Tech Stack

### Machine Learning
- XGBoost
- R
- 
### Frontend & Visualization
- Streamlit
- Folium

### Data Processing
- Pandas
- NumPy

## Machine Learning Pipeline

### Data Preprocessing

- Handling missing values
- Data cleaning
- Feature selection
- Data normalization

### Feature Engineering

Traffic-related features were generated to improve predictive performance, including:

- Traffic volume indicators
- Temporal patterns
- Congestion trends
- Historical observations

### Model Training

The congestion forecasting model was trained using XGBoost, a gradient boosting framework known for high predictive performance on structured datasets.

### Evaluation

Performance was evaluated using regression metrics including:

- R² Score
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

## Results

- Achieved **R² Score > 0.85**
- Successfully forecasted congestion trends
- Enabled real-time prediction serving through APIs

## Installation

### Clone Repository

```bash
git clone https://github.com/Shivraj-Pun/Intelligent-Traffic-Management.git

cd Intelligent-Traffic-Management
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Backend API

```bash
Rscript api.R
```

### Launch Dashboard

```bash
streamlit run app.py
```

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
