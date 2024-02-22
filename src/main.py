#!/usr/bin/env python3

import multiprocessing
from manipulator.http_socket_server import SocketServer
# from common.services.db import apply_migrations

if __name__ == "__main__":

    # @todo read settings file
    host = "0.0.0.0"
    port = 80
    max_threads = 5

    print("Setting UP Db")

    # apply_migrations("sqlite:///memory")

    server = SocketServer(host, port, max_threads)
    server_process = multiprocessing.Process(target=server.start)
    server_process.start()

    # Add other main application code here if needed

    server_process.join()