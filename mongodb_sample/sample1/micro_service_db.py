from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

import ConfigParser
import io
SAMPLE=True

def connect_database():
        try:
            # Load the configuration file
            with open("db.conf") as f:
                dbconf = f.read()
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(io.BytesIO(dbconf))
        except:
            raise RuntimeError('Can not read database config in db.conf file!')

        try:
            # Connect to MongoDB first. PyMODM supports all URI options supported by
            # PyMongo. Make sure also to specify a database in the connection string:
            connect('mongodb://' + config.get('mongodb', 'ip') + ':' + config.get('mongodb', 'port') + '/' + config.get('mongodb', 'database'))
            print('Connected to %s' % 'mongodb://' + config.get('mongodb', 'ip') + ':' + config.get('mongodb', 'port') + '/' + config.get('mongodb', 'database'))
        except:
            raise RuntimeError('Can not connect to %s!' % 'mongodb://' + config.get('mongodb', 'ip') + ':' + config.get('mongodb', 'port') + '/' + config.get('mongodb', 'database') )

if SAMPLE:
    ##### Model #####
    class User(MongoModel):
        email = fields.EmailField(primary_key=True)
        first_name = fields.CharField()
        last_name = fields.CharField()

    class Comment(EmbeddedMongoModel):
        author = fields.ReferenceField(User)
        content = fields.CharField()

    class Post(MongoModel):
        title = fields.CharField()
        author = fields.ReferenceField(User)
        revised_on = fields.DateTimeField()
        content = fields.CharField()
        comments = fields.EmbeddedDocumentListField(Comment)
        tags = fields.ListField(fields.CharField(max_length=20))
