from app.storage import load_data, save_data


posts = load_data("posts.json")


def get_next_post_id():
    return max(
        [post["post_id"] for post in posts],
        default=0
    ) + 1


def create_post(post_data):
    post = post_data.model_dump()
    post["post_id"] = get_next_post_id()

    posts.append(post)

    save_data("posts.json", posts)

    return post


def get_all_posts():
    return posts


def get_post_by_id(post_id):
    return next(
        (
            post for post in posts
            if post["post_id"] == post_id
        ),
        None
    )
