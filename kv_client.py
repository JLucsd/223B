

from __future__ import print_function
import logging

import grpc

import kvstore_pb2
import kvstore_pb2_grpc
import random


def get_host():
    #TODO
    Host = ['54.200.135.126:50050', '52.24.196.183:50050']

    selected = random.randint(0,1)
    return Host[selected]


def run():
    #One server test cases
    with grpc.insecure_channel(get_host()) as channel:
        stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
        print("Trying...")
        response = stub.Put(kvstore_pb2.PutRequest(key='a', value ='b', flag ='user'))
        print("Put response code: "+ str(response.ret))

        response = stub.Get(kvstore_pb2.GetRequest(key='c', flag = 'user'))
        print("Get received code: "+ str(response.ret))
        print("Get received value: "+ str(response.value))

if __name__ == '__main__':
    logging.basicConfig()
    run()