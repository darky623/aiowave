from datetime import datetime, date, timedelta
from aiohttp import web
import uuid
import os

from db import DatabaseConnection
db = DatabaseConnection()


async def register(data):
    response_data = []
    return web.json_response(response_data)


async def auth(data):
    response_data = []
    return web.json_response(response_data)


async def new_post(data):
    response_data = []
    return web.json_response(response_data)


async def delete_post(data):
    response_data = []
    return web.json_response(response_data)


async def all_posts(data):
    response_data = []
    return web.json_response(response_data)


async def like(data):
    response_data = []
    return web.json_response(response_data)


async def dislike(data):
    response_data = []
    return web.json_response(response_data)
