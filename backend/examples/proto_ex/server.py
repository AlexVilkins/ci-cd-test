import grpc
from grpc_utils.proto import bid_pb2, bid_pb2_grpc
import asyncio

class ExampleServiceServicer(bid_pb2_grpc.MessageAddService):
    async def SendMessage(self, request, context):
        print(f"Received: {request.user_id} {request.url}, {request.type_mess}")
        """
        some process
        """
        await asyncio.sleep(2)
        return bid_pb2.MessageFromPyro(text="Success URL",
                                      type_mess="OK")

async def serve():
    server = grpc.aio.server()
    bid_pb2_grpc.add_MessageAddServiceServicer_to_server(ExampleServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Server started on port 50051")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
