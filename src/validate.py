import pandas as pd
from extract import load_sales

# In vadilation we will report
# Check for bads    

# Negative quantities
# Negative prices
# Missing values
# Duplicate IDs
# Invalid types



def validate(fileData: pd.DataFrame):
    # transaction_id,product,category,quantity,price

    empty_columns = missing_columns(file_data=fileData)
    prices_negatives = negative_prices(file_data=fileData)
    quantities_negatives = negative_quantites(file_data=fileData)

    print(empty_columns)
    print()
    print(f"Negatives Prices: \n{prices_negatives}")
    print()
    print(f"Quantities Negatives: \n{quantities_negatives}")

def negative_quantites(file_data: pd.DataFrame) -> list[int]:   
    quantities = []
    strings = []
    for index, row in file_data.iterrows():
            quantity = row["quantity"] 
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    quantities.append(row["transaction_id"])
            except ValueError:
                strings.append(row["transaction_id"])
    return quantities, strings

def negative_prices(file_data: pd.DataFrame):
    prices = []
    strings = []
    for index, row in file_data.iterrows():
            price = row["price"] 
            try:
                price = int(price)
                if price <= 0:
                    prices.append(row["transaction_id"])
            except ValueError:
                strings.append(row["transaction_id"])
    return prices,strings

def missing_columns(file_data: pd.DataFrame) -> dict:
    # Missing Coloumns
    missing_values = {}
    for index, row in file_data.iterrows():
        # Find missing coloumns
        if pd.isna(row["product"]):
            if "product" in missing_values.keys():
                missing_values["product"].append([row["transaction_id"]])
                continue
            missing_values["product"] = [row["transaction_id"]]

        if pd.isna(row["category"]):
            if "category" in missing_values.keys():
                missing_values["category"].append([row["transaction_id"]])
                continue
            missing_values["category"] = [row["transaction_id"]]

        if pd.isna(row["quantity"]):
            if "quantity" in missing_values.keys():
                missing_values["quantity"].append([row["transaction_id"]])
                continue
            missing_values["quantity"] = [[row["transaction_id"]]]

        if pd.isna(row["price"]):
            if "price" in missing_values.keys():
                missing_values["price"].append([row["transaction_id"]])
                continue
            missing_values["price"] = [[row["transaction_id"]]]

    return missing_values

def duplicates(file_data: pd.DataFrame) -> list[tuple[int]]:
    all_transactions = [int(row["transaction_id"]) for index, row in file_data.iterrows()]
    counting = {num: all_transactions.count(num) for num in all_transactions}
    duplicates_ = [(row, counting[row]) for row in counting if counting[row] > 1]
    return duplicates_
df = load_sales()
# validate(df)


duplicates(file_data=df)



