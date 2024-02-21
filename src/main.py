#!/usr/bin/env python3

"""
1. Read settings
2. Bootstrap Manupilator
3. Bootstrap Control Panel

"""
import multiprocessing
from manipulator.http_socket_server import SocketServer

if __name__ == "__main__":

    # @todo read settings file
    host = "0.0.0.0"
    port = 80
    max_threads = 5

    server = SocketServer(host, port, max_threads)
    server_process = multiprocessing.Process(target=server.start)
    server_process.start()

    # Add other main application code here if needed

    server_process.join()