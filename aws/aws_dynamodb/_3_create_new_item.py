from _2_using_exist_table import table

table.put_item(
    Item={
        'username': 'janedoe',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'age': 25,
        'account_type': 'standard_user',
    }
)

table.put_item(
    Item={
        'username': 'Janedoe',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'age': 25,
        'account_type': 'super_user',
    }
)

table.put_item(
    Item={
        'username': 'Janedoe',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'age': 25,
        'account_type': 'super_user',
        'address': {'city': 'Los Angeles',
               'state': 'CA',
               'zipcode': 90001,
               'road': '1 Jefferson Street'},
    }
)
