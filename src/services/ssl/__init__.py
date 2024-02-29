import ssl


class ContextFactory:

    def __init__(self,db):
        super.__init__(host,port,max_threads)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    def sni_callback(self):
        