import uuid
from aiohttp import web
import json


def url_exists(url):
    try:
        with open('db.json', 'r', encoding='utf-8') as file:
            history = json.load(file)
            return any(entry['original_url'] == url for entry in history)
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def create_history(data):
    try:
        with open('db.json', 'r', encoding='utf-8') as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(data)

    with open('db.json', 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


async def create_short_url(request):
    try:
        data = await request.json()
        url = data['url']
        short_prefix = uuid.uuid4().hex[:6]

        if url_exists(url):
            return web.json_response({'orig': url, 'Err': 'уже было'})

        context = {
            "original_url": url,
            "short_prefix": short_prefix
        }

        create_history(context)
        return web.json_response(context)

    except Exception as e:
        return web.json_response({'error': str(e)}, status=400)


async def get_full_url(request):
    try:
        shortlink = request.match_info['shortlink']

        with open('db.json', 'r', encoding='utf-8') as file:
            history = json.load(file)

        for entry in history:
            if entry.get('short_prefix') == shortlink:
                return web.json_response({'original_url': entry['original_url']})

        return web.json_response({'error': 'Ссылка не найдена'}, status=404)

    except Exception as e:
        return web.json_response({'error': str(e)}, status=400)


app = web.Application()
app.add_routes([web.post('/short', create_short_url)])
app.add_routes([web.get('/full/{shortlink}', get_full_url)])

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)