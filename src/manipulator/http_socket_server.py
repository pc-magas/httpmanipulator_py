import socket
import threading
import queue
import ssl

from httptools import HttpRequestParser
from manipulator.parser import HttpParser

class SocketServer:
    """
        Basic Socket Server in python
    """

    def __init__(self,host,port,max_threads,ssl_context:ssl.SSLContext=None):
        self.id='HTTP'
        if(ssl_context is None):
            print("Create http Server")        
        else:
            self.id='HTTPS'
            print("create https server")

        self.host = host
        self.port = port
        self.server_socket = self.initSocket()
        self.max_threads = max_threads
        self.request_queue = queue.Queue()   

        self.ssl_context=None
        self.is_ssl = False
        if(ssl_context != None):
            print("Initialise SSL context")        
            self.ssl_context = ssl_context
            self.is_ssl = True

    def initSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock
   
    def __accept(self):
        self.server_socket.listen(5)
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                
                if self.ssl_context is not None :
                    print(self.ssl_context)
                    client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
                print(self.id+": Queue Client Socket")
                self.request_queue.put((client_socket, client_address))
            except:
                print(self.id+":Error Occured")


    def __handle(self):
        while True:
            client_socket, address = self.request_queue.get()
            print(self.id+": Address",address)
            
            try:
                # Read HTTP Request
                # Log Http Request
                # Manipulate Http Request
                # Forward or respond

                def oncomplete(request):
                    content = '<html><body>Hello World</body></html>\r\n'.encode()
                    headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n'.encode()
                    client_socket.sendall(headers + content)

                parser = HttpParser(oncomplete,self.is_ssl)

                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        print("break")
                        break
                    parser.feed_data(data)

            except Exception as e:
                print(getattr(e, 'message', repr(e)))
                print(getattr(e, 'message', str(e)))
            finally:
                print("CLose Socket")
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                self.request_queue.task_done()


    def __initThreads(self):
        for _ in range(self.max_threads):
            threading.Thread(target=self.__handle, daemon=True).start()


    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.__initThreads()
        self.__accept()

