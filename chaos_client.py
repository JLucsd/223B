from __future__ import print_function
import logging

import grpc

import chaosmonkey_pb2
import chaosmonkey_pb2_grpc

Host = ['localhost:50050', '52.24.196.183:50050']


def run():
    #One server test cases
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = chaosmonkey_pb2_grpc.ChaosMonkeyStub(channel)

        op = 1 
        if op == 0:
            l0 = chaosmonkey_pb2.ConnMatrix.MatRow(vals=[0.0,0.1,0.2])
            l1 = chaosmonkey_pb2.ConnMatrix.MatRow(vals=[0.3,0.4,0.5])
            l2 = chaosmonkey_pb2.ConnMatrix.MatRow(vals=[0.6,0.7,0.8])
            matrix = chaosmonkey_pb2.ConnMatrix(rows=[l0,l1,l2])
            stub.UploadMatrix(matrix)
        else:
	    mv = chaosmonkey_pb2.MatValue(row=1, col =2, val =0.0)
	    stub.UpdateValue(mv)
        #print("Put response code: "+ str(response.ret))

if __name__ == '__main__':
    logging.basicConfig()
    run()
