import grpc
from grpc_utils.proto_ws import ws_pb2_grpc, ws_pb2
import asyncio

def run():
    channel = grpc.insecure_channel(f'localhost:50053')
    stub = ws_pb2_grpc.MessageWsServiceStub(channel)
    response = stub.SendMessage(ws_pb2.MessageSendPyro(user_id="dsdfsf",
                                                      text=f"sdsdffds",
                                                      type_mess="video_info"))
    print(response)

if __name__ == '__main__':
    run()
