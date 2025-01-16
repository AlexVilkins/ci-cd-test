import logging

import grpc

from grpc_utils.proto_ws import ws_pb2_grpc, ws_pb2
import asyncio


class ExampleServiceServicer(ws_pb2_grpc.MessageWsService):
    async def SendMessage(self, request, context):
        user_id = request.user_id
        text = request.text
        type_mess = request.type_mess
        match type_mess:
            case "query_pos":
                logging.info(text)
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