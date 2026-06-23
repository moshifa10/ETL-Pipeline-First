import pandas as pd
from config.extensions import SessionLocal, Base, engine
from pathlib import Path
from models.sales import Sale
from models.invalid_transaction import InvaliTransactions


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



    if check_file_exists("reports", "invalid_records.csv"):
        save_invalid = {}

        invalid = pd.read_csv("reports/invalid_records.csv")
        for index, row in invalid.iterrows():
            save_invalid[int(row['transaction_id'])] = row['description']


        path = "data/sales.csv"
        df = pd.read_csv(path)


        for index, row in df.iterrows():
            
            if int(row['transaction_id']) in save_invalid.keys():
                id, product, category, quantity, price, description = None, None, None, None, None, None

                id = row['transaction_id']
                description = save_invalid[id]
                if not pd.isna(row['product']):
                    product = row['product']
                if not pd.isna(row['category']):
                    category = row['category']
                if not pd.isna(row['quantity']):
                    quantity = row['quantity']
                if not pd.isna(row['price']):
                    price = row['price']


                add_transactions(transaction_id=id, 
                                description=description,
                                product=product,
                                category=category,
                                quantity=quantity,
                                price=price,
                                total=total,
                                )
                

        for index, row in df.iterrows():
            t_id = int(row['transaction_id'])
            
            if t_id in save_invalid.keys():
                kwargs_to_pass = {
                    'transaction_id': row['transaction_id'],
                    'description': save_invalid[t_id],
                }
                
                optional_fields = ['product', 'category', 'quantity', 'price']
                for field in optional_fields:
                    if pd.notna(row[field]): 
                        kwargs_to_pass[field] = row[field]
                        
                add_transactions(**kwargs_to_pass)
                
        print("Processed invalid transactions.")

    else:
        print("The file of invalid transactions is not existing")


def add_transactions(**kwags):
    valid_transactions = ["transaction_id", "product", "category", "quantity", "price", "total"]


    if sorted(kwags.keys()) == sorted( valid_transactions):
    
        data = session.query(Sale).filter(kwags.get('transaction_id') == Sale.transaction_id).first()
        if data:
            print("The transaction id exist")
            return
        sale = Sale(
            transaction_id=kwags.get('transaction_id'), 
            product=kwags.get('product'),
            category=kwags.get('category'),
            quantity=kwags.get('quantity'),
            price=kwags.get('price'),
            total_sale=kwags.get('total')
        )

        session.add(sale)
        session.commit()

    else:

        data = session.query(InvaliTransactions).filter(InvaliTransactions.transaction_id == kwags.get('transaction_id') ).first()
        if data:
            print("The transaction id exist")
            return
        sale = InvaliTransactions(
            transaction_id=kwags.get('transaction_id'), 
            product=kwags.get('product'),
            category=kwags.get('category'),
            quantity=kwags.get('quantity'),
            price=kwags.get('price'),
            description=kwags.get('description')
        )

        session.add(sale)
        session.commit()


load()