from manipulator.serializer.HttpRequest import HttpRequest
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
        
    def on_headers_complete(self):
        self.requestSerialization.method = self.get_method()
        print(self.get_method())

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
            print('URL',url)
        except Exception as e:
            print(e)
            raise e
    
    def on_body(self,body):
        self.requestSerialization.body = body
        print("BODY",body)

    def on_message_complete(self):
        if self.oncomplete is not None:
            print(self.requestSerialization.toDict())
            print(self.requestSerialization.headers)
            print(self.requestSerialization.cookies)
            try:
                print(self.requestSerialization.url)
            except Exception as e:
                print(e)
            self.oncomplete(self.requestSerialization)
