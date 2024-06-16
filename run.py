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

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet 
    update the relevant worsheet with the data provided.
    """
    print(f"Updating {worksheet} worksheet...")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


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
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting the last
    5 entries for each sandwiches and returns the data as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
      
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type adding 10%
    """
    print("calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data

# outside of the functions so it can run the functions
def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches Data Automation")
main()
