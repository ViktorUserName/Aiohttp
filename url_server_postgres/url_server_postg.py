import uuid
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise
from config import TORTOISE_ORM
from models import URL



async def create_short_url(request):
    try:
        data = await request.json()
        original_url = data.get("original_url")
        short_url = uuid.uuid4().hex[:6]

        existing = await URL.get_or_none(original_url=original_url)
        if existing:
            return web.json_response({
                "short": existing.short_url,
                "original_url": existing.original_url,
                "message": "уже было"
            })

        url = await URL.create(original_url=original_url, short_url=short_url)

        return web.json_response({
            "short": url.short_url,
            "original_url": url.original_url
        })
    except Exception as e:
        return web.json_response({'error': str(e)}, status=400)

async def get_long_url_by_short(request):
    try:
        short_code = request.match_info.get("short_url")
        short_url = await URL.get_or_none(short_url=short_code)

        if not short_url:
            return web.json_response({'error': 'нету'})

        url_obj = await URL.get_or_none(short_url=short_code)
        if not url_obj:
            return web.json_response({'error': 'URL not found'}, status=404)
        return web.json_response({"long_url": url_obj.original_url})

    except Exception as e:
        return web.json_response({'error': str(e)}, status=400)

def server():
    app = web.Application()

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
    )

    app.add_routes([web.post('/short/', create_short_url)])
    app.add_routes([web.get('/long/{short_url}', get_long_url_by_short)])

    return app

if __name__ == '__main__':
    web.run_app(server(), host='127.0.0.1', port=8080)