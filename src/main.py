#!/usr/bin/env python3

import multiprocessing
from manipulator.http_socket_server import SocketServer
from services.db import create_db
from services.ssl import ContextFactory

if __name__ == "__main__":

    # @todo read settings file
    host = "0.0.0.0"
    port = 80
    tls_port=443
    max_threads = 5

    db_conn = create_db("/home/manipulator/db/app.db")
    
    server = SocketServer(host, port, max_threads,False)
    server_process = multiprocessing.Process(target=server.start)
    server_process.start()

    contexFactory = ContextFactory(db_conn,'/etc/manipulator/certs/key.key','/etc/manipulator/certs/cert.crt')

    # Add other main application code here if needed
    tls_server = SocketServer(host, tls_port, max_threads,contexFactory.getContext())
    tls_server_process = multiprocessing.Process(target=tls_server.start)
    tls_server_process.start()

    tls_server_process.join()