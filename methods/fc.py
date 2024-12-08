import pandas as pd
import numpy as np
from skforecast.sarimax import Sarimax

def sliding_window_arima_predictions(
    df : pd.DataFrame,
    target_name: str,
    pdq : tuple = (1,1,1),  # p autoregression lags, d differences, q moving average
    window_size : int = 12,) -> pd.DataFrame:

    target_pred_name = target_name + '_PRED'

    model = Sarimax(order = pdq)

    # Add a column to the dataframe for the prediction
    df[target_pred_name] = np.nan

    for pred_step in range(window_size, len(df)-1):
        training_window_start_step = pred_step-window_size

        # Fit the model on the most recent window
        window_df = df[[target_name]].iloc[training_window_start_step:pred_step,:]
        model.fit(y = window_df[target_name])

        # Predict and record a prediction for the next timestep
        pred = model.predict(steps=1)
        df.at[pred_step, target_pred_name] = pred.iloc[0]

    return df


def add_fc_eval_columns(
        df : pd.DataFrame,
        pred_feature : str) -> pd.DataFrame:

    df = df
    # Calculate prediction error, error ratio, and absolute error
    df[pred_feature+'_ERRVAL'] = df[pred_feature+''] - df[pred_feature+'_PRED']
    df[pred_feature+'_ERRRAT'] = df[pred_feature+'_ERRVAL'] / df[pred_feature+'']
    df[pred_feature+'_ERRABS'] = np.abs(df[pred_feature+'_ERRVAL'])

    # Calculate delta and predicted delta (since previous trading day)
    df[pred_feature+'_DELTA'] = df[pred_feature+''] - df[pred_feature+''].shift(1)
    df[pred_feature+'_DELTA_PRED'] = df[pred_feature+'_PRED'] - df[pred_feature+''].shift(1)

    # Calculate sign of delta and predicted delta
    df[pred_feature+'_DELTA_SIGN'] = np.sign(df[pred_feature+'_DELTA'])
    df[pred_feature+'_DELTA_SIGN_PRED'] = np.sign(df[pred_feature+'_DELTA_PRED'])

    # Calculate error value, absolute value, and product of signs of deltas
    df[pred_feature+'_DELTA_ERRVAL'] = df[pred_feature+'_DELTA'] - df[pred_feature+'_DELTA_PRED']
    df[pred_feature+'_DELTA_ERRABS'] = np.abs(df[pred_feature+'_DELTA_ERRVAL'])
    df[pred_feature+'_DELTA_SIGN_PRODUCT'] = df[pred_feature+'_DELTA_SIGN'] * df[pred_feature+'_DELTA_SIGN_PRED']

    return df