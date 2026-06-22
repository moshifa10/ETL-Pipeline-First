import pandas as pd


def get_valid_transaction(file_name: pd.DataFrame) -> list[int]:
    return file_name["transaction_id"].to_list()


