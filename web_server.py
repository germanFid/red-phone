import asyncio
from functools import partial
from aiohttp import web
from queue import Queue

async def handle_get(request, id_queue:Queue):
    discord_id = request.query.get("discord_id")
    if not discord_id:
        return web.Response(text="Error: discord_id is required", status=400)
    
    print(f'Получен discord_id: {discord_id}')
    # recieved_ids.append(discord_id)
    id_queue.put(discord_id)

    return web.Response(text=f'Recieved {discord_id}')

async def start_webserver(id_queue:Queue, address='localhost', port='8000'):
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

async def main():
    recieved_ids = Queue()
    server_task = asyncio.create_task(start_webserver(recieved_ids))

    while True:
        await asyncio.sleep(10)
        if not recieved_ids.empty():
            print(f'IDs: {recieved_ids.get()}')
        else:
            print(f'Queue empty!')

if __name__ == '__main__':
    asyncio.run(main())
