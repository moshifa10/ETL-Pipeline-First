from src.extract import load_sales
from src.validate import validate
from src.transform import transform
from src.load import load

import logging



def main():
    print("Hey")

    logging.basicConfig(level=logging.DEBUG, 
                        filename="logs/pipeline.log", 
                        filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s"
                        )

    logging.info("STARTING THE OPERATION")
    print("Hey")
    df = load_sales()

    validate(df)
    transform(df)
    load()



if __name__ == "__main__":
    main()





















# Be mindful of off quantity, price e.g Negative price or quantinty
# Same transaction id transactions
# Product can be none And I have to account that
# Category Can be None but since if we have product we can actually take all products we have and category and autofill that with similar category same as product
# Missing Values


# Off data types for every category , check if the datatype is a valid datatype for every coloumn 

# Off pricing 


# Detect and report
    # Example
# Records Read: 10
# Valid Records: 7
# Invalid Records: 3
        # or
# invalid_records
# Store:
# transaction_id	reason
# 8	Negative Quantity
# 9	Negative Price
# 15	Invalid Quantity Type



# logger = logging.getLogger(__name__)
# logger.info("Test custome logger")

# # Levels
# logging.debug("Debugging")
# logging.info("Information")
# logging.warning("Warning")
# logging.error("Error")
# logging.critical("Critical")



