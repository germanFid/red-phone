"""Module for creating and working with server"""
import asyncio
from functools import partial
from queue import Queue
from aiohttp import web

async def handle_get(request, id_queue:Queue):
    """async function for processing requests"""
    discord_id = request.query.get("discord_id")
    if not discord_id:
        return web.Response(text="Error: discord_id is required", status=400)
    print(f'Получен discord_id: {discord_id}')
    # recieved_ids.append(discord_id)
    id_queue.put(discord_id)
    return web.Response(text=f'Recieved {discord_id}')

async def start_webserver(id_queue:Queue, address='localhost', port='8000'):
    """async function for starting web server"""
    app = web.Application()

    handler_w_args = partial(handle_get, id_queue=id_queue)

    app.router.add_get("/", handler_w_args)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()
    print(f"Сервер запущен на {address}:{port}")

    while True:
        await asyncio.sleep(3600)
