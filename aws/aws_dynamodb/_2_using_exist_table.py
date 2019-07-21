import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb',
                          region_name='eu-west-1',
                          endpoint_url='http://localhost:8000')
                          
# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('users')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)