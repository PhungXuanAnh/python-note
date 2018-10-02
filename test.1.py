def convert_redis_str_to_binary_str(s):
    bitmap = ""
    for c in s:
        x = ord(c)
        str = bin(x).split('b')[1]
        if len(str) < 8:
            str = '0' * (8 - len(str)) + str
        bitmap += str
    return bitmap

str1 = "@\x00"
str1 = 'L'
# str1 = '\xca'
print(convert_redis_str_to_binary_str(str1))