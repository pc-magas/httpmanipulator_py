import socket
import threading
import queue
import ssl
from manipulator.parser import LineBuffer,LoggableHttpRequest

class SocketServer:
    """
        Basic Socket Server in python
    """

    def __init__(self,host,port,max_threads,ssl_context:ssl.SSLContext=None):
        print("Create Server For Http")        

        self.host = host
        self.port = port
        self.server_socket = self.initSocket()
        self.max_threads = max_threads
        self.request_queue = queue.Queue()   

        self.ssl_context=None
        if(ssl_context != None):
            print("Initialise SSL context")        
            self.ssl_context = ssl_context

    def initSocket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   
    def __accept(self):
        self.server_socket.listen(5)
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                
                if self.ssl_context is not None :
                    print(self.ssl_context)
                    client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)

                self.request_queue.put((client_socket, client_address))
            except:
                print("Error Occured")


    def __handle(self):
        while True:
            client_socket, address = self.request_queue.get()
            print("Address",address)
            
            try:
                # Read HTTP Request
                # Log Http Request
                # Manipulate Http Request
                # Forward or respond

                buffer = LineBuffer()
                request =  HttpRequest(self.db)

                buffer.pushData(client_socket.recv(2048))
                line = buffer.getLine()
                if(line is not None):
                    request.parse(line)

                content = '<html><body>Hello World</body></html>\r\n'.encode()
                headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n'.encode()
                client_socket.sendall(headers + content)
          
            finally:
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