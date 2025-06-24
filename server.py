# from aiohttp import web
# import json
#
#
# incriment = 0
#
#
# async def get_incriment(request):
#     try:
#         with open('db.json') as data:
#             data = json.load(data)
#             data_last = len(data)-1
#             data_show = data[data_last]
#             data_incriment = data_show['try']
#
#             context = {
#                 # 'data': data,
#                 # 'data_show': data_show,
#                 'data_incriment': data_incriment,
#             }
#             return web.json_response(context)
#     except FileNotFoundError:
#         return web.json_response({'error': 'database not found'})
#
#
# def create_history(data):
#     try:
#         with open('db.json', 'r', encoding='utf-8') as file:
#             history = json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         history = []
#
#     history.append(data)
#
#     with open('db.json', 'w', encoding='utf-8') as file:
#         json.dump(history, file, ensure_ascii=False, indent=4)
#
#
# async def calculate(request):
#     try:
#         data = await request.json()
#         a = float(data.get('a'))
#         b = float(data.get('b'))
#         operator = data.get('operator')
#
#         # get_incriment()
#
#         global incriment
#         incriment = incriment+1
#
#         if operator == '+':
#             result = a + b
#         elif operator == '-':
#             result = a - b
#         elif operator == '*':
#             result = a * b
#         elif operator == '/':
#             if b == 0:
#                 return web.json_response({'error': 'Деление на ноль'}, status=400)
#             result = a / b
#         else:
#             return web.json_response({'error': 'Неверный оператор'}, status=400)
#
#         context = {
#             'try': incriment,
#             'a': a,
#             'b': b,
#             'operator': operator,
#             'result': result,
#         }
#
#         create_history(context)
#
#         return web.json_response({'result': result, 'context': context}, status=200)
#
#     except Exception as e:
#         return web.json_response({'error': str(e)}, status=400)
#
#
# async def get_history(request):
#     try:
#         with open('db.json', 'r', encoding='utf-8') as file:
#             history = json.load(file)
#             if history:
#                 return web.json_response(history, status=200)
#             else:
#                 return web.json_response({}, status=404)
#     except Exception as e:
#         return web.json_response({'error': str(e)}, status=404)
#
#
# app = web.Application()
# app.add_routes([web.post('/calc', calculate)])
# app.add_routes([web.get('/history', get_history)])
# app.add_routes([web.get('/check', get_incriment)])
#
#
# if __name__ == '__main__':
#     web.run_app(app, host='127.0.0.1', port=8080)