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

## Testing

### Bugs

* When creating the Food subclass, an error "too many positional arguments for method call" would pop up. This was caused by the "date_added" variable being passed as an argument, while in the Product parentclass, this is not passed as an argument. After removing this argument from the Food init method, the error was resolved and the class worked as expected.