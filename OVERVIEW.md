### Problem + Solution Design

Say you want to make money and mitigate your risk by trading certain commodities. First, you want to know: will prices be in the future? But a price prediction is not a decision, so next we ask: given these expected prices, what should we do?

So we have two models: one forecasting, the next using the forecasts to make purchase and sale decisions.

TODO add diagram


### Assumptions and Strategies

A few assumptions and strategies guide feature selection, forecasting, and agent training:
- Commodities prices are subject to soft upper bounds (above which consumers of copper must find substitutes or cease operation) and soft lower bounds (below which producers can't afford to continue operating)
- 


### Data Selection




### Exploratory Data Analysis


### Forecasting


### Market Simulation + Agent Operation

Each simulated period is divided into a small number of timesteps.  At each timestep, features based on realtime prices are presented at a particular price chosen from range of the day's actual values.  (Other features are presented a static values at each timestep in the period.) For traded commodities, the agent may decide to buy, sell (if any lots are owned), or do nothing with respect to each traded commodity at the prices presented.
