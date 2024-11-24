


    # {Date->ForecastFeatures}
    # Includes a mix of raw features and transformed features
    features = {} 

    # {Date + TimeOfDay -> Forecasts}
    # Forecasts are made AT OPENING and include: 
    # Current day high, low, close (same day regression model):
    # Next day prices for high, low, open, and close
    # Confidence classifications for these price predictions (high means we think it'll be within a few %)
    forecasts = {}