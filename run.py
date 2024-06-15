import gspread
from google.oauth2.service_account import Credentials

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
    print("Please enter sales data from the last market")
    print("Data should be six numbers, separated by comma")
    print("Example: 10,20,30,40,50,60\n")
    # \n is to make space in the terminal

    data_str = input("Enter your data here: ")
    # the split() to return the broken up values as a list and in the terminal it will remove the commmas
    sales_data = data_str.split(",")
    print(sales_data)
    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try, coverts all string values into intgers. raises ValueError if strings cannot be converted into int, 
    or if there are not exaclty 6 values
    """
    # we call this function inside the get_sales_data fucntion because it is validating the data
    try:
        if len(values) != 6:
            raise ValueError (
                f"Exaclty 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
            print(f"Invalid data: {e}, please try again. \n")




# outside of the functions so it can run the functions
get_sales_data()