import grpc

from AsyncQueue import AsyncQueue
from grpc_utils.to_fast import bid_pb2, bid_pb2_grpc
import asyncio


class ExampleServiceServicer(bid_pb2_grpc.MessageAddService):
    def __init__(self, queue: AsyncQueue):
        self.queue = queue

    async def SendMessage(self, request, context):
        print(f"Received: {request.user_id} {request.url}, {request.type_mess}")
        url = request.url
        user_id = request.user_id
        position = await self.queue.add_to_queue_from_browser(url=url, user_id=user_id)
        if isinstance(position, int):
            return bid_pb2.MessageFromPyro(text=f"{position}",
                                           type_mess=f"success")
        else:
            return bid_pb2.MessageFromPyro(text=f"{position}",
                                           type_mess=f"error")
        print("res")



async def serve(queue: AsyncQueue):
    server = grpc.aio.server()
    bid_pb2_grpc.add_MessageAddServiceServicer_to_server(ExampleServiceServicer(queue), server)
    server.add_insecure_port('[::]:50052')
    await server.start()
    print("Server started on port 50052")
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())