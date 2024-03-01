import socket
import threading
import queue
import time
import ssl

import os,pathlib

path = os.path.join(pathlib.Path(__file__).parent.absolute(),"../../certs")
certfile = os.path.join(path,"cert.crt")
keyfile = os.path.join(path,"key.key")

print(path,certfile,keyfile)

class SocketServer:
    """
        Basic Socket Server in python
    """

    def __init__(self,host,port,max_threads,tls=False):
        print("Create Server For Http")        

        self.host = host
        self.port = port
        self.server_socket = self.initSocket()
        self.max_threads = max_threads
        self.request_queue = queue.Queue()   

        self.ssl_context=None
        if(tls == True):
            print("Initialise SSL context")        
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

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
                
            # Read HTTP Request
            # Log Http Request
            # Manipulate Http Request
            # Forward or respond

            content = '<html><body>Hello World</body></html>\r\n'.encode()
            headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n'.encode()
            client_socket.sendall(headers + content)
          
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

if __name__ == "__main__":
    host = "127.0.0.1"
    tls_port=8443
    max_threads = 5
    tls_server = SocketServer(host, tls_port, max_threads,True)
    tls_server.start()