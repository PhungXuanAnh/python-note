import hashlib 

string = '123456admin'

print(hashlib.md5(string.encode('utf-8')).digest())
print(hashlib.md5(string.encode('utf-8')).hexdigest())