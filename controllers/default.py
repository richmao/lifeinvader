# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    images = db().select(db.image.ALL, orderby=~db.image.posted_on, limitby=(0, 20))
    return dict(get_username_from_email = get_username_from_email, get_firstname_from_email = get_firstname_from_email,
                get_screenname=get_screenname, images = images)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

def get_username_from_email(email):
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])

def get_firstname_from_email(email):
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return u.first_name

def get_screenname(email):
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return u.username


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def profile():
    query = db.image.author == auth.user.email
    images = db(query).select(orderby=~db.image.posted_on, limitby=(0, 20))
    return dict(get_screenname=get_screenname, get_firstname_from_email=get_firstname_from_email,
                images=images)

@auth.requires_login()
def upload():
    form = SQLFORM(db.image)
    if form.process().accepted:
        session.flash = T('Image Posted.')
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def search():
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        tokens = form.vars.name.split()
        query = reduce(lambda a,b:a&b,
                       [db.auth_user.username.contains(k)|db.auth_user.last_name.contains(k)|db.auth_user.first_name.contains(k) \
                            for k in tokens])
        people = db(query).select(orderby=db.auth_user.first_name)
    else:
        people = []
    q = db.follow.follower == auth.user.email
    followlist = db(q).select()
    return locals()

def follow():
    if request.env.request_method!='POST': raise HTTP(400)
    if request.args(0) == 'follow' and not db.follow(follower=auth.user.email, followee = request.args(1)):
        db.follow.insert(follower = auth.user.email, followee=request.args(1))
    elif request.args(0)=='unfollow':
        db(db.follow.follower==auth.user.email)(db.follow.followee==request.args(1)).delete()

