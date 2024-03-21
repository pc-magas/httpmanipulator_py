from src.manipulator.serializer.HttpRequest import HttpRequest
from httptools import HttpRequestParser

class HttpParser(HttpRequestParser):
    
    def __init__(self,oncomplete=None,ssl=False):
        super().__init__(self)
        self.id = None
        self.oncomplete = oncomplete       
        if ssl :
            self.protocol = 'https'
        else:
            self.protocol='http'
        
        self.requestSerialization = None
        self.buffer = b""

    def feed_data(self,data):
        self.buffer+=data
        super().feed_data(data)

    def on_headers_complete(self):
        self.requestSerialization.method = self.get_method()

    def on_message_begin(self):
        try:
            self.requestSerialization = HttpRequest()
            self.requestSerialization.protocol = self.protocol
        except Exception as e:
            print(e)
            raise e

    def on_status(self,status):
        print("STATUS: "+status)
    
    def on_header(self,name, value):
        try:
            self.requestSerialization.setheader(name,value)
        except Exception as e:
            print(e)
            raise e

    def on_url(self,url):
        try:
            self.requestSerialization.path = url
        except Exception as e:
            print(e)
            raise e
    
    def on_body(self,body):
        print("BODY",body)
        self.requestSerialization.body = body

    def on_message_complete(self):
        print(self.buffer)
        self.buffer=b""
        if self.oncomplete is not None:
            self.oncomplete(self.requestSerialization)
