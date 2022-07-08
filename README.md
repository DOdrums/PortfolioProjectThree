# Smart House Inventory

## Portfolio Project 3: Python Essentials

![Multi screen mockup](assets/images/mockup.png)

This project is built as part of the Code Institute Full Stack Software Development course. For this course, Dirk Ornee had to built a third Portfolio Project. Inspired by the expired products in his fridge and the occasional lack of toilet paper in his bathroom, he decided to build a Smart House Inventory solution, that will keep track of all the products in his house.

## Live Site

[Smart House Inventory](https://smart-house-inventory.herokuapp.com/)

## Github Repository

[PortfolioProjectThree](https://github.com/DOdrums/PortfolioProjectThree)

## UX

### Business Goals

The goal of this project is to assist a user in keeping track of their house inventory and getting insights into when they should run out to the store to replenish some of their favorite products. It's built as a single user application, but could be forked and used with personal Google Sheets.

### Target Audience

I think a lot of people recognize the feeling of opening their fridge and finding their beautiful salmon or steak has sadly expired. Or perhaps you want to turn on the dishwasher at night and find yourself out of dishwasher tablets. Even worse, you are in the bathroom and have only one sheet of toilet paper left. Awkward and wasteful situations that can easily be prevented! With the smart house inventory you can easily generate an inventory with estimations when to get new products and neatly keep track of their expiry dates.

### User Stories

#### As the owner

* I want to build a helpful tool so users can better manage the inventory in their house.
* I want the user to waste less food.
* I want the user to not run out of products.
* I want the user to have a clear and well structured visual of their stock.

#### As a new user

* I want to understand the purpose of the app straight away, even if I stumbled upon it randomly.
* I want to intuitively navigate the app and have clear explanations about each section and function.
* I want to manage the stock in my house.
* I want the app to be smart and do things automatically for me.

#### As a returning user

* I want to be able to use the app in a quick way, without having to scroll trough needless explanations and options.
* I want to get an update about my stock each time I open the app.
* I want to get insights from the app about my stock and what I should do.

### Structure of the app

The app is designed to have a good flow, with clear options explained in a short and concise way. Inventory explanations is purposefully put on top, so returning users don't have to scroll through it every time to get to their inventory. The inventory is fully editable and products can be added to both lists easily.

### Color Scheme

Although colors are used on a few lines of text, no real color scheme was used. The text displays either purple, cyan or white.

### Features

The app is divided into to section, 'show/edit inventory' and 'add a product'. These to sections together hold all the features of the app:

#### Main page

This page shows a short introduction of the app and gives you the option to either show your inventory or add a product. New user are encouraged to first visit the inventory, because 'More info can be found when opening your inventory'.

[main page]()



## Credits

### Code

* [Regexland](https://regexland.com/regex-dates/) - to validate the date input with regex
* [datascienceparichay](https://datascienceparichay.com/article/python-check-list-contains-only-numbers/) - to check if a string/list of strings consists of digits
* [finxter](https://blog.finxter.com/how-to-convert-a-string-list-to-an-integer-list-in-python/#:~:text=The%20most%20Pythonic%20way%20to,x%20built%2Din%20function.) - to convert a list of strings to a list of integers
* [stackoverflow(answer from Shubham Naik)](https://stackoverflow.com/a/2803877/16545052) - to convert string date to datetime object
* [youtube](https://www.youtube.com/watch?v=yPQ2Gk33b1U) - to edit/update specific cells in Google Sheet
* [stackoverflow](https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal) - to style terminal text with colors

## Testing

### Bugs

* When creating the ```Food``` subclass, an error ```"too many positional arguments for method call"``` would pop up. This was caused by the ```date_added``` variable being passed as an argument, while in the ```Product``` parentclass, this is not passed as an argument. After removing this argument from the ```Food``` init method, the error was resolved and the class worked as expected.
* When using the ```sort()``` method in the ```delete_product()``` function, it kept returning ```None```. The reason for this, is that the ```sort()``` method sorts a list in place, instead of returning a new list. When writing ```list = list.sort()``` the result will be ```None``` because of this.