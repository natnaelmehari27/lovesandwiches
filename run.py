import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# Delete the 3 lines that were used to check the API was working 

def get_sales_data():
    """
    Get sales figure input from the user 
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers, separated by comma")
        print("Example: 10,20,30,40,50,60\n")
        # \n is to make space in the terminal

        data_str = input("Enter your data here: ")
        # the split() to return the broken up values as a list and in the terminal it will remove the commmas
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, coverts all string values into intgers. raises ValueError if strings cannot be converted into int, 
    or if there are not exaclty 6 values
    """
    
    # we call this function inside the get_sales_data fucntion because it is validating the data
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError (
                f"Exaclty 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
            print(f"Invalid data: {e}, please try again. \n")
            return False
    return True
    
def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure substracted from the stock:
    - Positive surplus indicates waste. 
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

# outside of the functions so it can run the functions
def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

main()