import pandas as pd
import logging

LOGGER = logging.getLogger(__name__)

def load_sales() -> pd.DataFrame:
    LOGGER.info("Extracting CSV")
    return pd.read_csv("data/sales.csv")