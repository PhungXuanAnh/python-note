from flask import jsonify, Flask, make_response, url_for

app = Flask(__name__)

def make_publish_context(context):
    new_context = {}
    for field in context:
        if field == 'id':
            new_context['uri'] = url_for('get_context', context_id=context['id'], _external=True)
        else:
            new_context[field] = context[field]
    return new_context

@app.errorhandler(400)
def error400(error):
    # 400 Bad Request
    app.logger.info("HTTP 400 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 400)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.errorhandler(401)
def error401(error):
    # 401 Unauthorized
    app.logger.info("HTTP 401 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 401)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(403)
def error403(error):
    # 403 Forbidden
    app.logger.info("HTTP 403 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 403)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(404)
def error404(error):
    # 404 Not Found
    app.logger.info("HTTP 404 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 404)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.errorhandler(408)
def error408(error):
    # 408 Request Timeout
    app.logger.info("HTTP 408 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 408)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.errorhandler(409)
def error409(error):
    # 409 Conflict
    app.logger.info("HTTP 409 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 409)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(500)
def error500(error):
    # 409 Conflict
    app.logger.info("HTTP 500 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 500)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(501)
def error501(error):
    # 409 Conflict
    app.logger.info("HTTP 501 error: {}".format(error.description))
    response = make_response(jsonify({'error': error.description}), 501)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def response_200(dict_msg):
    # 200 OK
    response = make_response(jsonify(dict_msg), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def response_201(dict_msg):
    # 201 Created
    response = make_response(jsonify(dict_msg), 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def response_202(dict_msg):
    # 202 Accepted
    response = make_response(jsonify(dict_msg), 202)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def response_204(dict_msg):
    # 204 No Content
    response = make_response(jsonify(dict_msg), 204)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
