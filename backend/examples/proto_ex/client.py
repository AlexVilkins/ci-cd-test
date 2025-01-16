import grpc
from examples.proto_ex import ex_pb2_grpc, ex_pb2
import asyncio

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = ex_pb2_grpc.MessageAddServiceStub(channel)
        request = ex_pb2.MessageSendData(user_id="Hello, gRPC!")
        print(f"send user_id=Hello, gRPC!")
        response = await stub.SendMessage(request)  # Асинхронный вызов
        print(f"Response from server: {response.text}")

if __name__ == '__main__':
    asyncio.run(run())
