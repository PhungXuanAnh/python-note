import hashlib
import hmac
import base64


api_name = "abc/v1/test"
utc = "_2019-08-22T11:50"

secret = bytes('secret', 'utf-8')

hash1 = base64.b64encode(hmac.new(secret, (api_name + utc).encode('utf-8'), digestmod=hashlib.sha256).digest())
hash2 = base64.b64encode(hmac.new(secret, api_name.encode('utf-8'), digestmod=hashlib.sha256).digest())

print(hash2)

b'GnLkwxsKHfJRI/bRHk0BfHTZgK0bUVKPx6q6aAhMWFY='
