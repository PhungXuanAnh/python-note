'''
Created on Mar 21, 2017

@author: xuananh
'''
import sqlite3

con = sqlite3.connect('test.db')

c = con.cursor()
# c.execute("DROP TABLE A;")

#computing values
Col1, Col2, Col3, Col4, Byte = ('1234', 2, '5678', 'qwerty', 'bytestr')

c.execute("""CREATE TABLE IF NOT EXISTS A
    (id INTEGER PRIMARY KEY,
    Col1 TEXT,
    Col2 INTEGER,
    Col3 TEXT,
    Col4 TEXT,
    Byte TEXT);""")


# Insert data into A
c.execute("""INSERT INTO A
                (Col1, Col2, Col3, Col4, Byte) VALUES (?, ?, ?, ?, ?)""",
                (Col1, Col2, Col3, Col4, Byte))

c.execute('SELECT * FROM A;')

print (c.fetchall()) #[(1, u'1234', 2, u'5678', u'qwerty', u'bytestr')]