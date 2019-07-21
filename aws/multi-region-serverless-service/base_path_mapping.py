import os
import sys
import boto3
import json
import logging
from utils import DateTimeEncoder, get_api_id

logging.basicConfig(level=logging.WARN)

logging.info(json.dumps(sys.path, indent=4, sort_keys=True))

apigateway_name = "multiregion-helloworld"
domain_name = os.environ['MultiregionDomainName']
base_path = 'v1'
region_name = os.environ['REGION']
stage_name = 'prod'

client = boto3.client('apigateway', region_name=region_name)


def create():
    try:
        response = client.create_base_path_mapping(
            domainName=domain_name,
            basePath=base_path,
            restApiId=get_api_id(client, apigateway_name),
            stage=stage_name
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True, cls=DateTimeEncoder))
    except Exception as e:
        if e.__class__.__name__ == 'ConflictException':
            logging.warn("base path '{}' existed".format(base_path))
        else:
            logging.exception(e)


def delete():
    try:
        response = client.delete_base_path_mapping(
            domainName=domain_name,
            basePath=base_path
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True, cls=DateTimeEncoder))
    except Exception as e:
        if e.__class__.__name__ == 'NotFoundException':
            logging.warn("base path '{}' not found".format(base_path))
        else:
            logging.exception(e)


if __name__ == "__main__":
    if sys.argv[1] == 'delete':
        delete()

    if sys.argv[1] == 'create':
        create()
