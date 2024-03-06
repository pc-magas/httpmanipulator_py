
class LineBuffer:

    def __init__(self):
        self.buffer = b''
    
    def pushData(self,line):
        self.buffer += str.encode(line)
    
    def getLine(self):
        if  b'\r\n' in self.buffer:
            line,sep,self.buffer = self.buffer.partition(b'\r\n')
            return line+sep
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
        return
