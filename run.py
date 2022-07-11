import datetime
import math
import re
import gspread
from google.oauth2.service_account import Credentials

# API code taken from love sandwiches walk through project from Code Institute.
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


class Colors:
    """
    A class with colors to style the text in the terminal
    """
    # code taken from Stackoverflow (see readme)
    hr = '\033[95m'
    bl = '\033[94m'
    cy = '\033[96m'
    gr = '\033[92m'
    wrn = '\033[93m'
    f = '\033[91m'
    end = '\033[0m'
    bld = '\033[1m'
    und = '\033[4m'


class Product:
    """
    Class to initialise a product
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


class Food(Product):
    """
    Food class that subclasses the Product class,
    inherits all variables and adds expiry variable.
    """
    def __init__(self, name, quantity, days_per, expiry_date):
        super().__init__(name, quantity, days_per)
        self.expiry_date = expiry_date


def get_name():
    """
    Function to get name of product from user
    """
    name = "1234567890123456789"
    print(
        "\nWhat is the name of your product (max 18 characters)?\n"
        "..................\n"
    )
    while len(name) > 18:
        # check if name doesn't exceed the max length
        name = input()
        if len(name) > 18:
            print(
                "Please enter a name with a max length of 18 characters:\n"
                "..................\n"
                )
    return name


def get_quantity():
    """
    Function to get quantity of product from user
    """
    quantity = ""
    print("\nHow many items does your product contain?\n")
    while not quantity.isdigit():
        # check if quantity is digit
        print(
            "Please enter a whole number:\n"
            )
        quantity = input()
    return quantity


def get_days_p_use():
    """
    Function to get days per use of product from user
    """
    days_per_item = ""
    print("\nHow many days does it take to use up 1 item of your product?\n")
    while not days_per_item.isdigit():
        # check if days per item is digit
        print(
            "Please enter a whole number:\n"
            )
        days_per_item = input()
    return days_per_item


def get_expiry_date():
    """
    Function to get expiry date of product from user
    """
    print("\nWhen does the product expire (yyyy-mm-dd)?\n")
    expiry = input()
    date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    while re.fullmatch(date_regex, expiry) is None:
        # compare regex to entered date, to see if date is in valid format
        # regex code taken from 'regexland' (see readme)
        print("\nPlease enter expiry date in format yyyy-mm-dd:\n")
        expiry = input()
    return expiry


def make_product():
    """
    Creates instance of Product or Food class and adds
    it to google sheet database.
    """
    food_or_item = ""
    print("\nDo you want to add food or an item (F/I)?\n")
    while food_or_item != "F" and food_or_item != "I":
        # check if answer is F or I
        food_or_item = input().upper()
        if food_or_item != "F" and food_or_item != "I":
            print("\nPlease enter 'F' or 'I':\n")

    name = get_name()
    quantity = get_quantity()
    days_per_item = get_days_p_use()

    if food_or_item == "F":
        # if food, get expiry date and than
        # create instance of food
        expiry = get_expiry_date()
        product = Food(name, int(quantity), int(days_per_item), expiry)
    elif food_or_item == "I":
        # if item, create instance of product
        product = Product(name, int(quantity), int(days_per_item))

    print("\nAdd product (Y/N)?\n")
    user_add_y_n = ""
    while user_add_y_n != "Y" and user_add_y_n != "N":
        # give user the option to add product or not
        user_add_y_n = input().upper()
        if user_add_y_n == "Y":
            product.add_product()
            print("\nProduct added!")
        elif user_add_y_n == "N":
            print("\nProduct not added!")
        else:
            print("\nPlease enter 'Y' or 'N'\n")

    print(
        "\nHit 'A' to add another product, 'R' to return\n"
        "to the start of the program or 'Q' to exit:\n"
    )

    valid_input = ["A", "R", "Q"]
    user_input = ""
    while user_input not in valid_input:
        # give user multiple options after adding product
        user_input = input().upper()
        if user_input == "A":
            make_product()
        elif user_input == "R":
            main_function()
        elif user_input == "Q":
            pass
        else:
            print("\nPlease enter an 'A', 'R' or 'Q'\n")


def edit_product():
    """
    function to edit individual cells in the google sheet
    """
    item_or_food = ""
    sheet = ""
    print(
        "\nDo you want to edit a product from "
        "the food or item list(F/I)?\n"
    )
    while item_or_food != "I" and item_or_food != "F":
        # check if answer is F or I
        item_or_food = input().upper()
        if item_or_food == "I":
            sheet = item
        elif item_or_food == "F":
            sheet = food
        else:
            print("\nPlease enter an 'I' or 'F'\n")

    print("\nWhich product you want to edit?")
    product_number = 0
    while product_number < 1:
        # get product number from user
        print(
            "\nPlease enter the product number as listed in the inventory:\n"
            )
        product_number = int(input())

    valid_input = ["N", "Q", "D"]
    user_input = ""
    print(
        "\nDo you want to edit the name, quantity "
        "or days per use of your product (N/Q/D)?\n"
        )
    while user_input not in valid_input:
        # get answer from user to which value they want to edit
        user_input = input().upper()
        if user_input == "N":
            # get name and update name in google sheet
            print("\nOkay let's update the name!")
            name = get_name()
            name_cell = "A" + str((int(product_number) + 1))
            sheet.update_acell(name_cell, name)
            # code to update cell taken from youtube (see readme)
            print("\nName updated!")
        elif user_input == "Q":
            # get quantity and automatically update date added as well
            # if product is food, ask for and update expiry as well
            print("\nOkay let's update the quantity!")
            quantity = get_quantity()

            if item_or_food == "F":
                print("\nWe should also update the expiry date!")
                expiry = "'" + get_expiry_date()
                expiry_cell = "E" + str((int(product_number) + 1))
                sheet.update_acell(expiry_cell, expiry)

            qt_cell = "B" + str((int(product_number) + 1))
            sheet.update_acell(qt_cell, quantity)
            date_added = "'" + str(datetime.date.today())
            date_cell = "D" + str((int(product_number) + 1))
            sheet.update_acell(date_cell, date_added)
            print("\nQuantity updated!")
        elif user_input == "D":
            # get and update the days per use in google sheet
            print("\nOkay let's update the days per use!")
            days_per_use = get_days_p_use()
            days_cell = "C" + str((int(product_number) + 1))
            sheet.update_acell(days_cell, days_per_use)
            print("\nDays per use updated!")
        else:
            print("\nPlease enter an 'N', 'Q' or 'D'\n")

    display_stock_data()


def delete_product():
    """
    deletes products from the sheet by row number
    it's possible for user to delete multiple rows at once
    """
    item_or_food = ""
    sheet = ""
    print(
        "Do you want to delete a product from "
        "the item or food list(I/F)?\n"
    )
    while item_or_food != "I" and item_or_food != "F":
        # check if answer is F or I
        item_or_food = input().upper()
        if item_or_food == "I":
            sheet = item
        elif item_or_food == "F":
            sheet = food
        else:
            print("Please enter an 'I' or 'F':\n")

    products_to_delete = ""
    is_numbers = False
    print("Which products do you want to delete?")
    while not is_numbers:
        # verify if string entered is filled with digits
        # code taken from datasciencepirachay (see readme)
        print(
            "Please enter the product numbers, separated by comma's\n"
            "and without spaces (for example: 2,4,7)\n"
        )
        products_to_delete = input().split(",")
        is_numbers = all(item.isdigit() for item in products_to_delete)

    products_to_delete = [int(x) for x in products_to_delete]
    # code taken from finxter (see readme)
    products_to_delete.sort(reverse=True)
    for number in products_to_delete:
        # delete (all) product(s), making sure
        # the first column doesn't get deleted
        if number != 0:
            sheet.delete_rows(number + 1)
    print("\nProducts deleted!")
    display_stock_data()


def inventory_explanation():
    """
    prints explanation of inventory to terminal
    """
    new_line = "\n"
    print(
        f"{new_line * 25}{Colors.hr}Your inventory explained!{new_line}"
        f"{Colors.end}"
        f"{new_line}{Colors.cy}Name:{Colors.end}{new_line}"
        f"The name of your product."
        f"{new_line}"
        f"{new_line}{Colors.cy}Quantity:{Colors.end}{new_line}"
        f"The quantity of your product. Fill this in any"
        f"{new_line}way you'd like! For example: 2 bags of pasta, 2 containers"
        f"{new_line}of bacon or even 10 slices of bacon. The quantity of your"
        f"{new_line}product is used to calculate how many days there are left"
        f"{new_line}before you run out of the product, so enter this value in"
        f"{new_line}the way that's most useful to you! It will then show your"
        f"{new_line}estimated current quantity and original quantity separated"
        f"{new_line}by a slash like so: current/original (e.g.: 4/10)"
        f"{new_line}"
        f"{new_line}{Colors.cy}Days/Use:{Colors.end}{new_line}"
        f"This value simply describes how many days"
        f"{new_line}it takes to finish 1 item of your product. So if you"
        f"{new_line}usually spend 10 days to finish one bag of pasta, your"
        f"{new_line}days per use is 10."
        f"{new_line}"
        f"{new_line}{Colors.cy}Date Added:{Colors.end}{new_line}"
        f"This is the date you added a product. This"
        f"{new_line}value is generated automatically when you add a new "
        f"product."
        f"{new_line}"
        f"{new_line}{Colors.cy}Expiry Date:{Colors.end}{new_line}"
        f"This is the expiry date of your product."
        f"{new_line}"
        f"{new_line}{Colors.cy}Days left:{Colors.end}{new_line}"
        f"This is the amount of days that are left"
        f"{new_line}before you run out of the product. Since it is an "
        f"{new_line}estimate, the accuracy will depend on how realistic"
        f" the days per use is.{new_line}"
    )


def general_explanation():
    """
    prints explanation of app to terminal
    """
    new_line = "\n"
    print(
        f"{new_line * 25}{new_line}{Colors.hr}Explanation{new_line}"
        f"{Colors.end}"
        f"{new_line * 2}Welcome to the Smart House Inventory explanation! Here"
        f"{new_line}we'll teach you what this app does and how to use it."
        f"{new_line * 2}"
        f"{new_line}Smart House Inventory, what does that mean? Well, it means"
        f"{new_line}that this app will assist you in a smart way with keeping"
        f"{new_line}track of all the items in your house. For example:"
        f"{new_line * 2}Are you ever on the toilet and find out you are out of"
        f"{new_line}toilet paper? Or made a beautiful pasta sauce but now see"
        f"{new_line}you don't have any pasta? This app will help you to"
        f"{new_line}prevent just that!"
        f"{new_line * 2}"
        f"When you add products to your Smart House Inventory, the app will"
        f"{new_line}ask for a {Colors.cy}Days/Use{Colors.end}. This means"
        f"the days necessary for you to finish{new_line}a product or item of"
        f"your product. {new_line}For example, if you have 10 apples and you"
        f"{new_line}eat an apple every 3 days, your "
        f"{Colors.cy}Days/Use{Colors.end} is 3."
        f"{new_line}This then gets used to calculate how many items are left."
        f"{new_line}After 6 days, you'd likely have eaten 2 apples, so you now"
        f"{new_line}have 8 out of 10 apples. This will be shown like '8/10' in"
        f"{new_line}the {Colors.cy}Quantity{Colors.end} column of your "
        f" inventory. You will also {new_line}find how many days there are"
        f"left until you will likely run out of {new_line}a product, in the"
        f"{Colors.cy}Days left{Colors.end} column. In the example"
        f"{new_line}of the apple, there would be 24 days left until you finish"
        f"{new_line}all the apples."
        f"{new_line * 2}{Colors.cy}Edit product{Colors.end}"
        f"{new_line}When editing a product in your inventory, there are a few"
        f"{new_line}things to note. When editing the {Colors.cy}Quantity"
        f"{Colors.end}, it's important{new_line}to realize that you are not"
        f"{new_line}adding to the original quantity, but replacing it. This"
        f"{new_line}means that if you have 10 apples and bought 5 more, you"
        f"{new_line}should fill in '15' as the new value for quantity. When"
        f"{new_line}you buy a new product that is already in your inventory,"
        f"{new_line}but has a different expiry date, it is advised to add it"
        f"{new_line}as a new product instead, so you can keep track of both"
        f"{new_line}both expiry dates."
        f"{new_line * 2}{Colors.cy}Add product{Colors.end}"
        f"{new_line}The add product feature guides you through a few questions"
        f"{new_line}to add a new product. Most of this is pretty simple."
        f"{new_line}When adding a product, it is important to add a realistic"
        f"{new_line}{Colors.cy}Days/Use{Colors.end} so the app can calculate "
        f"properly when you will {new_line}run out of it."
        f"{new_line}As a side note, when you use multiple items per day of"
        f"{new_line}a product, you could fill in a lower quantity to"
        f"{new_line}account for that. For example, if you eat 2 apples per day"
        f"{new_line}and you bought 10, you can set the quantity to 5 and leave"
        f"{new_line}the Days/Use at 1. This way, the app can still give"
        f"{new_line}correct estimates."
        f"{new_line * 2}I think it is time to head over to your inventory now,"
        f"{new_line}so you can see all of this in action! In your inventory"
        f"{new_line}you can scroll up to get a explanation of each column."
    )

    print(
        f"{new_line * 2}"
        "Hit 'I' to see/edit your inventory, 'R' to return to the start of "
        "the app\nor 'Q' to exit the program:\n"
    )
    answer = ""
    valid_answers = ["I", "R", "Q"]
    while answer not in valid_answers:
        # ask user what they want to do and validate answer
        answer = input().upper()
        if answer == "I":
            display_stock_data()
        elif answer == "R":
            main_function()
        elif answer == "Q":
            break
        else:
            print("Please enter an 'I', 'R' or 'Q'\n")


def display_stock_data():
    """
    function to display all the stock of the house.
    """
    new_line = '\n'

    # get the data from the google sheet and format it
    data_food_raw = food.get_all_values()
    data_food = format_stock_data(data_food_raw)
    data_item_raw = item.get_all_values()
    data_item = format_stock_data(data_item_raw)

    print(
        # print the entire inventory
        f"{inventory_explanation()}"
        f"{2 * new_line}"
        f"{Colors.hr}These are all the products you have in your house:"
        f"{Colors.end}{2 * new_line}"
        f"{Colors.bld}Items:{Colors.end}{2 * new_line}"
        f"{data_item}{new_line}"
        f"This is all the food you have in your house:{2 * new_line}"
        f"{Colors.bld}Foods:{Colors.end}{2 * new_line}"
        f"{data_food}{new_line}"
        f"{Colors.cy}Scroll up to see an explanation of the "
        f"inventory.{Colors.end}"
        f"{2 * new_line}"
        f"Hit 'E' to edit an item, 'D' to delete an item,"
        f"{new_line}'R' to return to the start of the program or 'Q' to exit:"
        f"{new_line}"
    )

    valid_input = ["E", "D", "R", "Q"]
    user_input = ""
    while user_input not in valid_input:
        # ask user what they want to do next and validate their input
        user_input = input().upper()
        if user_input == "E":
            edit_product()
        elif user_input == "D":
            delete_product()
        elif user_input == "R":
            main_function()
        elif user_input == "Q":
            pass
        else:
            print("Please enter an 'E', 'D', 'R' or 'Q'\n")


def format_stock_data(data):
    """
    format the raw stock data so the display stock data function
    can display it in a neat table
    """
    new_line = '\n'
    stock_data = ""
    product_number = 0
    quantity_and_days = calculate_quantity_and_days_left(data)
    for product in data:
        sheet_length = len(product)
        name_length = len(product[0])
        new_qt_length = len(str(quantity_and_days[0][0]))
        qt_length = len(product[1])
        # loop trough each row of google sheet and manipulate
        # data into a string
        if product_number < 1:
            # add name and quantity column
            # stock_data += f"' ' {product[0]}{(19 - name_length) * qt_length}"
            # stock_data += "  " + product[0] + (19 - name_length) * " " + "|"
            stock_data += (
                Colors.und + "  " + product[0] + (19 - name_length) * " " +
                "|" + Colors.end
                )
            stock_data += (
                Colors.und + product[1] + (11 - qt_length) * " " +
                "|" + Colors.end
                )
        else:
            # add product number, name and quantity data
            stock_data += f"{product_number} "
            stock_data += product[0] + (
                20 - name_length - len(str(product_number))) * " " + "|"
            stock_data += str(
                quantity_and_days[0][0]) + "/" + product[1] + (
                10 - (
                    qt_length + new_qt_length)
                    ) * " " + "|"
            quantity_and_days[0].pop(0)
        for ind in range(2, sheet_length):
            # add days p use, date added and in case of food sheet, expiry date
            if product_number < 1:
                stock_data += (
                    Colors.und + product[ind] + (11 - len(product[ind])) *
                    " " + "|" + Colors.end
                    )
            else:
                stock_data += (
                    product[ind] + (11 - len(product[ind])) * " " + "|"
                    )
        if product_number < 1:
            # add days left column
            stock_data += Colors.und + "Days left" + Colors.end
        else:
            # add days left data
            stock_data += str(quantity_and_days[1][0])
            quantity_and_days[1].pop(0)
        stock_data += f"{new_line}"
        product_number += 1
    return stock_data


def calculate_quantity_and_days_left(sheet):
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
        # put quantity, days per use and data added in separate lists
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
        # calculate the new quantity by dividing the days spend by days per use
        # and subtracting that from the original quantity
        days_spend = current_date - datetime.datetime.strptime(
            date_added[index], "%Y-%m-%d"
            ).date()
        # code taken from Stackoverflow (see readme)
        quantity_left = (
            int(quantity[index]) - days_spend.days / int(days_p_use[index])
            )
        quantity_left = max(quantity_left, 0)
        new_quantity.append(math.ceil(quantity_left))
        # calculate days left by multiplying quantity left with days per use
        days = math.ceil(quantity_left) * int(days_p_use[index])
        days_left.append(days)

    quantity_and_days_left = []
    quantity_and_days_left.append(new_quantity)
    quantity_and_days_left.append(days_left)
    return quantity_and_days_left


def main_function():
    """
    main function of the program, asks user to see inventory or add a product.
    """
    print(
        Colors.hr + "\nWelcome to your Smart House Inventory!\n" + Colors.end
        )
    print(
        "With this program, you can track all the products in your house and "
        "fridge.\nYou can see things like the current quantity of a product, "
        "\nits expiry date and the date you added the product."
        "\nYou can even see when you will likely run out of a product!" +
        Colors.cy + "\n\nFirst time here? Make sure to read the explanation "
        "section first (hit 'E')!.\n" + Colors.end
        )
    print(
        "Hit 'I' to see/edit your inventory, 'P' to add a product"
        "\n'E' for explanation of the app or 'Q' to exit the program:\n"
    )
    answer = ""
    valid_answers = ["I", "E", "P", "Q"]
    while answer not in valid_answers:
        # ask user what they want to do and validate answer
        answer = input().upper()
        if answer == "I":
            display_stock_data()
        elif answer == "E":
            general_explanation()
        elif answer == "P":
            print("\nCool let's add a product!")
            make_product()
        elif answer == "Q":
            break
        else:
            print("Please enter an 'I', 'P' 'E' or 'Q'\n")


main_function()
