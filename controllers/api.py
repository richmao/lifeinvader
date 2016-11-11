# These are the controllers for your ajax api.
def index():
    pass

def get_posts():
    start_index = int(request.vars.start_index) if request.vars.start_index is not None else 0
    end_index = int(request.vars.end_index) if request.vars.end_index is not None else 0
    posts = []
    has_more = False
    rows = db().select(db.post.ALL, limitby=(start_index, end_index + 1), orderby=~db.post.created_on)
    for i, r in enumerate(rows):
        if i < end_index - start_index:
            p = dict(
                id=r.id,
                post_content = r.post_content,
                created_on=r.created_on,
                updated_on=r.updated_on,
                author=r.author
            )
            posts.append(p)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more
    ))


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