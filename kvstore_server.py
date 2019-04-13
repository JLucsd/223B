from concurrent import futures
import time
import logging

import grpc

import kvstore_pb2
import kvstore_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class KVStoreServer(kvstore_pb2_grpc.KeyValueStoreServicer):

    def Put(self, request, context):
        return kvstore_pb2.PutResponse(ret = 0 )

    def Get(self, request, context):
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(KVStoreServer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
