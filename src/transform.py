import pandas as pd
from pathlib import Path


def get_invalid_transaction(file_data: pd.DataFrame) -> list[int]:
    return file_data['transaction_id'].tolist()

def transform(file_data: pd.DataFrame):

    invalid_transaction_file = pd.read_csv("reports/invalid_records.csv")
    invalid_transaction = get_invalid_transaction(invalid_transaction_file)
    print(invalid_transaction)

    revenue_by_product(file_data, invalid_transaction)


def revenue_by_product(file_data: pd.DataFrame , invalid_transactions: list[int]=None):
    transactions = {}
    data = {
        "product" : [],
        "quantity": [],
        "price": [],
        "total": []
    }


    for index, row in file_data.iterrows():
        if not int(row['transaction_id']) in invalid_transactions:
            if not row['product'] in transactions.keys():

                transactions[row['product']] = {
                    "quantity": int(row['quantity']),
                    "price": int(row['price'])
                }
                continue
            transactions[row['product']]['quantity'] += int(row['quantity'])                    
            transactions[row['product']]['price'] += int(row['price'])
    
    
    for product in transactions:
        quantity, price = transactions[product]['quantity'], transactions[product]['price']
        total = quantity * price

        data['product'].append(product)
        data['quantity'].append(quantity)
        data['price'].append(price)
        data['total'].append(total)

    print(transactions)

    print(data)
    write_product_revenue(data)

    # write to a file 

    
def write_product_revenue(data: dict[list]):

    directory = Path("reports")
   
    file_path = directory / "revenue_by_product.csv"

    if file_path.is_file() and file_path.stat().st_size > 0:
        original = pd.read_csv(file_path)
        df = pd.DataFrame(data)
        original.update(df)
    
    else:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        



# df = pd.read_csv("reports/invalid_records.csv")
# print(get_invalid_transaction(df))

df = pd.read_csv("data/sales.csv")
transform(df)

