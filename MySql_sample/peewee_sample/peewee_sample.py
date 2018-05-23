import peewee
myDB = peewee.MySQLDatabase('test', host='localhost', port = 3306, user='root', passwd='1')

class MySqlModel(peewee.Model):
    class Meta:
        database = myDB
        
class Book(MySqlModel):
    author = peewee.CharField()
    title = peewee.TextField()
    
# Book.create_table()
# book = Book(author="xuananh1", title='test\'xuananh1')
# book.save()
# for book in Book.filter(author="xuananh"):
#     print book.title    

class Tbl_Sample(MySqlModel):
    id = peewee.AutoField(primary_key=True)
    name = peewee.TextField()
    
class Tbl_Output(MySqlModel):
    id = peewee.AutoField(primary_key=True)
    name = peewee.TextField()

Tbl_Sample.create_table()

# for i in range(1,10):
#     Tbl_Sample(id = i, name=str(123 + i)).save(force_insert=True)
#     
# for name in Tbl_Sample.filter(id=4):
#     print name.name

# for name in Tbl_Sample.select().where(Tbl_Sample.id >= 3, Tbl_Sample.id <= 8):
#     print (name.id)

for name in Tbl_Sample.select():
    print (name.id)

# for name in Tbl_Sample.select().limit(4):
#     print (name.id)

# for name in Tbl_Sample.select().limit(2).offset(0):
#     print name.name

# expression =  (peewee.fn.Lower(peewee.fn.Substr(Tbl_Sample.name, 1, 1)) == 'x')     
# for name in Tbl_Sample.select().limit(2).offset(0).where(expression):
#     print name.name
#     
# for name in Tbl_Sample.select(peewee.fn.Upper(Tbl_Sample.name)).limit(2).offset(0):
#     print name.name

# for name in Tbl_Sample.select().columns(Tbl_Sample.id).limit(4):
#     print (name.id)

# for name in Tbl_Sample.select().columns(Tbl_Sample.id).paginate(2,4):
#     print (name.id)

# for name in Tbl_Sample.select().paginate(page=3, paginate_by=2):
#     print (name.id)

# fields = [Tbl_Sample.id, Tbl_Sample.name]
# # rows = [(1, "123"), (2, "124"), (3, "125"), 
# #         (4, "126"), (5, "127"), (6, "128"), 
# #         (7, "129"), (8, "130"), (9, "131")]
# rows = [(1, "1"), (2, "2"), (3, "3"), 
#         (4, "4"), (5, "5"), (6, "6"), 
#         (7, "7"), (8, "8"), (9, "9")]
# Tbl_Sample.replace_many(rows, fields).execute()
    
    
    