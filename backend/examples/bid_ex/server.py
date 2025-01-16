import asyncio
import grpc

from grpc_utils.proto import bid_pb2_grpc, bid_pb2

class SampleServiceServicer(bid_pb2_grpc.BidServiceServicer):
    async def createBulkEntries(self, request_iterator, context):
        async for request_it in request_iterator:
            request = request_it
            print(request.text)
            print(request.type_mess)
        percent = 0
        for _ in range(5):
            entry_info = {
                "text": f"{percent}",
                "type_mess": "status",
            }
            await asyncio.sleep(1)
            percent += 20
            yield bid_pb2.EntryResponse(**entry_info)

async def serve():
    server = grpc.aio.server()

    bid_pb2_grpc.add_BidServiceServicer_to_server(SampleServiceServicer(), server)

    server.add_insecure_port("localhost:50051")
    await server.start()
    print("Started gRPC server: 0.0.0.0:50051")
    await server.wait_for_termination()


asyncio.run(serve())