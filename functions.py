from datetime import datetime, date, timedelta
from aiohttp import web
import uuid

max_length = {
    "nickname": 16,
    "password": 16,
    "firstname": 16,
    "surname": 16,
    "city": 16,
    "website": 120,
    "text": 120}

datetime_format = '%d/%m/%Y %H:%M:%S'

token_life = timedelta(minutes=15)


def get_auth_token(db, user_id):
    today = datetime.now()
    token = str(uuid.uuid1())
    db.create("auth", {
        "user_id": user_id,
        "token": token,
        "date_create": today.strftime(datetime_format)})

    return [{"token": token}]


def check_auth_token(db, token):
    today = datetime.now()
    session = db.read('auth', {"token": token})
    if auth:
        create_date = datetime.strptime(session[0][3], datetime_format)
        time_diff = today - create_date
        if time_diff < token_life:
            return session[0][1]
        else:
            return None


async def register(db, data):
    nickname = data.get("nickname")
    password = data.get("password")
    password_repeat = data.get("password_repeat")

    if nickname and password and password_repeat:
        same_nickname = db.read('users', {"nickname": nickname})

        if not same_nickname:
            if password == password_repeat:
                del data["password_repeat"]

                for key, value in data.items():
                    if key in max_length:
                        if len(value) > max_length[key]:
                            return web.Response(
                                text=f"Character limit exceeded in {key} field (max.{max_length[key]})",
                                status=404)
                    else:
                        return web.Response(
                            text=f"This field is not expected ({key})",
                            status=404)

                user_id = db.create("users", data)
                return web.json_response(get_auth_token(db, user_id))

            else:
                return web.Response(
                    text="Password mismatch",
                    status=404)

        else:
            return web.Response(
                text="Nickname is already taken",
                status=404)

    else:
        return web.Response(
            text="Required fields are not filled in",
            status=404)


async def auth(db, data):
    nickname = data.get("nickname")
    password = data.get("password")
    if nickname and password:
        for key, value in data.items():
            if key in max_length:
                if len(value) > max_length[key]:
                    return web.Response(
                        text=f"Character limit exceeded in {key} field (max.{max_length[key]})",
                        status=404)
            else:
                return web.Response(
                    text=f"This field is not expected ({key})",
                    status=404)

        user = db.read('users', data)
        if user:
            return web.json_response(get_auth_token(db, user[0][0]))

        else:
            return web.Response(
                text=f"User does not exist",
                status=404)

    else:
        return web.Response(
            text="Required fields are not filled in",
            status=404)


async def new_post(db, data):
    token = data.get("token")
    text = data.get("text")
    if token and text:
        user_id = check_auth_token(db, token)
        if user_id:
            del data["token"]
            for key, value in data.items():
                if key in max_length:
                    if len(value) > max_length[key]:
                        return web.Response(
                            text=f"Character limit exceeded in {key} field (max.{max_length[key]})",
                            status=404)
                else:
                    return web.Response(
                        text=f"This field is not expected ({key})",
                        status=404)

            today = datetime.now()
            post_id = db.create('posts', {
                "user_id": user_id,
                "text": text,
                "date_create": today.strftime(datetime_format),
                "status": "active"})

            response_data = [{"post_id": post_id}]
            return web.json_response(response_data)

        else:
            return web.Response(
                text="Authorisation Error",
                status=404)

    else:
        return web.Response(
            text="Required fields are not filled in",
            status=404)


async def delete_post(db, data):
    token = data.get("token")
    post_id = data.get("post_id")
    if token and post_id:
        user_id = check_auth_token(db, token)
        if user_id:
            post = db.read("posts", {"id": post_id, "user_id": user_id})
            if post:
                db.update("posts", post_id, {"status": "deleted"})
                response_data = [{"status": "Successfully deleted"}]
                return web.json_response(response_data)
            else:
                return web.Response(
                    text="Post not found",
                    status=404)

        else:
            return web.Response(
                text="Authorisation Error",
                status=404)

    else:
        return web.Response(
            text="Required fields are not filled in",
            status=404)


async def all_posts(db, data):
    token = data.get("token")
    if token:
        user_id = check_auth_token(db, token)
        if user_id:
            response_data = []
            posts = db.read("posts", {"status": "active"})
            for post in posts:
                user_like_status = False
                likes = db.read("likes", {"post_id": post[0], "status": True})
                for user_like in likes:
                    if user_like[1] == user_id:
                        user_like_status = True

                author = db.read("users", {"id": post[1]})
                response_data.append({
                    "post_id": post[0],
                    "author_id": post[1],
                    "author_name": author[0][1],
                    "text": post[2],
                    "date_create": post[3],
                    "likes": len(likes),
                    "user_like": user_like_status
                })

            return web.json_response(response_data)

        else:
            return web.Response(
                text="Authorisation Error",
                status=404)

    else:
        return web.Response(
            text="Required fields are not filled in",
            status=404)


async def like(db, data):
    token = data.get("token")
    post_id = data.get("post_id")
    if token and post_id:
        user_id = check_auth_token(db, token)
        if user_id:
            post = db.read("posts", {"id": post_id})
            if post:
                if post[0][1] != user_id:
                    user_like = db.read("likes", {
                        "user_id": user_id,
                        "post_id": post_id})

                    if user_like:
                        user_like_status = not (int(user_like[0][3]) == 1)
                        user_like_id = user_like[0][0]
                        db.update("likes", user_like_id, {"status": user_like_status})

                    else:
                        user_like_status = True
                        db.create("likes", {
                            "user_id": user_id,
                            "post_id": post_id,
                            "status": user_like_status})

                    response_data = [{"post_id": post_id, "user_like": user_like_status}]
                    return web.json_response(response_data)

                else:
                    return web.Response(
                        text="You can't like yourself",
                        status=404)

            else:
                return web.Response(
                    text="Post not found",
                    status=404)

        else:
            return web.Response(
                text="Authorisation Error",
                status=404)

    else:
        return web.Response(
            text="Required fields are not filled in",
            status=404)
