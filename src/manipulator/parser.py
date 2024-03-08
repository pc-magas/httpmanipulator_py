import uuid
from httptools import HttpRequestParser

class HttpParser(HttpRequestParser):
    
    def __init__(self,client_socket):
        super().__init__(self)
        self.client_socket=client_socket
    
    def on_message_complete(self):
        print("Hello")
        print(self.get_http_version())
        content = '<html><body>Hello World</body></html>\r\n'.encode()
        headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n'.encode()
        self.client_socket.sendall(headers + content)

    def on_status(self,status):
        print(status)
    
    def on_header(self,name, value):
        print(name,value)
    
    def on_url(self,url):
        print(url)