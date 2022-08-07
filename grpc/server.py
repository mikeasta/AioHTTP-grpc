import asyncio
import logging
import grpc
from settings import BACKEND_PORT
from utils.pb_handler import API_Server
from messages.msg_pb2_grpc import add_AioServiceServicer_to_server

async def serve() -> None:
    server = grpc.aio.server()
    add_AioServiceServicer_to_server(API_Server(), server)
    server.add_insecure_port(f'[::]:{BACKEND_PORT}')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    print(f'Server is running on port {BACKEND_PORT}.')
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())