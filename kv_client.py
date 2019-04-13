

from __future__ import print_function
import logging

import grpc

import kvstore_pb2
import kvstore_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    #TODO localhost
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
        print("Trying...")
        response = stub.Put(kvstore_pb2.PutRequest(key='a', value ='b'))
        print("Put received: "+ str(response.ret))


if __name__ == '__main__':
    logging.basicConfig()
    run()