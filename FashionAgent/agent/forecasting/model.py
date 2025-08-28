from prophet import Prophet
import pandas as pd


class DemandModel:
    def __init__(self, horizon: int = 28):
        self.horizon = horizon


    def fit_predict(self, df: pd.DataFrame) -> pd.DataFrame:
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=self.horizon)
        forecast = m.predict(future)
        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]