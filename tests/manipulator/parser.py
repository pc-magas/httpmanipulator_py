import unittest
from unittest.mock import Mock

from src.manipulator.parser import HttpParser
from src.manipulator.serializer.HttpRequest import HttpRequest

REQUEST_CHUNKS=(
   "P","OST /test.php?a=b","+c"," ",
   "HTTP/1.1\r\nUser-Agent: Fooo\r\n",
   "HOST: example.com\r\n",
    "Content-Type: text/html;",
    "char","s","et=UTF-8\r",
    "\n",
    "Cont","en","t-Le","ngth: ","39\r\n"
    "\r","\n",
    "<!DOCTYPE html><html>",
    "lorem Ipsum</html>",
    "\r\n"
)

class TestHttpParser(unittest.TestCase):
  
    def test_BasicPostSubmitParse(self):
       
       def oncomplete(request):
            print("CALLBACK")
            self.assertEqual(request.url,"http://example.com/test.php?a=b+c")
            self.assertEqual(request.method,'POST')
            self.assertEqual(request.path,"/test.php")
            self.assertEqual(request.host,"example.com")
            self.assertEqual(request.port,80)
            self.assertEqual(request.protocol,"http")
            self.assertListEqual(request.cookies,list())
            self.assertEqual(request.body,b"<!DOCTYPE html><html>lorem Ipsum</html>")
            pass

       parser = HttpParser(oncomplete,False)
       for chunk in REQUEST_CHUNKS:
            parser.feed_data(chunk.encode('utf-8'))

       

if __name__ == '__main__':
    unittest.main()