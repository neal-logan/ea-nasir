def sliding_window_sarimax_predictions(
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