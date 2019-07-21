import json
import datetime
import logging


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


def get_api_id(client, api_name):
    response = client.get_rest_apis(
        # position='0',   # start page
        limit=500       # max is 500
    )

    logging.info(json.dumps(response, indent=4, sort_keys=True, cls=DateTimeEncoder))

    if response.get('items'):
        for api in response['items']:
            if api['name'] == api_name:
                return api['id']
        raise Exception('can not get api id')
    else:
        raise Exception('can not get api id')