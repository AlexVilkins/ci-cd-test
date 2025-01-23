import logging

import grpc

from grpc_utils.proto_ws import ws_pb2_grpc, ws_pb2
import asyncio

from redis_utils.RedisManager import redis_connection


class ExampleServiceServicer(ws_pb2_grpc.MessageWsService):
    async def SendMessage(self, request, context):
        user_id = request.user_id
        print(request)
        value = {
            "text": request.text,
            "type_mess": request.type_mess
        }
        await redis_connection.add_value(user_id, value)
        return ws_pb2.MessageFromBack(text=f"OK")



async def serve():
    server = grpc.aio.server()
    ws_pb2_grpc.add_MessageWsServiceServicer_to_server(ExampleServiceServicer(), server)
    server.add_insecure_port('[::]:50053')
    await server.start()
    print("Server started on port 50053")
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())