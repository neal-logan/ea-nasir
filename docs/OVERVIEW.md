## Ea-Nasir

### Problem + Solution Outline

Say you want to make money  trading in futures for certain commodities. First, you want to know: what are the prices and how will they change? But price predictions are not decisions, so next we must ask: given these expected changes in price, what should we do?

So we need two models: one for forecasting, the next using the forecasts to make purchase and sale decisions.

##### Trading Commodities Futures

Commodity futures contracts can be purchased and sold similarly to equities like stocks or ETFs.  However, more in line with stock options, commodity futures contracts expire in a particular month.  At expiration, the contract must be settled.  Depending on the type of contract, this can mean a cash settlement for the value of the underlying commodity--or it can mean physical delivery.  Typically, traders liquidate or offset their contracts prior to expiration (particularly if the contract is for physical delivery) so they don't have to come up with 1000 barrels of crude oil or find space in the garage for 500 metric tons of iron ore.

By convention, most trading volume involves contracts for only a few certain time periods.  For example, traded copper futures contracts are almost always for March, May, July, September, or December delivery.

[More information on trading commodities futures](https://www.cmegroup.com/education/courses/introduction-to-futures/understanding-futures-expiration-contract-roll.html)

##### Assumptions and Simplifications

- Purchases and sales by our agent are small enough that their effects on prices and the overall economy can be ignored.
- Contracts are automatically liquidated on the last day of trading before expiration.  This means we don't have to consider delivery and can provide our agents with a clear number of days until expiration.
- Contracts can be traded no more than a year before expiration.  This limits the number of predictions we're trying to make for a particular commodity at any given time. (Irrelevant right now because simplified data are being used.)

##### Solution Diagram

TODO add diagram

### Datasets

[Appendix: Datasets](DATA.md)

### Preprocessing


##### Dates and Rows

To make next-day price predictions and current-day purchase/sale decisions, we must have a row for each day that is a trading day for any target contract.

Datasets providing commodity contract prices already include a row for each of that contract's trading days and for no other days.  If there are differences between commodities/contracts in which days are trading days, rows will be added to all commodity datasets so that there are rows in all such datasets for each day that is a trading day for any commodity.  So for target commodities, all features in added rows will be set to NaN.

Datasets providing features such as consumer sentiment and inflation rates, include rows for only one day each month, or in some cases even less frequenly.  Still other datasets might include rows for non-trading days.  This pipeline will handle all such data by adding a row for each day that is a trading day for any commodity.  For non-commodity datasets, the most recent information for each feature will be used to impute feature values on added rows.

#####

See 

### Exploratory Data Analysis


### Forecasting


### Simulation & Decisioning

Each simulated period is divided into a small number of timesteps.  At each timestep, features based on realtime prices are presented at a particular price chosen from range of the day's actual values.  (Other features are presented a static values at each timestep in the period.) For traded commodities, the agent may decide to buy, sell (if any lots are owned), or do nothing with respect to each traded commodity at the prices presented.
