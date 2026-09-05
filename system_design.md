# System Design

## High Level Architecture

The system follows this flow:

NHS 111 data  
↓  
Data quality checks and cleaning  
↓  
England daily aggregation  
↓  
Merge weather, influenza and bank holiday data  
↓  
Leakage safe feature engineering  
↓  
Chronological validation and model comparison  
↓  
Final CatBoost model  
↓  
Prediction interval  
↓  
Streamlit forecasting interface

## Low Level Design

### Data Preparation

The NHS 111 files are combined and checked for missing values, duplicate reporting keys, negative values, zero values and partial reporting.

Daily NHS 111 call demand is aggregated across England.

Weather, influenza and bank holiday data are prepared separately and merged by date.

### Feature Engineering

The model uses past demand, calendar effects, holiday features, lagged temperature and lagged influenza information.

Only information available before the forecast date is used.

### Model Development

The project compares a seasonal naive baseline, SARIMAX, Prophet, XGBoost, LightGBM and CatBoost.

Chronological walk forward validation is used for model development.

Feature screening and hyperparameter tuning use training period data only.

### Final Forecasting System

Tuned CatBoost was selected as the final model.

The final system produces one day ahead forecasts for total NHS 111 call demand across England and provides an empirical 90% prediction interval.

The Streamlit application displays the forecast, actual reported demand, absolute error and prediction interval for held out evaluation dates.
