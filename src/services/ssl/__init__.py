import ssl
from common.utils import convertDomainIntoWildcard

class ContextFactory:

    def __init__(self,db,default_key,default_crt):
        
        self.db = db

        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_context.sni_callback = self.__sni_callback
        self.ssl_dict = self.__getCertPaths()

        self.default_crt = default_crt
        self.default_key = default_key


    def __getCertPaths(self):
        ssl_dict = {}
        cursor = self.db.cursor()
        cursor.execute("SELECT * from certs")
        data = cursor.fetchall()
        for item in data:
            ssl_dict[item.domain]= {
                'cert': item.cert_path,
                'key': item.key_path,
                'ca': item.ca_path
            }
        
        return ssl_dict


    def __sni_callback(self,ssl_socket,server_name,context):

        wildcard_domain=convertDomainIntoWildcard(server_name)
        extended_wildcard_domain="*."+server_name

        if(server_name is None):
            context.load_cert_chain(keyfile=self.default_key,certfile=self.default_crt)
        elif (server_name in self.ssl_dict):
            context.load_cert_chain(keyfile=self.ssl_dict[server_name].key,certfile=self.ssl_dict[server_name].cert)
        elif(wildcard_domain in self.ssl_dict):
            context.load_cert_chain(keyfile=self.ssl_dict[wildcard_domain].key,certfile=self.ssl_dict[wildcard_domain].cert)
        elif(extended_wildcard_domain in self.ssl_dict):
            context.load_cert_chain(keyfile=self.ssl_dict[extended_wildcard_domain].key,certfile=self.ssl_dict[extended_wildcard_domainim].cert)
        else:
            context.load_cert_chain(keyfile=self.default_key,certfile=self.default_crt)

        return None
    
    def getContext(self):
        return self.ssl_context