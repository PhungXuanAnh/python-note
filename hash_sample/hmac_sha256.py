import hashlib
import hmac
import base64


api_name = "/twilio/v1/extension/dynamic/next"
utc = "_2019-08-22T11:50"

secret = bytes('secret', 'utf-8')

hash1 = base64.b64encode(hmac.new(secret, (api_name + utc).encode('utf-8'), digestmod=hashlib.sha256).digest())
hash2 = base64.b64encode(hmac.new(hash1, api_name.encode('utf-8'), digestmod=hashlib.sha256).digest())

print(hash1.decode())
print(hash2.decode())
