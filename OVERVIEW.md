## Ea-Nasir

### Problem + Solution Design

Say you want to make money and mitigate your risk by trading certain commodities. First, you want to know: will prices be in the future? But a price prediction is not a decision, so next we ask: given these expected prices, what should we do?

So we have two models: one forecasting, the next using the forecasts to make purchase and sale decisions.

TODO add diagram


### Assumptions and Strategies

A few assumptions and strategies guide feature selection, forecasting, simulation, and agent training:
- Commodities prices are subject to soft upper bounds (above which consumers of copper must find substitutes or cease operation) and soft lower bounds (below which producers can't afford to continue operating)
- Purchases and sales by our agent are small enough that their effects on prices and the overall economy can be ignored.
-

### Datasets

##### Selection Considerations
Almost anything might help predict commodities prices and a colossal range of potentially-relevant datasets are available.  Based on the assumptions and strategies outlined [here](README.md), the following criteria for selecting data are used:
* Must be consistently availabe to inform the model at decision-time
* Must be publicly available

Key types of data identified:
* Price data for target commodities and closely-related commodities
* Economic indicators

##### Selected Datasets

See [Appendix: Datasets](DATA.md)

### Preprocessing


##### Dates and Rows

The purpose of this modeling effort is to predict prices and make real-time decisions on trading days for each selected commodity, so we must have rows for each day that is a trading day for any selected commodity.

Datasets providing commodity prices include a row for each of that commodity's trading days and for no other days.  If there are differences between commodities in which days are trading days, rows will be added to all commodity datasets so that there are rows in all such datasets for each day that is a trading day for any commodity.  For commodities, all features in added rows will be set to NaN.

Datasets providing features such as consumer sentiment and inflation rates, include rows for only one day each month, or in some cases even less frequenly.  Still other datasets might include rows for non-trading days.  This pipeline will handle all such data by adding a row for each day that is a trading day for any commodity.  For non-commodity datasets, the most recent information for each feature will be used to impute feature values on added rows.

#####

See 

### Exploratory Data Analysis


### Forecasting


### Simulation & Decisioning

Each simulated period is divided into a small number of timesteps.  At each timestep, features based on realtime prices are presented at a particular price chosen from range of the day's actual values.  (Other features are presented a static values at each timestep in the period.) For traded commodities, the agent may decide to buy, sell (if any lots are owned), or do nothing with respect to each traded commodity at the prices presented.
