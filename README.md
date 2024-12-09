# Ea-Nasir: Honest Copper Futures Trader

### Contents

- [Notebook: **Exploratory Data Analysis**](01_eda_data_prep.ipynb) - Covers initial preprocessing (including merging and aligning numerous datasets and engineering a variety of features) and some exploratory data analysis.  Outputs passed along to Forecasting via [data_forecasting](/data_forecasting/) folder.
- [Notebook: **Forecasting Model Development**](02_forecasting.ipynb) - Covers additional feature engineering and forecast modeling.  Outputs including forecasts and other engineered features passed along to Decisioning via [data_decisioning](/data_decisioning/) folder.
- [Notebook: **Decisioning Model Development**](03_decisioning.ipynb) - Covers final feature engineering and agent training/simulations.  No outputs yet.

### Setup

NOTE:  The notebooks will not function without the [methods](/methods/) folder and their respective data folders.  

Clone the git repo:

```bash/cmd
git clone https://github.com/neal-logan/ea-nasir.git
```

Install requirements with pip:

```bash/cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Developed on Windows 10 with Python 3.11.9 - see requirements.txt for all other requirements

### Incomplete Items

- Dockerfile for Jupyter server: Not tested, but might provide an alternative to installation.
- Streamlit: Incomplete

### Problem + Solution Outline

Ea-Nasir wants to make money trading copper futures.  To do this, he uses two sets of models: the first forecasts how prices will change, while the second uses the forecasts to decide how to balance the portfolio between cash and copper futures.

##### Background: Trading Commodities Futures

Commodity futures contracts can be purchased and sold similarly to equities like stocks or ETFs.  However, more in line with stock options, commodity futures contracts expire in a particular month.  At expiration, the contract must be settled.  Depending on the type of contract, this can mean a cash settlement for the value of the underlying commodity--or it can mean physical delivery.  Typically, traders liquidate or offset their contracts prior to expiration (particularly if the contract is for physical delivery) so they don't have to come up with 1000 barrels of crude oil or find space in the garage for 500 metric tons of iron ore.

By convention, most trading volume involves contracts for only certain time periods, this varies by commodity.  By traded volume, copper futures contracts are almost entirely for March, May, July, September, or December delivery.

[More information](https://www.cmegroup.com/education/courses/introduction-to-futures/understanding-futures-expiration-contract-roll.html)

##### Assumptions and Simplifications

- Purchases and sales by our agent are small enough that their effects on prices and the overall economy can be ignored.
- Agent will engage in very limited trading strateges - for example, buying right at opening each day.
- Contracts automatically rolled before expiration, so the prospect of actual delivery need not be considered.

### Data

##### Prediction & Decisioning Target

- [Copper](https://www.cmegroup.com/education/articles-and-reports/copper-financial-futures-faq.html)

More specifically, we will target copper futures opening price.

##### Explored Features and Sources

[**Investing.com**](https://www.investing.com/)
- COPPER: Copper futures
- GOLD: Gold futures
- LUMBER: Lumber futures
- NATGAS: Natural gas futures
- OIL: Crude oil futures
- CORN: Corn futures
- SOY: Soy future
- R2000: Russell 2000 index
- SP500: S&P 500 index
- VIX: Volatility index

[**FRED: Federal Reserve Economic Data**](https://fred.stlouisfed.org/)
- CSENT: US consumer sentiment
- CPI: US consumer price index
- POP: US population
- WAGE: US hourly wages
- HOUSEPRICE: Median US house prices
- HOUSESTARTS:  US housing starts
- UNEMPLOYMENT: US unemployment rate U3

### Models

In the end, 

