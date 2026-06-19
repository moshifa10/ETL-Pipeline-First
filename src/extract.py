import pandas as pd

def load_sales() -> pd.DataFrame:
    return pd.read_csv("data/sales.csv")