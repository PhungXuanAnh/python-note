# khai bao hien thi 

import json
from flask import Blueprint, abort
from flask_restful import Resource, reqparse
from Restful_API_flask.bai3_my_app.catalog.models import Product
from Restful_API_flask.bai3_my_app import db

catalog = Blueprint('catalog', __name__)

@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home"

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('price', type=float)

class ProductApi(Resource):

    def get(self, id=None, page=1):
        if not id:
            products = Product.query.paginate(page, 10).items
        else:
            products = [Product.query.get(id)]
            
        if not products:
            abort(404)
            
        res = {}
        for product in products:
            res[product.id] = {
                'name': product.name,
                'price': product.price,
            }
        return json.dumps(res)
    
    def post(self):
        args = parser.parse_args()
        name =  args['name']
        price = args['price']
        product = Product(name, price)
        db.session.add(product)
        db.session.commit()
        
        res = {}
        res[product.id] = {
            'name': product.name,
            'price': product.price,
        }
        return json.dumps(res)
    