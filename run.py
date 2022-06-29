import datetime
import re
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


def display_stock_data():
    """
    function to display all the stock of the house.
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
    can be either Food or Item.
    """
    def __init__(self, name, amount, days_per):
        self.name = name
        self.amount = amount
        self.days_per = days_per
        self.date_added = str(datetime.datetime.now())

    def add_product(self):
        """
        add product data to google sheet.
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
    inherits all variables and adds expiry variable.
    """
    def __init__(self, name, amount, days_per, expiry_date):
        super().__init__(name, amount, days_per)
        self.expiry_date = expiry_date


def make_product():
    """
    Creates instance of Product or Food class and adds
    it to google sheet database.
    """
    food_or_item = ""
    name = ""
    amount = ""
    days_per_item = ""

    while food_or_item != "F" and food_or_item != "I":
        # check if answer if F or I
        print("Do you want to add food or an item(F/I)?")
        food_or_item = input().upper()
    print("What is the name of your product?")
    name = input()

    while not amount.isdigit():
        # check if amount is digit
        print("How many items does your product contain?")
        amount = input()

    while not days_per_item.isdigit():
        # check if days per item is digit
        print("How many days does 1 item last?")
        days_per_item = input()

    if food_or_item == "F":
        # if food, ask for date and validate it
        # than create istance of food and add to sheet
        print("When does the product expire (yyyy-mm-dd)?")
        expiry = input()
        date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        while re.fullmatch(date_regex, expiry) is None:
            print("Please enter expiry date in format yyyy-mm-dd:")
            expiry = input()
        food_item = Food(name, int(amount), int(days_per_item), expiry)
        food_item.add_product()
    elif food_or_item == "I":
        # if item, create instance of product and add to sheet
        item_item = Product(name, int(amount), int(days_per_item))
        item_item.add_product()


def main_function():
    """
    main function of the program, ask user to see inventory or add a product.
    """
    print("Do you want to see your inventory ('I') or add a product ('P')?")
    answer = input().upper()
    if answer == "I":
        print(display_stock_data())
    elif answer == "P":
        print("Cool let's add a product!")
        make_product()
    else:
        print("Please enter and 'I' or an 'P'")
        main_function()


main_function()

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
