import datetime
import math
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


class Product:
    """
    class to initialise a product
    can be either Food or Item.
    """
    def __init__(self, name, quantity, days_per):
        self.name = name
        self.quantity = quantity
        self.days_per = days_per
        self.date_added = str(datetime.date.today())

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
    def __init__(self, name, quantity, days_per, expiry_date):
        super().__init__(name, quantity, days_per)
        self.expiry_date = expiry_date


def make_product():
    """
    Creates instance of Product or Food class and adds
    it to google sheet database.
    """
    food_or_item = ""
    name = ""
    quantity = ""
    days_per_item = ""

    while food_or_item != "F" and food_or_item != "I":
        # check if answer if F or I
        print("Do you want to add food or an item? Please enter 'F' or 'I':")
        food_or_item = input().upper()
    print(
        "What is the name of your product (max 18 charachters)?\n"
        ".................."
        )
    name = input()

    while not quantity.isdigit():
        # check if quantity is digit
        print(
            "How many items does your product contain?\n"
            "Please enter a whole number"
            )
        quantity = input()

    while not days_per_item.isdigit():
        # check if days per item is digit
        print(
            "How many days does it take to use up 1 item?\n"
            "Please enter a whole number:"
            )
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
        item_item = Food(name, int(quantity), int(days_per_item), expiry)
    elif food_or_item == "I":
        # if item, create instance of product and add to sheet
        item_item = Product(name, int(quantity), int(days_per_item))
        # item_item.add_product()
    print("Add product(Y/N)")
    user_add_y_n = ""
    while user_add_y_n != "Y" or "N":
        user_add_y_n = input().upper()
        if user_add_y_n == "Y":
            item_item.add_product()
            break
        elif user_add_y_n == "N":
            break
        else:
            print("Please enter 'Y' or 'N'")

    print(
        "Hit 'A' to add another product, 'R' to return\n"
        "to the start of the program or 'Q' to exit:"
    )

    user_input = input().upper()
    if user_input == "A":
        make_product()
    elif user_input == "R":
        main_function()
    elif user_input == "Q":
        pass


def delete_product(sheet):
    """
    deletes products from the sheet by row number
    it's possible for user to delete multiple rows at once
    """
    products_to_delete = ""
    is_numbers = False
    while not is_numbers:
        print(
            "Which products do you want to delete? "
            "Please enter the numbers, seperated by comma's "
            "(for example: 2,4,7)"
        )
        products_to_delete = input().split(",")
        is_numbers = all(item.isdigit() for item in products_to_delete)
    products_to_delete = [int(x) for x in products_to_delete]
    products_to_delete.sort(reverse=True)
    for number in products_to_delete:
        if number != 1:
            sheet.delete_rows(number)
    display_stock_data()


def display_stock_data():
    """
    function to display all the stock of the house.
    """
    new_line = '\n'

    data_food_raw = food.get_all_values()
    data_food = ""
    data_item_raw = item.get_all_values()
    data_item = ""
    quantity_and_days = calculate_quantity_left(data_food_raw)
    i = 1

    for product in data_food_raw:
        data_food += f"{i} "
        data_food += product[0] + (19 - len(product[0])) * " " + "|"
        if i > 1:
            data_food += str(
                quantity_and_days[0][0]) + "/" + product[1] + (
                10 - (
                    len(str(product[1])) + len(str(quantity_and_days[0][0])))
                    ) * " " + "|"
            quantity_and_days[0].pop(0)
        else:
            data_food += product[1] + (11 - len(product[1])) * " " + "|"
        for data in range(2, 5):
            data_food += product[data] + (11 - len(product[data])) * " " + "|"
        if i < 2:
            data_food += "Days left"
        else:
            data_food += str(quantity_and_days[1][0])
            quantity_and_days[1].pop(0)
        data_food += f"{new_line}"
        i += 1

    quantity_and_days = calculate_quantity_left(data_item_raw)
    i = 1
    for product in data_item_raw:
        data_item += f"{i} "
        data_item += product[0] + (19 - len(product[0])) * " " + "|"
        if i > 1:
            data_item += str(
                quantity_and_days[0][0]) + "/" + product[1] + (
                10 - (
                    len(str(product[1])) + len(str(quantity_and_days[0][0])))
                    ) * " " + "|"
            quantity_and_days[0].pop(0)
        else:
            data_item += product[1] + (11 - len(product[1])) * " " + "|"
        for data in range(2, 4):
            data_item += product[data] + (11 - len(product[data])) * " " + "|"
        if i < 2:
            data_item += "Days left"
        else:
            data_item += str(quantity_and_days[1][0])
            quantity_and_days[1].pop(0)
        data_item += f"{new_line}"
        i += 1

    print(
        f"{new_line}"
        f"These are all the items you have in your house:{2 * new_line}"
        f"{data_item}{new_line}"
        f"This is all the food you have in your house:{2 * new_line}"
        f"{data_food}{new_line}"
        f"Hit 'D' to delete an item, 'R' to return"
        f" to the start of the program or 'Q' to exit:"
    )

    user_input = input().upper()
    if user_input == "D":
        item_or_food = ""
        print(
            "Do you want to delete a product from the item or food list(I/F)?"
        )
        item_or_food = input().upper()
        if item_or_food == "I":
            delete_product(item)
        elif item_or_food == "F":
            delete_product(food)
    elif user_input == "R":
        main_function()
    elif user_input == "Q":
        pass


def calculate_quantity_left(sheet):
    """
    function to calculate the days left until user
    runs out of a product.
    """
    quantity = []
    days_p_use = []
    date_added = []
    expiry_date = []
    length = len(sheet)
    length_items = len(sheet[0])
    for product in range(1, length):
        quantity.append(sheet[product][1])
        days_p_use.append(sheet[product][2])
        date_added.append(sheet[product][3])
        if length_items > 4:
            expiry_date.append(sheet[product][4])
    current_date = datetime.date.today()
    length -= 1
    new_quantity = []
    days_left = []
    for index in range(length):
        days_spend = current_date - datetime.datetime.strptime(
            date_added[index], "%Y-%m-%d"
            ).date()
        quantity_left = (
            int(quantity[index]) - days_spend.days / int(days_p_use[index])
            )
        if quantity_left < 0:
            quantity_left = 0
        new_quantity.append(math.ceil(quantity_left))
        days = math.ceil(quantity_left) * int(days_p_use[index])
        days_left.append(days)
    quantity_and_days_left = []
    quantity_and_days_left.append(new_quantity)
    quantity_and_days_left.append(days_left)
    return quantity_and_days_left
    # current date - date added = days spend
    # quantity - round(days spend / days per use) = quantity left
    # quantity left * days per use = days left


def main_function():
    """
    main function of the program, asks user to see inventory or add a product.
    """
    print(
        "\nWelcome to your Smart House Inventory!\n\n"
        "With this program, you can track all the products in your house and "
        "fridge,\nand see when you'd have to restock an item! When adding"
        " a product,\nmake sure to enter a realistic 'days per use', so the "
        "Smart House Inventory\ncan calculate when you'll run out of it!\n"
        )
    print(
        "Do you want to see/edit your inventory ('I') or add a product ('P')?"
        )
    answer = input().upper()
    if answer == "I":
        display_stock_data()
    elif answer == "P":
        print("Cool let's add a product!")
        make_product()
    else:
        print("Please enter an 'I' or a 'P'")
        main_function()


main_function()

# 1. make seperate function for calculating days left/items
# left (called by get stock data function)
# 2. for calculating the days left, data added needs to be converted back
# to datetime object
# 3. Add function to edit quantity and expiry date of product
