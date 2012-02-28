import unittest
from mulishtester.exceptions import AttributeNotExistInModel, ATTRIBUTE_NOT_EXISTS_IN_MODEL_TEMPLATE

class AttributeNotExistInModelTest(unittest.TestCase):
    
    def test_check_return_string(self):
        class C(object):
            pass
        c = C()
        exception = AttributeNotExistInModel(c, "key")
        expected = ATTRIBUTE_NOT_EXISTS_IN_MODEL_TEMPLATE % ("key", c)
        self.assertEqual(expected, str(exception))

  