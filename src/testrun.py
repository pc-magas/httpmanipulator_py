from manipulator.http_socket_server import SocketServer


if __name__ == "__main__":
    try:
        server = SocketServer('127.0.0.1',8080,4)
        server.start()
    except KeyboardInterrupt:
        exit(0)