import socket
import threading
import queue
import time
import ssl


def sni_callback(ssl_socket,server_name,context):

    if server_name is None:
        print("Loading default cert")
        context.load_cert_chain(keyfile="/etc/manipulator/certs/key.key",certfile="/etc/manipulator/certs/cert.crt")
        return None
    
    if server_name == 'test.example.com':
        print("Loading cert1 and key1")
        context.load_cert_chain(keyfile="/etc/manipulator/certs/key1.key",certfile="/etc/manipulator/certs/cert1.crt")
    else:
        print("Loading default cert")
        context.load_cert_chain(keyfile="/etc/manipulator/certs/key.key",certfile="/etc/manipulator/certs/cert.crt")

    return None

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
            self.ssl_context.sni_callback = sni_callback

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