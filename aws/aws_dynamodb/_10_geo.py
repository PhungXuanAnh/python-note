import boto3
import dynamodbgeo
import uuid
import json

# Import the AWS sdk and set up your DynamoDB connection
dynamodb = boto3.client("dynamodb", region_name="ap-southeast-2")

# Create an instance of GeoDataManagerConfiguration for each geospatial table you wish to interact with
config = dynamodbgeo.GeoDataManagerConfiguration(dynamodb, "test_geo_table")

# Initiate a manager to query and write to the table using this config object
geoDataManager = dynamodbgeo.GeoDataManager(config)

# ----------------------------------------------------------------


def create_table():
    # Pick a hashKeyLength appropriate to your usage
    config.hashKeyLength = 3

    # Use GeoTableUtil to help construct a CreateTableInput.
    table_util = dynamodbgeo.GeoTableUtil(config)
    create_table_input = table_util.getCreateTableRequest()

    # tweaking the base table parameters as a dict
    create_table_input["ProvisionedThroughput"]["ReadCapacityUnits"] = 5

    # Use GeoTableUtil to create the table
    table_util.create_table(create_table_input)


def add_point(latitude, longitude, addition_data):
    # preparing non key attributes for the item to add

    PutItemInput = {
        "Item": addition_data,
        "ConditionExpression": "attribute_not_exists(hashKey)",  # ... Anything else to pass through to `putItem`, eg ConditionExpression
    }
    result = geoDataManager.put_Point(
        dynamodbgeo.PutPointInput(
            dynamodbgeo.GeoPoint(latitude, longitude),  # latitude then latitude longitude
            str(uuid.uuid4()),  # Use this to ensure uniqueness of the hash/range pairs.
            PutItemInput,  # pass the dict here
        )
    )
    print(result)
    

def update_non_location_fields():
    # define a dict of the item to update
    UpdateItemDict = {  # Dont provide TableName and Key, they are filled in for you
        "UpdateExpression": "set Capital = :val1",
        "ConditionExpression": "Capital = :val2",
        "ExpressionAttributeValues": {
            ":val1": {"S": "Tunis"},
            ":val2": {"S": "Ariana"},
        },
        "ReturnValues": "ALL_NEW",
    }
    geoDataManager.update_Point(
        dynamodbgeo.UpdateItemInput(
            dynamodbgeo.GeoPoint(
                36.879163, 10.24312
            ),  # latitude then latitude longitude
            "1e955491-d8ba-483d-b7ab-98370a8acf82",  # Use this to ensure uniqueness of the hash/range pairs.
            UpdateItemDict,  # pass the dict that contain the remaining parameters here
        )
    )


def delete_point():
    # Preparing dict of the item to delete
    DeleteItemDict = {
        "ConditionExpression": "attribute_exists(Country)",
        "ReturnValues": "ALL_OLD"
        # Don't put keys here, they will be generated for you implecitly
    }
    geoDataManager.delete_Point(
        dynamodbgeo.DeleteItemInput(
            dynamodbgeo.GeoPoint(
                36.879163, 10.24312
            ),  # latitude then latitude longitude
            "0df9742f-619b-49e5-b79e-9fb94279d30c",  # Use this to ensure uniqueness of the hash/range pairs.
            DeleteItemDict,  # pass the dict that contain the remaining parameters here
        )
    )


def rectangular_query_point():
    # Querying a rectangle
    QueryRectangleInput = {
        "FilterExpression": "Country = :val1",
        "ExpressionAttributeValues": {
            ":val1": {"S": "Italy"},
        },
    }
    print(
        geoDataManager.queryRectangle(
            dynamodbgeo.QueryRectangleRequest(
                dynamodbgeo.GeoPoint(36.878184, 10.242358),
                dynamodbgeo.GeoPoint(36.879317, 10.243648),
                QueryRectangleInput,
            )
        )
    )


def circular_query_point(center_point, radius):
    # Querying 95 meter from the center point (36.879131, 10.243057)
    # QueryRadiusInput = {
    #     "FilterExpression": "Country = :val1",
    #     "ExpressionAttributeValues": {
    #         ":val1": {"S": "Italy"},
    #     },
    # }

    result = geoDataManager.queryRadius(
        dynamodbgeo.QueryRadiusRequest(
            dynamodbgeo.GeoPoint(*center_point),  # center point
            radius,
            # QueryRadiusInput,
            sort=True,
        )
    )  # diameter
    # print(json.dumps(result, indent=4, sort_keys=True))
    for value in result:
        print(f'{value["Name"]["S"]}:\t{value["distance"]["N"]}')


if __name__ == "__main__":
    # create_table()
    # add_point(
    #     longitude=21.0278,
    #     latitude=105.8342,
    #     addition_data={
    #         "Country": {"S": "Vietnam"},
    #         "Capital": {"S": "Hanoi"},
    #         "year": {"S": "2020"},
    #     }
    # )
    # update_non_location_fields()
    # delete_point()
    # rectangular_query_point()
    
    center_point = (-33.855487566099534, 151.21735424489904)
    radius = 2015 # meters
    circular_query_point(center_point, radius)
    
    # latitude longitude
    
    test_points = [
        {
            "latitude": -33.855487566099534,
            "longitude": 151.21735424489904,
            "addition_data": {
                "Name": {"S": "sydney opera house"},
                "distance": {"N": '0'},
            }
        },
        {
            "latitude": -33.868294643153575,
            "longitude": 151.20189064689876,
            "addition_data": {
                "Name": {"S": "SEA LIFE Sydney Aquarium"},
                "distance": {"N": '2020'},
            }
        },
        {
            "latitude": -33.870361952592894,
            "longitude": 151.2129300577644,
            "addition_data": {
                "Name": {"S": "St Mary's Cathedral"},
                "distance": {"N": '1700'},
            }
        },
        {
            "latitude": -33.8484370293292,
            "longitude": 151.2105632510547,
            "addition_data": {
                "Name": {"S": "Sydney Harbour Bridge"},
                "distance": {"N": '1000'},
            }
        },
        {
            "latitude": -33.909756150174154,
            "longitude": 151.18541806133808,
            "addition_data": {
                "Name": {"S": "Sydney Park"},
                "distance": {"N": '6710'},
            }
        },
        {
            "latitude": -33.81982875481394,
            "longitude": 151.1913728103726,
            "addition_data": {
                "Name": {"S": "Royal North Shore Hospital"},
                "distance": {"N": '4630'},
            }
        },
        {
            "latitude": -33.97786321296097,
            "longitude": 151.25123050062118,
            "addition_data": {
                "Name": {"S": "Little Bay Beach"},
                "distance": {"N": '13930'},
            }
        }
    ]
    
    # for point in test_points:
    #     add_point(
    #     longitude=point['longitude'],
    #     latitude=point['latitude'],
    #     addition_data=point['addition_data']
    # )
    
    