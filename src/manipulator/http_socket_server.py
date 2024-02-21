import socket
import threading
import queue
import time

class SocketServer:
    """
        Basic Socket Server in python
    """

    def __init__(self,host,port,max_theads):
        self.host = host
        self.port = port
        self.server_socket = self.__initSocket()
        self.max_theands = max_theads
        self.request_queue = queue.Queue()        

    def __initSocket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def __accept(self):
        self.server_socket.listen(5)
        while True:
            client_socket, client_address = self.server_socket.accept()    
            self.request_queue.put((client_socket, client_address))


    def __handle(self):
        while True:
            # Dequeue a request and process it
            client_socket, address = self.request_queue.get()    

            # Read HTTP Request
            # Log Http Request
            # Manipulate Http Request
            # Forward or respond

            client_socket.sendall(b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body>Hello World</body></html>\r\n""");

            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
            self.request_queue.task_done()


    def __initThreads(self):
        for _ in range(self.max_theands):
            threading.Thread(target=self.__handle, daemon=True).start()


    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.__initThreads()
        self.__accept()


class TCPTLSSocketServer(SocketServer):

    def __initSocket(self):
        socket = super().__initSocket()
        # @todo create SSL context        
