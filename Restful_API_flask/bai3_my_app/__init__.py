# khoi tao app, database va ket noi dung voi nhau
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
 
from Restful_API_flask.bai3_my_app.catalog.views import catalog
app.register_blueprint(catalog)
 
db.create_all()

from flask_restful import Api
from Restful_API_flask.bai3_my_app.catalog.views import ProductApi

api = Api(app)

api.add_resource(
    ProductApi,
    '/api/product',
    '/api/product/<int:id>',
    '/api/product/<int:id>/<int:page>'
)