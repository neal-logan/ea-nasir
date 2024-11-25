# Ea-Nasir

### Contents

- [Notebook: **Exploratory Data Analysis**](01_eda.ipynb) - notebook that includes initial preprocessing and baseline forecast modeling
- [Notebook: **Forecasting Model Development**](02_forecasting.ipynb) - notebook that will include feature engineering for forecasting, forecasting model evaluation
- [Notebook: **Decisioning Model Development**](03_decisioning.ipynb) - notebook that will include feature engineering for agent training simulations and decision-making, decision model evaluation
- [Appendix: **SETUP**](docs/SETUP.md) - information on setting up your environment to run pieces of the project
- [Appendix: **DATA**](docs/DATA.md) - more detailed information on the specific data used in this project

### Problem + Solution Outline

For this project, we want to try to make money trading copper futures.  For this, we need two sets of models.  The first set of models makes predictions about prices and other information relevant to decisions.  The second set of models use the forecasts to make decisions to buy or sell.

##### Background: Trading Commodities Futures

Commodity futures contracts can be purchased and sold similarly to equities like stocks or ETFs.  However, more in line with stock options, commodity futures contracts expire in a particular month.  At expiration, the contract must be settled.  Depending on the type of contract, this can mean a cash settlement for the value of the underlying commodity--or it can mean physical delivery.  Typically, traders liquidate or offset their contracts prior to expiration (particularly if the contract is for physical delivery) so they don't have to come up with 1000 barrels of crude oil or find space in the garage for 500 metric tons of iron ore.

By convention, most trading volume involves contracts for only certain time periods, this varies by commodity.  By traded volume, copper futures contracts are almost entirely for March, May, July, September, or December delivery.

[More information on trading commodities futures](https://www.cmegroup.com/education/courses/introduction-to-futures/understanding-futures-expiration-contract-roll.html)

##### Assumptions and Simplifications

- Purchases and sales by our agent are small enough that their effects on prices and the overall economy can be ignored.
- Agent will engage in very limited trading strateges - for example, buying right at opening each day.

If spreads of different futures are used in a subsequent verion:
- Contracts automatically liquidated on the last day of trading before expiration, so the prospect of actual delivery need not be considered. 
- Contracts tradable no more than a year before expiration to limit the number of predictions we're trying to make for a particular commodity at any given time.

##### Solution Diagram

TODO add diagram
