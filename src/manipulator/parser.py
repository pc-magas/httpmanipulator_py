
class HttpRequestParseHandler:
    
    def __init__(self,client_socket):
        self.client_socket = client_socket

    def on_message_complete(self):
        print("Hello")
        content = '<html><body>Hello World</body></html>\r\n'.encode()
        headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n'.encode()
        self.client_socket.sendall(headers + content)
