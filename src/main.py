#!/usr/bin/env python3

import multiprocessing
from manipulator.http_socket_server import SocketServer,TLSSocketServer
from services.db import create_db

if __name__ == "__main__":

    # @todo read settings file
    host = "0.0.0.0"
    port = 80
    tls_port=443
    max_threads = 5

    db_conn = create_db("/home/manipulator/db/app.db")

    
    server = SocketServer(host, port, max_threads)
    server_process = multiprocessing.Process(target=server.start)
    server_process.start()

    # Add other main application code here if needed
    tls_server = TLSSocketServer(host, tls_port, max_threads)
    tls_server_process = multiprocessing.Process(target=tls_server.start)
    tls_server_process.start()

    tls_server_process.join()