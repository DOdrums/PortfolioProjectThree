import datetime
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
SHEET = GSPREAD_CLIENT.open("smart_house_inventory")
food = SHEET.worksheet("food")
item = SHEET.worksheet("item")


def get_stock_data():
    """
    function to display all the stock of the house
    """
    new_line = '\n'

    data_food_raw = food.get_all_values()
    data_food = ""
    data_item_raw = item.get_all_values()
    data_item = ""

    for product in data_food_raw:
        for data in product:
            data_food += data + (30 - len(data)) * " "
        data_food += f"{new_line}"

    for product in data_item_raw:
        for data in product:
            data_item += data + (30 - len(data)) * " "
        data_item += f"{new_line}"

    return (
        f"These are all the items you have in your house:{2 * new_line}"
        f"{data_item}{new_line}"
        f"This is all the food you have in your house:{2 * new_line}"
        f"{data_food}"
    )


class Product:
    """
    class to initialise a product
    can be either Food or Item
    """
    def __init__(self, name, amount, days_per):
        self.name = name
        self.amount = amount
        self.days_per = days_per
        self.date_added = datetime.datetime.now()

    def add_item(self):
        """
        add item data to google sheet
        """
        data = [self.name, self.amount, self.days_per, str(self.date_added)]
        item.append_row(data)


def main_function():
    """
    main function of the program, ask user to see inventory or add a product.
    """
    print("Do you want to see your inventory ('I') or add a product ('P')?")
    answer = input()
    if answer == "I":
        print(get_stock_data())
    elif answer == "P":
        print("Cool let's add a product!")


main_function()


# 1. for delete function, show names with row number and
# let user enter number to delete data
# 2. make seperate function for calculating days left/items
# left (called by get stock data function)
# 3. for calculating the days left, data added needs to be converted back
# to datetime object
