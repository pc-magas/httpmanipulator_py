import unittest
from manipulator.parser import HttpParser
from services.db import create_db

REQUEST_CHUNKS=(
   "P","OST /test.php?a=b+c",
   "HTTP/1.1\r\nUser-Agent: Fooo\r\n",
   "HOST: example.com\r\n",
    "Content-Type: text/html;",
    "char","s","et=UTF-8\r",
    "\n","\r","\n",
    "<!DOCTYPE html><html>",
    "lorem Ipsum</html>",
)

class TestHttpParser(unittest.BaseTestSuite):
    def testRequestSavedIntoDB():
        conn = create_db(":memory:")
        def onComplete(parser):
            pass
        parser = HttpParser(onComplete,false,db)

        for chunk in REQUEST_CHUNKS:
            parser.feed_data(chunk)
