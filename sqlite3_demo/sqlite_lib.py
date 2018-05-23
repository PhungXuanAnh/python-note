#!/usr/bin/python
import os.path
import json
import sqlite3
import os

HOME_DIR = os.path.expanduser('~')
home_folder = os.environ.get('HOME', None)
if home_folder == None:
    user_name = os.environ.get('USER', None)
    if user_name == None:
        raise ValueError('Can not get home folder.')
    else:
        validium_database = '/home/' + user_name + '/.validium/validium.db'
else:
    validium_database = home_folder + '/.validium/validium.db'

create_deployment_table = '''CREATE TABLE if not exists deployment
    (
    deployment_id  TEXT    PRIMARY KEY     NOT NULL,
    plugin_id      TEXT    NOT NULL,
    mano_ip        TEXT    NOT NULL
    );'''
    
create_server_table = '''CREATE TABLE if not exists servers
    (
    context_id     TEXT    NOT NULL,
    server_name    TEXT    NOT NULL,
    context_name   TEXT,
    user           TEXT,
    ip             TEXT,
    private_ip     TEXT,
    port           INT,
    key_filename   TEXT,
    password       TEXT,
    vnf_type       TEXT,
    PRIMARY KEY (context_id, server_name)
    );'''
    
create_plugin_table = '''CREATE TABLE if not exists plugin
    (
    plugin_id           TEXT    PRIMARY KEY     NOT NULL,
    plugin_file_name    TEXT
    );'''
    
create_mano_table = '''CREATE TABLE if not exists mano
    (
    mano_ip        TEXT    PRIMARY KEY     NOT NULL,
    mano_user      TEXT,
    mano_password  TEXT,
    mano_keypair   TEXT
    );'''

class SqlLite:
    @staticmethod
    def init(database_name):    
        global conn
        global c
        conn = sqlite3.connect(database_name, check_same_thread=False)
        c = conn.cursor()
        SqlLite.create_database()

    @staticmethod
    def create_database():
        c.execute(create_deployment_table)
        c.execute(create_server_table)
        c.execute(create_plugin_table)
        #c.execute(create_mano_table)
        conn.commit()
        print ("Tables created successfully")

    @staticmethod
    def drop_database():
        c.execute('drop table deployment')
        c.execute('drop table servers')
        c.execute('drop table plugin')
        #c.execute('drop table mano')
        conn.commit()
        print ("Tables dropped successfully")

    @staticmethod
    def insert_table(tbl, row):
        keys = []
        values = []
        for key, value in row.iteritems():
            keys.append(str(key))
            values.append(str(value))

        sql = "INSERT OR IGNORE INTO %s (%s) VALUES (%s)" % (tbl, str(keys)[1:-1], \
                                                   str(values)[1:-1])
        print (sql)
        c.execute(sql)
        conn.commit()

    @staticmethod
    def query(keys, tbls, cond):
        results = []
        slt = ','.join(str(e) for e in keys)
        frm = ','.join(str(e) for e in tbls)
        sql = "SELECT %s from %s" % (slt, frm)
        if cond:
            sql += " where %s" % cond
        c.execute(sql)
        rows = c.fetchall()
        # convert sql query result into map
        for row in rows:
            r = {}
            for i, val in enumerate(row):
                r[keys[i]] = val
            results.append(r)
        return results
        
    @staticmethod
    def delete_record1(table, key_value):
        # this method remove a record with conditions are (keys, values) 
        # were specified in key_value dictionary
        conn.text_factory = str
        list_cond = []
        separator = ' AND '
#         query = "DELETE FROM %s WHERE %s = '%s';" % (table, key, value)
        query = "DELETE FROM %s WHERE " % (table)
        for key, value in key_value.iteritems():
            
            list_cond.append("%s = '%s' " % ( key, value))
            
        list_cond = separator.join(list_cond)
        
        query = query + list_cond + ';'
        print(query)
        c.execute(query)
        conn.commit()
        
    @staticmethod
    def delete_record2(tbls, cond): 
        # this method remove all tables that suit with cond condition 
        frm = ','.join(str(e) for e in tbls)
        sql = "DELETE from %s" % frm
        if cond:
            sql += " where %s" % cond
        c.execute(sql)
        conn.commit()
        
if __name__ == '__main__':
    '''Note: with column has attribute NOT NULL, it must be have in table which is inserted to table,
    if not this table will be IGNORE 
    for example context_id and server_name in servers table''' 
        
    SqlLite.init(validium_database)
    
#     SqlLite.insert_table('servers', {"context_id":"tester1111", "server_name":"tester", "user":"123456"})
#     SqlLite.insert_table('servers', {"context_id":"tester1121", "server_name":"tester12", "user":"1234562"})
    
    
    queryData =  SqlLite.query(['context_id', 'server_name', 'user', 'ip', 'private_ip', 'password', 'key_filename'], ['servers'], "")
#     queryData =  SqlLite.query(['context_id', 'server_name', 'user', 'ip', \
#                                 'private_ip', 'password', 'key_filename'], ['servers'], \
#                                "context_id = 'heat555'")
    print (json.dumps(queryData, indent=4, sort_keys=True))

#     SqlLite.delete_record('servers', {"context_id":"tester1121", "server_name":"tester12", "user":"1234562"})
    
    c.close()




