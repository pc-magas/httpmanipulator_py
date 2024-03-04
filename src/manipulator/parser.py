
class LineBuffer:

    def __init__(self,sock):
        self.sock = sock
        self.buffer = b''
    
    def pushData(line):
        self.buffer += data
    
    def getLine():
        if  b'\r\n' in self.buffer:
            line,sep,self.buffer = self.buffer.partition(b'\r\n')
            return line
        return None
       

class LoggableHttpRequest:

    def __init__(self,db):
        self.headers={} #ParsedHeaderrs
        self.body="" #Http Body
        self.version=None
        self.method=None
        self.id=None
        self.raw=""
    
    def parse(line):
        
