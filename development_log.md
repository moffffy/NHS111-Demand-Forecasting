# Development Log

This file summarises the main stages of the NHS 111 forecasting project.

## Development Stages

1. Prepared and combined NHS 111 call activity data.

2. Added data quality checks for missing values, duplicates, zero values and partial reporting.

3. Aggregated NHS 111 activity to daily England level.

4. Prepared and merged weather, influenza and bank holiday data.

5. Created leakage safe forecasting features using past demand and lagged external variables.

6. Added chronological train, validation and test periods.

7. Compared Seasonal Naive, SARIMAX, Prophet, XGBoost, LightGBM and CatBoost.

8. Added training only feature screening and Optuna hyperparameter tuning.

9. Added residual diagnostics, SHAP, permutation importance and sensitivity analysis.

10. Added empirical 90% prediction intervals.

11. Developed the final Streamlit forecasting interface.

12. Final selected model: Tuned CatBoost.
