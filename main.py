from aiohttp import web
import json

import functions

allow_functions = {
    "register": functions.register,
    "auth": functions.auth,
    "new_post": functions.new_post,
    "delete_post": functions.delete_post,
    "all_posts": functions.all_posts,
    "like": functions.like,
    "dislike": functions.dislike}


async def api_handler(request):
    func = request.query.get('func')
    if func in allow_functions:
        byte_str = await request.read()
        decoded_str = byte_str.decode('utf-8')
        try:
            data = json.loads(decoded_str)

        except json.decoder.JSONDecodeError as e:
            return web.Response(
                text='Raw does not contain JSON or it is broken.',
                status=404)

        response_data = await allow_functions[func](data)
        return response_data

    else:
        return web.Response(
            text='Function not supported',
            status=404)


async def setup():
    app = web.Application()
    app.router.add_get('/api', api_handler)
    app.router.add_post('/api', api_handler)
    return app

if __name__ == '__main__':
    web.run_app(
        setup(),
        host='localhost',
        port=80)
