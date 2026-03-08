# Dengue Risk Monitoring and Prediction Application

Welcome to the **Dengue Risk Monitoring and Prediction App**, a comprehensive, interactive data tool designed to analyze and predict Dengue incidence trends across districts in Sri Lanka. It combines interactive data exploration, complex statistical modeling, and predictive simulations based on climatic and environmental factors.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)

## Features

- **Data Explorer**: An interactive data viewer and charting tool to explore the relationship between historical Dengue cases and climatic variables (temperature, rainfall, humidity).
- **Simulator**: A prediction module allowing users to input specific climatic data (through interactive sliders) for any district and instantly obtain predicted Dengue case counts and risk classifications.
- **Statistical Analysis**: The statistical foundation of the application, featuring three detailed sub-modules to explore and understand Dengue risk:
  - **Regression Model**: Deep dive into the mathematical relationship between climatic elements and Dengue using Negative Binomial Regression modeling. Displays detailed parameter estimates, incident rate ratios (IRR), equations, and overall model performance metrics.
  - **Risk Classification**: Geographic heat maps and spatial visualizations mapping the Dengue risk level (Low, Moderate, High) across Sri Lanka based on simulated or historical data.
  - **Climate Insights**: Dedicated exploratory analyses focusing on long-term weather trends and how sudden climatic shifts impact Dengue outbreaks.

## Project Structure

The project has been organized into a robust Streamlit multi-page structure:

```text
├── app.py                            # Main entry point of the app
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git configuration
├── assets/                           # Static assets like images/logos and maps
├── components/                       # Reusable functional components
│   ├── data_loader.py                # Handles data ingestion and model processing
│   ├── ui_elements.py                # Reusable UI cards and widgets
│   ├── theme.py                      # Consistent aesthetic styling rules
│   └── header.py / sidebar.py        # Centralized UI navigation components
├── pages/                            # Individual viewable pages of the application
│   ├── home.py                       # Project landing page
│   ├── data_explorer.py              # Visualizations of climate/disease relationships
│   ├── simulator.py                  # The predictive simulation engine
│   ├── statistical_analysis.py       # Gateway to the three statistical modules
│   ├── regression_model.py           # Deep statistical insights (Models & IRR)
│   ├── risk_classification.py        # Map-based risk visualizations
│   └── climate_insights.py           # Climate trend analysis
└── dengue_data_with_weather_data.csv # The core dataset powering the models
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/deeps-pixel/dengue-forecasting-app.git
cd dengue-forecasting-app
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```

Activate the environment:
- On Windows: `venv\Scripts\activate`
- On Mac/Linux: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

To start the local Streamlit server and launch the web interface, run the following command from the root directory:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

## Technologies Used
- Frontend & UI: [Streamlit](https://streamlit.io/)
- Data Manipulation: Pandas, NumPy
- Statistical Modeling: Statsmodels (Poisson & Negative Binomial Regressions)
- Visualizations: Plotly

---
*Disclaimer: This tool is for educational/analytical purposes and is built upon historical models.*
