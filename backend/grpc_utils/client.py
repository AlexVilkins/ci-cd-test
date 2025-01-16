import grpc
import asyncio
from grpc_utils.proto import bid_pb2, bid_pb2_grpc


class ClientGrpc:
    async def entry_request_iterator(self, url, type_mess):
        entry_request = bid_pb2.EntryCreateRequest(
            text=f"{url}",
            type_mess=f"{type_mess}"
        )
        yield entry_request

    async def start_stream(self, url, type_mess):
        async with grpc.aio.insecure_channel("localhost:50051") as channel:
            stub = bid_pb2_grpc.BidServiceStub(channel)

            async for entry_response in stub.createBulkEntries(self.entry_request_iterator(url, type_mess)):
                yield entry_response
