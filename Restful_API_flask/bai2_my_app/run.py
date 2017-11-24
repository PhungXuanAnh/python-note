from Restful_API_flask.bai2_my_app import app, db
from Restful_API_flask.bai2_my_app.catalog.models import Product

# khai bao manager de tao rest api
from flask_restless import APIManager
manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Product, methods=['GET', 'POST'])

# chay app
app.run(debug=True)