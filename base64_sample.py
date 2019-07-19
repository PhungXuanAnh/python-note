import base64

string = u'complex string: ñáéíóúÑ'
string = '123'
string = 'hà nội'

a = base64.b64encode(bytes(string, "utf-8"))
b = base64.b64decode(a).decode("utf-8", "ignore")

print(type(a))
print(type(a.decode('ascii')))
print(type(b))
print(b)
