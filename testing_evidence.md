# System Testing Evidence

The forecasting system was tested at data, modelling and application stages.

| Test | Expected Result | Outcome |
| --- | --- | --- |
| NHS 111 dates parsed correctly | No missing national dates after preparation | Pass |
| Negative call values | No negative A01 values | Pass |
| Duplicate national dates | No duplicate daily national records | Pass |
| Weather coverage | Weather available across the modelling period | Pass |
| Flu coverage | Flu data available across the modelling period | Pass |
| Target leakage check | Same-day target not included as a feature | Pass |
| Rolling feature leakage check | Rolling demand features use previous values only | Pass |
| Chronological split | Training dates occur before test dates | Pass |
| Same-day weather check | Same-day observed temperature not used for prediction | Pass |
| Same-day flu check | Same-day flu not used for prediction | Pass |
| Model comparison | All models evaluated on the same chronological folds | Pass |
| SARIMAX convergence | Final SARIMAX fit converged | Pass |
| Streamlit date validation | Only valid held-out forecast dates are available | Pass |

## Manual Testing

Manual checks were also carried out by reviewing:

- data quality summaries;
- train and test date ranges;
- model result tables;
- actual versus predicted plots;
- residual diagnostics;
- feature importance results;
- prediction interval coverage;
- the final Streamlit forecasting interface.

The complete notebook contains the code output used as evidence for these tests.
