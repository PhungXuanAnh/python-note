# reference: https://stackabuse.com/format-number-as-currency-string-in-python

def using_locale_lib():
    print('\n---------------------------- format currency using_locale_lib --------------------')
    import locale
    # locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
    locale.setlocale( locale.LC_ALL, 'vi_VN.utf8' )
    print(locale.currency(1346896.67444, grouping=True, symbol=True))
    print(locale.currency(10000000, grouping=True, symbol=True))
    print(locale.currency(10000000, grouping=True, symbol=True, international=True))
    print(locale.format_string('%.2f', 10000000, True))


def using_string_format():
    print('\n---------------------------- format currency using_string_format --------------------')
    print("{:,.2f}VND".format(10000000))
    print("{:,.0f}VND".format(10000000))
    print("{:,.0f}VND".format(0))


if __name__ == '__main__':
    using_locale_lib()
    using_string_format()

