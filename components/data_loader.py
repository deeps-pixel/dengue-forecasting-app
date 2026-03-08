import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import streamlit as st
import pickle


# Global Constants
SRI_LANKA_POPULATION = {
    'Western': 6149000,
    'Central': 2766000,
    'Southern': 2654000,
    'Northern': 1143000,
    'Eastern': 1729000,
    'North Western': 2551000,
    'North central': 1377000,
    'Uva': 1376000,
    'Sabaragamuwa': 2058000
}

# Load the dataset once
@st.cache_data  # caches the dataframe so it's not reloaded every rerun
def load_dengue_data(file_path="dengue_data_with_weather_data.csv"):
    df_raw = pd.read_csv(file_path)
    return df_raw

def preprocess_data(df_raw):
    """
    Performs data cleaning and feature engineering as required for the analysis.
    """
    # Create a copy to avoid SettingWithCopyWarning
    df_clean = df_raw.copy()
    df_clean.dropna(inplace=True)

    # Ensure correct types as required by the analysis
    df_clean['District'] = df_clean['District'].astype('category')
    df_clean['Province'] = df_clean['Province'].astype('category')
    df_clean['Month'] = df_clean['Month'].astype(int)
    df_clean['Year'] = df_clean['Year'].astype(int)
    
    # Add Population Data (per Province) for model offset
    df_clean['Population'] = df_clean['Province'].map(SRI_LANKA_POPULATION).astype(float)
    
    return df_clean

@st.cache_resource
def run_regression_analysis(df_clean):
    """
    Performs Poisson and Negative Binomial regression analysis as defined in New_Analysis.ipynb
    """    
    # Preprocess the data
    df = df_clean.copy()
    
    # 3. Simple Poisson Model (Weather Features only)
    poisson_model = smf.glm(
        formula="Cases ~ Temp_avg + Precipitation_avg + Humidity_avg + Elevation",
        data=df,
        family=sm.families.Poisson()
    ).fit()
    
    # 4. Strong Negative Binomial Model (with District fixed effects and Population offset)
    # Using np.log of population as offset for exposure
    nb_model = smf.glm(
        formula="Cases ~ Temp_avg + Precipitation_avg + Humidity_avg + Elevation + C(District)",
        data=df,
        family=sm.families.NegativeBinomial(),
        offset=np.log(df['Population'])
    ).fit()
    
    # 5. Extract Incident Rate Ratios (IRR)
    irr = np.exp(nb_model.params)
    
    # 6. Generate Predictions (Include offset to get counts)
    df['Predicted_Cases'] = nb_model.predict(df, offset=np.log(df['Population']))
    
    # 7. Compile Summary Metrics
    metrics = {
        'mean_cases': df['Cases'].mean(),
        'var_cases': df['Cases'].var(),
        'dispersion_ratio': df['Cases'].var() / (df['Cases'].mean() + 1e-9),
        'poisson_dispersion': poisson_model.deviance / (poisson_model.df_resid + 1e-9),
        'nb_dispersion': nb_model.deviance / (nb_model.df_resid + 1e-9)
    }
    
    return {
        'df': df,
        'poisson_model': poisson_model,
        'nb_model': nb_model,
        'irr': irr,
        'metrics': metrics
    }



@st.cache_data
def run_risk_classification(df):
    """
    Classification of geographic areas into low-, medium-, and high-risk dengue zones
    as defined in Objective1.ipynb
    """
    # Preprocess the data
    df_ready = preprocess_data(df)
    
    # 1. District monthly average cases calculation
    district_monthly_avg_cases = (
        df_ready.groupby(['District', 'Year'], observed=True)['Cases']
          .mean()
          .reset_index())

    # 2. Overall average dengue cases per district
    district_yearly_avg_cases = (
        district_monthly_avg_cases
        .groupby('District', observed=True)['Cases']
        .mean()
        .reset_index())

    # 3. Add Province mapping
    district_province_map = df_ready[['District', 'Province']].drop_duplicates()
    district_year_cases_with_province = pd.merge(
        district_yearly_avg_cases,
        district_province_map,
        on='District',
        how='left'
    )

    # 4. Total average cases per province
    province_total_cases = (
        district_year_cases_with_province
        .groupby('Province', observed=True)['Cases']
        .sum()
        .reset_index(name='total_cases'))

    # 5. Map Population from constant and calculate Incidence
    province_total_cases['Population'] = province_total_cases['Province'].map(SRI_LANKA_POPULATION).astype(float)
    
    province_total_cases['incidence_per_100k'] = (
        province_total_cases['total_cases'] /
        province_total_cases['Population']
    ) * 100000

    # 6. Determine risk levels using quantiles
    low_threshold = province_total_cases['incidence_per_100k'].quantile(0.33)
    high_threshold = province_total_cases['incidence_per_100k'].quantile(0.66)

    def classify_risk(incidence):
        if incidence <= low_threshold:
            return 'Low Risk'
        elif incidence <= high_threshold:
            return 'Medium Risk'
        else:
            return 'High Risk'

    province_total_cases['risk_level'] = (
        province_total_cases['incidence_per_100k']
        .apply(classify_risk)
    )
    
    return {
        'province_risk': province_total_cases,
        'thresholds': (low_threshold, high_threshold)
    }
