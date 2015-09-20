import unittest
#TODO: Make this import slightly less confusing by changing to more meaningful names.
from settings.settings import Settings

s = Settings()

class ChangeName(unittest.TestCase):
    '''Change the name of the device.'''
    def runTest(self):

        #Get the current name so we can restore it afterwards.
        current_name = s.getName()

        #Generate a random name
        random_name = 'Cameron'

        #Change the name and see if it worked
        s.setName(random_name)
        test_name = s.getName()
        self.assertEqual(random_name, test_name)

        #Change the name back and see if it worked
        s.setName(current_name)
        test_name = s.getName()
        self.assertTrue(current_name, test_name)

#For debugging
if  __name__ =='__main__':
    c = ChangeName()
    c.runTest()
