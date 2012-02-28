import unittest

from mulishtester import ObjectFactory
from mulishtester.exceptions import AttributeNotExistInModel

CLASS_ARG1 = "CLASS ARG1"
CLASS_ARG2 = "CLASS ARG2"
CLASS_ARG3 = "CLASS ARG3"

INSTANCE_ARG2 = "INSTANCE ARG1"

METHOD_ARG3 = "METHOD ARG1"

class User(object):
    def __init__(self):
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None

class UserFactory(ObjectFactory):
    class Meta:
        model = User
    arg1 = CLASS_ARG1
    arg2 = CLASS_ARG2
    arg3 = CLASS_ARG3

class ModelDefaultsTest(unittest.TestCase):

    def test_method_default_for_class(self):
        obj = UserFactory.create(arg3=METHOD_ARG3)
        self.assertEqual(CLASS_ARG1, obj.arg1)
        self.assertEqual(CLASS_ARG2, obj.arg2)
        self.assertEqual(METHOD_ARG3, obj.arg3)
        self.assertEqual(User, type(obj))

    def test_method_default_for_instance(self):
        obj_factory = UserFactory(arg2=INSTANCE_ARG2)
        obj = obj_factory.create(arg3=METHOD_ARG3)
        self.assertEqual(User, type(obj))
        self.assertEqual(CLASS_ARG1, obj.arg1)
        self.assertEqual(INSTANCE_ARG2, obj.arg2)
        self.assertEqual(METHOD_ARG3, obj.arg3)

    def test_attr_not_exist_in_model(self):
        try:
            UserFactory.create(non_exists_attribute = "FirstName")
            self.fail("AttributeNotExistInModel exception must be thrown")
        except AttributeNotExistInModel:
            pass

