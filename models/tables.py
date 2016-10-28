# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

# db.define_table('lifeinvader_user',
#                 Field('email', default=auth.user.email if auth.user_id else None),
#                 Field('li_id', default=auth.user_id if auth.user_id else None),
#                 Field('first_name', 'text'),
#                 Field('username', default=auth.user.username if auth.user.username else None),
#                 # We follow
#                 Field('follow_list', 'list:reference lifeinvader_user'),
#                 # They follow us
#                 Field('audience_list', 'list:reference lifeinvader_user'),
#                 Field('image_list', 'list:reference image')
#                 )
import datetime


db.define_table('image',
                #Field('poster_id', default=auth.user.email if auth.user_id else None),
                Field('poster_id', 'reference auth_user'),
                Field('image_content', 'upload'),
                #Field('like_list', 'list:reference auth_user'),
                #Field('comment_list', 'list:reference post_comment'),
                Field('caption', 'text'),
                Field('posted_on','datetime', update=datetime.datetime.utcnow()),
                )

db.define_table('post_comment',
                Field('comment_content', 'text'),
                Field('commenter_id', 'reference auth_user'),
                Field('image_id', 'reference image')
                )

db.image.poster_id.readable = db.image.poster_id.writable = False
db.image.posted_on.readable = db.image.posted_on.writable = False
db.image.poster_id.requires = IS_IN_DB(db, 'auth_user.id', '%(username)s')
# I don't want to display the user email by default in all forms.
#db.lifeinvader_user.email.readable = db.lifeinvader_user.email.writable = False
#db.lifeinvader_user.id.readable = db.lifeinvader_user.id.writable = False


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
