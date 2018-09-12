from app_source import app
import unittest


class MyTest(unittest.TestCase):
    def test(self):
        print ('\n\n\n\n\n\nInside the test\n\n\n\n')
        app.tata()


if __name__ == '__main__':
    unittest.main()
