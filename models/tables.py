import datetime


db.define_table('image',
                Field('author', default=auth.user.username if auth.user_id else None),
                Field('image_content', 'upload', label = 'Image'),
                Field('like_list', 'list:string', default = []),
                Field('comment_list', 'list:integer'),
                Field('caption', 'text'),
                Field('posted_on','datetime', default=datetime.datetime.utcnow()),
                )

db.define_table('image_comment',
                Field('comment_content', 'text'),
                Field('commenter', 'string'),
                Field('image_id', 'integer'),
                Field('posted_on','datetime', default=datetime.datetime.utcnow()),
                )

db.image.posted_on.readable = db.image.posted_on.writable = False
db.image.author.readable = db.image.author.writable = False
db.image.like_list.readable = db.image.like_list.writable = False