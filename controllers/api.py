# These are the controllers for your ajax api.
import time

def index():
    pass

def get_images():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    # Implement me!
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # We just generate a lot of of data.
    images = []
    has_more = False
    rows = db().select(db.image.ALL, orderby=~db.image.created_on, limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            t = dict(
                id=r.id,
                user_email=r.user_email,
                like_list=r.like_list,
                created_on=r.created_on,
            )
            images.append(t)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        images=images,
        logged_in=logged_in,
        has_more=has_more,
    ))


def unlike_image():
    i = db(db.image.id == request.vars.image_id).select().first()
    list = i.like_list
    if request.vars.username in list: list.remove(request.vars.username)
    i.update_record(
        like_list=list,
    )

def like_image():
    i = db(db.image.id == request.vars.image_id).select().first()
    list = i.like_list
    if request.vars.username not in list:
        list = i.like_list + [request.vars.username]
    i.update_record(
        like_list=list,
    )