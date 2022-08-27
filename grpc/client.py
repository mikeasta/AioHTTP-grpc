import logging
from aiohttp import web
from utils.pb_handler import API_Client
from utils.bytes2image import bytes2image
from aiohttp_healthcheck import HealthCheck, EnvironmentDump
import settings

app    = web.Application()
routes = web.RouteTableDef()
client = API_Client(f"{settings.BACKEND_HOST}:{settings.BACKEND_PORT}")

health = HealthCheck()
app.router.add_get("/healthcheck", health)

def health_check():
    return True, "Ping ok"

health.add_check(health_check)

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
    # Request raw pattern
    # { "data": "string"}

    req_body = await request.json()
    result  = await StringRequest(req_body['data'])
    logging.info(result)
    return web.json_response({'result': result}, status=200)

@routes.get('/ndarray/')
async def ndarray_get_request(request):
    # Request raw pattern
    # { "data": array }

    req_body = await request.json()
    result = await NDArrayRequest(req_body['data'])
    result = result.tolist()
    logging.info(result)
    return web.json_response({'result': result}, status=200)

@routes.get('/image/')
async def image_get_request(request):
    result = await ImageRequest()
    [width, height, image_data] = result
    bytes2image(image_data) # Image downloading
    logging.info(f'Width: {width}, height: {height}')
    return web.json_response({'result': {'width' : width, 'height': height}}, status=200)

app.add_routes(routes)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, port=settings.FRONTEND_PORT)