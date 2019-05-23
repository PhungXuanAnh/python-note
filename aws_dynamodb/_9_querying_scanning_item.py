from boto3.dynamodb.conditions import Key  # used when the condition is related to the key of the item.
from boto3.dynamodb.conditions import Attr  # used when the condition is related to an attribute
from _2_using_exist_table import table

print('------------------querying')
response = table.query(
    KeyConditionExpression=Key('username').eq('janedoe')
)
items = response['Items']
print(items)

print('------------------scanning')
response = table.scan(
    FilterExpression=Attr('age').lt(27)
)
items = response['Items']
print(items)

print('------------------multi condition')
response = table.scan(
    FilterExpression=Attr('first_name').begins_with('J') & Attr('account_type').eq('super_user')
)
items = response['Items']
print(items)

print('-----------------conditions of a nested attribute')
response = table.scan(
    FilterExpression=Attr('address.state').eq('CA')
)
items = response['Items']
print(items)

print('-----------------scan all')
response = table.scan()
items = response['Items']
print(items)
