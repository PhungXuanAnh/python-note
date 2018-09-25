import re

line = "Cats are smarter than dogs"

matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

if matchObj:
    print("matchObj.groups() : ", matchObj.groups())
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))
else:
    print("No match!!")

print('--------------------------------------------------------')    

str = "/officialdoda/photos/a.535710036474284/2038010436244229/?type=3&__xts__%5B0%5D=68.ARBDqQ0SZom8vthg_N5uXGS8SLYxjVeMIQl14iICLyxaZswjl3Mm6EvZAQTfUe5o9Y3pC8z9-WW7oBDMFXVHzRfOFPpvmPD8t5P2YZk0qVohxAxE7ObsXt-TRpW5vSAHIhYmAyMS8ZzaW8ndlJSdwIe1dbpB2EKmZj08H6HpUQo9KfLRIvRMxw&__tn__=-R"
print(re.search(r'/(\d+)/', str).group(1))

# https://www.facebook.com/officialdoda/posts/320666585359581
# https://www.facebook.com/officialdoda/posts/2038010436244229

str = "https://facebook.com/officialdoda/"
print(re.search(r'facebook.com/([a-zA-Z0-9]+)/', str).group(1))

