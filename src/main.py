#!/usr/bin/env python3

import multiprocessing

import os
import sys

from manipulator.http_socket_server import SocketServer
from services.db import create_db
from services.ssl import ContextFactory

def runServer(server: SocketServer):
    try:
        server.start()
    except Exception as e:
        print(e,flush=True)



if __name__ == "__main__":

    print("HTTP Manipulator is Starting")
    # @todo read settings file
    host = "0.0.0.0"
    port = 80
    tls_port=443
    max_threads = 5

    db_conn = create_db("/home/manipulator/db/app.db")
    
    server = SocketServer(host, port, max_threads,None)
    contexFactory = ContextFactory(db_conn,'/etc/manipulator/certs/key.key','/etc/manipulator/certs/cert.crt')

    try:
        server_process = multiprocessing.Process(target=runServer,kwargs=dict(server=server))
        server_process.start()


        # Add other main application code here if needed
        tls_server = SocketServer(host, tls_port, max_threads,contexFactory.getContext())
        tls_server_process = multiprocessing.Process(target=runServer,kwargs=dict(server=tls_server))
        tls_server_process.start()

        tls_server_process.join()
        server_process.join()
    except KeyboardInterrupt:
        print("Shutting Down servers")
        server_process.kill()
        tls_server_process.kill()

