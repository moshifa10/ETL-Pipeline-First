import pandas as pd
from config.extensions import SessionLocal
from pathlib import Path


def get_valid_transaction(file_name: pd.DataFrame) -> list[int]:
    return file_name["transaction_id"].to_list()


def load():


    folder = Path("database")

    file = "sales.db"

    path = folder / file

    if path.is_file():
        