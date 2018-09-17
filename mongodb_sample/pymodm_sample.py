from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


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


connect('mongodb://127.0.0.1:27017/pymodm-test')

anhdv = User('user@email.com', last_name='Ross', first_name='Bob').save()
Post(
    # Since this is a ReferenceField, we had to save han_solo first.
    author=anhdv,
    title="Five Crazy Health Foods Jabba Eats.",
    content="...",
    tags=['alien health', 'slideshow', 'jabba', 'huts'],
    comments=[
        Comment(author=anhdv, content='Rrrrrrrrrrrrrrrr!'),
        Comment(author=anhdv, content='xxxxxxxxxxxxxxxx!'),
    ]
).save()


###### Access #####
# Find objects with a condition
slideshows = Post.objects.raw({'tags': 'slideshow', 'content': '...'})
print('Find an User with condition: ' + slideshows[0].title)

# Query all
for user in User.objects.all():
    print('Query all User table: ' + user.first_name + ' ' + user.last_name)

for post in Post.objects.all():
    print('Query all Post table: ' + post.title + ' - ' + post.author.first_name)
