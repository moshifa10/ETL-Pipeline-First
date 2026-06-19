import pandas as pd
from src.extract import load_sales
from config.config import GROK
from groq import Groq

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
    duplicates_ = duplicates(fileData)
    # Algo that detects quantity is matching price

    print(empty_columns)
    print()
    print(f"Negatives Prices: \n{prices_negatives}")
    print()
    print(f"Quantities Negatives: \n{quantities_negatives}")
    print()
    print(f"Duplicates\n{duplicates_}")

def negative_quantites(file_data: pd.DataFrame) -> list[tuple[int]]:   
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

def negative_prices(file_data: pd.DataFrame) -> list[tuple[int]]:
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
            if pd.isna(row["category"]):
                if "product" in missing_values.keys():
                    missing_values["product"].append([row["transaction_id"]])
                    continue
                missing_values["product"] = [row["transaction_id"]]

        if pd.isna(row["category"]):
            if pd.isna(row["product"]):
                if "category" in missing_values.keys():
                    missing_values["category"].append([row["transaction_id"]])
                    continue
                missing_values["category"] = [row["transaction_id"]]

            else:
                product_category = get_product_category(row["product"])
                file_data.at[index, "category"] = product_category
                
                df = pd.DataFrame(file_data)
                df.to_csv("data/sales.csv")




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

def get_product_category(product_name: str) -> str:
    """Classifies a product into one of the predefined dataset categories."""

    groq_client = Groq(api_key=GROK)

    categories = ["Drinks", "Food", "Dairy", "Snacks", "Household"]

    system_instruction = (
        "You are a strict data classification assistant. "
        "Your task is to look at a product name and return ONLY its category. "
        f"You must pick exactly one category from this list: {', '.join(categories)}. "
        "Do not write full sentences. Do not add punctuation. Return only the category name."
    )

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.0,  # Setting to 0 ensures deterministic, consistent classifications
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Product: {product_name}"}
        ]
    )
    
    return response.choices[0].message.content.strip() 


df = load_sales()
validate(df)


# duplicates(file_data=df)


# print(get_product_category("Chocolate"))
