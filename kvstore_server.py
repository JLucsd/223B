from concurrent import futures
import time
import logging

import grpc

import kvstore_pb2
import kvstore_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
host_list = []

class KVStoreServer(kvstore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.map = {}


    def Put(self, request, context):
        key = request.key
        value = request.value
        flag = request.flag
        print("Putting key.." + key )
        print("Putting value.." + value )

        self.map[key] = value
        
        if flag == "user":
            for host in host_list:
                with grpc.insecure_channel(host) as channel:
                    stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
                    print("Trying to replicate put...")

                    #TODO add try catch here 
                    response = stub.Put(kvstore_pb2.GetRequest(key=key, value =value, flag ="server"))

        
        return kvstore_pb2.PutResponse(ret = kvstore_pb2.SUCCESS)

    def Get(self, request, context):

        key = request.key
        flag = request.flag

        print("Getting..." + key )
        value = ""

        found_value = False
        # raise Exception("chaos monkey")

        if key in self.map:
            value = self.map[key]
            found_value = True
        elif flag == "server":
            print("Not in this server, broadcast to all the other servers...")
            for host in host_list:
                with grpc.insecure_channel(host) as channel:
                    stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
                    print("Trying...")

                    #TODO add try catch here 
                    response = stub.Get(kvstore_pb2.GetRequest(key=key))
                    if response.ret == kvstore_pb2.SUCCESS:
                        print("Put received: "+ str(response.value) )
                        value = response.value
                        found_value = True
                        break
        
        if found_value:
            return kvstore_pb2.GetResponse(value = value , ret = kvstore_pb2.SUCCESS)
        else:
            return kvstore_pb2.GetResponse(value = "" , ret = kvstore_pb2.FAILURE)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(KVStoreServer(), server)

    server.add_insecure_port('[::]:50050')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)



if __name__ == '__main__':
    logging.basicConfig()
    serve()
