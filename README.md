# NHS 111 Call Demand Forecasting

This project forecasts daily NHS 111 call demand in England using historical call data, flu activity, weather data and calendar information.

## Project Aim

The aim is to test whether machine learning models can forecast daily NHS 111 call demand and identify which factors contribute most to the predictions.

## Data Sources

The project uses publicly available data from the following sources:

- **NHS 111 data**  
  NHS England Integrated Urgent Care Aggregate Data Collection  
  https://www.england.nhs.uk/statistics/statistical-work-areas/iucadc-new-from-april-2021/integrated-urgent-care-aggregate-data-collection-iucadc-inc-nhs111-statistics-apr-2026-mar-2027/

- **Flu data**  
  UK Health Security Agency national flu surveillance reports  
  https://www.gov.uk/government/statistics/national-flu-and-covid-19-surveillance-reports-2025-to-2026-season

- **Weather data**  
  Met Office HadCET daily temperature data  
  https://www.metoffice.gov.uk/hadobs/hadcet/data/download.html

  CEDA archive  
  https://catalogue.ceda.ac.uk/uuid/31819552d6764b58871507bc20f6b198/

- **Bank holiday data**  
  UK Government Bank Holidays API  
  https://www.api.gov.uk/gds/bank-holidays/

## Data Licence

The datasets used in this project are publicly available.

- NHS England data is available under the Open Government Licence.
- UKHSA data is available under the Open Government Licence.
- UK Government bank holiday data is available under the Open Government Licence.
- HadCET data is publicly accessible through the CEDA archive and its use is covered by the Open Government Licence v3.0.
  
## Models

The following models were tested:

- Seasonal Naive
- SARIMAX
- Prophet
- XGBoost
- LightGBM
- CatBoost

## Evaluation

Model performance was compared using:

- MAE
- RMSE
- R²
- MASE
- RMSSE
- WAPE

## Forecasting Approach

The project uses chronological training and testing for one day ahead forecasting.

The final model is evaluated on a held out test period.

## Streamlit App

A simple Streamlit app is included to view the daily forecast, reported calls, forecast error and expected forecast range.

## How to Run

Open the notebook in Google Colab and run the cells in order.
Make sure the dataset is downloaded and stored in your google drive with the same name if not it won't run.

The Streamlit app can be launched from the final section of the notebook.

## Author

Mofe Beatrice Eno  
