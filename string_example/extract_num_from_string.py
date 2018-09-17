str1 = "3158 reviews"
# python2
# num = int(filter(str.isdigit, str1)) 

# python3
num = int(''.join(list(filter(str.isdigit, str1))))
print(num)

str = '27K lượt xem'
print(str[:-9])