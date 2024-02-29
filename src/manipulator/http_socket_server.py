import socket
import threading
import queue
import time
import ssl

class SocketServer:
    """
        Basic Socket Server in python
    """

    def __init__(self,host,port,max_threads):
        print("Create Server For Http")
        self.host = host
        self.port = port
        self.server_socket = self.initSocket()
        self.max_threads = max_threads
        self.request_queue = queue.Queue()        

    def initSocket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def postProcessSocket(self,client_socket):
        return client_socket

    def __accept(self):
        self.server_socket.listen(5)
        while True:
            client_socket, client_address = self.server_socket.accept()
            actual_client_socket = self.postProcessSocket(client_socket)
            self.request_queue.put((actual_client_socket, client_address))


    def __handle(self):
        while True:
            # Dequeue a request and process it
            client_socket, address = self.request_queue.get()    
            print(address)
            # Read HTTP Request
            # Log Http Request
            # Manipulate Http Request
            # Forward or respond

            content = '<html><body>Hello World</body></html>\r\n'.encode()
            headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n'.encode()
            client_socket.sendall(headers + content)
            client_socket.close()
            self.request_queue.task_done()


    def __initThreads(self):
        for _ in range(self.max_threads):
            threading.Thread(target=self.__handle, daemon=True).start()


    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.__initThreads()
        self.__accept()


class TLSSocketServer(SocketServer):
    def postProcessSocket(self,client_socket):
        print("Load TLS")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile='/etc/manipulator/certs/cert.crt', keyfile='/etc/manipulator/certs/key.key')
        return context.wrap_socket(client_socket, server_side=True)

