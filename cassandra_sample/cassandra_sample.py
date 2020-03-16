from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# NOTE: reference: https://docs.datastax.com/en/developer/python-driver/3.22/getting_started/
def cassandra_conn(db_name):
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['127.0.0.1'], port=9042, auth_provider=auth_provider)
    if not db_name:
        session = cluster.connect()
    else:
        session = cluster.connect(db_name)
    return session, cluster


if __name__ == "__main__":
    db_name = None
    print(cassandra_conn(db_name))
