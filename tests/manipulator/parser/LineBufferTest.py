import unittest
from src.manipulator.parser import LineBuffer


class LineBufferTest(unittest.TestCase):

    def test_LineParse(self):
        buffer = LineBuffer()

        buffer.pushData("GET /in")
        self.assertEqual(None,buffer.getLine())

        buffer.pushData("put")
        self.assertEqual(None,buffer.getLine())

        buffer.pushData(".php")
        self.assertEqual(None,buffer.getLine())

        buffer.pushData(" ")
        self.assertEqual(None,buffer.getLine())

        buffer.pushData("HTTP/1.1\r")
        self.assertEqual(None,buffer.getLine())
        buffer.pushData("\nHost: example.com\r\n")
        self.assertEqual("GET /input.php HTTP/1.1",buffer.getLine().decode())
        self.assertEqual("Host: example.com",buffer.getLine().decode())



if __name__ == '__main__':
    unittest.main()