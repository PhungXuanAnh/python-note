from flask import Flask, jsonify, abort, make_response, request, redirect
from pymodm import fields, connect, MongoModel
import logging
import sys


class ShortLink(MongoModel):
    shortLink = fields.CharField(primary_key=True)
    longLink  = fields.CharField()
    
connect('mongodb://{ip}:{port}/{database}'.format(
    ip = '10.76.241.113',
    port = 28017,
    database = 'ShortLink'
    ))
        
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def encode(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def decode(string, alphabet=BASE62):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num

currentRandomshortLinkId = 0 #shoule save this value to disk to
                                # make it persistent even server crash
def  generateRandomshortLink():
    global currentRandomshortLinkId
    while True:
        shortLink = encode(currentRandomshortLinkId)

        # make sure the shortLink isn't already used
        is_shortLink_exist = False
        for link in ShortLink.objects.all():
            if link.shortLink == shortLink:
                is_shortLink_exist = True
                break
        
        currentRandomshortLinkId = currentRandomshortLinkId + 1

        if is_shortLink_exist:
            continue
        
        return shortLink


app = Flask(__name__)
@app.errorhandler(404)
def error404(error):
    return make_response(jsonify({'error': error}), 404)

def is_shortLink_valid(shortLink):
    valid_string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in shortLink:
        if char not in valid_string:
            return False
    return True

@app.route('/api/v1.0/shortlink', methods=['POST'])
def create_shortlink():
    if not request.json or not 'longLink' in request.json:
        abort(400, description="longLink should be provided")

    shortLink = request.json.get('shortLink')
    
    if  shortLink == None:
        shortLink = generateRandomshortLink()
    elif len(shortLink) > 7:
        abort(400, description="shortLink must be small than 7")
    elif is_shortLink_valid(shortLink) == False:
        abort(400, description="shortLink is only contain 0-9a-zA-Z")

    # save to database
    ShortLink(shortLink=shortLink, longLink=request.json.get('longLink')).save()

    return jsonify({'shortLink': shortLink}), 200

@app.route('/<string:shortLink>')
def redirect_to_longlink(shortLink):
    longlink = ShortLink.object.raw({"shortLink": shortLink})[0]
    return redirect(longlink, code=302)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S", 
        stream=sys.stdout,
    )
    app.run(debug=True)