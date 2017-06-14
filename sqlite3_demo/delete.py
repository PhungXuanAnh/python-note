'''
Created on Apr 7, 2017

@author: xuananh
'''

# The basic syntax of DELETE query with WHERE clause is as follows:

query = ''' DELETE FROM table_name
            WHERE [condition];
        '''
        
query = "DELETE FROM %s WHERE %s = '%s';" % (table, key, value)        
        
# If you have to select the id:

query = " DELETE FROM table WHERE id IN (SELECT id FROM somewhere_else) "

# If you already know them (and they are not in the thousands):

query = ' DELETE FROM table WHERE id IN (?,?,?,?,?,?,?,?) '
# or
args = (1,2,3,4,5)
query =  "DELETE FROM rows WHERE ids IN (%s);" % args

# You can also use BETWEEN if you have consecutive IDs :
query =  "DELETE from tablename WHERE id BETWEEN 1 AND 254;"

# You can of course limit for some IDs using other WHERE clause :
query =  "DELETE from tablename WHERE id BETWEEN 1 AND 254 AND id<>10;"