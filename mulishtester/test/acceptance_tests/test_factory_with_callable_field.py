import unittest
from mulishtester import ObjectFactory

class CustomFactory(ObjectFactory):
    arg1 = "constant"

    def arg2(self):
        return "test"

    arg3 = "arg3"



class FactoryWithCallableFieldTest(unittest.TestCase):
    
    def test_for_class(self):
        obj = CustomFactory.create()
        self.assertEqual("constant", obj.arg1)
        self.assertEqual("test", obj.arg2)

    def test_for_object(self):
        factory = CustomFactory()
        obj = factory.create()
        self.assertEqual("constant", obj.arg1)
        self.assertEqual("test", obj.arg2)

    def test_for_method(self):
        def my_func(obj):
            return "my_func"
        obj = CustomFactory.create(arg2=my_func)
        self.assertEqual("constant", obj.arg1)
        self.assertEqual("my_func", obj.arg2)

    def test_for_method_and_object(self):
        def my_func(obj):
            return obj.arg1 + ";" + obj.arg3
        obj = CustomFactory.create(arg2=my_func)
        self.assertEqual("constant", obj.arg1)
        self.assertEqual("arg3", obj.arg3)
        self.assertEqual("constant;arg3", obj.arg2)

  