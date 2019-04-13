from concurrent import futures
import time
import logging

import grpc

import kvstore_pb2
import kvstore_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class KVStoreServer(kvstore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.map = {}


    def Put(self, request, context):
        key = request.key
        value = request.value
        print("Putting key.." + key )
        print("Putting value" + value )

        self.map[key] = value

        return kvstore_pb2.PutResponse(ret = kvstore_pb2.SUCCESS)

    def Get(self, request, context):

        key = request.key
        print("Getting..." + key )
        value = self.map[key]

        return kvstore_pb2.GetResponse(value = value , ret = kvstore_pb2.SUCCESS)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(KVStoreServer(), server)

    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
