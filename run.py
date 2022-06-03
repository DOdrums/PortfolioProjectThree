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
        self.date_added = str(datetime.datetime.now())

    def add_product(self):
        """
        add product data to google sheet
        """
        data = []
        for value in self.__dict__.values():
            data.append(value)
        if len(data) == 4:
            item.append_row(data)
        elif len(data) == 5:
            food.append_row(data)
        else:
            print("Your list doesn't seem to have the right amount of items!")


class Food(Product):
    """
    Food class that subclasses the product class
    inherits all variables and adds expiry variable
    """
    def __init__(self, name, amount, days_per, expiry_date):
        super().__init__(name, amount, days_per)
        self.expiry_date = expiry_date


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


# main_function()

# broodje = Product("broodje", 3, 2)
# print(broodje.__dict__)
# broodje.add_product()

# soepje = Food("soepie", 2, 4, "06/10/2022")
# print(soepje.__dict__)
# soepje.add_product()

# 1. for delete function, show names with row number and
# let user enter number to delete data
# 2. make seperate function for calculating days left/items
# left (called by get stock data function)
# 3. for calculating the days left, data added needs to be converted back
# to datetime object
