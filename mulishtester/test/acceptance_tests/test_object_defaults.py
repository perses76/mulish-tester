import unittest

from mulishtester import ObjectFactory

CLASS_ARG1 = "CLASS ARG1"
CLASS_ARG2 = "CLASS ARG2"
CLASS_ARG3 = "CLASS ARG3"

INSTANCE_ARG2 = "INSTANCE ARG2"

METHOD_ARG3 = "METHOD ARG1"

class CustomFactory(ObjectFactory):
    arg1 = CLASS_ARG1
    arg2 = CLASS_ARG2
    arg3 = CLASS_ARG3

class ObjectDefaultsTest(unittest.TestCase):

    def test_class_default(self):
        obj = CustomFactory.create()
        self.assertEqual(CLASS_ARG1, obj.arg1)
        self.assertEqual(CLASS_ARG2, obj.arg2)
        self.assertEqual(CLASS_ARG3, obj.arg3)

    def test_instance_default(self):
        obj_factory = CustomFactory(arg2=INSTANCE_ARG2)
        obj = obj_factory.create()
        self.assertEqual(CLASS_ARG1, obj.arg1)
        self.assertEqual(INSTANCE_ARG2, obj.arg2)
        self.assertEqual(CLASS_ARG3, obj.arg3)

    def test_method_default_for_class(self):
        obj = CustomFactory.create(arg3=METHOD_ARG3)
        self.assertEqual(METHOD_ARG3, obj.arg3)

    def test_method_default_for_instance(self):
        obj_factory = CustomFactory(arg2=INSTANCE_ARG2)
        obj = obj_factory.create(arg3=METHOD_ARG3)
        self.assertEqual(CLASS_ARG1, obj.arg1)
        self.assertEqual(INSTANCE_ARG2, obj.arg2)
        self.assertEqual(METHOD_ARG3, obj.arg3)







  