import pandas as pd
from extract import load_sales

# In vadilation we will report
# Check for bads    

# Negative quantities
# Negative prices
# Missing values
# Duplicate IDs
# Invalid types



def validate_df(fileData: pd.DataFrame):
    # transaction_id,product,category,quantity,price

    # Missing Coloumns
    missing_values = {}
    for index, row in fileData.iterrows():
        # Find missing coloumns
        if pd.isna(row["product"]):
            if "product" in missing_values.keys():
                missing_values["product"].append(index)
                continue
            missing_values["product"] = [index]

        if pd.isna(row["category"]):
            if "category" in missing_values.keys():
                missing_values["category"].append(index)
                continue
            missing_values["category"] = [index]

        if pd.isna(row["quantity"]):
            if "quantity" in missing_values.keys():
                missing_values["quantity"].append(index)
                continue
            missing_values["quantity"] = [index]

        if pd.isna(row["price"]):
            if "price" in missing_values.keys():
                missing_values["price"].append(index)
                continue
            missing_values["price"] = [index]

    print(missing_values)
df = load_sales()
validate_df(df)



