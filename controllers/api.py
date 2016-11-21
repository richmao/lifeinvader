# These are the controllers for your ajax api.
def index():
    pass


# Note that we need the URL to be signed, as this changes the db.
@auth.requires_signature()
def add_post():
    post_id = db.post.insert(
        post_content = request.vars.post_content
        # I should have put author here, but I
        # handled it in tables.py
    )
    p = db.post(post_id)
    return response.json(dict(post=p))

def edit_post():
    #db(db.post.id == request.vars.post_id).update(post_content=vars.request.post_content)
    p = db.post(request.vars.post_id)
    p.post_content = request.vars.post_content
    p.update_record()

@auth.requires_signature()
def del_post():
    db(db.post.id == request.vars.post_id).delete()

def do_search():
    users = request.vars.form_search_content
    query = db.auth_user.username.contains(users)
    people = db(query).select()

def get_people():
    start_index = int(request.vars.start_index) if request.vars.start_index is not None else 0
    end_index = int(request.vars.end_index) if request.vars.end_index is not None else 0
    people = []
    has_more = False
    rows = db().select(db.auth_user.ALL, limitby=(start_index, end_index + 1), orderby=db.auth_user.username)
    for i, r in enumerate(rows):
        if i < end_index - start_index:
            p = dict(
                id=r.id,
                first_name=r.first_name,
                last_name=r.last_name,
                username=r.username,
                email=r.email
            )
            people.append(p)
        else:
            has_more = True
    return response.json(dict(
        people=people,
        has_more=has_more
    ))

def toggle_like():
    i = db(db.image.id == request.vars.image_id).select().first()
    list = i.like_list
    if request.vars.username not in list:
        list = i.like_list + [request.vars.username]
    else:
        list.remove(request.vars.username)
    i.update_record(
        like_list=list,
    )

def toggle_follow():
    user = db(db.auth_user.username == request.vars.username).select().first()
    add = db(db.auth_user.username == request.vars.add_user).select().first()

    aud_list = user.audience_list
    fol_list = add.follow_list

    if request.vars.add_user not in aud_list:
        aud_list = user.audience_list + [request.vars.add_user]
        fol_list = add.follow_list + [request.vars.username]
    else:
        aud_list.remove(request.vars.add_user)
        fol_list.remove(request.vars.username)
    user.update_record(
        audience_list=aud_list,
    )

    add.update_record(
        follow_list=fol_list,
    )

def get_comments():
    comments = []
    rows = db().select(db.image_comment.ALL, orderby=db.image_comment.posted_on)
    for i, r in enumerate(rows):
        p = dict(
            id=r.id,
            comment_content=r.comment_content,
            commenter=r.commenter,
            image_id=r.image_id,
            posted_on=r.posted_on
        )
        comments.append(p)
    return response.json(dict(
        comments=comments
    ))

@auth.requires_signature()
def add_comment():
    comment_id = db.image_comment.insert(
        comment_content=request.vars.comment_content,
        image_id = request.vars.image_id,
        commenter = auth.user.username if auth.user_id else None
    )

    # i = db(db.image.id == request.vars.image_id).select().first()
    # list = i.comment_list
    #
    # if request.vars.username not in list:
    #     list = i.comment_list + [comment_id]
    #
    # i.update_record(
    #     comment_list=list,
    # )

    c = db.image_comment(comment_id)
    return response.json(dict(comment=c))