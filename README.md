# Shopify Infrastructure Backend

### Setup
The website can be re-created using Python. I suggest to create a virtual environment via Conda. The requirements.txt file contains all the libraries used to create this website.

All examples assume that localhost:5000 is hosting the webapp (Flask's default). 

### Data
A sample database is stored within each instance of the application. It is a list of dictionary of shoes. 

### Endpoints

`/products`: Returns all shoes in the database.

Optional arguments:

* `inStock`: A boolean flag that will filter out-of-stock shoes
* `name`: A string parameter that will return the information for a single shoe if found. If the name is not found, it returns an empty list.

Examples:
* http://localhost:5000/products: returns all shoes
* http://localhost:5000/products?inStock=1: returns all shoes in-stock
* http://localhost:5000/products?name=citysocks: returns the information for CitySocks
* http://localhost:5000/products?name=jordans&inStock=1: returns an empty list as jordans have no stock


`/buy/<name:string>`: Purchases the shoe with the given name. If the shoe is out of stock or the name does not exist, the appropriate error message is returned.

Examples:
* http://localhost:5000/buy/jordans: Error message saying the shoe is out of stock
* http://localhost:5000/buy/citysocks: Purchase message indicating the price and the item bought
* http://localhost:5000/products?inStock=1: Updated database after the purchase of citysocks (citysocks no longer shows up as there is no stock)
