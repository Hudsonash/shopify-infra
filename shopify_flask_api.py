from flask import Flask, request
from flask_restplus import Api, Resource, reqparse, inputs

app = Flask(__name__)
api = Api(app)


@api.route('/products')
class Products(Resource):
    def get(self):
        '''
        Returns all available items in a JSON document

        Optional parameters:
            name: returns the matching item, none otherwise
            inStock: returns only stocked items

        Future improvements:
            - only allow the two request arguments
            - limit the request instock to boolean values and
              item name to a string
            - validate the querystring names to prevent attacks
        '''
        item_name = request.args.get('name')
        instock = request.args.get('inStock')
        if instock:
            instock = int(instock)
        if item_name:
            response = get_item_name(item_name)
        else:
            response = get_all_items()
        if instock:
            response = filter_stock(response)
        return response


@api.route('/buy/<string:name>')
class Purchase(Resource):
    def get(self, name):
        '''
        Purchases the item one time and reduces the stock in
        the database.

        Returns an error message if the item does not exist or
        the item is out of stock.

        Improvements:
            - Change the get to a post for additional security
        '''
        item = get_item_name(name)
        if item:
            successful_purchase = purchase_of_item(name)
            if successful_purchase:
                return "Thank you for purchasing {name} for ${price}.00".format(
                    name=item['name'], price=item['price'])
            else:
                return "Sorry, the item is out of stock."
        else:
            return "No item exists with this name"


# helper functions for data retrieval
def get_item_name(name):
    '''
    Returns the dictionary element of an item if
    it exists, otherwise an empty list
    '''
    for prod in product_dict:
        if prod['name'] == name:
            return prod
    return prod

def get_all_items():
    return product_dict


def filter_stock(data):
    '''
    Filters the item dictionary to only contain instock items
    Returns the filtered list of dictionaries.
    '''
    if data == []:
        return []
    else:
        return [prod for prod in data if prod['inventory_count'] > 0]


def purchase_of_item(name):
    for prod in product_dict:
        if prod['name'] == name:
            if prod['inventory_count'] <= 0:
                return False
            else:
                 prod['inventory_count'] -= 1
                 return True
    return False # unable to find name in dictionary


# sample database for Shopify challenge challenge
'''
Improvements
    - None, storing the website's instance is perfectly secure
    - In reality, store this information in a database for security

'''
product_dict = [
    {
        'name': 'ultraboosts',
        'price': 250,
        'inventory_count': 50
    },
    {
        'name': 'jordans',
        'price': 100,
        'inventory_count': 0
    },
    {
        'name': 'citysocks',
        'price': 900,
        'inventory_count': 1
    },
    {
        'name': 'acronym',
        'price': 200,
        'inventory_count': 5
    },
    {
        'name': 'newbalance',
        'price': 50,
        'inventory_count': 0
    }
]

if __name__ == '__main__':
    app.run(debug=True)
