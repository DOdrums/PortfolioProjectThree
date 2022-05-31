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


def get_stock_data():
    """
    function to display all the stock of the house
    """
    new_line = '\n'
    food = SHEET.worksheet("food")
    item = SHEET.worksheet("item")

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


print(get_stock_data())
