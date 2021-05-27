import phonenumbers

"""
pip install phonenumbers
https://pypi.org/project/phonenumbers/

There are many feature: format, check valid, geo desc, find phone in a string, formatting applied as the user types phone in a view...

"""
def check_phone_number(number):
    z = phonenumbers.parse(number=number, region="VN")
    print("\nOrigin phone number: ", number)
    print("Detail about this phone number: ", z)
    print("This phone number is valid: ", phonenumbers.is_valid_number(z))
    print("This phone number after format NATIONAL: ", phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.NATIONAL))
    print("This phone number after format INTERNATIONAL: ", phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
    print("This phone number after format E164: ", phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.E164))

    print("------------------------")

if __name__ == "__main__":
    check_phone_number("0349623123")
    check_phone_number("034962312")
    check_phone_number("0349623123a")
    check_phone_number("0349.6231.23aa")