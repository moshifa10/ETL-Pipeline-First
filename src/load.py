import pandas as pd
from config.extensions import SessionLocal, Base, engine
from pathlib import Path
from models.sales import Sale


session = SessionLocal()

def get_valid_transaction(file_name: pd.DataFrame) -> list[int]:
    return file_name["transaction_id"].to_list()


def check_file_exists(folder: str, file: str) -> bool:
    folder = Path(folder)
    file = file
    path = folder / file
    if not path.is_file():
        return False
    return True

def load():
    
    Base.metadata.create_all(bind=engine)

    if check_file_exists("reports", "valid_transactions.csv"):
        path = "reports/valid_transactions.csv"
        df = pd.read_csv(path)

        for index, row in df.iterrows():

            id = row['transaction_id']
            product = row['product']
            category = row['category']
            quantity = row['quantity']
            price = row['price']
            total = row['total']
            add_transactions(transaction_id=id, 
                             product=product,
                             category=category,
                             quantity=quantity,
                             price=price,
                             total=total
                            )
            
        print("Added all transactions to the database")

    else:
        print("No valid transiction yet so I cant just put things in the database")

def add_transactions(transaction_id: int, product: str, category: str, quantity: int, price: int, total: int):

    sale = Sale(
        transaction_id=transaction_id, 
        product=product,
        category=category,
        quantity=quantity,
        price=price,
        total_sale=total
    )
    session.add(sale)
    session.commit()

load()