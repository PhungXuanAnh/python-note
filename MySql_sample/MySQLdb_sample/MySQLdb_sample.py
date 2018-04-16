import MySQLdb

host = 'localhost'
user = 'root'
password = '1'
port = 3306
db = 'test'

conn = MySQLdb.Connect(
    host=host,
    user=user,
    passwd=password,
    port=port,
    db=db
)

# Example of how to insert new values:
conn.query("""INSERT INTO test VALUES ('xuananh1', 'test insert db')""")
conn.commit()

# Example of how to fetch table data:
conn.query("""SELECT * FROM test""")
result = conn.store_result()
for i in range(result.num_rows()):
    print(result.fetch_row())