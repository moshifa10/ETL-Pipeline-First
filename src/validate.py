import pandas as pd
from src.extract import load_sales
from config.config import GROK
from groq import Groq
from pathlib import Path
import logging

# In vadilation we will report
# Check for bads    

# Negative quantities
# Negative prices
# Missing values
# Duplicate IDs
# Invalid types

# def report_invalid_records()

LOGGER = logging.getLogger(__name__)

def report(all_records: int, failed: int):
    LOGGER.info("Writing reports for valid and invalid with total receipt records.")
    with open(file="reports/report.txt", mode="w") as file:
        file.write(f"Records Read: {all_records}\n")
        file.write(f"Valid Records: {all_records-failed}\n")
        file.write(f"Invalid Records: {failed}\n")

def validate(fileData: pd.DataFrame):
    # transaction_id,product,category,quantity,price
    LOGGER.info("VALIDATING DATA")
    empty_columns = missing_columns(file_data=fileData)
    prices_negatives, unsupported_opperand_price = negative_prices(file_data=fileData)
    quantities_negatives, unsupported_opperand_quantites = negative_quantites(file_data=fileData)
    duplicates_ = duplicates(fileData)
    strange_prices_ = strange_prices(fileData)

    failed_data = calculate_everyFailed_method(empty_columns,
                                               prices_negatives,
                                               unsupported_opperand_price,
                                               quantities_negatives,
                                               unsupported_opperand_quantites,
                                               duplicates_,
                                               strange_prices_
    )
    report(len(fileData), failed_data)

    report_csv(prices_negatives, quantities_negatives, duplicates_, strange_prices_, unsupported_opperand_price, unsupported_opperand_quantites, empty_columns)
    # print(empty_columns)
    # print()
    # print(f"Negatives Prices: \n{prices_negatives}")
    # print()
    # print(f"Quantities Negatives: \n{quantities_negatives}")
    # print()
    # print(f"Duplicates\n{duplicates_}")
    # print()
    # print(f"Strange Prices\n{strange_prices_}")




def report_csv(negative_prices=None, negative_quantitiy=None, dublicates_=None, strange=None, unsupported_opperand_price=None, unsupported_opperand_quantites=None, empty_columns=None):
    # prices

    LOGGER.error("Writing invalid transactions to csv with its reasoning")
    if negative_prices != None:
        for transaction_id in negative_prices:
            write_to_csv(transaction_id, "Negative Price")

    if negative_quantitiy != None:
        for transaction_id in negative_quantitiy:
            write_to_csv(transaction_id, "Negative quantities")

    if dublicates_ != None:
        for transaction_id in dublicates_:
            write_to_csv(transaction_id[0], "Dublicates")

    if strange != None:
        for transaction_id in strange:
            write_to_csv(transaction_id, "We have strange transactions like quantity is bigger than price")

    
    if unsupported_opperand_price != None:
        for  transaction_id in unsupported_opperand_price:
            write_to_csv(transaction_id, "Uknown types like we got alphabets or symbols instead of numbers from price")

    
    if unsupported_opperand_quantites != None:
        for  transaction_id in unsupported_opperand_quantites:
            write_to_csv(transaction_id, "Uknown types like we got alphabets or symbols instead of numbers from quantity")

    if empty_columns != None:
        for value in empty_columns:
            if value == "product":
                for transaction_id in empty_columns[value]:
                    write_to_csv(transaction_id, "Product missing")
            
            elif value == "quantity":
                for transaction_id in empty_columns[value]:
                    write_to_csv(transaction_id, "quantity missing")
            
            elif value == "price":
                for transaction_id in empty_columns[value]:
                    write_to_csv(transaction_id, "Price missing")
    
    
def write_to_csv(transaction_id: int, description: str):
    data = {
        "transaction_id" : [transaction_id],
        "description": [description]
    }

    dir_path = Path("reports")

    file_path = dir_path / "invalid_records.csv"
    # dir_path.mkdir(parents=True, exist_ok=True)
    if not file_path.is_file() or file_path.stat().st_size == 0:

        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

    else:
        df = pd.DataFrame(data)
        original = pd.read_csv(file_path)


        updated_df = pd.concat([original, df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)

        
    


def calculate_everyFailed_method(*args) -> int:
    return  sum([len(i) for i in args])

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

    LOGGER.critical("Finding missing columns")
    # Missing Coloumns
    missing_values = {}

    for index, row in file_data.iterrows():
        # Find missing coloumns
        if pd.isna(row["product"]):
            if "product" in missing_values.keys():
                missing_values["product"].append(row["transaction_id"])
                continue
            missing_values["product"] = [row["transaction_id"]]
            

        if pd.isna(row["category"]):
            if pd.isna(row["product"]):
                if "category" in missing_values.keys():
                    missing_values["category"].append(row["transaction_id"])
                    continue
                missing_values["category"] = [row["transaction_id"]]

            else:
                product_category = get_product_category(row["product"])
                file_data.at[index, "category"] = product_category
                
                df = pd.DataFrame(file_data)
                df.to_csv("data/sales.csv", index=False)


        if pd.isna(row['quantity']):
            if "quantity" in missing_values.keys():
                missing_values["quantity"].append(row["transaction_id"])
                continue
            missing_values["quantity"]= [[row["transaction_id"]]]
        
        if pd.isna(row['price']):
            if "price" in missing_values.keys():
                missing_values["price"].append(row["transaction_id"])
                continue
            missing_values["price"]= [row["transaction_id"]]
    # print(missing_values)
    return missing_values

def duplicates(file_data: pd.DataFrame) -> list[tuple[int]]:
    LOGGER.error("Finding dublicates Transactions")
    all_transactions = [int(row["transaction_id"]) for index, row in file_data.iterrows()]
    counting = {num: all_transactions.count(num) for num in all_transactions}
    duplicates_ = [(row, counting[row]) for row in counting if counting[row] > 1]
    return duplicates_ 

def get_product_category(product_name: str) -> str:
    LOGGER.info("Asking Grok for category that is missing while having the product name")
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
        temperature=0.0,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Product: {product_name}"}
        ]
    )
    
    return response.choices[0].message.content.strip() 


def strange_prices(file_data: pd.DataFrame) -> list:
    LOGGER.critical("Finding Strange prices")
    strange =  []
    for index, row in file_data.iterrows():
        try:
            if int(row["price"]) < 0:
                continue
            if int(row["quantity"]) > int(row["price"]):
                strange.append(row["transaction_id"])
        except ValueError:
            continue

    return strange


# df = load_sales()
# validate(df)


# duplicates(file_data=df)


# print(get_product_category("Chocolate"))
