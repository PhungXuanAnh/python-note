from flask import jsonify, Flask, make_response, url_for
import logging
app = Flask(__name__)

@app.errorhandler(404)
def error404(error):
    response = make_response(jsonify({'error': error.description}), 404)
    response.headers['Access-Control-Allow-Origin'] = '*'
    logging.info("Response HTTP 404 {}".format(error.description))
    return response

@app.errorhandler(400)
def error400(error):
    response = make_response(jsonify({'error': error.description}), 400)
    response.headers['Access-Control-Allow-Origin'] = '*'
    logging.info("Response HTTP 400 {}".format(error.description))
    return response

def response_200(dict_msg):
    response = make_response(jsonify(dict_msg), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    logging.info("Response HTTP 200 {}".format(jsonify(dict_msg)))
    return response

def response_201(dict_msg):
    response = make_response(jsonify(dict_msg), 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    logging.info("Response HTTP 201 {}".format(jsonify(dict_msg)))
    return response

def make_publish_context(context):
    new_context = {}
    for field in context:
        if field == 'id':
            new_context['uri'] = url_for('get_context', context_id=context['id'], _external=True)
        else:
            new_context[field] = context[field]
    return new_context
