"""
    docker run -d --name test-mongodb \
				-p 27018:27017 \
				-v /tmp/test-mongodb-data:/data/db \
				-e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
				-e MONGO_INITDB_ROOT_PASSWORD=secret \
				mongo
"""

AUTHEN_URL = 'mongodb://{user}:{password}@{hostname}:{port}/'.format(
    user='mongoadmin',
    password='secret',
    hostname='localhost',
    port=27017)
