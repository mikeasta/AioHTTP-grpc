import logging
from aiohttp import web
from utils.pb_handler import API_Client
from utils.bytes2image import bytes2image
import settings

app    = web.Application()
routes = web.RouteTableDef()
client = API_Client(f"{settings.BACKEND_HOST}:{settings.BACKEND_PORT}")

# Async data request commands
async def StringRequest(msg):
    return client.StringRequest(msg)

async def NDArrayRequest(array):
    return client.NDArrayRequest(array)

async def ImageRequest():
    return client.ImageRequest()

# Routes
@routes.get('/')
async def home(request):
    logging.info("Hello World!")
    return web.json_response({'result': "Hello World!"}, status=200)

@routes.get('/string/')
async def string_get_request(request):
    result = await StringRequest("This is string request")
    logging.info(result)
    return web.json_response({'result': "This is string request"}, status=200)

@routes.get('/ndarray/')
async def ndarray_get_request(request):
    result = await NDArrayRequest([[1, 2], [3, 4]])
    result = result.tolist()
    logging.info(result)
    return web.json_response({'result': result}, status=200)

@routes.get('/image/')
async def image_get_request(request):
    result = await ImageRequest()
    [width, height, image_data] = result
    bytes2image(image_data) # Image downloading
    return web.json_response({'result': {'width' : width, 'height': height}}, status=200)

app.add_routes(routes)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, port=settings.FRONTEND_PORT)