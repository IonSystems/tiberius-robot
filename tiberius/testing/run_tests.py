import unittest
import os

if __name__ == '__main__':
    this_dir = os.path.dirname(__file__)
    suite = unittest.TestLoader().discover(this_dir, pattern='test*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)
