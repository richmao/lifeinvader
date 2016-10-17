# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

db.define_table('user',
                Field('email', default=auth.user.email if auth.user_id else None),
                Field('first_name', 'text'),
                Field('last_name', 'text'),
                Field('follow_list', 'list:reference user'),
                Field('audience_list', 'list:reference user'),
                Field('image_list', 'list:reference image')
                )

db.define_table('image',
                Field('poster_id', 'reference user'),
                Field('image_content', 'upload'),
                Field('like_list', 'list:reference user'),
                Field('comment_list', 'list:reference comment'),
                Field('caption', 'text')
                )

db.define_table('comment',
                Field('content', 'text'),
                Field('commenter_id', 'reference user'),
                Field('image_id', 'reference image')
                )
# I don't want to display the user email by default in all forms.
db.user.email.readable = db.user.email.writable = False
db.post.id.readable = db.post.id.writable = False

# after defining tables, uncomment below to enable auditing
#auth.enable_record_versioning(db)
