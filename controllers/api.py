# These are the controllers for your ajax api.
import time

def index():
    pass

def get_posts():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    # Implement me!
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # We just generate a lot of of data.
    posts = []
    has_more = False
    rows = db().select(db.post.ALL, orderby=~db.post.created_on, limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            t = dict(
                id=r.id,
                user_email=r.user_email,
                post_content=r.post_content,
                created_on=r.created_on,
                updated_on=r.updated_on,
            )
            posts.append(t)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,
    ))


# Note that we need the URL to be signed, as this changes the db.
@auth.requires_signature()
def add_post():
    """Here you get a new post and add it.  Return what you want."""
    p_id = db.post.insert(
        #user_email=auth.user.email,
        post_content=request.vars.post_content,
        #created_on=datetime.datetime.utcnow(),
        #updated_on=datetime.datetime.utcnow(),
    )
    p = db.post(p_id)
    return response.json(dict(post = p))


@auth.requires_signature()
def del_post():
    """Used to delete a post."""
    db(db.post.id == request.vars.post_id).delete()

@auth.requires_signature()
def edit_post():
    """Used to edit a post."""
    db.post(request.vars.post_id).update_record(
        post_content=request.vars.post_content,
        updated_on=datetime.datetime.utcnow(),
        )
    p = db.post(request.vars.post_id).updated_on;
    return response.json(dict(updated_on=p))