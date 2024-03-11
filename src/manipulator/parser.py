import uuid
from httptools import HttpRequestParser
    

class HttpParser(HttpRequestParser):
    
    def __init__(self,client_socket,ssl=False,db=None):
        super().__init__(self)
        self.db = db
        self.id = None
       
        if ssl :
            self.protocol = 'https'
        else:
            self.protocol='http'
        
        self.client_socket = client_socket
    
    def on_message_begin(self):
        self.id = uuid.uuid4()
    
    def on_status(self,status):
        print(self.id)
        print("STATUS: "+status)
    
    def on_header(self,name, value):
        print(self.id)
        print("HEADER",name,value)
    
    def on_url(self,url):
        print(self.id,'URL',url)
    
    def on_body(body):
        print(self.id,"BODY",body)

    def on_message_complete(self):

        print("Completed",self.get_http_version())

        content = '<html><body>Hello World</body></html>\r\n'.encode()
        headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n'.encode()
        self.client_socket.sendall(headers + content)