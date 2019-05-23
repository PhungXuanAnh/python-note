from _2_using_exist_table import table

table.delete_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)

# then get item again
response = table.get_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)
print(response)
item = response['Item']
print(item)