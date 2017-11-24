from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

users = [
    {"email": "masnun@gmail.com", "name": "Masnun", "id": 1}
]

def get_user_by_id(user_id):
    for x in users:
        if x.get("id") == int(user_id):
            return x

subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True,
                                       help="Name has to be valid string")
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument("id", type=int, required=True,
                                       help="Please enter valid integer as ID")

class SubscriberCollection(Resource):
    def get(self):
        return users
    
    def post(self):
        args = subscriber_request_parser.parse_args()
        users.append(args)
        return {"msg": "Subscriber added", "subscriber_data": args}
    
class Subscriber(Resource):
    def get(self, id):
        user = get_user_by_id(id)
        if not user:
            return {"error": "User not found"}
        return user
    
    def put(self, id):
        args = subscriber_request_parser.parse_args()
        user = get_user_by_id(id)
        if user:
            user.remove(user)
            user.append(args)
            
        return args
    
    def delete(self, id):
        user = get_user_by_id(id)
        if user:
            users.remove(user)
        return {"message": "Deleted"}
    
api.add_resource(SubscriberCollection, '/subscribers')
api.add_resource(Subscriber, '/subscribers/<init>:id')

if __name__ == '__main__':
    app.run(debug=True)
    
        