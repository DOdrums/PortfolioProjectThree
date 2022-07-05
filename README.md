# Smart House Inventory

## Portfolio Project 3: Python Essentials

![Multi screen mockup]()

This project is built as part of the Code Institute Full Stack Software Development course. For this course, Dirk Ornee had to built a third Portfolio Project. Inspired by the expired products in his fridge and the occasional lack of toilet paper in his bathroom, he decided to build a Smart House Inventory solution, that will keep track of all the products in his house.

## Live Site

[Smart House Inventory]()

## Github Repository

[PortfolioProjectThree](https://github.com/DOdrums/PortfolioProjectThree)

## Credits

### Code

* [Regexland](https://regexland.com/regex-dates/) - to validate the date input with regex
* [datascienceparichay](https://datascienceparichay.com/article/python-check-list-contains-only-numbers/) - to check if a string/list of strings consists of digits
* [finxter](https://blog.finxter.com/how-to-convert-a-string-list-to-an-integer-list-in-python/#:~:text=The%20most%20Pythonic%20way%20to,x)%20built%2Din%20function.) - to convert a list of strings to a list of integers
* [stackoverflow(answer from Arash)](https://stackoverflow.com/a/70391597/16545052) - to delete rows of data from google sheet
* [stackoverflow(answer from Shubham Naik)](https://stackoverflow.com/a/2803877/16545052) - to convert string date to datetime object

## Testing

### Bugs

* When creating the ```Food``` subclass, an error ```"too many positional arguments for method call"``` would pop up. This was caused by the ```date_added``` variable being passed as an argument, while in the ```Product``` parentclass, this is not passed as an argument. After removing this argument from the ```Food``` init method, the error was resolved and the class worked as expected.
* When using the ```sort()``` method in the ```delete_product()``` function, it kept returning ```None```. The reason for this, is that the ```sort()``` method sorts a list in place, instead of returning a new list. When writing ```list = list.sort()``` the result will be ```None``` because of this.