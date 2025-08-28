import pandas as pd


def build_training_frame(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={"date": "ds", "units": "y"})
    df = df[["ds", "y"]].dropna()
    df["ds"] = pd.to_datetime(df["ds"])
    df = df.sort_values("ds")
    return df