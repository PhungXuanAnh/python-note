
def extract_number_from_string():
    str1 = "3158 reviews"

    # python2
    # num = int(filter(str.isdigit, str1)) 

    # python3
    num = int(''.join(list(filter(str.isdigit, str1))))
    print("extract number from string using str.isdigit: ", num)


extract_number_from_string()
