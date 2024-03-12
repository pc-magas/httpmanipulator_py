import uuid
from httptools import HttpRequestParser

class HttpRequest:
    id = uuid.uuid4()
    method=""
    body=""
    headers=dict()
    path = ""
    host = ""
    protocol=""
    _url=None

    @property
    def url(self):

        if(self.__url is None):
            self.protocol+"://"+self.host+self.url

        return self.__url
    

class RequestCookie:
    name=""
    value=""
    httpOnly=False

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
        self.requestSerialization = HttpRequest()
        self.requestSerialization.protocol = self.protocol

    def on_status(self,status):
        print("STATUS: "+status)
    
    def on_header(self,name, value):
        self.requestSerialization.headers[name]=value

        sanitizedHeaderName = name.lower()
        if(sanitizedHeaderName== 'host'):
            self.requestSerialization.host = host
        elif(sanitizedHeaderName == 'cookie'):
            cookies = value.decode('utf-8').split(",")

    def on_url(self,url):
        self.requestSerialization.path = url
        print('URL',url)
    
    def on_body(self,body):
        self.requestSerialization.body = body
        print("BODY",body)

    def on_message_complete(self):
        print(self.requestSerialization)
        if self.oncomplete is not None:
            self.oncomplete(self.requestSerialization)
