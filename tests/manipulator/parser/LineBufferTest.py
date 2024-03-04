import unittest
from parser import LineBuffer


class LineBufferTest(unittest.TestCase):

    def testLineParse():
        buffer = LineBuffer()
        