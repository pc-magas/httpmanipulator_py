import uuid
import base64
from urllib.parse import urlparse,parse_qs

class HttpRequest:
    id =uuid.uuid4()
    
    method=""
    body=""
    __path = ""
    __pathDirty=""
    host = ""
    __port=None
    protocol=""
    
    __username=None
    __password=None
    __authorizationType=None
    __authorizationHeaderId = None


    __cookies=list()
    __headers=list()

    __params=dict(
        url=list(),
        body=list()
    )

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self,value):
        value = value.decode('utf-8')
        self.__pathDirty = value
        results = urlparse(value)
        self.__path = results.path

    @property
    def port(self):
        if self.__port is None:
            return (lambda protocol: 80 if protocol=="http" else 443)(self.protocol)
        return self.__port

    @property
    def url(self):
        host = self.host+(lambda port:""if port is None else str(port))(self.__port)
        return self.protocol+"://"+host+self.__pathDirty

    @property
    def headers(self):
        return self.__headers

    @property
    def cookies(self):
        return self.__cookies

    def setheader(self,name,value):
        
        name = name.decode('utf-8')
        value = value.decode('utf-8')

        header_id = uuid.uuid4()
        headerSerialization = dict(
            id=header_id,
            name=name,
            value=value
        )

        self.__headers.append(headerSerialization)
        sanitizedHeaderName=name.lower()
        if(sanitizedHeaderName == 'host'):
            try:
                self.__serializeHost(value)
            except Exception as e:
                print("SSSS",e)
                raise e
        elif(sanitizedHeaderName == 'cookie'):
            self.__serializeCookies(headerSerialization.id,value)
        elif(sanitizedHeaderName == 'authorization'):
            self.__analyzeAuthorization(value,headerSerialization.id,value)

    def __analyzeAuthorization(self,id,value):
        self.__authorizationHeaderId=id
        (self.__authorizationType,value) = value.split(" ")
        
        if(self.__authorizationType.trim() == 'Basic'):
            (self.__username,self.__password) = base64.decode(value).split(":")
        elif(self.__authorizationType.trim() == 'Bearer'):
            self.__password = value

    def __serializeCookies(self,id,value):
        cookies = value.decode('utf-8').split(";")
        for cookie in cookies:
            cookievalues = cookie.split("=")
            self.__cookies.append(dict(name=cookievalues[0],value=cookievalues[1],header_id=header_id))

    def __serializeHost(self,host):
        host = host.split(":")
        self.host = host[0]

        if host[1] is not None:
            self.__port = int(host[1])

    def toDict(self):
        try:
            return self.__dict__
        except Exception as e:
            print(e)
            raise e