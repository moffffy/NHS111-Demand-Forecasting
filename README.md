# NHS 111 Daily Call Demand Forecasting

This project forecasts daily NHS 111 call demand across England using time series and machine learning methods.

## Research Question

Can machine learning models using historical call demand, influenza activity, weather conditions and seasonal factors forecast daily NHS 111 call demand in England, and which factors have the greatest influence on demand?

## Data Sources

The project uses data from:

- NHS England NHS 111 call activity data
- UKHSA influenza surveillance data
- Met Office temperature data
- GOV.UK bank holiday data

## Modelling Approach

The project compares:

- Seasonal naive baseline
- SARIMAX
- Prophet
- XGBoost
- LightGBM
- CatBoost

Chronological walk forward validation is used to reduce data leakage.

## Final Model

Selected model: Tuned CatBoost

Held out MAE: 1,928.32 calls

Held out RMSE: 2,991.69 calls

Held out R²: 0.919

## Application

A Streamlit application is included to demonstrate one day ahead NHS 111 demand forecasts for England.

## Repository Contents

The repository contains the final forecasting notebook, model outputs, figures, testing evidence and the Streamlit application.
